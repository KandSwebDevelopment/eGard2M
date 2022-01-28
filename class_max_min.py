from datetime import datetime

from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import QObject
from PyQt5 import QtCore, QtWidgets

from defines import *
from functions import dict2str


class MaxMin(QObject):

    def __init__(self, parent):
        super(MaxMin, self).__init__()
        self.sensor = parent  # The parent will be the sensor this belongs to
        self.db = parent.db
        self.max = -999
        self.min = 999
        self.max_time = datetime.now()
        self.min_time = datetime.now()
        self.day_night = UNSET
        self.log_data = [0, 999, 0, -999, 0, 999, 0, -999]      # Day min time, day min, day max time, day max .. then night
        self.log_path = self.sensor.area_controller.main_window.logger.log_path + "\\"
        self.display_ctrl_max = getattr(self.sensor.area_controller.main_panel, "le_max_%i" % self.sensor.display_id)
        self.display_ctrl_min = getattr(self.sensor.area_controller.main_panel, "le_min_%i" % self.sensor.display_id)
        self.display_ctrl_max.installEventFilter(self)
        self.display_ctrl_min.installEventFilter(self)
        if self.sensor.id in [1, 2, 9]:
            self.type = 2   # Clock cycle
        else:
            self.type = 1   # Process cycle

    def eventFilter(self, source, event):
        # Remember to install event filter for control first
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if source is self.display_ctrl_max or source is self.display_ctrl_min:
                modifiers = QtWidgets.QApplication.keyboardModifiers()
                # if modifiers == QtCore.Qt.ShiftModifier:
                # elif modifiers == QtCore.Qt.ControlModifier:
                #     print('Control+Click')
                if modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
                    self.reset(0)
        return QWidget.eventFilter(self, source, event)

    def check(self, value):
        if value < self.min:
            self.min = round(value, 1)
            self.min_time = datetime.now()
            self.update_display()
            if self.day_night == DAY:
                self.log_data[0] = self.min
            else:
                self.log_data[2] = self.min
            # self.save()
        if value > self.max:
            self.max = round(value, 1)
            self.max_time = datetime.now()
            self.update_display()
            if self.day_night == DAY:
                self.log_data[1] = self.max
            else:
                self.log_data[3] = self.max
            # self.save()

    def update_display(self):
        # txt = ">{}  <{}".format(self.max if self.max > -999 else "----", self.min if self.min < 999 else "----")
        self.display_ctrl_max.setText(str(self.max) if self.max > -999 else "--")
        self.display_ctrl_min.setText(str(self.min) if self.min < 999 else "--")
        self.display_ctrl_max.setToolTip("{}".format(self.max_time.strftime("%a %H:%M")))
        self.display_ctrl_min.setToolTip("{}".format(self.min_time.strftime("%a %H:%M")))

    def reset(self, day_night):
        self.max = -999
        self.min = 999
        self.max_time = datetime.now()
        self.min_time = datetime.now()
        self.day_night = day_night
        self.update_display()

    def save_to_file(self):
        f = open(self.log_path + datetime.strftime(datetime.now(), "%Y%m") + ".mmd", "w")
        text = datetime.strftime(datetime.now(), "%d, ") + str(self.sensor.area) + ", " + dict2str(self.log_data) + self.new_line
        f.write(text)
        f.close()
