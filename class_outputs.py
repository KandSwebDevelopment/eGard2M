from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot
from datetime import timedelta, datetime

from PyQt5.QtGui import QIcon, QPixmap

from defines import *
from winsound import Beep

from functions import play_sound, string_to_float, sound_on, sound_off


class OutputClass(QObject):
    # output_update = pyqtSignal(int, int, str)   # id, state, tooltip

    def __init__(self, parent, ctrl_id):
        super().__init__()
        """ :type parent: MainWindow """
        self.output_controller = parent
        self.db = self.output_controller.db
        self.ctrl_id = ctrl_id
        self.detection = DET_FALL  # How it is triggered
        self.output_pin = None  # The output number/pin number to switch
        self.name = ""
        self.area = 0
        self.status = -1  # The output current status
        self.status_last = None
        self.mode = 0   # 0=Off, 1=Manual, 2=Sensor, 3=Timer, 4=Both, 5=Day only, 6=Night only,
        self.type = 1   # 1=Normal, 5=Water heater
        self.input_sensor = None
        self.range = [0, 0]
        self.has_process = False    # If area 1 to 3, is there an active process
        self.linked = ""    # The sensor name it is linked to
        self.temp_on_adjusted = 15       # The outputs value = sensor value - range adjustment
        self.temp_off_adjusted = 18      # The outputs value = sensor value - range adjustment
        self.temp_off = 18               # The sensors set value
        self.temp_on = 15                # The sensors set value
        self.relay_position = OFF        # The actual position of the output, this should only be changed by switch_update
        self.is_active = False  # If False then it is off and will not do anything
        self.duration = 0  # Time on max duration
        self.off_time = datetime.now()
        self.status_ctrl = None  # The control used to indicate output status
        self.info_ctrl = None   # The control which shows the on off settings
        self.remaining = 0  # The minuets remaining for on
        self.short_name = ""
        self.tooltip = ""
        self.font_i = QtGui.QFont()
        self.font_i.setItalic(True)
        self.font_i.setPointSize(11)
        self.font_n = QtGui.QFont()
        self.font_n.setItalic(False)
        self.font_n.setPointSize(11)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_event)
        self.locked = 0

    def load_profile(self):
        if self.output_controller.area_controller.get_light_status(self.area):
            row = self.db.execute_one_row('SELECT `name`, `area`, `type`, `input`, `range`, `pin`, `short_name`, '
                                          '`trigger`, locked FROM {}'
                                          ' WHERE id = {}'. format(DB_OUTPUTS, self.ctrl_id))
        else:
            row = self.db.execute_one_row('SELECT `name`, `area`, `type`, `input`, `range_night`, `pin`, '
                                          '`short_name`, `trigger`, locked FROM {}'
                                          ' WHERE id = {}'. format(DB_OUTPUTS, self.ctrl_id))
        if len(row) == 0:
            return
        self.name = row[0]
        self.area = row[1]
        self.mode = row[2]
        self.input_sensor = row[3]
        self.detection = row[7]
        self.range = (row[4]).split(",")
        self.output_pin = row[5]
        self.short_name = row[6]
        self.locked = row[8]
        self.has_process = False
        if self.area < 4 and self.output_controller.area_controller.area_has_process(self.area):
            self.has_process = True
        self.tooltip = row[0] + "<br>Type:" + str(row[2]) + " Sensor:" + str(row[3])
        self._check()
        self.calculate_limits()
        self.update_control(self.status)

    def load_ranges(self):
        s, hi, lo = self.output_controller.area_controller.sensors[self.input_sensor].get_set_temperatures()
        if self.output_controller.area_controller.get_light_status(self.area):
            range_ = self.db.execute_single('SELECT `range` FROM {} WHERE id = {}'. format(DB_OUTPUTS, self.ctrl_id))
        else:
            range_ = self.db.execute_single('SELECT `range_night` FROM {} WHERE id = {}'. format(DB_OUTPUTS, self.ctrl_id))
        self.temp_on = lo
        self.temp_off = s
        range_ = range_.split(",")
        self.range[0] = string_to_float(range_[0])
        self.range[1] = string_to_float(range_[1])
        self.calculate_limits()
        self.update_info()

    def set_locked(self, lock):
        if lock == self.locked:
            return
        self.locked = lock
        self.db.execute_write('UPDATE {} SET locked = {} WHERE id = {} LIMIT 1'.format(DB_OUTPUTS, lock, self.ctrl_id))
        self.update_info()

    def set_mode(self, mode):
        """ Updates the outputs mode and saves it to the db and updates the outputs info control """
        self.mode = mode
        self.db.execute_write('UPDATE {} SET type = {} WHERE id = {} LIMIT 1'.format(DB_OUTPUTS, mode, self.ctrl_id))
        self._check()
        self.update_info()
        # Don't send this from here as is causes a loop
        # self.output_controller.coms_interface.relay_send(NWC_OUTPUT_MODE, self.id, self.mode)

    def set_mode_by_state(self, state=None):
        """ This will only be triggered as a result of a user clicking on/off """
        if state is None:
            state = int(not self.status)
        if state == 1:
            self.set_mode(1)  # Manual = On
        elif state == 0:
            self.set_mode(0)    # Off

    def update_mode(self, mode):
        """ Updates the outputs mode does not save it to the db but updates the outputs info control"""
        self.mode = mode
        self._check()
        self.update_info()

    def set_range(self, on_dif, off_dif, tmz):
        """ Set new values for range (Difference between sensor set point and output switching values
            and updates the db and the control """
        self.range[0] = round(on_dif, 1)
        self.range[1] = round(off_dif, 1)
        r = "{}, {}".format(on_dif, off_dif)
        if tmz == DAY:
            sql = 'UPDATE {} SET `range` = "{}" WHERE id = {}'.format(DB_OUTPUTS, r, self.ctrl_id)
        else:
            sql = 'UPDATE {} SET `range_night` = "{}" WHERE id = {}'.format(DB_OUTPUTS, r, self.ctrl_id)
        print(sql)
        self.db.execute_write(sql)

        self.calculate_limits()
        
    def set_input_sensor(self, sensor_id):
        """ Updates the input sensor and saves it to the db and reloads all outputs for the area.
            This ensures the sensor classes handler list has any old inputs removed"""
        self.db.execute_write('UPDATE {} SET input = {} WHERE id = {} LIMIT 1'.format(DB_OUTPUTS, sensor_id, self.ctrl_id))
        self.output_controller.load_outputs(self.area)

    def set_detection(self, detection):  # See defines DET_ detection types
        self.detection = detection
        self.db.execute_write('UPDATE {} SET `trigger` WHERE id = {} LIMIT 1'. format(DB_OUTPUTS, self.ctrl_id))

    def set_limits(self, on_temp, off_temp):
        """ Set the on and off temperatures for the output and updates all """
        self.temp_on = on_temp
        self.temp_off = off_temp
        self.calculate_limits()

    def get_set_temperatures(self):
        return self.temp_on, self.temp_off

    def calculate_limits(self):
        r = 0
        if self.range[1] != "":
            r = float(self.range[1])
        self.temp_off_adjusted = float(self.temp_off) + r
        r = 0
        if self.range[0] != "":
            r = float(self.range[0])
        self.temp_on_adjusted = float(self.temp_on) + r
        self.update_info()

    def get_status(self):
        return self.status

    def _check(self):
        if self.mode == 0:  # Off
            self.switch(OFF)
            return
        if self.mode == 1:  # Manual = On
            self.switch(ON)
            return
        if self.mode == 5:  # Day
            if self.area == 1 and self.has_process:
                self.switch(self.output_controller.area_controller.get_area_process(1).get_light_status())
                return
            if self.area == 2 and self.has_process:
                self.switch(self.output_controller.area_controller.get_area_process(2).get_light_status())
                return
        if self.mode == 6:  # Night
            if self.area == 1 and self.has_process:
                self.switch(1 - self.output_controller.area_controller.get_area_process(1).get_light_status())
                return
            if self.area == 2 and self.has_process:
                self.switch(1 - self.output_controller.area_controller.get_area_process(2).get_light_status())
                return

    def check(self, value):
        try:
            self._check()
            if self.mode == 2 or self.mode == 4:  # Sensor or both
                if self.detection & DET_RISE == DET_RISE:
                    if value >= self.temp_off_adjusted:
                        self.switch(OFF)
                    elif value <= self.temp_on_adjusted:
                        self.switch(ON)
                elif self.detection & DET_FALL == DET_FALL:
                    if (self.area < 3 and self.output_controller.area_controller.cool_warm[self.area] <= NORMAL) or self.area > 2:
                        if value <= self.temp_on_adjusted and value <= self.temp_off_adjusted:
                            self.switch(ON)
                        elif value >= self.temp_off_adjusted:
                            self.switch(OFF)
            if self.detection & DET_TIMER == DET_TIMER and self.off_time is not None:
                if self.remaining <= 0 or self.off_time <= datetime.now():
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
        if state is None:
            state = int(not self.status)
        if state != self.status_last and self.output_controller.master_mode == MASTER:
            self.output_controller.area_controller.main_window.coms_interface.send_switch(self.output_pin, state)
            # @Todo Add to event log

    def switch_hard(self, state=None):
        """ This will send switch if it is the master or slave, use for user switching requests
        @param state: On or Off
        @type state: int
        """
        if state is None:
            state = int(not self.status)
        self.output_controller.area_controller.main_window.coms_interface.send_switch(self.output_pin, state)
        # @Todo Add to event log

    def switch_update(self, state):
        self.update_control(state)
        self.status = state
        self.relay_position = state
        if state != self.status_last:
            if state == 1:
                # play_sound(SND_ON)
                sound_on()
            else:
                sound_off()
                # play_sound(SND_OFF)
        self.status_last = state

    def soft_switch(self, state):
        """ This is only used by the relay command, it only updates it's output state and display, it does
            not do any switching"""
        self.update_control(state)
        self.status_last = state
        self.status = state
        if state == ON:
            if self.status_last is not None:
                sound_on()
                # play_sound(SND_ON)
            if self.detection & DET_TIMER == DET_TIMER and self.type != 5:
                if self.duration > 0:
                    self.off_time = (datetime.now() + timedelta(minutes=self.duration))
                    self.remaining = self.duration
                    self.timer.start()
        else:
            if self.detection & DET_TIMER == DET_TIMER:
                self.is_active = False
                self.timer.stop()
                self.output_controller.lbl_workshop_timer.setText("")
            if self.status_last is not None:
                sound_off()
                # play_sound(SND_OFF)

    def timer_event(self):
        self.remaining = int(self.remaining - 1)
        if self.remaining < 1:
            self.timer.stop()
            self.switch()
            self.output_controller.lbl_workshop_timer.setText("")
            return
        m, s = divmod(self.remaining, 60)
        h, m = divmod(m, 60)
        if self.remaining >= 3600:
            s = '{:d}:{:02d}'.format(h, m)
        else:
            s = '{:02d}:{:02d}'.format(m, s)
        self.output_controller.lbl_workshop_timer.setText(s)

    def update_control(self, state):
        """ Displays on or off """
        ctrl = getattr(self.output_controller.main_panel, "pb_output_status_%i" % self.ctrl_id)

        if state == ON:
            ctrl.setIcon(QIcon(":/normal/output_on.png"))
        else:
            ctrl.setIcon(QIcon(":/normal/output_off.png"))

    def update_info(self):
        """ Displays the output type icon, sensor icon and mode icon """
        # Locked
        if self.locked:
            getattr(self.output_controller.main_panel, "lbl_output_number_%i" % self.ctrl_id).setText("L")
        else:
            getattr(self.output_controller.main_panel, "lbl_output_number_%i" % self.ctrl_id).setText("")

        # Output type
        ctrl = getattr(self.output_controller.main_panel, "lbl_output_%i" % self.ctrl_id)
        if self.short_name[:1] == "H":
            ctrl.setPixmap(QPixmap(":/normal/output_heater.png"))
        if self.short_name[:1] == "A":
            ctrl.setPixmap(QPixmap(":/normal/output_aux.png"))
        if self.short_name[:1] == "S":
            ctrl.setPixmap(QPixmap(":/normal/output_socket.png"))

        # Output mode
        if self.has_process or self.area > 3 or self.output_controller.area_controller.area_is_manual(self.area):
            getattr(self.output_controller.main_panel, "frm_output_%i" % self.ctrl_id).setEnabled(True)
            ctrl = getattr(self.output_controller.main_panel, "pb_output_mode_%i" % self.ctrl_id)
            if self.mode == 0:
                ctrl.setIcon(QIcon(":/normal/output_off_1.png"))
                ctrl.setToolTip("Mode: Off")
            elif self.mode == 1:
                ctrl.setIcon(QIcon(":/normal/output_manual_1.png"))
                ctrl.setToolTip("Mode: Manual On")
                # t = OUT_TYPE[self.mode]
            elif self.mode == 2:  # Sensor
                ctrl.setIcon(QIcon(":/normal/output_auto.png"))
                ctrl.setToolTip("Mode: Auto")
            elif self.mode == 3:
                ctrl.setIcon(QIcon(":/normal/output_timer.png"))
                ctrl.setToolTip("Mode: Timer")
            elif self.mode == 4:
                ctrl.setIcon(QIcon(":/normal/output_both.png"))
                ctrl.setToolTip("Mode: Sensor and timer")
            elif self.mode == 5:
                ctrl.setIcon(QIcon(":/normal/output_day.png"))
                ctrl.setToolTip("Mode: All Day")

            elif self.mode == 6:
                ctrl.setIcon(QIcon(":/normal/output_night.png"))
                ctrl.setToolTip("Mode: All Night")

            ctrl = getattr(self.output_controller.main_panel, "lbl_output_sensor_%i" % self.ctrl_id)
            if self.mode == 1:
                ctrl.setPixmap(QtGui.QPixmap())
            else:
                if self.input_sensor < 0:
                    ctrl.setPixmap(QtGui.QPixmap(":/normal/none.png"))
                else:
                    if self.output_controller.area_controller.sensors[self.input_sensor].short_name.find("Hum") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/065-humidity.png"))
                    elif self.output_controller.area_controller.sensors[self.input_sensor].short_name.find("Roo") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/061-care.png"))
                    elif self.output_controller.area_controller.sensors[self.input_sensor].short_name.find("Pro") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/067-leaf.png"))
                    elif self.output_controller.area_controller.sensors[self.input_sensor].short_name.find("Cor") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/062-plant.png"))

            if self.mode == 2 or self.mode == 4:
                getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).setText(str(self.temp_off_adjusted))
                getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).setText(str(self.temp_on_adjusted))
                if self.temp_on != self.temp_on_adjusted:
                    getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).setFont(self.font_i)
                else:
                    getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).setFont(self.font_n)
                if self.temp_off != self.temp_off_adjusted:
                    getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).setFont(self.font_i)
                else:
                    getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).setFont(self.font_n)
            else:
                getattr(self.output_controller.main_panel, "lbl_output_set_off_%i" % self.ctrl_id).clear()
                getattr(self.output_controller.main_panel, "lbl_output_set_on_%i" % self.ctrl_id).clear()
                # t += "<br>F: {}<br>N: {}".format(self.temp_off_adjusted, self.temp_on_adjusted)
            # self.info_ctrl.setText(t)
        else:
            if not self.output_controller.area_controller.area_is_manual(self.area):
                getattr(self.output_controller.main_panel, "frm_output_%i" % self.ctrl_id).setEnabled(False)
            pass
