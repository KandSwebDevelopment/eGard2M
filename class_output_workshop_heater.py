from datetime import datetime, timedelta

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

from class_outputs import OutputClass
from defines import *
from functions import string_to_float


class OutputWorkshopHeater(OutputClass):
    def __init__(self, parent, o_id):
        super().__init__(parent, o_id)
        self.output_controller = parent
        # self.output_controller.area_controller.main_window.coms_interface.update_float_switch.connect(self.float_update)

        self.max = 0
        self.min = 0
        self.max_frost = 0
        self.min_frost = 0
        self.auto_boost = 0
        self.duration = int(self.db.get_config(CFT_WORKSHOP_HEATER, "duration", 30))
        self.frost = 0
        self.load_ranges()
        self.load_settings()
        self.boost_timer = QTimer()
        self.boost_timer.timeout.connect(self.boost_timer_update)
        self.remaining = 0
        # self.output_controller.area_controller.main_window.coms_interface.update_switch.connect(self.switch_auto_boost)

    def switch_update(self, state):
        OutputClass.switch_update(self, state)
        if state == ON:
            self.remaining = self.duration
            self.boost_timer.start(1000)
        else:
            self.boost_timer.stop()
            self.remaining = 0

    def load_settings(self):
        self.auto_boost = int(self.db.get_config(CFT_WORKSHOP_HEATER, "auto boost", 1))
        self.frost = int(self.db.get_config(CFT_WORKSHOP_HEATER, "frost", 1))

    def load_ranges(self):
        self.max = string_to_float(self.db.get_config(CFT_WORKSHOP_HEATER, "high", 19.5))
        self.min = string_to_float(self.db.get_config(CFT_WORKSHOP_HEATER, "low", 10))
        self.min_frost = string_to_float(self.db.get_config(CFT_WORKSHOP_HEATER, "frost min", 2))
        self.max_frost = string_to_float(self.db.get_config(CFT_WORKSHOP_HEATER, "frost max", 6))
        self.update_info()

    def set_duration(self, duration=None):
        """ Set timer duration and update display
            If called with duration as none it will load value from db"""
        if duration is None:
            self.duration = int(self.db.get_config(CFT_WORKSHOP_HEATER, "duration", 30))
            return
        if duration == self.duration:
            return
        self.duration = duration
        self.db.set_config_both(CFT_WORKSHOP_HEATER, "duration", duration)

    def switch_manual(self):
        if self.status == ON:
            self.remaining = 0
            self.switch(OFF)
        else:
            self.remaining = self.duration
            self.switch(ON)

    def check(self, value):
        self._check()
        if self.frost and value <= self.max_frost:
            if value <= self.min_frost:
                self.switch(ON)
            else:
                self.switch(OFF)
        if self.mode == 2:  # Auto with auto boost
            if value <= self.max and self.remaining > 0:
                self.switch(ON)
            else:
                self.switch(OFF)

    def boost_timer_update(self):
        if self.remaining == 0:
            self.boost_timer.stop()
            return
        self.remaining -= 1
        getattr(self.output_controller.main_panel, "lbl_output_number_%i" % self.ctrl_id).setText(str(self.remaining))

    def boost_start(self):
        self.remaining = self.duration
        self.output_controller.main_panel.coms_interface.send_switch(SW_WORKSHOP, ON)

    def change_frost(self, frost):
        if frost == self.frost:
            return
        self.frost = frost
        self.db.set_config_both(CFT_WORKSHOP_HEATER, "frost", frost)
        self.update_info()

    def change_boost(self, boost):
        if boost == self.auto_boost:
            return
        self.auto_boost = boost
        self.db.set_config_both(CFT_WORKSHOP_HEATER, "auto boost", boost)
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
        if self.auto_boost and self.mode > 0:
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setPixmap(QtGui.QPixmap(":/normal/029-hot-thermometer.png"))
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setToolTip("Auto boost is enabled")
        else:
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setPixmap(QtGui.QPixmap(""))
            getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setToolTip("Auto boost is Disabled")

        if self.mode > 0:
            getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).setText(str(self.min))
            getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).setText(
                str(self.max))
        else:
            getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).clear()
            getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).clear()

        if self.frost:
            getattr(self.output_controller.main_panel, "lbl_frost").setPixmap(QtGui.QPixmap(":/normal/drying_1.png"))
            if self.mode == 0:
                getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).setText(str(self.min_frost))
                getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).setText(
                    str(self.max_frost))
        else:
            getattr(self.output_controller.main_panel, "lbl_frost").setPixmap(QtGui.QPixmap(""))


