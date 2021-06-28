import collections

from PyQt5 import QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap

from class_sensor import SensorClass
from defines import *
from class_process import ProcessClass


class AreaController(QObject):
    def __init__(self, parent):
        """

        :type parent: _main
        """
        super(AreaController, self).__init__()
        self.my_parent = parent
        self.db = self.my_parent.db
        self.main_panel = parent.main_panel
        self.sensors = collections.defaultdict(SensorClass)
        self.areas_pid = collections.defaultdict(int)                         # The PID in the area
        self.areas_items = collections.defaultdict(list)     # The items in the area
        self.areas_processes = collections.defaultdict(ProcessClass)
        self.area_manual = collections.defaultdict(int)      # Area is in manual mode

        self.load_areas()
        self.load_processes()
        self.load_sensors(1)
        self.load_sensors(2)
        self.load_sensors(3)

        self.main_panel.timer.start()

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

            else:
                # No process
                self.areas_pid[area] = 0
                self.areas_items[area] = []
                # Check if in manual mode
                if self.area_is_manual(area) > 0:
                    getattr(self.main_panel, "le_stage_{}".
                            format(area)).setPixmap(QPixmap(":/normal/manual_feed.png"))
                    if area > 2:
                        return
                    # Check to see if light should be on or off
                    if self.area_is_manual(area) == 2:
                        self.my_parent.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 1, MODULE_IO)
                    else:
                        self.my_parent.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 0, MODULE_IO)

                else:
                    # Not in manual and no process
                    getattr(self.main_panel, "le_stage_{}".
                            format(area)).setPixmap(QtGui.QPixmap(":/normal/none.png"))
                    if area < 3:
                        # Light should be off
                        self.my_parent.coms_interface.send_switch(OUT_LIGHT_1 - 1 + area, 0, MODULE_IO)

    def load_processes(self):
        for area in self.areas_pid:
            if self.areas_pid[area] > 0:
                self.areas_processes[area] = ProcessClass(self.areas_pid[area], self.my_parent)
                # Put process id in area status bar
                ctrl = getattr(self.main_panel, "lbl_sp_%i_4" % area)
                ctrl.setText(str(self.areas_processes[area].id))
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

            if self.area_has_process(area):
                # Load process range values
                if self.sensors[sid].area < 3:  # Only load process temperature ranges for areas 1 & 2
                    p = self.areas_processes[area]
                    if p != 0:
                        r = p.temperature_ranges_active
                        if r is not None:
                            r = r[self.sensors[sid].area_range]
                            self.sensors[sid].set_range(r)
                            ro = p.temperature_ranges_active_org[self.sensors[sid].area_range]
                            self.sensors[sid].set_range_org(ro)
                        else:
                            # @todo Add call to msg sys - No temperature range for process
                            pass
            else:
                if self.area_manual[area]:
                    # Load default range as area has no process and is on manual
                    # As manual only displays room temperature, skip others
                    if row[6] == 2:
                        sql = 'SELECT low, set_point, high FROM {} WHERE area = {}'\
                            .format(DB_TEMPERATURES_DEFAULT, area)
                        row = self.db.execute_one_row(sql)
                        if row is None:
                            # @todo Add call to msg sys - No default temperature range for area
                            return
                        self.sensors[sid].set_range({'low': row[0], 'set': row[1], 'high': row[2]})
                else:
                    self.sensors[sid].off()

    def load_sensor_ranges(self, area):
        if self.area_has_process(area):
            pass

    def load_manual_ranges(self, area):
        """ Load the set manual ranges for an area"""

    def get_area_pid(self, area):
        """ Returns the PID in the area"""
        return self.areas_pid[area]

    def area_has_process(self, area):
        if self.areas_pid[area] == 0:
            return False
        return True

    def area_is_manual(self, area):
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

    def get_area_process(self, area):
        """
        Returns the process in the area
        :type area: int
        :rtype : ProcessClass
        """
        try:
            return self.areas_processes[area]
        except Exception as e:
            return 0
