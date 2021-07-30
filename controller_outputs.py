import collections
import winsound

from PyQt5.QtCore import QObject, pyqtSlot

from class_outputs import OutputClass
from defines import *
from functions import play_sound, sound_click


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
                self.outputs[oid] = OutputClass(self, row[0])   # ID used for controls id
            self.outputs[oid].load_profile()
            if self.outputs[oid].input > 0:
                self.areas_controller.sensors[self.outputs[oid].input].set_action_handler(self.outputs[oid])  # Link sensor to output

    def get_set_temperatures(self, op_id):
        return self.outputs[op_id].get_set_temperatures()

    def get_actual_position(self, op_id):
        return self.outputs[op_id].relay_position

    def change_mode(self, op_id, mode):
        self.outputs[op_id].set_mode(mode)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_MODE, op_id, mode)

    def change_sensor(self, op_id, sid):
        self.outputs[op_id].save_input_sensor(sid)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_SENSOR, op_id)

    def change_range(self, op_id, on, off):
        self.outputs[op_id].set_range(on, off)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_RANGE, op_id)

    def change_trigger(self, op_id, mode):
        self.outputs[op_id].set_detection(mode)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_TRIGGER, op_id)

    def switch_output(self, op_id, state=None):
        if self.outputs[op_id].mode >= 2:    # Auto modes
            self.outputs[op_id].switch()
        else:   # Manual off or on
            # Instead of calling switch this calls set_mode_by_state as user has clicked on/off so output will go into
            # manual off or manual on, and this set_mode_by_state calls the switch
            self.outputs[op_id].set_mode_by_state(state)
        sound_click()

    @pyqtSlot(int, int, int, name="updateSwitch")
    def switch_update(self, sw, state, module):
        if sw in self.outputs:
            self.outputs[sw].switch_update(state)
