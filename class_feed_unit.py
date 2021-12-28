import collections
import math

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
        self.feed_litres = int(self.db.get_config(CFT_FEEDER, "feed L", 10))
        self.max_man_litres = int(self.db.get_config(CFT_FEEDER, "max manual feed", 1))
        self.correction_mix_fill = int(self.db.get_config(CFT_FEEDER, "correction_mix_fill", 50))
        self.correction_mix_empty = int(self.db.get_config(CFT_FEEDER, "correction_mix_empty", 50))
        self.valve_open = 0     # Feed valve open so it knows what open to close

        self.load_pots()

    def load_pots(self):
        rows = self.db.execute('SELECT pot, size, current_level, max, min, ml10, pin FROM {}'.format(DB_FEEDER_POTS))
        for row in rows:
            name = self.db.execute_single("SELECT nn.name FROM {} nn INNER JOIN {} np WHERE nn.id = np.nid "
                                          "AND np.pot = {}".
                                          format(DB_NUTRIENTS_NAMES, DB_NUTRIENT_PROPERTIES, row[0]))
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

    def nid_from_pot(self, pot):
        n = self.db.execute_single('SELECT nid FROM {} WHERE pot = {}'.format(DB_NUTRIENT_PROPERTIES, pot))
        if n is None:
            return 0
        return n

    def get_pot_level(self, pot):
        return self.pots[pot]['level']

    def set_pot_level(self, pot, level):
        self.pots[pot]['level'] = level

    def dispense_nid(self, nid, mls):
        pot = self.pot_from_nid(nid)
        self.dispense_pot(pot, mls)

    def dispense_pot(self, pot, mls):
        if pot == 0:
            return
        dur = mls * self.pots[pot]['time']
        self.dispense_ms(pot, dur)
        self.deduct_from_pot(pot, math.ceil(mls))

    def dispense_ms(self, pot, ms):
        self.coms.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, self.pots[pot]['pin'], ON, ms)

    def deduct_from_pot(self, pot, mls):
        self.db.execute_write("UPDATE {} SET current_level = current_level - {} WHERE pot = {} LIMIT 1".
                              format(DB_FEEDER_POTS, mls, pot))
        self.pots[pot]['level'] -= mls

    def check_pot_level(self, pot):
        """ Checks the level in a pot
            :returns 0= ok, 1= low, 2=empty, -1= Not in use """
        if self.pots[pot]['name'] is None:
            return -1
        if self.pots[pot]['level'] <= self.pots[pot]['min']:
            return 2
        if self.pots[pot]['level'] <= self.pots[pot]['min'] * 2:
            return 1    # Low
        return 0

    def deduct_from_stock(self, nid, mls):
        self.db.execute_write("UPDATE {} SET current_level = current_level - {} WHERE nid = {} LIMIT 1".
                              format(DB_NUTRIENT_PROPERTIES, mls, nid))

    def get_duration(self, pot, mls):
        return mls * self.pots[pot]['time']

    def stir_nutrients(self):
        self.coms.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, SW_NUTRIENT_STIR, ON, self.nutrient_stir_time)

    def stir_mix(self):
        self.coms.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, SW_MIX_STIR, ON, self.mix_stir_time)

    def set_valve_position(self, valve, pos):
        self.coms.send_data(CMD_VALVE, True, MODULE_FU, valve, pos)

    def set_servo_feed_valves(self, area, feed_flush, state):
        """ For Servo valves
            If area = 0 then it is manual, feed_flush doesn't matter
            else for area 1 and 2 feed_flush, 1 = Feed, 2 = Flush
            state will be either ON or OFF """
        if area == 0:   # Manual
            self.coms.send_data(CMD_VALVE, True, MODULE_FU, 5, state)
            self.valve_open = 5
        elif area == 1:
            if feed_flush == 1:
                self.coms.send_data(CMD_VALVE, True, MODULE_FU, 6, state)
                self.valve_open = 6
            elif feed_flush == 2:
                self.coms.send_data(CMD_VALVE, True, MODULE_FU, 8, state)
                self.valve_open = 8
        elif area == 2:
            if feed_flush == 1:     # Feed
                self.coms.send_data(CMD_VALVE, True, MODULE_FU, 7, state)
                self.valve_open = 7
            elif feed_flush == 2:
                self.coms.send_data(CMD_VALVE, True, MODULE_FU, 9, state)
                self.valve_open = 9

    def set_feed_valves(self, area, feed_flush, state):
        """ For solenoid valves
            If area = 0 then it is manual, feed_flush doesn't matter
            else for area 1 and 2 feed_flush, 1 = Feed, 2 = Flush
            state will be either ON or OFF """
        if area == 0:   # Manual
            self.coms.send_switch(SW_MAN_FEED, state, MODULE_FU)
        elif area == 1:
            if feed_flush == 1:
                self.coms.send_switch(SW_A1_FEED, state, MODULE_FU)
            else:
                self.coms.send_switch(SW_A1_DRAIN, state, MODULE_FU)
        elif area == 2:
            if feed_flush == 1:
                self.coms.send_switch(SW_A2_FEED, state, MODULE_FU)
            else:
                self.coms.send_switch(SW_A2_DRAIN, state, MODULE_FU)

    def set_calibration_weight(self, weight):
        self.coms.send_data(COM_MIX_SET_CAL, weight)
