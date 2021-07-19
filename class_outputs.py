from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from datetime import timedelta, datetime

from PyQt5.QtGui import QIcon, QPixmap

from defines import *
import winsound


def play_sound(sound):
    winsound.Beep(sound[0], sound[1])
    if len(sound) > 2:
        winsound.Beep(sound[2], sound[3])


class Output(QObject):
    output_update = pyqtSignal(int, int, str)   # id, state, tooltip

    def __init__(self, parent, o_id):
        super().__init__()
        """ :type parent: MainWindow """
        self.my_parent = parent
        self.db = self.my_parent.db
        self.id = o_id
        self.detection = DET_FALL  # How it is triggered
        self.output_pin = None  # The output number/pin number to switch
        self.name = ""
        self.area = None
        self.status = -1  # The output current status
        self.mode = 0   # 0=Off, 1=Manual, 2=Sensor, 3=Timer, 4=Both, 5=Day only, 6=Night only,
        #                 11=Advance on till off, 12 advance off till on
        #                 99 = Not a mode, indicates
        self.type = 1   # 1=Normal, 5=Water heater
        self.input = None
        self.range = [0, 0]
        self.has_process = False    # If area 1 to 3, is there an active process
        self.linked = ""    # The sensor name it is linked to
        self.temp_on_adjusted = 15       # The outputs value = sensor value - range adjustment
        self.temp_off_adjusted = 18      # The outputs value = sensor value - range adjustment
        self.temp_off = 18               # The sensors set value
        self.temp_on = 15                # The sensors set value
        # self.temp_set = 20
        self.is_active = False  # If False then it is off and will not do anything
        self.duration = 0  # Time on max duration
        self.off_time = datetime.now()
        self.out_status_last = None
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

        # if self.id < 14:
        # self.lbl = getattr(self.my_parent, "pb_output_status_%i" % self.id)
        getattr(self.my_parent, "pb_output_status_%i" % self.id).clicked.connect(self.switch_by_button)
        if self.id == 7:
            getattr(self.my_parent, "pb_output_mode_%i" % self.id).\
                clicked.connect(lambda: self.my_parent.show_drying_area())
        elif self.id == 8:
            getattr(self.my_parent, "pb_output_mode_%i" % self.id).\
                clicked.connect(lambda: self.my_parent.show_workshop())
        elif self.id < 11:
            a = self.db.execute_single('SELECT `area` FROM {}'
                                       ' WHERE id = {}'.format(DB_OUTPUTS, self.id))
            getattr(self.my_parent, "pb_output_mode_%i" % self.id).\
                clicked.connect(lambda: self.my_parent.show_outputs(a))
        else:
            getattr(self.my_parent, "pb_output_mode_%i" % self.id).\
                clicked.connect(lambda: self.my_parent.show_water_heaters())

    def load_profile(self):
        row = self.db.execute_one_row('SELECT `name`, `area`, `type`, `input`, `range`, `pin`, `short_name` FROM {}'
                                      ' WHERE id = {}'. format(DB_OUTPUTS, self.id))
        if len(row) == 0:
            return
        self.name = row[0]
        self.area = row[1]
        self.mode = row[2]
        self.input = row[3]
        self.range = (row[4]).split(",")
        self.output_pin = row[5]
        self.short_name = row[6]
        self.has_process = False
        if self.area < 4 and self.my_parent.areas[self.area] is not None:
            self.has_process = True
        self.tooltip = row[0] + "<br>Type:" + str(row[2]) + " Sensor:" + str(row[3])
        if self.mode == 0:
            self.switch(OFF)
        elif self.mode == 2 or self.mode == 3 or self.mode == 5 or self.mode == 6 or self.mode == 0:
            self.update_info()
        # if self.id > 10:
        #     return
        self.calculate_limits()
        self.update_control(self.status)

    def save_mode(self, mode):
        """ Updates and saves the outputs mode and saves it to the db and updates the outputs info control """
        self.mode = mode
        self.db.execute_write('UPDATE {} SET type = {} WHERE id = {} LIMIT 1'.format(DB_OUTPUTS, mode, self.id))
        self._check()
        self.update_info()
        # Don't send this from here as is causes a loop
        # self.my_parent.coms_interface.relay_send(NWC_OUTPUT_MODE, self.id, self.mode)

    def update_mode(self, mode):
        """ Updates the outputs mode does not save it to the db but updates the outputs info control"""
        self.mode = mode
        self._check()
        self.update_info()

    def set_range(self, on_dif, off_dif):
        """ Set new values for range (Difference between sensor set point and output switching values
            and updates the db and the control """
        self.range[0] = on_dif
        self.range[1] = off_dif
        r = "{}, {}".format(on_dif, off_dif)
        sql = 'UPDATE {} SET `range` = "{}" WHERE id = {}'.format(DB_OUTPUTS, r, self.id)
        print(sql)
        self.db.execute_write(sql)

        self.calculate_limits()
        
    def save_input_sensor(self, sensor_id):
        """ Updates the input sensor and saves it to the db and reloads all outputs for the area.
            This ensures the sensor classes handler list has any old inputs removed"""
        self.db.execute_write('UPDATE {} SET input = {} WHERE id = {} LIMIT 1'.format(DB_OUTPUTS, sensor_id, self.id))
        self.my_parent.load_outputs(self.area)

    def set_detection(self, detection):  # See defines DET_ detection types
        self.detection = detection

    def set_duration(self, duration):   # Only for timer
        """ Set timer duration
            duration can either be an int with duration as minuets ie 240 or as a string ie 'hh:mm'
        """
        if type(duration) == str:
            s = duration.split(':')
            duration = (int(s[0]) * 60) + int(s[1])

        self.duration = int(duration)

    def set_active(self, active=None):
        # If active is not provided it will just swap states
        if active is None:
            self.is_active = not self.is_active
        else:
            self.is_active = active
        if self.is_active:
            if self.detection & DET_TIMER == DET_TIMER:
                if self.duration > 0:
                    self.off_time = (datetime.now() + timedelta(minutes=self.duration))
                else:
                    self.off_time = None
                self.update_control(active)
            else:
                self.is_active = True
                self.update_control(OFF)
        else:
            self.switch(OFF)

    def set_limits(self, on_temp, off_temp):
        """ Set the on and off temperatures for the output and updates all
            Call with 0, 0 to have the output use its sensors values"""
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
                self.switch(self.my_parent.process_from_location(1).get_light_status())
                return
            if self.area == 2 and self.has_process:
                self.switch(self.my_parent.process_from_location(2).get_light_status())
                return
        if self.mode == 6:  # Night
            if self.area == 1 and self.has_process:
                self.switch(1 - self.my_parent.process_from_location(1).get_light_status())
                return
            if self.area == 2 and self.has_process:
                self.switch(1 - self.my_parent.process_from_location(2).get_light_status())
                return

    def check(self, value):
        try:
            self._check()
            # if (0 < self.area < 4) and not self.has_process:
            #     self.switch(OFF)
            #     return  # Areas 1 to 3 but but NO process running

            if self.mode == 2 or self.mode == 4:  # Sensor or both
                if self.detection & DET_RISE == DET_RISE:   # and self.off_time is not None:
                    if value >= self.temp_off_adjusted:
                        self.switch(OFF)
                    elif value <= self.temp_on_adjusted:
                        self.switch(ON)
                elif self.detection & DET_FALL == DET_FALL:
                    if value <= self.temp_on_adjusted:
                        self.switch(ON)
                    elif value >= self.temp_off_adjusted:
                        self.switch(OFF)
            if self.detection & DET_TIMER == DET_TIMER and self.off_time is not None:
                # self.remaining = (self.off_time - datetime.now()).seconds
                if self.remaining <= 0 or self.off_time <= datetime.now():
                    self.switch(OFF)
                self.update_control(self.status)
        except Exception as e:
            print("Output ERROR ", e.args)
        return

    def switch_by_button(self):
        if self.mode == 1:
            self.switch(OFF, True)
            self.save_mode(0)
            # self.my_parent.coms_interface.send_switch(self.output_pin, 0)
            self.my_parent.coms_interface.relay_send(NWC_OUTPUT_MODE, self.id, self.mode)
            # self.my_parent.coms_interface.relay_send(NWC_OUTPUT, self.id, OFF)
        elif self.mode == 0:
            self.switch(ON, True)
            self.save_mode(1)
            # self.my_parent.coms_interface.send_switch(self.output_pin, 1)
            self.my_parent.coms_interface.relay_send(NWC_OUTPUT_MODE, self.id, self.mode)
            # self.my_parent.coms_interface.relay_send(NWC_OUTPUT, self.id, ON)
        else:
            self.switch(None, True)
            # self.my_parent.coms_interface.relay_send(NWC_OUTPUT, self.id, int(not self.status))

    def switch(self, state=None, override_master=False):
        """
        Both the master and slave will call this with override_master False, (auto mode, software controlled)
        but only master will send command unless the the override_master is True (Manual operation)
        @param state: On or Off
        @type state: int
        @param override_master: When True slave switch Will send the commands
        @type override_master: bool
        """
        if state is None:
            state = int(not self.status)
        if state != self.out_status_last:
            if self.my_parent.mode == MASTER or override_master:    # This filters out any auto switches from slave
                self.my_parent.coms_interface.send_switch(self.output_pin, state)
                self.my_parent.coms_interface.relay_send(NWC_OUTPUT, self.id, state)
            # @Todo Add to event log
            if state == OFF:
                if self.type < 5:   # Not water heater
                    self.off_time = None
                if self.detection & DET_TIMER == DET_TIMER:
                    self.is_active = False
                    self.timer.stop()
                    self.my_parent.lbl_workshop_timer.setText("")
                if self.out_status_last is not None:
                    play_sound(SND_OFF)
            else:   # Water heater
                if self.out_status_last is not None:
                    play_sound(SND_ON)
                if self.detection & DET_TIMER == DET_TIMER and self.type != 5:
                    if self.duration > 0:
                        self.off_time = (datetime.now() + timedelta(minutes=self.duration))
                        self.remaining = self.duration
                        self.timer.start()
                    else:
                        self.off_time = None
                        self.remaining = 0
            self.update_control(state)
            self.out_status_last = state
            self.status = state
        return

    def soft_switch(self, state):
        """ This is only used by the relay command, it only updates it's output state and display, it does
            not do any switching"""
        self.update_control(state)
        self.out_status_last = state
        self.status = state
        if state == ON:
            if self.out_status_last is not None:
                play_sound(SND_ON)
            if self.detection & DET_TIMER == DET_TIMER and self.type != 5:
                if self.duration > 0:
                    self.off_time = (datetime.now() + timedelta(minutes=self.duration))
                    self.remaining = self.duration
                    self.timer.start()
        else:
            if self.detection & DET_TIMER == DET_TIMER:
                self.is_active = False
                self.timer.stop()
                self.my_parent.lbl_workshop_timer.setText("")
            if self.out_status_last is not None:
                play_sound(SND_OFF)

    def timer_event(self):
        self.remaining = int(self.remaining - 1)
        if self.remaining < 1:
            self.timer.stop()
            self.switch()
            self.my_parent.lbl_workshop_timer.setText("")
            return
        m, s = divmod(self.remaining, 60)
        h, m = divmod(m, 60)
        if self.remaining >= 3600:
            s = '{:d}:{:02d}'.format(h, m)
        else:
            s = '{:02d}:{:02d}'.format(m, s)
        self.my_parent.lbl_workshop_timer.setText(s)

    def update_control(self, state):
        self.output_update.emit(self.id, self.status, self.tooltip)
        ctrl = getattr(self.my_parent, "pb_output_status_%i" % self.id)

        if state == ON:
            ctrl.setIcon(QIcon(":/normal/output_on.png"))
        else:
            ctrl.setIcon(QIcon(":/normal/output_off.png"))

    def update_info(self):
        getattr(self.my_parent, "lbl_output_number_%i" % self.id).setText(self.short_name[1:])
        ctrl = getattr(self.my_parent, "lbl_output_%i" % self.id)
        if self.short_name[:1] == "H":
            ctrl.setPixmap(QPixmap(":/normal/output_heater.png"))
        if self.short_name[:1] == "A":
            ctrl.setPixmap(QPixmap(":/normal/output_aux.png"))
        if self.short_name[:1] == "S":
            ctrl.setPixmap(QPixmap(":/normal/output_socket.png"))

        if self.has_process or self.area > 3 or self.my_parent.area_manual[self.area] == 1:
            getattr(self.my_parent, "frm_output_%i" % self.id).setEnabled(True)
            ctrl = getattr(self.my_parent, "pb_output_mode_%i" % self.id)
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

            ctrl = getattr(self.my_parent, "lbl_output_sensor_%i" % self.id)
            if self.mode == 1:
                ctrl.setPixmap(QtGui.QPixmap())
            else:
                if self.input < 0:
                    ctrl.setPixmap(QtGui.QPixmap(":/normal/none.png"))
                else:
                    if self.my_parent.sensors[self.input].short_name.find("Hum") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/065-humidity.png"))
                    elif self.my_parent.sensors[self.input].short_name.find("Roo") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/061-care.png"))
                    elif self.my_parent.sensors[self.input].short_name.find("Pro") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/067-leaf.png"))
                    elif self.my_parent.sensors[self.input].short_name.find("Cor") == 0:
                        ctrl.setPixmap(QtGui.QPixmap(":/normal/062-plant.png"))

            if self.mode == 2 or self.mode == 4:
                getattr(self.my_parent, "lbl_output_set_off_%i" % self.id).setText(str(self.temp_off_adjusted))
                getattr(self.my_parent, "lbl_output_set_on_%i" % self.id).setText(str(self.temp_on_adjusted))
                if self.temp_on != self.temp_on_adjusted:
                    getattr(self.my_parent, "lbl_output_set_on_%i" % self.id).setFont(self.font_i)
                else:
                    getattr(self.my_parent, "lbl_output_set_on_%i" % self.id).setFont(self.font_n)
                if self.temp_off != self.temp_off_adjusted:
                    getattr(self.my_parent, "lbl_output_set_off_%i" % self.id).setFont(self.font_i)
                else:
                    getattr(self.my_parent, "lbl_output_set_off_%i" % self.id).setFont(self.font_n)
            else:
                getattr(self.my_parent, "lbl_output_set_off_%i" % self.id).clear()
                getattr(self.my_parent, "lbl_output_set_on_%i" % self.id).clear()
                # t += "<br>F: {}<br>N: {}".format(self.temp_off_adjusted, self.temp_on_adjusted)
            # self.info_ctrl.setText(t)
        else:
            getattr(self.my_parent, "frm_output_%i" % self.id).setEnabled(False)
            pass
