from PyQt5 import QtCore
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import *


def find_it(key, my_list):
    for index, sublist in enumerate(my_list):
        if sublist[0] == key:
            return index
    return None


def string_to_float(s) -> float:
    """
    Converts a string to a float. The string can be a float or an int
    If an invalid string it will return 0.00
    :param s: String to convert
    :type s: str
    :return: Float value of string or 0.00 if not valid
    :rtype: float
    """
    try:
        float(s)
        return float(s)
    except ValueError:
        return 0.00


def multi_status_bar(self):
    # Do multipart status bar
    self.panel_1 = QLabel("1", self)
    self.panel_1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.panel_1.setFixedWidth(50)
    self.panel_1.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.statusbar.addPermanentWidget(self.panel_1, 0)
    self.panel_2 = QLabel("2", self)
    self.panel_2.setFixedWidth(45)
    self.panel_2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    # self.panel_2.setGeometry(QtCore.QRect(self.panel_2.x(), self.panel_2.y(), 250, self.panel_2.height()))
    self.statusbar.addPermanentWidget(self.panel_2, 0)
    self.panel_3 = QLabel("3", self)
    self.panel_3.setFixedWidth(80)
    self.panel_3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_3.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.panel_3.setToolTip("3")
    self.statusbar.addPermanentWidget(self.panel_3, 0)
    self.panel_4 = QLabel("4", self)
    self.panel_4.setFixedWidth(80)
    self.panel_4.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_4.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.panel_4.setToolTip("4")
    # self.panel_4.setGeometry(QtCore.QRect(self.panel_4.x(), self.panel_4.y(), 250, self.panel_4.height()))
    self.statusbar.addPermanentWidget(self.panel_4, 0)
    self.panel_5 = QLabel("5", self)
    self.panel_5.setFixedWidth(80)
    self.panel_5.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_5.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.panel_5.setToolTip("5")
    self.statusbar.addPermanentWidget(self.panel_5, 0)
    self.panel_6 = QLabel("6", self)
    self.panel_6.setFixedWidth(95)
    self.panel_6.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_6.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.statusbar.addPermanentWidget(self.panel_6, 0)
    self.panel_7 = QLabel("7", self)
    self.panel_7.setFixedWidth(80)
    self.panel_7.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_7.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.statusbar.addPermanentWidget(self.panel_7, 0)
    self.panel_8 = QLabel("8", self)
    self.panel_8.setFixedWidth(90)
    self.panel_8.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_8.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.statusbar.addPermanentWidget(self.panel_8, 0)

    self.panel_14 = QLabel("", self)
    self.panel_14.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_14.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.statusbar.addPermanentWidget(self.panel_14, 1)


