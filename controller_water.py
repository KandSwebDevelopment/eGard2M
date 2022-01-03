import collections
import math

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap

from class_water_tank import WaterTank
from defines import *


class WaterController(QObject):
    def __init__(self, parent):
        """

        :type parent: MainWindow
        """
        super(WaterController, self).__init__()
        self.main_window = parent     # Areas controller
        self.db = self.main_window.db

        self.tanks = collections.defaultdict(WaterTank)
        self.tanks[1] = WaterTank(self, 1)
        self.tanks[2] = WaterTank(self, 2)

        self.main_window.coms_interface.update_feeder_unit.connect(self.fu_update)
        self.main_window.coms_interface.send_data(COM_TANK_LEVEL, True, MODULE_FU, 1)
        self.main_window.coms_interface.send_data(COM_TANK_LEVEL, True, MODULE_FU, 2)

    def get_tank_require_level(self, tank):
        req = self.main_window.feed_controller.get_next_water_required()
        req += self.main_window.feeder_unit.flush_litres
        req += self.main_window.feeder_unit.spillage_litres
        if tank == 2 and req <= self.tanks[1].max:
            return 0        # 2nd tank and tank 1 is able to hold required
        if req < self.tanks[1].min:
            return self.tanks[1].min
        if req > self.tanks[1].max:
            return math.ceil(req / 2)   # This will be same for both tanks as they will hold equal amounts
        return req

    def get_total_required(self):
        return self.get_tank_require_level(1) + self.get_tank_require_level(2)

    def set_current_level(self, tank, reading):
        if tank < 1 or tank > 2:
            return
        self.tanks[tank].update_level(reading)

    def get_current_level(self, tank):
        return self.tanks[tank].current_level

    def fill_tank(self, tank, level):
        if level <= self.tanks[tank].current_level:
            return
        reading = self.tanks[tank].litres_to_reading(level)
        self.main_window.coms_interface.send_data(COM_TANK_FILL, True, MODULE_FU, tank, reading)

    def drain_tank(self, tank, level):
        if level >= self.tanks[tank].current_level:
            return
        reading = self.tanks[tank].litres_to_reading(level)
        self.main_window.coms_interface.send_data(COM_TANK_DRAIN, True, MODULE_FU, tank, reading)

    def stop_fill(self):
        self.main_window.coms_interface.send_data(COM_STOP_FILL, True, MODULE_FU)

    def stop_drain(self):
        self.main_window.coms_interface.send_data(COM_STOP_DRAIN, True, MODULE_FU)

    def read_tank(self, tank):
        self.main_window.coms_interface.send_data(COM_TANK_LEVEL, True, MODULE_FU, tank)

    def fu_update(self, command, data):
        if command == COM_TANK_LEVEL:
            print("Water controller tank level ", data[1])
            self.set_current_level(int(data[0]), int(data[1]))
        elif command == CMD_SWITCH:
            if int(data[0]) == SW_WATER_MAINS_1:
                if int(data[1]) == ON:
                    getattr(self.main_window.main_panel, "lbl_water_1").setPixmap(QPixmap(":/normal/valve.png"))
                else:
                    getattr(self.main_window.main_panel, "lbl_water_1").setPixmap(QPixmap(":/normal/valve_closed.png"))
            elif int(data[0]) == SW_WATER_MAINS_2:
                if int(data[1]) == ON:
                    getattr(self.main_window.main_panel, "lbl_water_2").setPixmap(QPixmap(":/normal/valve.png"))
                else:
                    getattr(self.main_window.main_panel, "lbl_water_2").setPixmap(QPixmap(":/normal/valve_closed.png"))

