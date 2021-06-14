import time
import socket
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal

from defines import MASTER


class UdpServer(QObject):
    update_status = pyqtSignal(int, int, name="updateStatus")   # Sender id, status
    finished = pyqtSignal()

    def __init__(self, parent):
        super(UdpServer, self).__init__()
        self.my_parent = parent
        self.mode = parent.mode
        self.remote_ip = parent.this_ip
        self.remote_port = parent.this_server_port
        self.id = None
        self.mySocket = None
        self.is_connected = False
        if self.mode == MASTER:
            self.name = "UPD_server"
        else:
            self.name = "UDP_slave"

    def connect(self):
        try:
            if self.mySocket is not None:
                self.mySocket.close()
                self.mySocket = None
            self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.mySocket.bind((self.remote_ip, self.remote_port))
        except Exception as e:
            print(e)

    @pyqtSlot()
    def run(self):
        while True:
            try:
                data, ip = self.mySocket.recvfrom(1024)
                data = data.decode()
                # print("Message: ", data)
                # print("From: ", ip)
                self.my_parent.process_incoming(data, self.name, ip)
                time.sleep(1)
            except Exception as e:
                print(e)
