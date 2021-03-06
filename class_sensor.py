import collections
from datetime import *

from class_max_min import MaxMin
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
        self.has_process = False    #
        self.status_ctrl = None  # The ctrl to indicate set point
        self.is_first_update = True  # Set false after 1st update, for data jump detection
        self.trend_ctrl = None
        self.calibration = 0
        self.show_calibration = True
        self.error_count = 0
        self.short_name = ""
        self.display_ctrl = None
        self.process_id = None
        self.graph_data = []
        self.graph_times = []
        self.range_inactive = None      # Hold the temperature range for inactive period
        self._is_fan = False  # True is this sensor is used by fan
        self.handler_info = collections.defaultdict()  # Holds info for display ctrl about sensors handler
        # print("Sensor " + str(self.id) + " maps to " + str(self.display_id))
        self.load_profile()  # Required here to load defaults for any that have no process
        self.max_min = MaxMin(self)

    def load_profile(self):
        """ Loads the sensor config"""
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
        """ Loads the sensors range values. For sensors with a process this will be from the process
            This loads the low, set and high values for all area sensors for both day and night
            Call this when any of the range values change, either by user or by changing day and night"""
        if self.area_controller.area_has_process(self.area) and self.area < 3:
            # Load process range values
            p = self.area_controller.get_area_process(self.area)
            if p != 0:
                # p.load_temperature_adjustments()
                r = p.get_temperature_range_item(self.item)
                if len(r) > 0:
                    self.set_range(r)
                    ro = p.get_temperature_range_item_default(self.item)
                    self.set_range_org(ro)
                    self.range_inactive = p.get_temperature_range_item_default(self.item, False)
                    self.has_process = True
                else:
                    # @todo Add call to msg sys - No temperature range for process
                    self.has_process = False
                    self.area_controller.sensor_load_manual_ranges(self.area, self.item)
        else:
            self.has_process = False
            if self.area_controller.area_is_manual(self.area) or self.area > 2:
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
        if did < 2:     # No status ctrl for outside
            self.status_ctrl = None
        else:
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
        # t = '<table cellspacing = "0" width="100%" border= "1px">'
        # #  Low value
        # if self.low_org != 999 and self.low != self.low_org:
        #     tv = "<i>{}</i>".format(self.low)
        # else:
        #     tv = self.low
        # # t += "<tr><td style='font-size:{}px; vertical-align:middle; padding:0px 0px 0px 0px;'>{}</td>"\
        # t += "<tr><td style='width:33%;'>{}</td>".format(tv)
        #
        # #  set value
        # if self.set_org != 999 and self.set != self.set_org:
        #     tv = "<i>{}</i>".format(self.set)
        # else:
        #     tv = self.set
        # if self._is_fan:
        #     t += "<td style='width:33%; color:blue'>{}</td>".format(tv)
        # else:
        #     # t += "<td style='padding:0px 6px 0px 6px;' style='text-align:center; vertical-align:middle;'>{}</td>". \
        #     t += "<td style='width:33%; padding:0px 8px 8px 6px;'>{}</td>". format(tv)
        #
        # #      high value
        # if self.high_org != 999 and self.high != self.high_org:
        #     tv = "<i>{}</i>".format(self.high)
        # else:
        #     tv = self.high
        # # t += "<td style='padding:0px 0px 0px 0px; vertical-align:middle; font-size:{}px;'>{}</td>".format(font_size, tv)
        # t += "<td style='width:33%;'>{}</td>".format(tv)
        # t += "</tr></table>"
        self.status_ctrl.setText(str(self.set))
        self.status_ctrl.setToolTip("Low: {}<br><b>Set: {}</b><br>High: {}".format(self.low, self.set, self.high))

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
            new_value = round(new_value + self.calibration, 2)

            cm = datetime.now().minute
            if cm % 2 == 0:
                self.graph_times.append(datetime.now().time())
                self.graph_data.append(new_value)
                if len(self.graph_data) > 30:
                    self.graph_data.pop(0)
                    self.graph_times.pop(0)

            if self.display_ctrl is None:
                return
            if self.display_id < 13:
                # Temperatures
                if new_value < - 100:
                    self.error_count += 1
                    self.value = self.value_last
                    if self.error_count > 5:
                        self.display_ctrl.setText("Err")
                        self.display_ctrl.setStyleSheet("background-color: white; color: black;")
                        if self.id < 9:     # DHT sensors so reset power to them
                            # Switch relay on to break power, when sw on is received back it will switch it off
                            if self.area_controller.master_mode == MASTER:
                                self.area_controller.main_window.coms_interface.send_switch(SW_DHT_POWER, ON)
                                colour_offset = 0
                                r, g, b, rt, gt, bt = self.get_colour(colour_offset)
                                self.display_ctrl.setStyleSheet(
                                    "background-color: rgb(" + str(r) + ", " + str(g) + ", " + str(b) +
                                    ");  color: rgb(" + str(rt) + ", " + str(gt) + ", " + str(bt) + ");")
                    return
                else:
                    self.value = new_value
                    self.max_min.check(new_value)

                self.error_count = 0
                self.display_ctrl.setText(str(round(self.value, 1)))
                if self.area < 3 and self.area_controller.cool_warm[self.area] != NORMAL:
                    colour_offset = 0
                elif self.has_range and (self.has_process and self.area < 3 or self.area_controller.area_is_manual(self.area)):
                    colour_offset = self.get_colour_offset()
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
        return round(self.value, 1)

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
