import collections

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap

from class_water_tank import WaterTank
from defines import *


class WaterController(QObject):
    def __init__(self, parent):
        """

        :type parent: _main
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

    def set_current_level(self, tank, reading):
        self.tanks[tank].update_level(reading)

    def fu_update(self, command, data):
        if command == COM_TANK_LEVEL:
            print("Water controller tank level ", data[1])
            self.set_current_level(int(data[0]), int(data[1]))
        elif command == CMD_SWITCH:
            if int(data[0]) == SW_WATER_MAINS_1:
                if int(data[1]) == ON_RELAY:
                    getattr(self.main_window.main_panel, "lbl_water_1").setPixmap(QPixmap(":/normal/valve-1.png"))
                else:
                    getattr(self.main_window.main_panel, "lbl_water_1").setPixmap(QPixmap(":/normal/valve_closed.png"))
            elif int(data[0]) == SW_WATER_MAINS_2:
                if int(data[1]) == ON_RELAY:
                    getattr(self.main_window.main_panel, "lbl_water_2").setPixmap(QPixmap(":/normal/valve-1.png"))
                else:
                    getattr(self.main_window.main_panel, "lbl_water_2").setPixmap(QPixmap(":/normal/valve_closed.png"))

