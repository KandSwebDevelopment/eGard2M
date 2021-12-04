import collections

from PyQt5.QtCore import QObject, pyqtSignal

from defines import *


class SoilSensorClass(QObject):
    update_soil_reading = pyqtSignal(int, collections.defaultdict, name="updateSoil")  # Area, List will contain avg as item 5

    def __init__(self, parent):
        """

        @type parent: pClass
        """
        super(SoilSensorClass, self).__init__()
        self.area_controller = parent
        self.db = parent.db

        self.raw_reading = collections.defaultdict(int)         # Raw reading from IO
        self.final_reading = collections.defaultdict(int)       # Raw converted to %
        self.dry_reading = collections.defaultdict(int)
        self.wet_reading = collections.defaultdict(int)
        self.item = collections.defaultdict(int)
        self.soil_sensors_status = collections.defaultdict(int)  # Hold soil sensor status, ie the plant number it is on or 0 if off
        self.soil_dry = 0
        self.soil_wet = 0
        self.area_active = [0, 0, 0]

        self.load_status()

        self.area_controller.main_window.coms_interface.update_soil_reading.connect(self.new_readings)

    def new_readings(self, data):
        s = 1
        for r in data:
            r = int(r)
            self.raw_reading[s] = r
            s += 1
        self.refresh()

    def refresh(self):
        s = 1
        for r in self.raw_reading:
            self.final_reading[s] = self.convert_reading(s)
            s += 1
        self.update_display()

    def load_status(self):
        rows = self.db.execute('SELECT id, item, dry, wet FROM {}'.format(DB_SOIL_SENSORS))
        for row in rows:
            self.dry_reading[row[0]] = row[2]
            self.wet_reading[row[0]] = row[3]
            self.item[row[0]] = row[1]

    def get_item(self, area, sensor):
        """ Returns the plant number sensor is in """
        if area == 2:
            sensor += 4
        return self.item[sensor]

    def update_item(self, area, sensor, item):
        """ Returns the plant number sensor is in """
        if area == 2:
            sensor += 4
        self.item[sensor] = item
        self.update_display()

    def set_item(self, area, sensor, item):
        self.update_item(area, sensor, item)
        if area == 2:
            sensor += 4
        self.db.execute_write("UPDATE {} SET item = {} WHERE id = {}".format(DB_SOIL_SENSORS, item, sensor))

    def get_wet_dry(self, area, sensor):
        if area == 2:
            sensor += 4
        return self.wet_reading[sensor], self.dry_reading[sensor]

    def get_raw(self, area, sensor):
        if area == 2:
            sensor += 4
        return self.raw_reading[sensor]

    def get_log_values(self):
        r = ""
        for o in self.final_reading:
            r += str(self.final_reading[o]) + ", "
        return r[0: len(r) - 2]

    def update_wet_dry(self, area, sensor, wet, dry):
        if area == 2:
            sensor += 4
        self.wet_reading[sensor] = wet
        self.dry_reading[sensor] = dry
        self.final_reading[sensor] = self.convert_reading(sensor)
        self.update_display()

    def set_wet_dry(self, area, sensor, wet, dry):
        self.update_wet_dry(area, sensor, wet, dry)
        if area == 2:
            sensor += 4
        self.db.execute_write("UPDATE {} SET wet = {}, dry = {} WHERE id = {}".
                              format(DB_SOIL_SENSORS, wet, dry, sensor))

    def convert_reading(self, sensor):
        r = 100 - (((self.raw_reading[sensor] - self.wet_reading[sensor]) /
                (self.dry_reading[sensor] - self.wet_reading[sensor])) * 100)
        r = round(r, 1)
        r = 0 if r < 0 else r
        r = 100 if r > 100 else r
        return r

    # def update_active(self, area):
    #     if self.area_active[area]:
    #         getattr(self.area_controller.main_window.main_panel, "le_avg_soil_%i" % area).setEnabled(True)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_1" % area).setEnabled(True)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_2" % area).setEnabled(True)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_3" % area).setEnabled(True)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_4" % area).setEnabled(True)
    #     else:
    #         getattr(self.area_controller.main_window.main_panel, "le_avg_soil_%i" % area).setEnabled(False)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_1" % area).setEnabled(False)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_2" % area).setEnabled(False)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_3" % area).setEnabled(False)
    #         getattr(self.area_controller.main_window.main_panel, "le_soil_%i_4" % area).setEnabled(False)
    #
    def update_display(self):
        try:
            for area in range(1, 3):
                for c in range(1, 5):
                    s = c + 4 if area == 2 else c
                    if self.raw_reading[s] > 1020 or self.item[s] == 0:
                        getattr(self.area_controller.main_window.main_panel, "le_soil_{}_{}".
                                format(area, c)).setText("--")
                        getattr(self.area_controller.main_window.main_panel, "le_soil_{}_{}".
                                format(area, c)).setToolTip("")
                    else:
                        getattr(self.area_controller.main_window.main_panel, "le_soil_{}_{}".
                                format(area, c)).setText(str(self.final_reading[s]))
                        getattr(self.area_controller.main_window.main_panel, "le_soil_{}_{}".
                                format(area, c)).setToolTip(str(self.item[s]))
        except Exception as e:
            print("Update soil display - ", e.args)

    # def calculate_soil(self, data):
    #     if len(data) < 8:
    #         print("ERROR soil data to short")
    #         return
    #     if len(self.soil_sensors_status) < 8:
    #         return      # For slave in case is receives an update before fully init
    #     total = 0
    #     avg = 0
    #     cnt = 0
    #     result = collections.defaultdict(int)
    #     for x in range(0, 4):
    #         if self.soil_sensors_status[x + 1] > 0:
    #             if int(data[x]) < 1000:
    #                 # total += int(data[x])
    #                 result[x + 1] = self.convert_reading(int(data[x]))
    #                 cnt += 1
    #     # if total > 0:
    #     #     avg = total / cnt
    #     # result[5] = self.convert_reading(avg)
    #     # self.update_soil_reading.emit(1, result)  # Signal new data
    #     self.update_display(1, result)
    #     # print(str(avg) + "%")
    #     # Area 2
    #     total = 0
    #     avg = 0
    #     cnt = 0
    #     result.clear()
    #     for x in range(0, 4):
    #         try:
    #             if self.soil_sensors_status[x + 5] > 0:
    #                 # total += int(data[x + 4])
    #                 result[x + 1] = self.convert_reading(int(data[x + 4]))
    #                 cnt += 1
    #         except Exception as e:
    #             print("Update display error COM_SOIL_READ 2 - ", e.args)
    #             pass
    #     # if total > 0:
    #     #     avg = total / cnt
    #     # result[5] = self.convert_reading(avg)
    #     # self.update_soil_reading.emit(2, result)  # Signal new data
    #     self.update_display(2, result)
