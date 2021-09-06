import collections

from PyQt5.QtCore import QObject, pyqtSignal

from defines import CFT_SOIL_SENSORS


class SoilSensorClass(QObject):
    update_soil_reading = pyqtSignal(int, collections.defaultdict, name="updateSoil")  # Area, List will contain avg as item 5

    def __init__(self, parent):
        """

        @type parent: pClass
        """
        super(SoilSensorClass, self).__init__()
        self.area_controller = parent
        self.db = parent.db

        self.soil_sensors_status = collections.defaultdict()  # Hold soil sensor status, ie the plant number it is in or 0 if off
        self.soil_dry = 0
        self.soil_wet = 0
        self.area_active = [0, 0, 0]

        self.load_status()

        self.area_controller.main_window.coms_interface.update_soil_reading.connect(self.calculate_soil)

    def load_status(self):
        self.soil_dry = int(self.db.get_config("soil limits", "dry", 600))
        self.soil_wet = int(self.db.get_config("soil limits", "wet", 300))
        # self.area_active[1] = int(self.db.get_config(CFT_SOIL_SENSORS, "area 1", 0) == "True")
        # self.area_active[2] = int(self.db.get_config(CFT_SOIL_SENSORS, "area 2", 0) == "True")
        for x in range(1, 9):
            self.soil_sensors_status[x] = int(self.db.get_config(CFT_SOIL_SENSORS, x, 0))

    def get_sensor_status(self, area):
        """ Returns a list of the sensor statuses for the area"""
        r = []
        for b in range(1, 5):
            idx = b + ((area - 1) * 4)
            r.append(self.soil_sensors_status[idx])
        return r

    def convert_reading(self, reading):
        r = 100 - (((reading - self.soil_wet) / (
                self.soil_dry - self.soil_wet)) * 100)
        r = round(r, 1)
        r = 0 if r < 0 else r
        r = 100 if r > 100 else r
        return r

    def update_active(self, area):
        if self.area_active[area]:
            getattr(self.area_controller.main_window.main_panel, "le_avg_soil_%i" % area).setEnabled(True)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_1" % area).setEnabled(True)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_2" % area).setEnabled(True)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_3" % area).setEnabled(True)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_4" % area).setEnabled(True)
        else:
            getattr(self.area_controller.main_window.main_panel, "le_avg_soil_%i" % area).setEnabled(False)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_1" % area).setEnabled(False)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_2" % area).setEnabled(False)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_3" % area).setEnabled(False)
            getattr(self.area_controller.main_window.main_panel, "le_soil_%i_4" % area).setEnabled(False)

    def update_display(self, area, lst):
        try:
            # getattr(self.area_controller.main_window.main_panel, "le_avg_soil_%i" % area).setText(str(lst[5]))
            for c in range(1, 5):
                if int(lst[c]) > 1020:
                    getattr(self.area_controller.main_window.main_panel, "le_soil_{}_{}".
                            format(area, c)).setText("--")
                else:
                    getattr(self.area_controller.main_window.main_panel, "le_soil_{}_{}".
                            format(area, c)).setText(str(lst[c]))
                    getattr(self.area_controller.main_window.main_panel, "le_soil_{}_{}".
                            format(area, c)).setToolTip(str(self.soil_sensors_status[c + ((area - 1) * 4)]))
        except Exception as e:
            print("Update soil display - ", e.args)

    def calculate_soil(self, data):
        if len(data) < 8:
            print("ERROR soil data to short")
            return
        if len(self.soil_sensors_status) < 8:
            return      # For slave in case is receives an update before fully init
        total = 0
        avg = 0
        cnt = 0
        result = collections.defaultdict(int)
        for x in range(0, 4):
            if self.soil_sensors_status[x + 1] > 0:
                if int(data[x]) < 1000:
                    # total += int(data[x])
                    result[x + 1] = self.convert_reading(int(data[x]))
                    cnt += 1
        # if total > 0:
        #     avg = total / cnt
        # result[5] = self.convert_reading(avg)
        # self.update_soil_reading.emit(1, result)  # Signal new data
        self.update_display(1, result)
        # print(str(avg) + "%")
        # Area 2
        total = 0
        avg = 0
        cnt = 0
        result.clear()
        for x in range(0, 4):
            try:
                if self.soil_sensors_status[x + 5] > 0:
                    # total += int(data[x + 4])
                    result[x + 1] = self.convert_reading(int(data[x + 4]))
                    cnt += 1
            except Exception as e:
                print("Update display error COM_SOIL_READ 2 - ", e.args)
                pass
        # if total > 0:
        #     avg = total / cnt
        # result[5] = self.convert_reading(avg)
        # self.update_soil_reading.emit(2, result)  # Signal new data
        self.update_display(2, result)
