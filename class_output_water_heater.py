from datetime import datetime, timedelta

from PyQt5.QtGui import QIcon

from class_outputs import OutputClass
from defines import *


class OutputWaterHeater(OutputClass):
    def __init__(self, parent, o_id):
        super().__init__(parent, o_id)
        self .on_time = datetime.now()      # Just to stop errors on initial loading
        self.output_controller = parent
        self.output_controller.areas_controller.main_window.coms_interface.update_float_switch.connect(self.float_update)
        self.float = FLOAT_DOWN
        self.is_feeding = False     # Set true if float goes down during feed time
        self.advance = 0    # For mode advance 0=Not used, 1=On till next off, 2=off till next on
        self.days_till_feed = 0         # This can not be set until the feed_control has initialised,
        #                                 init set by main_window calling new_day
        self.frequency = int(self.db.get_config(CFT_WATER_HEATER, "frequency {}".format(self.area), 1))
        self.use_float = int(self.db.get_config(CFT_WATER_HEATER, "float {}".format(self.area), 1))
        self.set_duration(self.db.get_config(CFT_WATER_HEATER, "heater duration", "03:00"))
        self.set_off_time(self.db.get_config(CFT_PROCESS, "feed time", "19:00"))
        self.feed_tol = int(self.db.get_config(CFT_PROCESS, "feed time tolerance", "2"))
        self.heater_id = self.ctrl_id - 10
        if not self.use_float:
            self.float = FLOAT_UP

    def set_off_time(self, off):
        dt = datetime.now()
        ot = datetime.strptime(off, "%H:%M:%S")
        self.off_time = datetime.combine(dt, ot.time())
        if dt > self.off_time:
            self.off_time = self.off_time + timedelta(days=1)
        self.calculate_on_time()

    def calculate_on_time(self):
        self.on_time = self.off_time - timedelta(minutes=self.duration)

    def float_update(self, tank, position):
        if not self.use_float:
            return
        if self.area == tank:
            self.float = position
            if self.status == ON and position == FLOAT_DOWN:
                self.switch(OFF)
                # Check to see if we are in feed window
                if datetime.now().time() >= (self.off_time - timedelta(hours=self.feed_tol)).time():
                    self.output_controller.areas_controller.main_window.msg_sys.\
                        add("Heater {} Off for feeding".format(tank), MSG_FLOAT_FEEDING + self.ctrl_id - 1, WARNING)
                    self.is_feeding = True
                else:
                    self.output_controller.areas_controller.main_window.msg_sys.\
                        add("Tank {} Empty".format(tank), MSG_FLOAT + self.ctrl_id - 1, WARNING)
            if position == FLOAT_UP:
                self.output_controller.areas_controller.main_window.msg_sys.remove(MSG_FLOAT + self.ctrl_id - 1)
                self.output_controller.areas_controller.main_window.msg_sys.remove(MSG_FLOAT_HEATER + self.ctrl_id - 1)

    def load_profile(self):
        row = self.db.execute_one_row('SELECT `name`, `area`, `type`, `input`, `range`, `pin`, `short_name`, '
                                      '`trigger`, `item` FROM {} WHERE id = {}'. format(DB_OUTPUTS, self.ctrl_id))
        if len(row) == 0:
            return
        self.name = row[0]
        self.area = row[8]
        self.mode = row[2]
        self.input = row[3]
        self.detection = row[7]
        self.range = (row[4]).split(",")
        self.output_pin = row[5]
        self.short_name = row[6]

        if self.output_controller.areas_controller.area_has_process(1) or\
                self.output_controller.areas_controller.area_has_process(2):
            self.has_process = True
        self._check()
        self.update_control(self.status)
        self.update_info()

    def check(self, value=None):
        if self.float == FLOAT_DOWN and not self.is_feeding:
            if self.status == ON:
                self.switch(OFF)
            else:
                if self.mode > 0:
                    self.output_controller.areas_controller.main_window.msg_sys.\
                        add("Tank {} Empty".format(self.area), MSG_FLOAT + self.ctrl_id - 1, WARNING)
                else:
                    self.output_controller.areas_controller.main_window.msg_sys.remove(MSG_FLOAT + self.ctrl_id - 1)
                self.output_controller.areas_controller.main_window.msg_sys.remove(MSG_FLOAT_HEATER + self.ctrl_id - 1)
        else:
            self.output_controller.areas_controller.main_window.msg_sys.remove(MSG_FLOAT + self.ctrl_id - 1)
            self.output_controller.areas_controller.main_window.msg_sys.remove(MSG_FLOAT_HEATER + self.ctrl_id - 1)

        try:
            self._check()
            if self.mode < 2:
                return
            if self.days_till_feed <= 0:
                if datetime.now().time() >= self.off_time.time():
                    self.switch(OFF)
                    if self.is_feeding:
                        self.output_controller.areas_controller.main_window.msg_sys.remove(
                            MSG_FLOAT_FEEDING + self.ctrl_id - 1)
                elif datetime.now().time() >= self.on_time.time():
                    if not self.is_feeding:
                        self.switch(ON)
            else:
                self.switch(OFF)
            self.update_control(self.status)
        except Exception as e:
            print("Output ERROR ", e.args)
        return

    def switch(self, state=None):
        """ This will only send switch if it is the master, use for software switching requests
        @param state: On or Off
        @type state: int
        """
        if self.float == FLOAT_DOWN and state == ON:
            if not self.is_feeding:
                self.output_controller.areas_controller.main_window.msg_sys. \
                    add("Tank {} Empty. Heater Required".format(self.area), MSG_FLOAT_HEATER + self.ctrl_id - 1, WARNING)
            if self.output_controller.areas_controller.main_window.msg_sys.has_msg_id(MSG_FLOAT + self.ctrl_id - 1):
                self.output_controller.areas_controller.main_window.msg_sys.remove(MSG_FLOAT + self.ctrl_id - 1)
            self.output_controller.areas_controller.main_window.coms_interface.send_switch(self.output_pin, OFF)
            return

        if state is None:
            state = int(not self.status)
        if state != self.status_last:
            self.output_controller.areas_controller.main_window.coms_interface.send_switch(self.output_pin, state)
            # @Todo Add to event log
        self.status = state
        self.status_last = state

    def update_info(self):
        OutputClass.update_info(self)
        getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).\
            setText(datetime.strftime(self.off_time, "%H:%M"))
        getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).\
            setText(datetime.strftime(self.on_time, "%H:%M"))
        getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id).setText(str(self.days_till_feed))
        if self.is_feeding:
            getattr(self.my_parent, "pb_output_mode_%i" % self.ctrl_id).setIcon(QIcon(":/normal/next_feed.png"))

    def set_days_till_feed(self, days):
        self.days_till_feed = days
        self.update_info()

    def new_day(self):
        # self.load_days_till_feed()
        pass
