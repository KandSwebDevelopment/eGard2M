import collections

from PyQt5.QtCore import QObject, pyqtSlot

from class_output_water_heater import OutputWaterHeater
from class_outputs import OutputClass
from defines import *
from functions import sound_click


class OutputController(QObject):
    def __init__(self, parent):
        """

        :type parent: _main
        """
        super(OutputController, self).__init__()
        self.areas_controller = parent     # Areas controller
        self.db = self.areas_controller.db
        self.main_panel = parent.main_panel
        self.master_mode = self.main_panel.master_mode
        self.outputs = collections.defaultdict(OutputClass)

        self.areas_controller.main_window.coms_interface.update_switch.connect(self.switch_update)
        # sql = 'SELECT name, area, type, input, range, pin, short_name, item FROM {}'.format(DB_OUTPUTS)
        # rows = self.db.execute(sql)
        # for row in rows:

    def load_all_areas(self):
        for a in range(1, 4):
            if self.areas_controller.area_has_process(a):
                # Area has process so load outputs
                self.load_outputs(a)
        # self.load_outputs(3)    # Drying
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
                else:
                    self.outputs[oid] = OutputClass(self, row[0])   # ID used for controls id
            self.outputs[oid].load_profile()
            if self.outputs[oid].input > 0:
                self.areas_controller.sensors[self.outputs[oid].input].set_action_handler(self.outputs[oid])  # Link sensor to output
            if self.master_mode == SLAVE:
                self.areas_controller.main_window.coms_interface.relay_send(NWC_SWITCH_REQUEST, oid)
                print("out request ", oid)

    def check_water_heaters(self):
        self.outputs[OUT_WATER_HEATER_1].check(0)
        self.outputs[OUT_WATER_HEATER_2].check(0)

    def get_set_temperatures(self, op_id):
        return self.outputs[op_id].get_set_temperatures()

    def get_actual_position(self, op_id):
        return self.outputs[op_id].relay_position

    def change_mode(self, op_id, mode):
        self.outputs[op_id].set_mode(mode)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_MODE, op_id, mode)

    def change_sensor(self, op_id, sid):
        self.outputs[op_id].set_input_sensor(sid)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_SENSOR, op_id, sid)

    def change_range(self, op_id, on, off):
        self.outputs[op_id].set_range(on, off)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_RANGE, op_id)

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
        self.areas_controller.main_window.feed_controller.set_last_feed_date(lfd)

    @pyqtSlot(int, int, int, name="updateSwitch")
    def switch_update(self, sw, state, module):
        if sw in self.outputs:
            self.outputs[sw].switch_update(state)

    def update_info(self, op_id):
        self.outputs[op_id].update_info()

    def update_water_heater_info(self):
        """ This should be called any time the feed date changes
            It updates the days_till_feed, displays it and relays to other pc"""
        d = min(self.areas_controller.main_window.feed_controller.days_till_feed(1),
                self.areas_controller.main_window.feed_controller.days_till_feed(2))
        self.outputs[OUT_WATER_HEATER_1].set_days_till_feed(d)
        self.outputs[OUT_WATER_HEATER_2].set_days_till_feed(d)
        self.main_panel.coms_interface.relay_send(NWC_FEED_DATE)

