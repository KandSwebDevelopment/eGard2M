import collections

from PyQt5.QtCore import QObject
from defines import *


class WaterTank(QObject):
    def __init__(self, parent, id):
        """

        :type parent: Water Controller
        """
        super(WaterTank, self).__init__()
        self.water_controller = parent     # Areas controller
        self.db = self.water_controller.db
        self.id = id

        self.max = self.db.get_config(CFT_WATER_SUPPLY, "tank_max", 20)
        self.min = self.db.get_config(CFT_WATER_SUPPLY, "tank_min", 6)

        self.levels = collections.defaultdict(int)
        self.current_level = 0
        self.load_levels()

    def update_level(self, reading):
        self.current_level = self.reading_to_litres(reading)
        getattr(self.water_controller.main_window.main_panel, "le_water_tank_{}".
                format(self.id)).setText(str(self.current_level))
        return self.current_level

    def get_current_level(self):
        return self.current_level

    def load_levels(self):
        rows = self.db.execute("SELECT litres, reading FROM {} WHERE tank = {} ORDER BY litres ASC".
                               format(DB_TANK_CONVERSION, self.id))
        for row in rows:
            self.levels[row[0]] = row[1]

    def reading_to_litres(self, reading):
        # print("Reading = ", reading)
        return self.closest(self.levels, reading)

    def litres_to_reading(self, litres):
        if litres < 0 or litres > 20:
            return 0
        litres = int(litres)
        return self.levels[litres]

    @staticmethod
    def closest(lst, find):
        return min(lst, key=lambda y: abs(float(lst[y]) - find))

