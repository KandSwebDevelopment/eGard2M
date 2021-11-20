import collections

from PyQt5.QtCore import QObject
from defines import *


class FeederUnit(QObject):
    def __init__(self, parent):
        super(FeederUnit, self).__init__()
        # super().__init__()
        self.main_window = parent
        self.db = parent.db
        self.pots = collections.defaultdict(dict)
        self.coms = self.main_window.coms_interface

        self.nutrient_stir_time = int(self.db.get_config(CFT_FEEDER, "nutrient stir time", 30)) * 1000
        self.soak_time = int(self.db.get_config(CFT_FEEDER, "soak time", 10))
        self.flush_litres = int(self.db.get_config(CFT_FEEDER, "flush litres", 4))
        self.max_mix_litres = int(self.db.get_config(CFT_FEEDER, "max mix litres", 6))
        self.mix_stir_time = int(self.db.get_config(CFT_FEEDER, "mix stir time", 30)) * 1000

        self.soak_time = int(self.db.get_config(CFT_FEEDER, "soak time", 10))
        self.flush_litres = int(self.db.get_config(CFT_FEEDER, "flush litres", 4))
        self.max_mix_litres = int(self.db.get_config(CFT_FEEDER, "max mix litres", 6))
        self.mix_stir_time = int(self.db.get_config(CFT_FEEDER, "mix stir time", 30)) * 1000

        self.load_pots()

    def load_pots(self):
        rows = self.db.execute('SELECT pot, size, current_level, max, min, ml10, pin FROM {}'.format(DB_FEEDER_POTS))
        for row in rows:
            name = self.db.execute_single("SELECT `name` FROM {} WHERE id = {}".format(DB_NUTRIENTS_NAMES, row[0]))
            self.pots[row[0]] = {'size': row[1],
                                 'level': row[2],
                                 'max': row[3],
                                 'min': row[4],
                                 'time': row[5],
                                 'pin': row[6],
                                 'name': name}

    def pot_from_nid(self, nid):
        p = self.db.execute_single('SELECT pot FROM {} WHERE nid = {}'.format(DB_NUTRIENT_PROPERTIES, nid))
        if p is None:
            return 0
        return p

    def dispense_nid(self, nid, mls):
        pot = self.pot_from_nid(nid)
        self.dispense_pot(pot, mls)

    def dispense_pot(self, pot, mls):
        if pot == 0:
            return
        dur = mls * self.pots[pot]['time']
        self.dispense_ms(pot, dur)

    def dispense_ms(self, pot, ms):
        self.coms.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, self.pots[pot]['pin'], ON_RELAY, ms)

    def get_duration(self, pot, mls):
        return mls * self.pots[pot]['time']

    def stir_nutrients(self):
        self.coms.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, SW_NUTRIENT_STIR, ON_RELAY, self.nutrient_stir_time)

    def stir_mix(self):
        self.coms.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, SW_MIX_STIR, ON_RELAY, self.mix_stir_time)

    def set_valve_position(self, valve, pos):
        self.coms.send_data(CMD_VALVE, True, MODULE_FU, valve, pos)

    def set_calibration_weight(self, weight):
        self.coms.send_data(COM_MIX_SET_CAL, weight)
