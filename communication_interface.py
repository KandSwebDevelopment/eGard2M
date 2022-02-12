import socket
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtNetwork import QHostAddress

from UPD_client import UdpClient
from UPD_server import UdpServer
from functions import string_to_float
from status_codes import *
from distutils.util import strtobool

# R@m5!tt8?E5eDHG@
MyIp = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
    [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
     [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]


class CommunicationInterface(QObject):
    update_sensors = pyqtSignal(list, name="updateSensors")
    update_other_readings = pyqtSignal(list, name="updateOthers")
    update_soil_reading = pyqtSignal(list, name="updateSoil")  # List will contain area 1 and area 2
    update_que_status = pyqtSignal(int, int, int, int,
                                   name="updateQueStatus")  # The length of the 3 command ques & stack lock
    update_cmd_issued = pyqtSignal(str, tuple, name="updateCmdIssued")  # command sent and (ip, port) sent to
    update_us_reading = pyqtSignal(int, int)  # Tank, value
    update_network_status = pyqtSignal(int, int)  # sender id, status
    update_status_feeder = pyqtSignal(int)
    update_received_answer = pyqtSignal(str)  # Raw data received from i/o. Only used for engineer
    update_received = pyqtSignal(str, tuple, name="updateReceived")  # Raw data received, from (ip, port). Used by engineer
    update_power = pyqtSignal(str, float,
                              name="updatePower")  # Power reading from DE Module str = com command, int = value
    update_access = pyqtSignal(int, int)  # Update from access inputs. int= item defined AUD_*, int = value
    update_access_settings = pyqtSignal(str,
                                        float)  # received setting from DE Module. str will be the setting ie = command
    update_float_switch = pyqtSignal(int, int, name="updateFloat")  # Float sw number, position
    update_mix_tank_status = pyqtSignal(str, int, name="update_mix_tank")
    update_mix_weight = pyqtSignal(float, name="update_mix_weight")
    update_from_relay = pyqtSignal(str, list, name="updateForHelper")
    update_switch = pyqtSignal(int, int, int, name="updateSwitch")   # Sw No, State, From Module
    update_switch_pos = pyqtSignal(int, int, int, name="updateSwitchPos")   # Sw No, State, From Module
    update_system = pyqtSignal(str, list, name="updateSystem")    # System related  command, data
    update_fan_speed = pyqtSignal(int, int, name="updateFanSpeed")     # Fan no, speed
    update_feeder_unit = pyqtSignal(str, list, name="updateFeeder_unit")    # A signal has been received from the FU.
    #  It is issued for all commands and will only be picked up by require dialogs. Cmd, prams

    def __init__(self, parent=None):
        """
        Communication Interface
        This is a wrapper for network communication. It creates threads and command stacks for each connection.
        All communication requests are sent to this and is puts the requests into the appropriate stack and starts
        the thread.
        Threads are instances of UdpClient,
        @type parent: MainWindow
        """
        QObject.__init__(self, parent)
        self.main_window = parent
        self.mode = parent.master_mode
        # Receiving
        self.command = ""

        # Sending
        self.priority_lock_io = False
        self.priority_lock_de = False
        self.priority_lock_slave = False
        self.priority_io = []
        self.command_io = []
        self.relay_stack = []
        self.command_de = []
        self.priority_slave = []
        self.command_slave = []
        self.last_communication = ''
        self.worker_tcp = None
        self.tcp_client = None
        self.lock = 0  # 0 = None, 1 = Lock release, 2 = Accept no commands till lock release,
        self.lock_cmd = ""
        self.last_io_status = 0
        self.last_de_status = 0
        self.lock_repeat_count = 0
        self.lock_repeat_max = 25

        self.master_mode = parent.master_mode
        self.io_errors = 0
        self.de_errors = 0
        # The following master/slave values will be picked by the database
        self.de_ip = self.main_window.db.get_config(CFT_DE_UNIT, "ip")
        self.de_port = int(self.main_window.db.get_config(CFT_DE_UNIT, "port"))
        self.io_ip = self.main_window.db.get_config(CFT_IO_UNIT, "ip")
        self.io_port = int(self.main_window.db.get_config(CFT_IO_UNIT, "port"))
        self.fu_ip = self.main_window.db.get_config(CFT_FEEDER, "ip")
        self.fu_port = int(self.main_window.db.get_config(CFT_FEEDER, "port"))
        self.slave_ip = self.main_window.db.get_config(CFT_NETWORK, "pc ip")     # Other PC
        self.slave_port = int(self.main_window.db.get_config(CFT_NETWORK, "pc port"))
        self.ip_broadcast = self.main_window.db.get_config(CFT_NETWORK, "broadcast ip")
        # self.this_ip = self.main_window.db.get_config(CFT_NETWORK, "ip")      # This PC
        self.this_port = int(self.main_window.db.get_config(CFT_NETWORK, "client port"))
        self.this_server_port = int(self.main_window.db.get_config(CFT_NETWORK, "port"))
        self.this_relay_port = int(self.main_window.db.get_config(CFT_NETWORK, "relay port"))
        self.pc_relay_port = int(self.main_window.db.get_config_alt(CFT_NETWORK, "relay port"))   # Note use of _alt to get other value
        self.this_pc_name = socket.gethostname()
        # self.this_ip2 = QHostAddress(self.this_ip_str)

        self.this_ip = socket.gethostbyname(self.this_pc_name)
        if self.main_window.master_mode == MASTER:
            pass

        if self.ip_broadcast != "":
            self.io_address = (self.ip_broadcast, self.io_port)
            self.de_address = (self.ip_broadcast, self.de_port)
            self.fu_address = (self.ip_broadcast, self.fu_port)
            self.slave_address = (self.ip_broadcast, self.slave_port)
        else:
            self.io_address = (self.io_ip, self.io_port)
            self.de_address = (self.de_ip, self.de_port)
            self.fu_address = (self.fu_ip, self.fu_port)
            self.slave_address = (self.slave_ip, self.slave_port)
        # self.slave_address = (self.slave_ip, self.slave_port)

        self.udp_client = UdpClient(self, 1)
        self.udp_relay = UdpClient(self, 2)
        self.udp_server = UdpServer(self)
        self.thread_udp_client = QThread(self)
        self.thread_udp_relay = QThread(self)
        self.thread_udp_server = QThread(self)
        self.startup()

    def startup(self):

        # UPD need to connect
        self.udp_client.connect()
        self.udp_client.update_status.connect(self.status_update)
        self.udp_client.finished.connect(self.udp_client_finished)
        self.udp_client.moveToThread(self.thread_udp_client)
        self.thread_udp_client.started.connect(self.udp_client.run)

        self.udp_relay.connect()
        self.udp_relay.moveToThread(self.thread_udp_relay)
        self.udp_relay.update_status.connect(self.status_update)
        self.udp_relay.finished.connect(self.udp_relay_finished)
        self.thread_udp_relay.started.connect(self.udp_relay.run)

        self.udp_server.connect()
        self.udp_server.moveToThread(self.thread_udp_server)
        self.thread_udp_server.started.connect(self.udp_server.run)
        self.thread_udp_server.start()

    def reconnect(self):
        self.udp_client.connect()
        self.udp_relay.connect()
        self.udp_server.connect()

    def udp_client_finished(self):
        # self.thread_udp_client.quit()
        # self.thread_udp_client.wait()
        self.thread_udp_client.terminate()
        print("UDP Client Finished")

    def udp_relay_finished(self):
        self.thread_udp_relay.quit()
        print("UDP Relay Finished")

    @pyqtSlot(int, int, int, name="updateStatus")
    def status_update(self, sid, status, from_port):
        if status == FC_UDP_RUNNING:
            if from_port == self.io_port:
                self.io_errors = 0
                self.update_network_status.emit(MODULE_IO, FC_NW_IO_RUNNING)
                # if self.last_io_status != FC_NW_IO_RUNNING:
                # self.relay_send(NWC_MODULES_STATUS, MODULE_IO, FC_NW_IO_RUNNING)
                self.last_io_status = FC_NW_IO_RUNNING
            elif from_port == self.de_port:
                self.de_errors = 0
                self.update_network_status.emit(MODULE_DE, FC_NW_DE_FOUND)
                if self.last_de_status != FC_NW_DE_FOUND:
                    self.relay_send(NWC_MODULES_STATUS, MODULE_DE, FC_NW_DE_FOUND)
                    self.last_de_status = FC_NW_DE_FOUND
        else:
            if from_port == self.io_port:
                self.io_errors += 1
                if self.io_errors > 1:
                    self.update_network_status.emit(MODULE_IO, FC_NW_IO_LOST)
                    if self.last_io_status != FC_NW_IO_LOST:
                        self.relay_send(NWC_MODULES_STATUS, MODULE_IO, FC_NW_IO_LOST)
                        self.last_io_status = FC_NW_IO_LOST
            elif from_port == self.de_port:
                self.de_errors += 1
                if self.de_errors > 2:
                    self.update_network_status.emit(MODULE_DE, FC_NW_DE_LOST)
                    if self.last_de_status != FC_NW_DE_LOST:
                        self.relay_send(NWC_MODULES_STATUS, MODULE_DE, FC_NW_DE_LOST)
                        self.last_de_status = FC_NW_DE_LOST

        # self.update_network_status.emit(sid, status)

    def process_incoming(self, received, source, sender=""):
        self.update_received.emit(received, sender)
        # print("sender ", sender)
        if sender[0] == self.slave_ip:
            if self.main_window.main_panel.slave_counter > 6:   # Will only remove if its there, and will only be here when received
                self.main_window.msg_sys.remove(MSG_DATA_LINK)
            self.main_window.main_panel.slave_counter = 0
        if source == "UPD_server":
            if "\r\n" in received:  # This will be IO & DE broadcasts and slave will receive here from master
                data_list = received.split("\r\n")
                command = data_list[0]
                command = command.replace('<', '')
                command = command.replace('>', '')
                data_list.pop(0)  # Remove command from list
                data_list.pop()  # Remove blank line
                data_list.pop()  # Remove goodbye
            else:  # Slave PC
                data_list = received.split(",")
                command = data_list[0]
                command = command.replace('<', '')
                command = command.replace('>', '')
                data_list.pop(0)  # Remove command from list
        else:  # This will be all responses to requests by other PC
            data_list = received.split("\r\n")
            command = data_list[0]
            command = command.replace('<', '')
            command = command.replace('>', '')
            data_list.pop(0)  # Remove command from list
            if len(data_list) > 0 and sender[1] != self.fu_port:
                data_list.pop()  # Remove blank line
                data_list.pop()  # Remove goodbye
        if self.master_mode == MASTER and (sender[1] == self.pc_relay_port or sender[1] == self.slave_port):
            relay_command = ""
        elif self.mode == SLAVE:
            relay_command = ""
        else:
            relay_command = received
        if sender[1] == self.io_port:
            module = MODULE_IO
        elif sender[1] == self.de_port:
            module = MODULE_DE
        elif sender[1] == self.pc_relay_port:
            module = MODULE_SL
        elif sender[1] == self.fu_port:
            module = MODULE_FU
            self.update_feeder_unit.emit(command, data_list)
            self.relay_send(NWC_FEEDER_UPDATE, received)
            return
        else:
            module = 999
        self.process_command(command, data_list, relay_command, module)

    def process_command(self, command, prams, relay_command, module):
        """
        @param module:
        @type module:
        @param relay_command: The original data received by UPD client may be relayed on to slave pc
        @type relay_command:
        @param command:
        @type command: str
        @type prams: list
        """
        # Inputs
        if command == COM_FANS:
            if self.main_window.master_mode == MASTER:
                if len(prams) > 0:
                    self.main_window.area_controller.fan_controller.update_temperature(1, string_to_float(prams[0]))
                    if len(prams) > 1:
                        self.main_window.area_controller.fan_controller.update_temperature(2, string_to_float(prams[1]))
            return
        if command == COM_SWITCH_POS:
            self.update_switch_pos.emit(int(prams[0]), int(prams[1]), module)
        if command == CMD_SWITCH:
            self.update_switch.emit(int(prams[0]), int(prams[1]), module)
            if module != MODULE_SL:
                self.relay_send(NWC_SWITCH, prams[0], prams[1])
        # if command == CMD_SWITCH_TIMED:
        #     if module != MODULE_SL:
        #         self.relay_send(NWC_SWITCH_TIMED, prams[0], prams[1])
        elif command == COM_SENSOR_READ:
            self.update_sensors.emit(prams)
            self.relay_command(relay_command)
        elif command == COM_OTHER_READINGS:
            self.update_other_readings.emit(prams)
            self.update_float_switch.emit(1, int(prams[2]))
            self.update_float_switch.emit(2, int(prams[3]))
            self.relay_command(relay_command)
        elif command == CMD_FAN_SPEED:
            self.update_fan_speed.emit(int(prams[0]), int(prams[1]))
            self.relay_send(NWC_FAN_SPEED, prams[0], prams[1])
        elif command == COM_SOIL_READ:
            self.update_soil_reading.emit(prams)
            self.relay_command(relay_command)
        elif command == COM_FLOAT_SWITCHES:
            self.update_float_switch.emit(int(prams[0]), int(prams[1]))
            self.relay_command(relay_command)
        elif command == NWC_US_READ:
            self.update_us_reading.emit(int(prams[0]), int(prams[1]))  # Signal emit - tank, value
            self.relay_command(relay_command)
        #  General
        elif command == COM_IO_REBOOT or command == CMD_IO_RESTART:
            self.main_window.main_panel.io_reboot()
        elif command == COM_OW_COUNT or command == COM_OW_SCAN:
            self.update_system.emit(command, prams)
        # DE Unit
        elif command == COM_DOOR_POSITION:
            self.update_access.emit(AUD_DOOR, int(prams[0]))
            self.relay_command(relay_command)
        elif command == COM_COVER_POSITION:
            self.update_access.emit(AUD_COVER_OPEN, int(prams[0]))
            self.relay_command(relay_command)
        elif command == COM_COVER_CLOSED:
            self.update_access.emit(AUD_COVER_CLOSED, int(prams[0]))
            self.relay_command(relay_command)
        elif command == COM_AUTO_SET:
            self.update_access.emit(AUD_AUTO_SET, int(prams[0]))
            self.relay_command(relay_command)
        elif command == COM_KWH_DIF or command == COM_SEND_FREQ:
            self.update_access_settings.emit(command, float(prams[0]))
            self.relay_command(relay_command)
        elif command == COM_PULSES:
            self.update_access_settings.emit(command, string_to_float(prams[0]))
            self.relay_command(relay_command)
        elif command == COM_KWH or command == COM_READ_KWH:
            self.update_power.emit(COM_KWH, float(prams[0]))
            self.relay_command(relay_command)
        elif command == COM_WATTS:
            self.update_power.emit(COM_WATTS, float(prams[0]))
            self.relay_command(relay_command)

        # Feeder
        elif command == NWC_FEEDER_STATUS:
            self.main_window.status_update_feeder(int(prams[0]) + FC_FR_OFF_LINE)
            self.relay_command(relay_command)

        # Mix tank
        elif command == COM_MIX_READ_LEVEL:
            print("Mix weight = ", prams[0])
            self.update_mix_weight.emit(round(float(prams[0]) / 1000, 1))
            self.relay_command(relay_command)
        elif command == COM_MIX_TARE or command == COM_MIX_CAL_1 or \
                command == COM_MIX_CAL_2 or command == COM_MIX_SET_CAL:
            self.update_mix_tank_status.emit(command, 0)
            self.relay_command(relay_command)
        elif command == COM_MIX_SET_CAL:
            self.update_mix_tank_status.emit(command, prams[0])
            self.relay_command(relay_command)

        self.process_relay_command(command, prams)

    def process_relay_command(self, command, prams):
        if command == NWC_MODULES_STATUS:
            self.update_network_status.emit(int(prams[0]), int(prams[1]))
            return
        elif command == NWC_QUE_STATUS:
            self.update_que_status.emit(int(prams[0]), int(prams[1]), int(prams[2]), int(prams[3]))
            return
            # Floats
        elif command == NWC_WATER_LEVELS or\
                command == NWC_FAN_REQUIRED:
            self.update_from_relay.emit(command, [float(prams[0]), float(prams[1])])
            return
            # Second pram is Bool
        elif command == NWC_OUTPUT_LOCK:
            self.update_from_relay.emit(command, [float(prams[0]), strtobool(prams[1])])
            return
        elif command == NWC_FEEDER_UPDATE:
            p = prams
            c = p.pop(0)
            c = c.replace('<', '')
            c = c.replace('>', '')
            self.update_feeder_unit.emit(c, p)
            return
        elif command == NWC_WORKSHOP_HEATER or \
                command == NWC_ACCESS_BOOST or \
                command == NWC_DRYING_AREA or \
                command == NWC_CHANGE_TO_FLUSHING or \
                command == NWC_MOVE_TO_FINISHING or \
                command == NWC_MESSAGE or \
                command == NWC_NUTRIENTS_AUTO_STIR or \
                command == NWC_RELOAD_PROCESSES or \
                command == NWC_SLAVE_START or \
                command == NWC_STAGE_ADJUST or \
                command == NWC_STOCK_TOTAL or \
                command == NWC_WORKSHOP_DURATION or \
                command == NWC_WORKSHOP_RANGES or \
                command == NWC_SOIL_LOAD:
            self.update_from_relay.emit(command, [])
            return
        # 1 pram
        elif command == NWC_FEED_DATE or \
                command == NWC_FAN_PID or \
                command == NWC_FEED or \
                command == NWC_FEED_ITEMS or \
                command == NWC_PROCESS_MIX_CHANGE or \
                command == NWC_PROCESS_FEED_MODE or \
                command == NWC_SWITCH_REQUEST or \
                command == NWC_OUTPUT_RANGE or \
                command == NWC_OUTPUT_LOCK or \
                command == NWC_ACCESS_OPERATE or \
                command == NWC_OUTPUT_TRIGGER or \
                command == NWC_OUTPUT_TRIGGER or \
                command == NWC_WORKSHOP_FROST or \
                command == NWC_WORKSHOP_BOOST:
            self.update_from_relay.emit(command, [int(prams[0])])
            return
        # 2 prams
        elif command == NWC_OUTPUT or \
                command == NWC_OUTPUT_MODE or \
                command == NWC_OUTPUT_SENSOR or \
                command == NWC_SENSOR_RELOAD or \
                command == NWC_WH_DURATION or \
                command == NWC_WH_FREQUENCY or \
                command == NWC_FAN_SENSOR or \
                command == NWC_FAN_SPEED or \
                command == NWC_FAN_MODE or \
                command == NWC_FAN_REQUIRED or \
                command == NWC_FAN_UPDATE:
            self.update_from_relay.emit(command, [int(prams[0]), int(prams[1])])
            return

        # No prams
        if prams is None:
            self.update_from_relay.emit(command, [])
        elif len(prams) == 1:
            self.update_from_relay.emit(command, [int(prams[0])])
        else:
            self.update_from_relay.emit(command, [int(prams[0]), int(prams[1])])

    # Sending functions communication
    def get_next_udp_communication(self, who) -> (str, tuple):
        """
        This will get the next command and the which UDP is requesting it
        @param who: The id of the UDP Client requesting the data
        @type who: int
        @return: The command as a string and the IP and port as a tuple for the destination of the command
        @rtype: str, tuple
        """
        org_cmd = cmd = ''
        to = -1
        if who == 1:
            if self.lock == 2:
                # org_cmd = self.lock_cmd
                cmd = self.lock_cmd.encode("utf-8", "replace")
                self.lock_cmd = ""
                return cmd, self.io_address
            if self.lock == 1:  # Send command and release lock
                # org_cmd = self.lock_cmd
                cmd = self.lock_cmd.encode("utf-8", "replace")
                self.lock_cmd = ""
                self.lock = 0
                self.update_que_status.emit(len(self.priority_io), len(self.relay_stack),
                                            len(self.command_io) + len(self.command_de),
                                            self.lock)
                return cmd, self.io_address
            if self.lock == 3:  # Repeat last command
                if self.lock_repeat_count >= self.lock_repeat_max:
                    self.lock_cmd = ""
                    self.lock = 0
                else:
                    self.lock_repeat_count += 1
                    return self.lock_cmd.encode("utf-8", "replace"), self.io_address

            if len(self.priority_io) > 0:
                self.priority_lock_io = True
                org_cmd = self.priority_io[0]['cmd']
                cmd = self.priority_io[0]['cmd'].encode("utf-8", "replace")
                to = self.priority_io[0]['address']
                self.priority_io.pop(0)
                # which_que = 1
                if len(self.priority_io) == 0:
                    self.priority_lock_io = False
            elif not self.priority_lock_io:
                if len(self.command_io) > 0:
                    org_cmd = self.command_io[0]['cmd']
                    cmd = self.command_io[0]['cmd'].encode("utf-8", "replace")
                    to = self.command_io[0]['address']
                    self.command_io.pop(0)
            # self.last_communication = org_cmd
            if org_cmd != "":
                self.update_cmd_issued.emit(org_cmd[1:len(org_cmd) - 1], to)

        if who == 2:    # Relay command
            if len(self.relay_stack) > 0:
                org_cmd = self.relay_stack[0]['cmd']
                cmd = self.relay_stack[0]['cmd'].encode("utf-8", "replace")
                to = self.relay_stack[0]['address']
                self.relay_stack.pop(0)
            if org_cmd != "":
                self.update_cmd_issued.emit(org_cmd[1:len(org_cmd) - 1], to)

        # self.last_communication = org_cmd
        return cmd, to

    def get_next_relay_communication(self) -> (str, int):
        """ This is NOT used. See get_next_udp where who = 2"""
        org_cmd = cmd = ''
        to = -1
        if len(self.relay_stack) > 0:
            org_cmd = self.relay_stack[0]['cmd']
            cmd = self.relay_stack[0]['cmd'].encode("utf-8", "replace")
            to = self.relay_stack[0]['address']
            self.relay_stack.pop(0)
            # if len(self.relay_stack) == 0:
            #     self.priority_lock_de = False
        # self.last_communication = org_cmd
        if cmd != '':
            self.update_cmd_issued.emit(org_cmd[1:len(org_cmd) - 1], to)
        return cmd, to

    def add_to_que(self, data, urgent=False, to=MODULE_IO):
        if to == MODULE_IO:
            self.stack_io(data, self.io_address, urgent)
        elif to == MODULE_DE:
            self.stack_io(data, self.de_address, urgent)
            # self.stack_de(data, urgent)
        elif to == MODULE_SL:
            self.stack_relay(data)
        elif to == MODULE_FU:
            self.stack_io(data, self.fu_address, urgent)
        # elif to == MODULE_NWC:

    def stack_io(self, data, to_address, urgent=False):
        if urgent:
            if next((item for item in self.priority_io if item["cmd"] == data), None) is None:
                self.priority_io.append({'address': to_address, 'cmd': data})
                self.priority_lock_io = True
        else:
            if next((item for item in self.command_io if item["cmd"] == data), None) is None:
                self.command_io.append({'address': to_address, 'cmd': data})

        # print("is finished ", self.thread_udp.isFinished())
        # print("is running ", self.thread_udp.isRunning())
        if len(self.command_io) > 0 or len(self.priority_io) > 0:
            if not self.thread_udp_client.isRunning():
                print("Starting UDP thread")
                self.thread_udp_client.start()

        self.update_que_status.emit(len(self.priority_io), len(self.relay_stack),
                                    len(self.command_io) + len(self.command_de),
                                    self.lock)
        # self.slave_send(NWC_QUE_STATUS, len(self.priority_io) + len(self.priority_de),
        #                 len(self.command_io) + len(self.command_de),
        #                 self.lock)

    def stack_relay(self, data):
        cmd = data[1:data.find(">")]
        if cmd in [NWC_MESSAGE, COM_SOIL_READ, COM_SENSOR_READ, COM_OTHER_READINGS, COM_READ_KWH, COM_WATTS]:
            # Find and replace
            if len(self.relay_stack) > 0:
                for item in self.relay_stack:
                    if item['cmd'].find(cmd):
                        item = data
            else:
                self.relay_stack.append({'address': self.slave_address, 'cmd': data})
                self.update_que_status.emit(len(self.priority_io), len(self.relay_stack),
                                            len(self.command_io) + len(self.command_de),
                                            self.lock)

        else:
            if next((item for item in self.relay_stack if item["cmd"] == cmd), None) is None:
                self.relay_stack.append({'address': self.slave_address,  'cmd': data})
            self.update_que_status.emit(len(self.priority_io), len(self.relay_stack),
                                        len(self.command_io) + len(self.command_de),
                                        self.lock)
        if len(self.relay_stack) > 0:
            if not self.thread_udp_relay.isRunning():
                print("Starting Relay thread")
                self.thread_udp_relay.start()

    @staticmethod
    def is_in_que(cmd, que):
        for i in que:
            if i == cmd:
                return True
        return False

    def send_switch(self, sw_num, state, to=MODULE_IO):
        self.send_data(CMD_SWITCH, True, to, sw_num, state)

    def send_switch_timed(self, sw_num, state, duration):
        self.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, sw_num, state, duration)

    def send_command(self, command, item=None, val=None, urgent=False, to=MODULE_IO):
        cmd = "<" + command
        if item is not None:
            cmd = cmd + "," + str(item)
        if val is not None:
            cmd = cmd + "," + str(val)
        cmd += ">"
        self.add_to_que(cmd, urgent, to)

    def send_data(self, command, urgent, to, *args):
        cmd = "<" + command
        for data in args:
            cmd += ", " + str(data)
        cmd += ">"
        self.add_to_que(cmd, urgent, to)

    def send_valve(self, valve, pos):
        self.send_command(CMD_VALVE, valve, pos, True)

    def send_valve_cluster(self, cluster, pos, pos2):
        self.send_data(CMD_VALVE_CLUSTER, True, MODULE_IO, cluster, pos, pos2)

    def release_lock(self):
        """ This releases a lock  set by send lock command but without needing a command"""
        self.lock = 0
        self.lock_cmd = ""

    def send_lock_command(self, lock, command, *args):
        """
        Any command sent by this will lock the get_next_udp_communication according to the lock state in the
        following ways
        2: Send this command and then no others from the command stack until a lock release command is received

        @param lock: int  0 = None, 1 = Lock release, 2 = Accept no commands till lock release,
                          3 = Will send this command till ech time ask for next until lock release is received or it
                          has been sent maximum times
        @type lock:
        @type command: str
        @rtype: None
        """
        cmd = "<" + command
        for data in args:
            cmd += ", " + str(data)
        cmd += ">"
        self.lock = lock
        self.lock_cmd = cmd
        if lock == 2 or lock == 1 or lock == 3:
            self.update_que_status.emit(len(self.priority_io), len(self.relay_stack),
                                        len(self.command_io) + len(self.command_de),
                                        self.lock)
            if not self.thread_udp_client.isRunning():
                self.thread_udp_client.start()

    def relay_command(self, command):
        """ Relays a preformatted command"""
        if command == "":
            return
        self.stack_relay(command)
        # self.update_cmd_issued.emit(command, self.slave_address)
        # self.udp_relay.send_only(command.encode("utf-8"), self.slave_address)
        # print("Sending Relay {} to IP {} Port {}".format(command, self.pc_ip, self.pc_port))

    def relay_send(self, command, *data):
        cmd = "<" + command + ">"
        for d in data:
            cmd += "\r\n" + str(d)
        cmd += "\r\n\r\n"
        self.stack_relay(cmd)
        # self.update_cmd_issued.emit(cmd, self.slave_address)
        # self.udp_relay.send_only(cmd.encode("utf-8"), self.slave_address)
