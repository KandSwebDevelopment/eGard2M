import time

from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
# from simple_pid import PID
from PyQt5.QtGui import QPixmap

import PID
from defines import *

""" Remember the IO unit uses speeds 0 to 5 and the class uses 1 to 6. This is adjusted at the switch command to 
    send the speed to the IO and again by the fan controller when it receives the speed back from the IO 
    The Slave also has to adjust it on receiving the relay command"""


class FanClass(QThread):
    update_fan_speed = pyqtSignal(int, int)     # Fan id, speed
    update_fan_mode = pyqtSignal(int, int)      # Fan id, mode

    def __init__(self, parent, _id):
        """ :type parent: MainWindow """
        QThread.__init__(self, parent)
        self.fan_controller = parent                         # This's parent which is Fan Controller
        self.db = self.fan_controller.db
        self.id = _id                                        # Fan 1 or 2 same as area
        self.pid = PID.PID(0, 0, 0)
        self.pid.sample_time = 1
        self.setObjectName("fan{}".format(self.id))
        self.input = 0
        self.input_calibration = 0
        self.last_input = 0
        self._speed = 0
        self.last_speed = -1
        self.last_request = UNSET   # Used by logging, same as last speed but updates instantly
        self._set_point = 0
        self._logging = True    # if True will log sensor temperature and fan speed at 2 min intervals
        self._mode = 0
        self._master_power = 0
        self.fan_spin_up = int(self.db.get_config(CFT_FANS, "spin up", 10))
        self.startup_timer = QTimer()
        self.trans_timer = QTimer()
        self.startup_timer.timeout.connect(self.spin_up_timeout)
        self.trans_timer.timeout.connect(self.trans_finish)
        self.startup_timer.setInterval(1000)
        self.load_trans_time()
        self.startup_counter = 0
        self.trans_end_temp = UNSET
        self.spin_up = False     # True when fan is in spin up mode
        row = self.db.execute_one_row("SELECT sensor, mode, Kp, Ki, Kd FROM {} WHERE id = {}".format(DB_FANS, self.id))
        self._sensor = row[0] if row[0] is not None else 0
        self.mode = row[1] if row[1] is not None else 0     # 0 = Off 1 = On, 2 = Auto
        row = self.db.execute_one_row("SELECT Kp, Ki, Kd FROM {} WHERE id = {}".format(DB_FANS, self.id))
        self.set_pid(row[0] if row[0] is not None else 0,
                     row[1] if row[1] is not None else 0,
                     row[2] if row[2] is not None else 0)
        # self._load_set_point()    # Not needed here as done later
        self._load_sensor_calibration()
        self.update_info()

    def trans_finish(self):
        self.trans_timer.stop()
        self.set_point(self.trans_end_temp)

    def trans_start(self, end_temp):
        self.trans_end_temp = end_temp
        self.trans_timer.start()

    def load_trans_time(self):
        self.trans_timer.setInterval(60000 * 60)

    def load_pid_values(self):
        row = self.db.execute_one_row("SELECT Kp, Ki, Kd FROM {} WHERE id = {}".format(DB_FANS, self.id))
        self.set_pid(row[0] if row[0] is not None else 0,
                     row[1] if row[1] is not None else 0,
                     row[2] if row[2] is not None else 0)
        self.reset()

    def _load_sensor_calibration(self):
        self.input_calibration = self.db.execute_single(
            "SELECT calibration FROM {} WHERE id = {}".format(DB_SENSORS_CONFIG, self._sensor))
        self.input_calibration = self.input_calibration if self.input_calibration is not None else 0

    def get_pid(self):
        """
        Return p, i, d
        @rtype: object
        """
        return self.pid.tunings

    @property
    def mode(self):
        """
        The fan operation mode
            0 = Off
            1 = Manual
            2 = Auto
        @return: Fan operation mode
        @rtype: int
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Set the fan operation mode and stores value in db
            0 = Off
            1 = Manual
            2 = Auto
        @param mode: Fan operation mode
        @type mode: int
        """
        if mode == self._mode:
            return
        self._mode = mode
        self.db.execute_write("UPDATE {} set mode = {} WHERE id = {}".format(DB_FANS, mode, self.id))
        self.update_info()

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, value):
        """
        Set the sensor which supplies the input and removes setting from old sensor. Stores new value in db
        @param value:
        @type value:
        """
        if self._sensor > 0:
            self.fan_controller.area_controller.sensors[self._sensor].is_fan = False
        self._sensor = value
        self.fan_controller.db.execute_write("UPDATE {} set sensor = {} WHERE id = {}".
                                             format(DB_FANS, value, self.id))
        self._load_set_point()
        self._load_sensor_calibration()
        self.pid.clear()
        self.fan_controller.area_controller.sensors[self._sensor].is_fan = True
        self.update_info()

    # def reload_sensor(self):
    #     """ reload sensor when relay command indicates a sensor change"""
    #     if self._sensor > 0:
    #         self.fan_controller.area_controller.sensors[self._sensor].is_fan = False
    #     row = self.db.execute_single("SELECT sensor FROM {} WHERE id = {}".format(DB_FANS, self.id))
    #     self._sensor = row if row is not None else 0
    #     self._load_set_point()
    #     self._load_sensor_calibration()
    #     self.pid.clear()
    #     self.fan_controller.area_controller.sensors[self._sensor].is_fan = True
    #     # self.fan_controller.update_fans_sensor()

    def update_speed(self, speed):
        """ This updates the class with the new speed received back from IO, called by fan_controller"""
        self._speed = speed
        if self.spin_up and self.last_speed <= 0:
            self.startup_counter = self.fan_spin_up
            self.startup_timer.start()
            getattr(self.fan_controller.main_panel, "lefanspeed_{}".format(self.id)).setStyleSheet("background-color: Yellow;")
        else:
            getattr(self.fan_controller.main_panel, "lefanspeed_{}".format(self.id)).setText(str(speed))

        print("Fan {} switched to speed {} at temperature {}".format(self.id, self._speed, self.input))
        self.last_speed = self._speed

    @property
    def speed(self):
        """ This sets the speed and switches fan to required speed"""
        return self._speed

    @speed.setter
    def speed(self, speed):
        self.switch(speed)

    @property
    def logging(self):
        return self._logging

    @logging.setter
    def logging(self, value):
        self._logging = value

    def set_sample_time(self, value):
        self.pid.sample_time = value

    def set_pid(self, kp, ki, kd):
        self.pid.tunings = (kp, ki, kd)

    def get_set_point(self):
        return self._set_point

    def set_point(self, value):
        self._set_point = value
        self.pid.SetPoint = value
        self.pid.clear()
        print("Fan {} set point {}".format(self.id, value))

    def set_kp(self, kp):
        self.pid.Kp = kp

    def set_ki(self, ki):
        self.pid.Ki = ki

    def set_kd(self, kd):
        self.pid.Kd = kd

    def update_input_value(self, value):
        if value < -120:
            return
        self.input = value + self.input_calibration
        # print("Fan input ", value)

    def reset(self):
        self.pid.clear()

    def stop_fan(self):
        self.mode = 0
        self.spin_up = False
        self.terminate()     # Stop thread
        # self.thread_udp_client.quit()
        # self.thread_udp_client.wait()
        self.switch(0)
        self.fan_controller.coms_interface.send_switch(SW_FAN_1_OFF - 1 + self.id, OFF)

    def fan_stopped(self):
        pass

    def start_auto(self):
        self.start_manual()
        self.mode = 2
        self.pid.clear()
        if not self.isRunning():
            self.start()

    def start_manual(self):
        if self.speed > 0:
            return
        self.switch(6)
        self.spin_up = True
        self.mode = 1
        self.fan_controller.coms_interface.send_switch(SW_FAN_1_OFF - 1 + self.id, ON)

    def run(self) -> None:
        if self.fan_controller.master_mode == SLAVE:
            return
        while self.mode == 2:
            self.pid.update(self.input)
            _speed = int(self.pid.output)
            # print("PID Raw ", _speed)
            self._switch(_speed)
            time.sleep(1)

    def _switch(self, speed_raw):
        if self._mode == 2:     # Only do switching from PID if in auto mode
            if speed_raw >= 0:
                self.switch(1)
                return
            s = speed_raw if speed_raw > - 10 else -10
            # s = s if s < 10 else 10
            # # s = int((20 - (10 - s)) / 5) + 1  # 5 Speed
            # s = int((10 - s) / 4) + 1   # 6 Speed
            s = ((10 - s) / 2) - 4
            self.switch(s)
            print(self.id, " PID ", speed_raw, " Sw ", s)
            # if self._logging_t and self.fan_controller.master_mode == MASTER:
            #     self.fan_controller.area_controller.main_window.logger.save_fan_log(
            #         "{}, {}, {}, {}".format(self.id, self.input, s, self._set_point))

    def spin_up_timeout(self):
        if self.startup_counter <= 0:
            self.spin_up = False
            self.switch(3)
            self.startup_timer.stop()
            self.fan_controller.area_controller.main_window.msg_sys.remove(MSG_FAN_START + self.id)
            getattr(self.fan_controller.main_panel, "lefanspeed_{}".format(self.id)).setStyleSheet("")
            getattr(self.fan_controller.main_panel, "lefanspeed_{}".format(self.id)).setText(str(self.speed))

            return
        self.startup_counter -= 1
        # self.update_fan_speed.emit(self.id, self.startup_counter)
        getattr(self.fan_controller.main_panel, "lefanspeed_{}".format(self.id)).setText(str(self.startup_counter))

    def switch(self, speed):
        if speed == self.last_speed:
            return
        if self.spin_up:
            return
        if speed == 0:
            self.fan_controller.coms_interface.send_switch(SW_FAN_1_OFF - 1 + self.id, OFF)
            return
        self.fan_controller.coms_interface.send_data(CMD_FAN_SPEED, True, MODULE_IO, self.id, speed - 1)

    def _load_set_point(self):
        if self._sensor == 0:
            return
        self.set_point(self.fan_controller.area_controller.sensors[self._sensor].get_set())

    def update_info(self):
        """ Displays the fan sensor and mode"""
        # Sensor for fan
        if self.sensor == 3 or self.sensor == 5:
            getattr(self.fan_controller.main_panel, "lbl_fan_sensor_{}".format(self.id)).setPixmap((QPixmap(":/normal/065-humidity.png")))
        elif self.sensor == 4 or self.sensor == 6:
            getattr(self.fan_controller.main_panel, "lbl_fan_sensor_{}".format(self.id)).setPixmap(QtGui.QPixmap(":/normal/061-care.png"))
        elif self.sensor == 10 or self.sensor == 12:
            getattr(self.fan_controller.main_panel, "lbl_fan_sensor_{}".format(self.id)).setPixmap(QtGui.QPixmap(":/normal/067-leaf.png"))
        elif self.sensor == 11 or self.sensor == 13:
            getattr(self.fan_controller.main_panel, "lbl_fan_sensor_{}".format(self.id)).setPixmap(QtGui.QPixmap(":/normal/062-plant.png"))

        # Fan mode
        ctrl = getattr(self.fan_controller.main_panel, "lbl_fan_mode_{}".format(self.id))
        if self.mode == 0:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/002-stop.png"))
        elif self.mode == 1:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/output_manual_1.png"))
        elif self.mode == 2:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/output_auto.png"))
