import threading
import time
import socket
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal

from status_codes import FC_UDP_RUNNING, FC_UDP_DROP


class UdpClient(QObject):
    update_status = pyqtSignal(int, int, int, name="updateStatus")   # Sender id, status
    finished = pyqtSignal()

    def __init__(self, parent, uid):
        super(UdpClient, self).__init__()
        self.my_parent = parent
        self.mode = parent.mode
        self.id = uid
        self.mySocket = None
        self.is_connected = False
        self.lock = 0       # 0 = None, 1 = Lock release, 2 = Accept no commands till lock release,
        self.lock_cmd = ""
        self.lock = threading.Lock()

    def connect(self):
        try:
            self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.mySocket.settimeout(2)
            # self.mySocket.connect((self.my_parent.ip_this, 5420))
            self.mySocket.bind((self.my_parent.this_ip, self.my_parent.this_port + self.id - 1))
            self.is_connected = True
        except socket.error:
            print("ERROR UDP socket failed to create")

    def dis_connect(self):
        self.mySocket.shutdown()
        self.mySocket.close()

    @pyqtSlot()
    def run(self):
        alive = True
        cmd, to = self.my_parent.get_next_udp_communication(self.id)
        while alive:
            try:
                # lock = threading.Lock()
                # lock.acquire()
                # Send the command
                try:
                    print("Sending {} to IP {} Port {}".format(cmd, to[0], to[1]))
                    # self.lock.acquire()
                    if to[1] != 5499:
                        self.mySocket.sendto(cmd, to)
                        data, ip = self.mySocket.recvfrom(1024)
                        print("UDP Client received ", data, " from ", ip)
                        data = data.decode()
                        self.my_parent.process_incoming(data, cmd, ip)
                    self.update_status.emit(None, FC_UDP_RUNNING, ip[1])
                    # self.lock.release()
                except socket.timeout:
                    self.update_status.emit(self.id, FC_UDP_DROP, to[1])
            except Exception as e:
                print("UDP Client Error Error: ", e)
            cmd = ""
            while cmd == "":
                cmd, to = self.my_parent.get_next_udp_communication(self.id)
                time.sleep(1)
            # if cmd == '':
            #     break
        # print("UDP exit")
        self.finished.emit()

    def send_only(self, command, to):
        print("Sending Only {} to IP {} Port {}".format(command, to[0], to[1]))
        self.mySocket.sendto(command, to)
