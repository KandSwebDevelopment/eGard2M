import collections

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from class_fan import FanClass
from defines import *


class FansController(QObject):
    update_fans_mode = pyqtSignal(int, int, int, name='updateFansMode')     # mode 1, mode 2, master power
    update_fans_speed = pyqtSignal(int, int, name="updateFansSpeed")     # speed 1, speed 2

    def __init__(self, parent):
        """

        """
        super(FansController, self).__init__()
        self.area_controller = parent
        self.main_panel = parent.main_panel
        self.coms_interface = self.area_controller.main_window.coms_interface
        self.db = self.main_panel.db
        self.master_mode = self.main_panel.master_mode
        self.fans = collections.defaultdict(FanClass)
        self._logging_t = int(self.db.get_config(CFT_FANS, "log tuning", 1))    # if True will log sensor temperature and fan speed on each switch

        self.master_power = UNSET
        self.fans[1] = FanClass(self, 1)
        self.fans[2] = FanClass(self, 2)
        current = self.db.execute_single('SELECT sensor FROM {} WHERE id = {}'.format(DB_FANS, 1))
        self.set_fan_sensor(1, current)
        current = self.db.execute_single('SELECT sensor FROM {} WHERE id = {}'.format(DB_FANS, 2))
        self.set_fan_sensor(2, current)

        # if self.area_controller.master_mode == MASTER:
        self.set_master_power(int(self.db.get_config(CFT_FANS, "master", 1)))
        self.update_fans_mode.emit(self.get_mode(1), self.get_mode(2), self.master_power)
        self.area_controller.main_window.coms_interface.update_fan_speed.connect(self.speed_update)
        self.area_controller.main_window.coms_interface.update_switch.connect(self.switch_update)

    def speed_update(self, fan, speed):
        """ A new fan speed has been received from the IO
            Just update the display and relay the speed"""
        speed += 1
        if fan == 1:
            if self.fans[1].spin_up and speed == 6:     # Just switched to speed 6 for start up
                self.area_controller.main_window.coms_interface.send_switch(SW_FAN_1_OFF, ON)
            else:
                self.main_panel.lefanspeed_1.setText(str(speed))
        elif fan == 2:
            if self.fans[2].spin_up and speed == 6:     # Just switched to speed 6 for start up
                self.area_controller.main_window.coms_interface.send_switch(SW_FAN_2_OFF, ON)
            else:
                self.main_panel.lefanspeed_2.setText(str(speed))
        self.fans[fan].update_speed(speed)
        if self.area_controller.master_mode == MASTER:
            self.coms_interface.relay_send(NWC_FAN_SPEED, fan, speed)

    def get_mode(self, area):
        return self.fans[area].mode

    def get_speed(self, area):
        return self.fans[area].speed

    def set_mode(self, area, mode):
        self.fans[area].mode = mode
        self.update_fans_mode.emit(self.get_mode(1), self.get_mode(2), self.master_power)

    def get_fan_sensor(self, area):
        return self.fans[area].sensor

    def get_log_values(self):
        return str(self.fans[1].input) + ", " + str(self.fans[1].speed) + ", " + str(self.fans[1].get_set_point()) + ", " +\
               str(self.fans[2].input) + ", " + str(self.fans[2].speed) + ", " + str(self.fans[2].get_set_point())

    def set_fan_sensor(self, area, sensor_id, is_relay=False):
        current = self.fans[area].sensor
        # Remove old setting
        if sensor_id != current:
            self.area_controller.sensors[current].is_fan = False
            self.area_controller.sensors[current].update_status_ctrl()
        # Apply new setting
        self.area_controller.sensors[sensor_id].is_fan = True
        self.area_controller.sensors[sensor_id].update_status_ctrl()
        if not is_relay:
            # Don't do if acting on a relay command as this was done by sender
            sql = 'UPDATE {} SET sensor = {} WHERE id = {}'.format(DB_FANS, sensor_id, area)
            self.db.execute_write(sql)
        self.fans[area].sensor = sensor_id

    def set_master_power(self, state):
        if state != self.master_power:
            # if self.area_controller.master_mode == MASTER:
            self.area_controller.main_window.coms_interface.send_switch(SW_FANS_POWER, state)
            self.master_power = state

    def set_speed(self, area, speed):
        """ Set the speed manually """
        self.fans[area].speed = speed

    def set_req_temperature(self, area, value):
        """ For manual changes to set temperature"""
        self.fans[area].set_point(value)
        self.area_controller.main_window.coms_interface.relay_send(NWC_FAN_REQUIRED, value)

    def load_req_temperature(self, area):
        s = self.fans[area].sensor
        if s > 0:
            # if in cool down transition don't change the set point if fan trans lock is on and trigger trans timer in
            # fan class. As this is only called once the set set value will have to be held by fan class
            if self.area_controller.cool_warm[area] == COOL:
                self.fans[area].trans_start(self.area_controller.sensors[s].get_set())
                return
            self.fans[area].set_point(self.area_controller.sensors[s].get_set())

    def start_fan(self, area):
        if self.area_controller.area_has_process(area):
            self.fans[area].start_auto()
        else:
            # if in manual mode
            # self.fans[area].start_manual()
            pass

    def start_manual(self, area):
        self.fans[area].start_manual()

    def stop_fan(self, area):
        self.fans[area].stop_fan()

    def update_temperature(self, area, value):
        self.fans[area].update_input_value(value)
        if self._logging_t and self.master_mode == MASTER:
            self.area_controller.main_window.logger.save_fan_tune_log(self.get_log_values())

    @pyqtSlot(int, int, int, name="updateSwitch")
    def switch_update(self, sw, state, module):
        if module != MODULE_IO:
            return
        if sw == SW_FANS_POWER:
            if self.master_power != state:
                self.db.set_config_both(CFT_FANS, "master", state)
            self.master_power = state
            if state == OFF:
                self.fans[1].stop_fan()
                self.fans[2].stop_fan()
            else:
                if self.area_controller.master_mode == MASTER:
                    self.start_fan(1)
                    self.start_fan(2)
                else:
                    self.area_controller.main_window.coms_interface.relay_send(NWC_FAN_UPDATE, 100, 100)
            self.update_fans_mode.emit(self.get_mode(1), self.get_mode(2), self.master_power)

    def refresh_info(self, fan):
        self.fans[fan].update_info()
