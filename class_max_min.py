from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject
from defines import *


class MaxMin(QObject):

    def __init__(self, parent):
        super(MaxMin, self).__init__()
        self.sensor = parent
        self.db = parent.db

    def update(self):
        pass
