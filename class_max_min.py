from datetime import datetime

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject
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
        self.display_ctrl = getattr(self.sensor.area_controller.main_panel, "te_max_min_%i" % self.sensor.display_id)

    def check(self, value):
        if value < self.min:
            self.min = value
            self.min_time = datetime.now()
            self.update_display()
            if self.day_night == DAY:
                self.log_data[0] = self.min
            else:
                self.log_data[2] = self.min
            # self.save()
        if value > self.max:
            self.max = value
            self.max_time = datetime.now()
            self.update_display()
            if self.day_night == DAY:
                self.log_data[1] = self.max
            else:
                self.log_data[3] = self.max
            # self.save()

    def update_display(self):
        txt = "> {}  < {}".format(self.max, self.min)
        self.display_ctrl.setText(txt)
        self.display_ctrl.setToolTip(
            "> {} < {}".format(self.max_time.strftime("%a %H:%M"), self.min_time.strftime("%a %H:%M")))

    def reset(self, day_night):
        self.max = -999
        self.min = 999
        self.max_time = datetime.now()
        self.min_time = datetime.now()

    def save(self):
        f = open(self.log_path + datetime.strftime(datetime.now(), "%Y%m") + ".mmd", "w")
        text = datetime.strftime(datetime.now(), "%d, ") + str(self.sensor.area) + ", " + dict2str(self.log_data) + self.new_line
        f.write(text)
        f.close()
