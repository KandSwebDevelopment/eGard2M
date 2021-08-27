import collections

from PyQt5.QtCore import QObject, pyqtSlot

from class_output_water_heater import OutputWaterHeater
from class_output_workshop_heater import OutputWorkshopHeater
from class_outputs import OutputClass
from defines import *
from functions import sound_click


class OutputController(QObject):
    def __init__(self, parent):
        """

        :type parent: _main
        """
        super(OutputController, self).__init__()
        self.area_controller = parent     # Areas controller
        self.db = self.area_controller.db
        self.main_panel = parent.main_panel
        self.master_mode = self.main_panel.master_mode
        self.outputs = collections.defaultdict(OutputClass)

        self.area_controller.main_window.coms_interface.update_switch.connect(self.switch_update)

    def load_all_areas(self):
        self.load_outputs(1)
        self.load_outputs(2)
        self.load_outputs(3)    # Drying
        self.load_outputs(4)    # Workshop
        self.load_outputs(7)    # Water heaters

    def load_outputs(self, area):
        sql = 'SELECT `id`, `name`, `area`, `type`, `input`, `range`, `pin`, `short_name` FROM {} WHERE area = {}'.\
            format(DB_OUTPUTS, area)
        rows = self.db.execute(sql)
        for row in rows:
            oid = row[6]    # Pin number
            if oid not in self.outputs.keys():
                if row[2] == 7:     # If area 7 then its a water heater
                    self.outputs[oid] = OutputWaterHeater(self, row[0])   # ID used for controls id
                elif row[2] == 4:     # If area 4 then its a workshop heater
                    self.outputs[oid] = OutputWorkshopHeater(self, row[0])   # ID used for controls id
                else:   # All other outputs
                    self.outputs[oid] = OutputClass(self, row[0])   # ID used for controls id
            self.outputs[oid].load_profile()
            if self.outputs[oid].input_sensor > 0:
                self.area_controller.sensors[self.outputs[oid].input_sensor].set_action_handler(self.outputs[oid])  # Link sensor to output
            if self.master_mode == SLAVE:
                self.area_controller.main_window.coms_interface.relay_send(NWC_SWITCH_REQUEST, oid)
                print("out request ", oid)

    def check_water_heaters(self):
        self.outputs[OUT_WATER_HEATER_1].check(0)
        self.outputs[OUT_WATER_HEATER_2].check(0)

    def get_set_temperatures(self, op_id):
        return self.outputs[op_id].get_set_temperatures()

    def get_actual_position(self, op_id):
        return self.outputs[op_id].relay_position

    def change_mode(self, op_id, mode):
        """ Set the mode for a output and relays it"""
        self.outputs[op_id].set_mode(mode)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_MODE, op_id, mode)

    def change_sensor(self, op_id, sid):
        self.outputs[op_id].set_input_sensor(sid)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_SENSOR, op_id, sid)

    def change_range(self, op_id, on, off):
        self.outputs[op_id].set_range(on, off)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_RANGE, op_id)

    def reload_range(self, op_id):
        self.outputs[op_id].load_ranges()
        self.outputs[op_id].update_info()

    def change_trigger(self, op_id, mode):
        self.outputs[op_id].set_detection(mode)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_TRIGGER, op_id, mode)

    def switch_output(self, op_id, state=None):
        if self.outputs[op_id].mode >= 2:    # Auto modes
            self.outputs[op_id].switch_hard(state)
        else:   # Manual off or on
            self.outputs[op_id].set_mode(int(not self.outputs[op_id].mode))
            self.main_panel.coms_interface.relay_send(NWC_OUTPUT_MODE, op_id, self.outputs[op_id].mode)
            self.outputs[op_id].switch_hard(state)
        sound_click()

    def set_last_feed_date(self, lfd):
        self.area_controller.main_window.feed_controller.set_last_feed_date(lfd)

    def set_limits(self, op_id, low, high):
        self.outputs[op_id].set_limits(low, high)

    @pyqtSlot(int, int, int, name="updateSwitch")
    def switch_update(self, sw, state, module):
        if module == MODULE_IO or module == MODULE_SL:
            if sw in self.outputs:
                self.outputs[sw].switch_update(state)
        elif module == MODULE_DE:
            if sw == SW_COVER_OPEN and state == ON_RELAY:
                if self.outputs[OUT_HEATER_ROOM].auto_boost:
                    self.outputs[OUT_HEATER_ROOM].switch_update(ON)
            elif sw == SW_COVER_CLOSE and state == ON_RELAY:
                self.outputs[OUT_HEATER_ROOM].switch_update(OFF)

    def update_info(self, op_id):
        self.outputs[op_id].update_info()

    def water_heater_update_info(self):
        """ This should be called any time the feed date changes
            It updates the days_till_feed, displays it and relays to other pc"""
        d = min(self.area_controller.main_window.feed_controller.days_till_feed(1),
                self.area_controller.main_window.feed_controller.days_till_feed(2))
        if not self.outputs[OUT_WATER_HEATER_1].mode == OFF:
            self.outputs[OUT_WATER_HEATER_1].set_days_till_feed(d)
        if not self.outputs[OUT_WATER_HEATER_2].mode == OFF:
            self.outputs[OUT_WATER_HEATER_2].set_days_till_feed(d)

    def water_heater_set_duration(self, duration):
        """ duration can either be an int with duration as minutes ie 240 or as a string ie 'hh:mm' or a QTime object"""
        if type(duration) == str:
            s = duration.split(':')
            d = (int(s[0]) * 60) + int(s[1])
        elif not type(duration) == int:
            d = ((duration.hour() * 60) + duration.minute())
        else:
            d = duration
        self.db.set_config_both(CFT_WATER_HEATER, 'heater duration', d)
        self.outputs[OUT_WATER_HEATER_1].set_duration(d)
        self.outputs[OUT_WATER_HEATER_2].set_duration(d)

    def water_heater_set_off_time(self, off_time):
        """ This only updates the water heater variable as main handling is done bt the feed_controller """
        self.outputs[OUT_WATER_HEATER_1].set_off_time(off_time)
        self.outputs[OUT_WATER_HEATER_2].set_off_time(off_time)

    def water_heater_set_frequency(self, output_pin, frequency):
        self.outputs[output_pin].set_frequency(frequency)
        self.db.set_config_both(CFT_WATER_HEATER, "frequency {}".format(self.outputs[output_pin].heater_id), frequency)
