from datetime import datetime, timedelta

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon

from class_outputs import OutputClass
from defines import *
from functions import string_to_float


class OutputWorkshopHeater(OutputClass):
    def __init__(self, parent, o_id):
        super().__init__(parent, o_id)
        self.output_controller = parent
        # self.output_controller.areas_controller.main_window.coms_interface.update_float_switch.connect(self.float_update)

        self.auto_boost = int(self.db.get_config(CFT_WORKSHOP_HEATER, "auto boost", 1))
        self.max = string_to_float(self.db.get_config(CFT_WORKSHOP_HEATER, "high", 19.5))
        self.min = string_to_float(self.db.get_config(CFT_WORKSHOP_HEATER, "low", 10))
        self.duration = int(self.db.get_config(CFT_WORKSHOP_HEATER, "duration", 30))
        self.frost = int(self.db.get_config(CFT_WORKSHOP_HEATER, "frost", 1))
        self.min_frost = int(self.db.get_config(CFT_WORKSHOP_HEATER, "frost min", 2))
        self.max_frost = int(self.db.get_config(CFT_WORKSHOP_HEATER, "frost max", 6))

    def change_frost(self, frost):
        if frost == self.frost:
            return
        self.frost = frost
        self.db.set_config(CFT_WORKSHOP_HEATER, "frost", frost)
        self.update_info()

    def change_boost(self, boost):
        if boost == self.auto_boost:
            return
        self.auto_boost = boost
        self.db.set_config(CFT_WORKSHOP_HEATER, "auto boost", boost)
        self.update_info()

    def set_limits(self, on_temp, off_temp):
        """ Set the on and off temperatures for the output and updates all """
        self.temp_on = on_temp
        self.temp_off = off_temp
        self.update_info()

    def update_info(self):
        OutputClass.update_info(self)
        getattr(self.output_controller.main_panel, "lbl_output_number_%i" % self.ctrl_id).setText(str(0))

        getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).setText(str(self.max))
        getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).setText(str(self.min))
        if self.auto_boost:
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setPixmap(QtGui.QPixmap(":/normal/029-hot-thermometer.png"))
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setToolTip("Auto boost is enabled")
        else:
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setPixmap(QtGui.QPixmap(""))
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setToolTip("Auto boost is Disabled")



