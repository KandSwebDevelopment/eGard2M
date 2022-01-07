import ctypes
import winsound
from datetime import *

from PyQt5 import QtCore
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import *
from pathlib import Path


def m_box(title, text, style):
    # Button styles:
    # 0 : OK
    # 1 : OK | Cancel
    # 2 : Abort | Retry | Ignore
    # 3 : Yes | No | Cancel
    # 4 : Yes | No
    # 5 : Retry | No
    # 6 : Cancel | Try Again | Continue

    # To also change icon, add these values to previous number
    # 16 Stop-sign icon
    # 32 Question-mark icon
    # 48 Exclamation-point icon
    # 64 Information-sign icon consisting of an 'i' in a circle
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def play_sound(sound):
    for s in range(0, len(sound), 2):  # read in pairs, freq and duration
        winsound.Beep(sound[s], sound[s + 1])


def check_for_sound():
    pass


def sound_click():
    winsound.PlaySound(get_wave_path("sound55.wav"), winsound.SND_FILENAME)


def sound_check_out():
    winsound.PlaySound(get_wave_path("sound63.wav"), winsound.SND_FILENAME)


def sound_error():
    winsound.PlaySound(get_wave_path("sound78.wav"), winsound.SND_FILENAME)


def sound_on():
    winsound.PlaySound(get_wave_path("sound86.wav"), winsound.SND_FILENAME)


def sound_off():
    winsound.PlaySound(get_wave_path("sound87.wav"), winsound.SND_FILENAME)


def sound_ok():
    winsound.PlaySound(get_wave_path("sound95.wav"), winsound.SND_FILENAME)


def sound_access_warn():
    winsound.PlaySound(get_wave_path("sound74.wav"), winsound.SND_FILENAME)


def get_wave_path(sound):
    parts = Path().absolute().parts
    path = ""
    for i in range(0, len(parts)):
        path += parts[i]
        if i > 0:
            path += "\\"
    path += "wave_files\\" + sound
    return path


def sound_error():
    # print(Path().absolute())
    parts = Path().absolute().parts
    path = ""
    for i in range(0, len(parts)):
        path += parts[i]
        if i > 0:
            path += "\\"
    # print(path)
    path += "wave_files\\error.wav"
    winsound.PlaySound(path, winsound.SND_FILENAME)


def find_it(key, my_list):
    for index, sublist in enumerate(my_list):
        if sublist[0] == key:
            return index
    return None


def auto_capital(line_edit_object):
    """
    Pass a line edit to this and it will change contents to upper case
    :param line_edit_object:
    :type line_edit_object:
    """
    edit = line_edit_object
    text = edit.text()
    edit.setText(text.upper())


def minutes_to_hhmm(minutes):
    h = int(minutes / 60)
    m = minutes % 60
    return h, m


def dict2str(items_dict):
    """ Lists dictionary item in a string, comma separated"""
    s = ""
    for i in items_dict:
        s += str(i) + ","
    return s[:len(s) - 1]      # Remove last comma


def get_last_friday(current_time=None):
    """
    Return the date of the friday before the date passed in. If no date is passed in it will use the current date
    :param current_time:
    :type current_time: datetime
    :return:
    :rtype: datetime
    """
    if current_time is None:
        current_time = datetime.now()
    wd = current_time.weekday()
    if wd == 4:
        td = 0
    elif wd > 4:
        td = wd - 4
    else:
        td = 3 + wd

    return current_time.date() - timedelta(days=td)
    # return (current_time.date()
    #         - timedelta(days=current_time.weekday())
    #         + timedelta(days=4, weeks=-1))


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
    self.panel_9 = QLabel("SS Unit", self)
    self.panel_9.setFixedWidth(90)
    self.panel_9.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_9.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.statusbar.addPermanentWidget(self.panel_9, 0)
    self.panel_10 = QLabel("", self)
    self.panel_10.setFixedWidth(130)
    self.panel_10.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_10.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.statusbar.addPermanentWidget(self.panel_10, 0)

    self.panel_14 = QLabel("", self)
    self.panel_14.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    self.panel_14.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    self.statusbar.addPermanentWidget(self.panel_14, 1)


