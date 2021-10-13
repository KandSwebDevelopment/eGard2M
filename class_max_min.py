from datetime import datetime

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject
from defines import *


class MaxMin(QObject):

    def __init__(self, parent):
        super(MaxMin, self).__init__()
        self.sensor = parent    # The parent will be the sensor this belongs to
        self.db = parent.db
        self.max = -999
        self.min = 999
        self.max_time = datetime.now()
        self.min_time = datetime.now()
        self.display_ctrl = getattr(self.sensor.area_controller.main_panel, "te_max_min_%i" % self.sensor.display_id)

    def check(self, value):
        if value < self.min:
            self.min = value
            self.min_time = datetime.now()
            self.update_display()
        if value > self.max:
            self.max = value
            self.max_time = datetime.now()
            self.update_display()

    def update_display(self):
        txt = "> {}  < {}".format(self.max, self.min)
        self.display_ctrl.setText(txt)
        self.display_ctrl.setToolTip("> {} < {}".format(self.max_time.strftime("%a %H:%M"), self.min_time.strftime("%a %H:%M")))
