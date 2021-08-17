#
#   data jump is when new reading is a large difference from last, so it's incorrect and ignore it

import collections

from defines import *
from functions import string_to_float


class SensorClass(object):
    def __init__(self, parent, sid, ctr=None):  # sid = sensor id, did = display id, ctr = name eg le_light_1
        self.id = sid
        self.display_id = None
        self.var_name = ctr
        self.area_controller = parent
        self.db = self.area_controller.db
        self.action_handler = collections.defaultdict()
        self.area = None
        self.item = 0  # An area with process has 4 ranges, this is which one to use, read from db
        self.step = 1
        self.high = 22.0
        self.set = 20.0
        self.low = 19.0
        self.high_org = 999  # Original values are only used for areas 1 & 2 and will hold the process default
        self.set_org = 999  # values so it can compare the set values to these to indicate the process values
        self.low_org = 999  # have be user changed
        self.value = None
        self.value_last = 0
        self.has_range = False  # Set True when set range is called. If false no colouring display
        self.status_ctrl = None  # The ctrl to indicate set point
        self.is_first_update = True  # Set false after 1st update, for data jump detection
        self.trend_ctrl = None
        self.calibration = 0
        self.short_name = ""
        self.display_ctrl = None
        self.process_id = None
        self._is_fan = False  # True is this sensor is used by fan
        self.handler_info = collections.defaultdict()  # Holds info for display ctrl about sensors handler
        # print("Sensor " + str(self.id) + " maps to " + str(self.display_id))
        self.load_profile()  # Required here to load defaults for any that have no process

    def load_profile(self):
        row = self.db.execute_one_row(
            'SELECT maps_to, calibration, step, area, area_range, short_name FROM {} WHERE id = '
            '{}'.format(DB_SENSORS_CONFIG, self.id))
        if row is None:
            self.area = 0
            return
        self.set_display_id(row[0])
        self.calibration = row[1]
        self.step = row[2]
        self.area = row[3]
        self.item = row[4]
        self.short_name = row[5]

    def load_range(self):
        if self.area_controller.area_has_process(self.area):
            # Load process range values
            p = self.area_controller.get_area_process(self.area)
            if p != 0:
                p.load_active_temperature_ranges()
                r = p.temperature_ranges_active
                if r is not None:
                    r = r[self.item]
                    self.set_range(r)
                    ro = p.temperature_ranges_active_org[self.item]
                    self.set_range_org(ro)
                else:
                    # @todo Add call to msg sys - No temperature range for process
                    self.area_controller.sensor_load_manual_ranges(self.area, self.item)
        else:
            self.area_controller.sensor_load_manual_ranges(self.area, self.item)

    @property
    def is_fan(self):
        return self._is_fan

    @is_fan.setter
    def is_fan(self, value):
        self._is_fan = value
        self.update_status_ctrl()

    def set_display_id(self, did):
        if did is None or did > 12:
            return
        self.display_id = did
        self.display_ctrl = getattr(self.area_controller.main_panel, "lereading_%i" % self.display_id)
        self.status_ctrl = getattr(self.area_controller.main_panel, "tesstatus_%i" % self.display_id)
        self.trend_ctrl = getattr(self.area_controller.main_panel, "lbltrend_%i" % self.display_id)

    def set_display_ctrl_name(self, name):
        self.var_name = name
        try:
            self.display_ctrl = getattr(self.area_controller, self.var_name)
        except():
            self.display_ctrl = None

    def set_status_ctrl(self, ctrl):
        self.status_ctrl = ctrl

    def set_action_handler(self, handler):
        if self._find_handler(handler.ctrl_id) == handler.ctrl_id:
            return
        self.action_handler[handler.ctrl_id] = handler
        self.update_handler(handler)

    def _find_handler(self, hid):
        for h in self.action_handler:
            if hid == h:
                return id
        return -1

    def set_range(self, range_):
        if range_ is not None:
            # print(range_)
            self.low = float(range_['low'])
            self.set = float(range_['set'])
            self.high = float(range_['high'])
            self.has_range = True
        self.update_status_ctrl()
        for handler in self.action_handler:
            self.update_handler(self.action_handler[handler])
            # handler.has_process = self.process_id

    def set_range_org(self, range_):
        self.low_org = float(range_['low'])
        self.set_org = float(range_['set'])
        self.high_org = float(range_['high'])

    def get_set(self):
        return self.set

    def get_set_temperatures(self):
        return self.set, self.high, self.low

    def get_org_temperatures(self):
        return self.set_org, self.high_org, self.low_org

    def update_handler(self, handler):
        handler.set_limits(self.low, self.set)
        if handler.short_name not in self.handler_info:
            self.handler_info[handler.short_name] = []
        self.handler_info[handler.short_name] = {'on': handler.temp_on_adjusted, 'off': handler.temp_off_adjusted}

    def update_status_ctrl(self):
        if self.status_ctrl is None:
            return
        # ht = ""
        # for h in self.handler_info.keys():
        #     ht += h + "<br>"
        t = "<table>"
        #  Low value
        if self.low_org != 999 and self.low != self.low_org:
            tv = "<i>{}</i>".format(self.low)
        else:
            tv = self.low
        t += "<tr><td style='font-size:12px; padding:2px 0px 0px 0px;'>{}</td>".format(tv)

        #  set value
        if self.set_org != 999 and self.set != self.set_org:
            tv = "<i>{}</i>".format(self.set)
        else:
            tv = self.set
        if self._is_fan:
            t += "<td style='padding:0px 12px 0px 12px;' rowspan='2' style='text-align:center; vertical-align:middle;" \
                 " color:blue'>{}</td>".format(tv)
        else:
            t += "<td style='padding:0px 12px 0px 12px;' style='text-align:center; vertical-align:middle'>{}</td>". \
                format(tv)

        #      high value
        if self.high_org != 999 and self.high != self.high_org:
            tv = "<i>{}</i>".format(self.high)
        else:
            tv = self.high
        t += "<td style='padding:2px 0px 0px 0px;' style='font-size:12px;'>{}</td>".format(tv)
        t += "</tr></table>"
        self.status_ctrl.setText(t)

    def off(self):
        self.status_ctrl.clear()

    def load_calibration(self):
        self._calibration = self.db.execute_single(
            "SELECT calibration FROM {} WHERE id = {}".format(DB_SENSORS_CONFIG, self.id + 1))
        if self._calibration is None:
            self._calibration = 0
        # print("sensor ID {}   Display ID {}    Calibration {}".format(self.id, self.display_id, self.calibration))

    @property
    def calibration(self):
        return self._calibration

    @calibration.setter
    def calibration(self, value):
        self._calibration = value
        self.db.execute_write(
            "UPDATE {} SET calibration = {} WHERE id = {}".format(DB_SENSORS_CONFIG, value, self.id + 1))
        # print("sensor ID {}   Display ID {}    Calibration {}".format(self.id, self.display_id, self._calibration))

    def update(self, new_value):
        try:
            new_value = string_to_float(new_value)
            self.value = round(new_value + self.calibration, 2)

            # if (self.value_last + 7 > new_value < self.value_last - 7) or new_value > 100 and not self.is_first_update:
            # ts = "Sensor {}   New {}    Old {}".format(self.id, self.value, self.value_last)
            # print(ts)
            if self.display_ctrl is None:
                return
            if self.display_id < 13:
                # Temperatures
                if self.value < - 100:
                    self.display_ctrl.setText("Err")
                    return

                self.display_ctrl.setText(str(self.value))
                if self.has_range:
                    # colour_offset = self.value - self.set
                    colour_offset = self.get_colour_offset()
                    # colour_offset = 2 - self.id
                else:
                    colour_offset = 0
                r, g, b, rt, gt, bt = self.get_colour(colour_offset)
                self.display_ctrl.setStyleSheet(
                    "background-color: rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ");  color: rgb(" + str(
                        rt) + ", " + str(gt) + ", " + str(bt) + ");")
                trend = self.value_last - self.value
                if abs(trend) <= 0.05:
                    self.trend_ctrl.setText("w")
                elif trend > 0.6:
                    self.trend_ctrl.setText("q")
                elif trend > 0.05:
                    self.trend_ctrl.setText("s")
                elif abs(trend) > 0.6:
                    self.trend_ctrl.setText("p")
                elif abs(trend) > 0.05:
                    self.trend_ctrl.setText("r")
                self.value_last = self.value

            elif 12 > self.display_id < 15:
                print("******** nv= " + str(self.value))
            for handler in self.action_handler:
                self.action_handler[handler].check(self.value)
            self.is_first_update = False
        except Exception as e:
            print("Class Sensor - Update value ERROR ", e.args)

    def get_value(self):
        return self.value

    def get_colour_offset(self):
        dif = self.value - self.set
        if dif > 0:
            r = self.high - self.set
            if (dif > (r * 0.65)) and dif <= r:
                return 1
            if dif <= r:
                return 0
            else:
                return int(dif + 1)
        elif dif < 0:
            r = self.low - self.set
            if (dif < (r * 0.65)) and dif >= r:
                return -1
            if dif >= r:
                return 0
            else:
                return int(dif + 1)
        return 0

    @staticmethod
    def get_colour(offset):
        if offset > 0:
            offset = 5 if offset > 5 else offset
            r = int(51 * offset)
            g = int(255 - (51 * offset))
            b = 0
        elif offset < 0:
            offset = -5 if offset < -5 else offset
            r = 0
            g = abs(int(255 + (51 * offset)))
            b = abs(int(51 * offset))
        else:
            r = 0
            g = 255
            b = 0
        rt = 255 - r
        gt = 255 - g
        bt = 255 - b
        return r, g, b, rt, gt, bt
