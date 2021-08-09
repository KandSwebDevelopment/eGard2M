import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
# from simple_pid import PID
import PID
from defines import *


class FanClass(QThread):
    update_fan_speed = pyqtSignal(int, int)     # Fan id, speed
    update_fan_mode = pyqtSignal(int, int)      # Fan id, mode

    def __init__(self, parent, _id):
        """ :type parent: MainWindow """
        QThread.__init__(self, parent)
        self.fan_controller = parent                         # This's parent which is Area Controller
        self.db = self.fan_controller.db
        self.id = _id
        self.pid = PID.PID(0, 0, 0)
        self.pid.sample_time = 1
        self.setObjectName("fan{}".format(self.id))
        self.input = 0
        self.input_calibration = 0
        self.last_input = 0
        self._speed = 0
        self.last_speed = -1
        self._set_point = 0
        self._logging = False    # if True will log sensor temperature and fan speed
        self._mode = 0
        self._master_power = 0
        self.fan_spin_up = int(self.db.get_config(CFT_FANS, "spin up"))
        self.startup_timer = QTimer()
        self.startup_timer.timeout.connect(self.spin_up_finished)
        self.startup_timer.setInterval(1000)
        self.startup_counter = 0
        self.spin_up = False     # True when fan is in spin up mode
        row = self.db.execute_one_row("SELECT sensor, mode, Kp, Ki, Kd FROM {} WHERE id = {}".format(DB_FANS, self.id))
        self._sensor = row[0] if row[0] is not None else 0
        self.mode = row[1] if row[1] is not None else 0     # 0 = Off 1 = On, 2 = Auto
        self.set_pid(row[2] if row[2] is not None else 0,
                     row[3] if row[3] is not None else 0,
                     row[4] if row[4] is not None else 0)
        self._load_set_point()
        self._load_sensor_calibration()

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
        Set the fan operation mode and stores value in db and calls for the display to update
            0 = Off
            1 = Manual
            2 = Auto
        @param mode: Fan operation mode
        @type mode: int
        """
        # self.fan_controller.main_panel.update_fan_mode(self.id, mode, self.fan_controller.master_power)
        if mode == self._mode:
            return
        self._mode = mode
        self.db.execute_write("UPDATE {} set mode = {} WHERE id = {}".format(DB_FANS, mode, self.id))

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, value):
        """
        Set the sensor which supplies the input. Stores new value in db and calls for display to update
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
        # self.fan_controller.main_panel.update_fans_sensor()

    def reload_sensor(self):
        """ reload sensor when relay command indicates a sensor change"""
        if self._sensor > 0:
            self.fan_controller.area_controller.sensors[self._sensor].is_fan = False
        row = self.db.execute_single("SELECT sensor FROM {} WHERE id = {}".format(DB_FANS, self.id))
        self._sensor = row if row is not None else 0
        self._load_set_point()
        self._load_sensor_calibration()
        self.pid.clear()
        self.fan_controller.area_controller.sensors[self._sensor].is_fan = True
        # self.fan_controller.update_fans_sensor()

    @property
    def speed(self):
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

    def get_point(self):
        return self._set_point

    def set_point(self, value):
        self._set_point = value
        self.pid.SetPoint = value

    def set_kp(self, kp):
        self.pid.Kp = kp

    def set_ki(self, ki):
        self.pid.Ki = ki

    def set_kd(self, kd):
        self.pid.Kd = kd

    def update_input_value(self, value):
        self.input = value + self.input_calibration
        # print("Fan input ", value)
        if self._logging:
            self.fan_controller.area_controller.main_window.logger.save_fan_log\
                (self.id, "{},{},{}".format(self.input, self._speed, self._set_point))

    def reset(self):
        self.pid.clear()

    def stop(self):
        self.mode = 0
        self.terminate()     # Stop thread
        # self.thread_udp_client.quit()
        # self.thread_udp_client.wait()
        self.switch(0)

    def start_auto(self):
        self.start_manual()
        self.mode = 2
        if not self.isRunning():
            self.start()

    def start_manual(self):
        if self.speed > 0:
            return
        self.fan_controller.area_controller.main_window.msg_sys.\
            add("Fan {} starting".format(self.id), MSG_FAN_START + self.id, INFO)
        self.switch(5)
        self.spin_up = True
        self.startup_timer.start()
        self.mode = 1

    def run(self) -> None:
        if self.fan_controller.master_mode == SLAVE:
            return
        while self.mode == 2:
            self.pid.update(self.input)
            _speed = int(self.pid.output)
            self._switch(_speed)
            time.sleep(1)

    def _switch(self, speed_raw):
        if self._mode == 2:     # Only do switching from PID if in auto mode
            # print(self.id, " PID ", speed_raw)
            s = speed_raw if speed_raw > - 10 else -10
            s = s if s < 10 else 10
            # s = int((20 - (10 - s)) / 5) + 1
            s = int((10 - s) / 5) + 1
            self.switch(s)

    def spin_up_finished(self):
        if self.startup_counter >= self.fan_spin_up:
            self.spin_up = False
            self.switch(2)
            self.startup_timer.stop()
            self.fan_controller.area_controller.main_window.msg_sys.remove(MSG_FAN_START + self.id)
            return
        self.startup_counter += 1
        self.update_fan_speed.emit(self.id, self.startup_counter - self.fan_spin_up)

    def switch(self, speed):
        if speed == self.last_speed:
            return
        if self.spin_up:
            return
        # self.update_fan_speed.emit(self.id, speed)
        self._speed = speed
        print("Fan {} switched to speed {} at temperature {}".format(self.id, self._speed, self.input))
        self.fan_controller.coms_interface.send_data(CMD_FAN_SPEED, True, MODULE_IO, self.id, speed)
        self.last_speed = self._speed

    def _load_set_point(self):
        if self._sensor == 0:
            return
        self.set_point(self.fan_controller.area_controller.sensors[self._sensor].get_set())
