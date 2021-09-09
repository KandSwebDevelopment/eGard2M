import collections

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QPixmap

from class_fan import FanClass
from class_outputs import OutputClass
from class_sensor import SensorClass
from class_soil_sensors import SoilSensorClass
from controller_fans import FansController
from controller_outputs import OutputController
from defines import *
from class_process import ProcessClass


class AreaController(QObject):
    def __init__(self, parent):
        """

        :type parent: _main
        """
        super(AreaController, self).__init__()
        self.main_window = parent
        self.db = self.main_window.db
        self.main_panel = parent.main_panel
        self.master_mode = self.main_panel.master_mode
        self.areas_pid = collections.defaultdict(int)                         # The PID in the area
        self.areas_items = collections.defaultdict(list)     # The items in the area
        self.areas_processes = collections.defaultdict(ProcessClass)
        self.sensors = collections.defaultdict(SensorClass)

        self.area_manual = collections.defaultdict(int)      # Area is in manual mode
        self.output_controller = OutputController(self)
        self.soil_sensors = SoilSensorClass(self)
        self.light_relay_1 = UNSET      # Hold the actual position of the relay, this is only changed by switch updates
        self.light_relay_2 = UNSET
        self.cool_warm = collections.defaultdict(int)        # Area is is cool = 1, warm = 2, normal = 0
        self.cool_warm[1] = NORMAL
        self.cool_warm[2] = NORMAL

        self.main_panel.timer.start()

        self.load_areas()
        self.fan_controller = FansController(self)

    def load_areas(self):
        """ Load the PID's and items for all the areas"""
        for area in range(1, 4):  # Areas 1 to 3, the only ones that can have a process
            sql = "SELECT process_id, item FROM {} WHERE area = {}".format(DB_AREAS, area)
            rows = self.db.execute(sql)
            if len(rows) > 0:
                # Has process
                self.areas_pid[area] = rows[0][0]
                items = []
                for row in rows:
                    items.append(row[1])
                self.areas_items[area] = items
                getattr(self.main_panel, "frmstagechange_%i" % area).setEnabled(True)
            else:
                # No process
                getattr(self.main_panel, "frmstagechange_%i" % area).setEnabled(False)
                if area < 3:
                    getattr(self.main_panel, "pbadjust_%i" % area).setEnabled(False)

                self.areas_pid[area] = 0
                self.areas_items[area] = []
                # Check if in manual mode
                if self.area_is_manual(area) > 0:
                    getattr(self.main_panel, "le_stage_{}".
                            format(area)).setPixmap(QPixmap(":/normal/manual_feed.png"))
                    if area > 2:
                        continue
                    # Check to see if light should be on or off
                    if self.area_is_manual(area) == 2:
                        self.main_window.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 1, MODULE_IO)
                    else:
                        self.main_window.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 0, MODULE_IO)

                else:
                    # Not in manual and no process
                    getattr(self.main_panel, "le_stage_{}".
                            format(area)).setPixmap(QtGui.QPixmap(":/normal/none.png"))
                    if area < 3:
                        # Light should be off
                        self.main_window.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 0, MODULE_IO)

        self.load_processes()

        self.load_sensors(1)
        self.load_sensors(2)
        self.load_sensors(3)
        self.load_sensors(4)    # Workshop
        self.load_sensors(5)    # Outside

        self.output_controller.load_all_areas()

    def reload_area(self, area):
        """ Load the PID's and items for the area"""
        sql = "SELECT process_id, item FROM {} WHERE area = {}".format(DB_AREAS, area)
        rows = self.db.execute(sql)
        if len(rows) > 0:
            # Has process
            self.areas_pid[area] = rows[0][0]
            items = []
            for row in rows:
                items.append(row[1])
            self.areas_items[area] = items
        else:
            # No process
            self.areas_pid[area] = 0
            self.areas_items[area] = []
            # Check if in manual mode
            if self.area_is_manual(area) > 0:
                getattr(self.main_panel, "le_stage_{}".
                        format(area)).setPixmap(QPixmap(":/normal/manual_feed.png"))
                if area > 2:
                    pass
                # Check to see if light should be on or off
                if self.area_is_manual(area) == 2:
                    self.main_window.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 1, MODULE_IO)
                else:
                    self.main_window.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 0, MODULE_IO)
            else:
                # Not in manual and no process
                getattr(self.main_panel, "le_stage_{}".
                        format(area)).setPixmap(QtGui.QPixmap(":/normal/none.png"))
                if area < 3:
                    # Light should be off
                    self.main_window.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 0, MODULE_IO)

        self.reload_process(area)

        self.load_sensors(area)

        self.output_controller.load_outputs(area)

    def load_processes(self):
        self.areas_processes.clear()
        for area in self.areas_pid:
            if area > 3:
                return
            self.reload_process(area)

    def reload_process(self, area):
        if self.areas_pid[area] > 0:
            self.areas_processes[area] = ProcessClass(self.areas_pid[area], self.main_window)
            # Put process id in process id button
            ctrl = getattr(self.main_panel, "pb_pid_{}".format(area))
            ctrl.setText(str(self.areas_processes[area].id))
            ctrl.setToolTip("Process ID\r\nClick for information")
            ctrl.setEnabled(True)
            self.display_stage_icon(area)
        else:
            getattr(self.main_panel, "pb_pid_{}".format(area)).setEnabled(False)

    def display_stage_icon(self, area):
        # Display stage icon
        ctrl = getattr(self.main_panel, "le_stage_%i" % area)
        stage = self.areas_processes[area].current_stage
        if stage == 1:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/gremination.png"))
        if stage == 2:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/veg.png"))
        if stage == 3:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/flowering.png"))

    def load_sensors(self, area):
        sql = 'SELECT * FROM {} WHERE area = {}'.format(DB_SENSORS_CONFIG, area)
        rows = self.db.execute(sql)
        for row in rows:
            sid = row[0]
            if sid not in self.sensors.keys():
                self.sensors[sid] = SensorClass(self, sid)
            else:
                self.sensors[sid].load_profile()
            self.sensors[sid].load_range()

    def reload_sensor_ranges(self, area):
        """ This is called when the light switches state, this will load in new temperature ranges for the sensors in
            the area"""
        if area == 1:
            self.sensors[3].load_range()
            self.sensors[4].load_range()
            self.sensors[10].load_range()
            self.sensors[11].load_range()
        if area == 2:
            self.sensors[5].load_range()
            self.sensors[6].load_range()
            self.sensors[12].load_range()
            self.sensors[13].load_range()

    def load_sensor_ranges(self, area, sid):
        if self.area_has_process(area):
            p = self.areas_processes[area]
            r = p.temperature_ranges_active
            if r is not None:
                r = r[self.sensors[sid].item]
                self.sensors[sid].set_range(r)
                ro = p.temperature_ranges_active_org[self.sensors[sid].item]
                self.sensors[sid].set_range_org(ro)
            else:
                # @todo Add call to msg sys - No temperature range for process
                pass
        else:
            self.sensor_load_manual_ranges(area, sid)

    def sensor_load_manual_ranges(self, area, item):
        """ Load the set manual ranges for an area"""
        sid = self.get_sid_from_item(area, item)
        rows = self.db.execute('SELECT setting, value FROM {} WHERE area = {} AND day = -1 AND item = {}'.
                               format(DB_PROCESS_TEMPERATURE, area, item))
        if len(rows) > 0:
            self.sensors[sid].set_range({'low': rows[0][1], 'set': rows[1][1], 'high': rows[2][1]})
            self.sensors[sid].update_status_ctrl()
        else:
            print("sensor_load_manual_ranges - Nothing found in db {} for area {} and item {}".
                  format(DB_PROCESS_TEMPERATURE, area, item))

    def get_area_pid(self, area):
        """ Returns the PID in the area"""
        return self.areas_pid[area]

    def area_has_process(self, area):
        """ Returns True if there is a process in the area """
        if self.areas_pid[area] == 0:
            return False
        return True

    def area_is_manual(self, area):
        """ Returns the manual mode of the area
            0 - Off or Auto
            1 - Manual, fan off
            2 - Manual, fan on """
        self.area_manual[area] = int(self.db.get_config(CFT_AREA, "mode {}".format(area), 0))
        return self.area_manual[area]

    def get_area_items(self, area):
        """
         Returns a list of the items in the area
        :param area:
        :type area: int
        :return:
        :rtype: list
        """
        return self.areas_items[area]

    def get_area_trans(self, area):
        return self.cool_warm[area]

    def get_area_process(self, area):
        """ Returns the process in the area
        :type area: int
        :rtype : ProcessClass
        """
        try:
            return self.areas_processes[area]
        except Exception as e:
            # print("get_area_process", e)
            return 0

    def get_light_status(self, area):
        if self.area_has_process(area):
            return self.get_area_process(area).get_light_status()
        return -1

    def get_process_active_temperature_ranges(self, area):
        if self.area_has_process(area):
            return self.get_area_process(area).temperature_ranges_active

    def sensors_set_as_fan(self, s_id, state):
        self.sensors[s_id].is_fan(state)

    def get_sid_from_item(self, area, item):
        """ This returns the sensor id from the area and the item number """
        return self.db.execute_single('SELECT id FROM {} WHERE area = {} AND area_range = {}'.
                                      format(DB_SENSORS_CONFIG, area, item))
