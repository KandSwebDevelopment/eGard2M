import time

import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal

from status_codes import *
from dbController import MysqlDB


class ScalesComs(QThread):
    db = ...  # type: MysqlDB
    new_reading = pyqtSignal(str, name='newReading')  # value from large scale
    new_reading_p = pyqtSignal(str, name='newReadingP')  # value from small scale
    update_status = pyqtSignal(str, name='updateStatus')
    update_status_p = pyqtSignal(str, name='updateStatusP')
    new_uid = pyqtSignal(str, name='newUID')
    update_cal = pyqtSignal(str, int, name='updateCal')

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        # super().__init__()
        self.my_parent = parent
        self.db = self.my_parent.db
        self.running = False  # True when thread is running
        self.is_connected = False  # Set true when connection is established
        self.has_coms = False  # Set true when CMD_HELLO is acknowledged
        self.has_received = False  # has received communicating
        self.connection = None  # The actual connection
        self.command_out = []  # Array of commands to be sent
        self.command_out_wait = []  # Array of commands to be sent, and wait on response
        self.last_command_received = None  # Last command received, use by wait
        self.wait_counter = 0  # Count how long waiting to enable break out of wait
        self.data_in = []
        self.port_list = []
        self.no_connection = False
        self.current_port = ""
        self.get_port()

    def connect(self):
        if self.is_connected or not self.my_parent.has_scales:
            return
        print("Coms connect")
        try:
            self.connection = serial.Serial(self.current_port, 115200, timeout=2)
            self.connection.flushInput()
            self.is_connected = True
            self.update_status.emit("connected")
            self.start()
        except Exception as e:
            # Possible errors
            # ("could not open port 'COM7': PermissionError(13, 'Access is denied.', None, 5)",)
            self.update_status.emit("disconnected")
            # self.my_parent.notifier.add(CRITICAL, "Unable to connect to sensor module", FC_COM_NO_CONNECTION,
            #                             str(e.args))
            # @ToDo Display this error in popup
            print("Error = ", e.args)
            self.is_connected = False

    def coms_disconnect(self):
        if self.is_connected:
            self.connection.close()
            self.is_connected = False
            self.update_status.emit('disconnected')

    def get_port(self):
        self.current_port = self.db.get_config(CFT_SS_UNIT, "com")

    def send_command(self, command, *args):
        cmd = "<" + command
        for data in args:
            cmd += ", " + str(data)
        cmd += ">"
        cmd = str.encode(cmd)
        if cmd not in self.command_out:
            self.command_out.append(cmd)
            print("Sent ", self.command_out)

    def run(self):
        while self.is_connected:
            # if not self.has_coms:
            #     self.handshake()
            try:
                raw_data = str(self.connection.readline())
                # print("Scales sent ", raw_data)
                self.process_data(raw_data)
                #     self.connection.flushInput()  # flush input buffer, discarding all its contents
                self.connection.flushOutput()

                if len(self.command_out_wait) > 0:
                    if self.last_command_received == self.command_out_wait[0]:
                        self.command_out_wait.pop(0)
                    else:
                        self.wait_counter += 1
                        if self.wait_counter > 4:
                            self.my_parent.notifier.add(WARNING, "Interface unit failed a system request",
                                                        FC_COM_WAIT_REQUEST_FAILED, "The command " + (
                                                            (self.command_out_wait[0].decode())[1:]).rstrip('>') + " was requested but not received")
                            self.my_parent.logger.save_system("Interface unit failed a system request.  The command " + (
                                                                  (self.command_out_wait[0].decode())[1:]).rstrip('>') + " was requested but not received")
                            self.command_out_wait.pop(0)
                        else:
                            print("scales send - ", self.command_out_wait[0])
                            self.connection.write(self.command_out_wait[0])

                if len(self.command_out) > 0 and len(self.command_out_wait) == 0:
                    self.connection.write(self.command_out[0])
                    self.command_out.pop(0)
                    # print("cmd stack = ", self.command_out)
            except Exception as e:
                print(e)
                self.is_connected = False
                self.update_status.emit('disconnected')
                # self.my_parent.logger.save_system(FC_MESSAGE[FC_COM_COMMUTATION_LOST]['message'])
                # @ToDo add to message system coms fail
            time.sleep(0.5)

    def process_data(self, raw_data):
        if raw_data != "b''":
            if not self.has_received:
                self.has_received = True
                # self.status_update_coms.emit(FC_COM_COMMUTATION_OK)
            raw_trimmed = raw_data[2:][:-5]
            # print("Received ", raw_trimmed)
            pos = raw_trimmed.find("=")
            data = None
            if pos > -1:
                cmd = raw_trimmed[0:][:pos]
                data = raw_trimmed[pos + 1:]
            else:
                cmd = raw_trimmed
            # print("command = ", cmd)
            # print("data = ", data)
            if cmd == 'w':
                self.new_reading.emit(data)
            elif cmd == 'g':
                self.new_reading_p.emit(data)
            elif cmd == 'cal_1a':
                self.update_cal.emit('cal_1a', 0)
            elif cmd == 'cal_1b':
                self.update_cal.emit('cal_1b', 0)
            elif cmd == 'cal_2a':
                self.update_cal.emit('cal_2a', 0)
            elif cmd == 'cal_2b':
                self.update_cal.emit('cal_2b', 0)
            elif cmd == 'tare_2':
                self.update_status_p.emit('tare')
            elif cmd == 'tare_1':
                self.update_status.emit('tare')
            elif cmd == 'UID tag':
                self.new_uid.emit(data.lstrip())
            elif cmd == "cal_weight_1":
                self.update_cal.emit("cal_weight_1", int(data))
            elif cmd == "cal_weight_2":
                self.update_cal.emit("cal_weight_2", int(data))

    def tare(self):
        self.send_command("tare_1")

    def tare_p(self):
        self.send_command("tare_2")

    def get_cal_weight(self, scale):
        if scale == 1:
            self.send_command("get_cal_weight_1")
        else:
            self.send_command("get_cal_weight_2")

    def set_cal_weight(self, scale, weight):
        if scale == 1:
            self.send_command("set_cal_weight_1, {}".format(weight))
        else:
            self.send_command("set_cal_weight_2, {}".format(weight))

    def calibrate(self, scale, step):
        if scale == 1:
            if step == 1:
                self.send_command("cal_1a")
            else:
                self.send_command("cal_1b")
        if scale == 2:
            if step == 1:
                self.send_command("cal_2a")
            else:
                self.send_command("cal_2b")
