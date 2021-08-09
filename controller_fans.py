import collections

from PyQt5.QtCore import QObject, pyqtSignal

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

        self.master_power = int(self.db.get_config(CFT_FANS, "master", 1))
        self.fans[1] = FanClass(self, 1)
        self.fans[2] = FanClass(self, 2)
        current = self.db.execute_single('SELECT sensor FROM {} WHERE id = {}'.format(DB_FANS, 1))
        self.set_fan_sensor(1, current)
        current = self.db.execute_single('SELECT sensor FROM {} WHERE id = {}'.format(DB_FANS, 2))
        self.set_fan_sensor(2, current)

        if self.area_controller.master_mode == MASTER:
            self.set_master_power(self.master_power)
        self.update_fans_mode.emit(self.get_speed(1), self.get_speed(2), self.master_power)
        self.area_controller.main_window.coms_interface.update_fan_speed.connect(self.speed_update)

    def speed_update(self, fan1, fan2):
        """ Used by slave to keep display updated """
        self.fans[1].update_speed(fan1)
        self.fans[2].update_speed(fan2)
        self.update_fans_speed.emit(fan1, fan2)

    def get_mode(self, area):
        return self.fans[area].mode

    def get_speed(self, area):
        return self.fans[area].speed

    def set_mode(self, area, mode):
        self.fans[area].mode = mode
        self.update_fans_mode.emit(self.get_speed(1), self.get_speed(2), self.master_power)

    def set_fan_sensor(self, area, sensor_id):
        current = self.fans[area].sensor
        # Remove old setting
        if sensor_id != current:
            self.area_controller.sensors[current].is_fan = False
            self.area_controller.sensors[current].update_status_ctrl()
        # Apply new setting
        self.area_controller.sensors[sensor_id].is_fan = True
        self.area_controller.sensors[sensor_id].update_status_ctrl()
        sql = 'UPDATE {} SET sensor = {} WHERE id = {}'.format(DB_FANS, sensor_id, area)
        self.db.execute_write(sql)

    def set_master_power(self, state):
        # if state == self.master_power:
        self.master_power = state
        self.area_controller.main_window.coms_interface.send_switch(37, state)
        self.db.set_config(CFT_FANS, "master", state)
        if state == OFF:
            self.fans[1].stop()
            self.fans[2].stop()
        else:
            self.start_fan(1)
            self.start_fan(2)
        # self.area_controller.main_panel.update_fan_mode()

    def set_speed(self, area, speed):
        self.fans[area].speed = speed

    def start_fan(self, area):
        if self.area_controller.area_has_process(area):
            self.fans[area].start_auto()
        else:
            # In manual mode
            pass

    def start_manual(self, area):
        self.fans[area].start_manual()

    def stop_fan(self, area):
        self.fans[area].stop()

    def update_temperature(self, area, value):
        self.fans[area].update_input_value(value)
