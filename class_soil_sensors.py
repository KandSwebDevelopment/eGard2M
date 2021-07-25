import collections

from PyQt5.QtCore import QObject, pyqtSignal

from defines import CFT_SOIL_SENSORS


class SoilSensorClass(QObject):
    update_soil_reading = pyqtSignal(list, name="updateSoil")  # List will contain area 1 and area 2

    def __init__(self, parent):
        """

        @type parent: pClass
        """
        super(SoilSensorClass, self).__init__()
        self.areas_controller = parent
        self.db = parent.db

        self.soil_sensors_status = collections.defaultdict()  # Hold soil sensor status
        self.soil_dry = int(self.db.get_config("soil limits", "dry", 600))
        self.soil_wet = int(self.db.get_config("soil limits", "wet", 300))

        self.load_status()

        self.areas_controller.main_window.coms_interface.update_soil_reading.connect(self.calculate_soil)

    def load_status(self):
        for x in range(1, 9):
            self.soil_sensors_status[x] = int(self.db.get_config(CFT_SOIL_SENSORS, x, 0) == "True")

    def calculate_soil(self, data):
        if len(data) < 8:
            print("ERROR soil data to short")
            return
        if len(self.soil_sensors_status) < 8:
            return      # For slave in case is receives an update before fully init
        total = 0
        avg = 0
        cnt = 0
        for x in range(0, 4):
            if self.soil_sensors_status[x + 1]:
                if int(data[x]) < 1000:
                    total += int(data[x])
                    cnt += 1
        if total > 0:
            avg = total / cnt
            r = 100 - (((avg - self.soil_wet) / (
                    self.soil_dry - self.soil_wet)) * 100)
            avg = round(r, 1)
            avg = 0 if avg < 0 else avg
            avg = 100 if avg > 100 else avg
        data.append(avg)
        # print(str(avg) + "%")
        # Area 2
        total = 0
        avg = 0
        cnt = 0
        for x in range(0, 4):
            try:
                if self.soil_sensors_status[x + 5]:
                    total += int(data[x + 4])
                    cnt += 1
            except Exception as e:
                print("Update display error COM_SOIL_READ 2 - ", e.args)
                pass
        if total > 0:
            avg = total / cnt
            r = 100 - (((avg - self.soil_wet) / (
                    self.soil_dry - self.soil_wet)) * 100)
            avg = round(r, 1)
            avg = 0 if avg < 0 else avg
            avg = 100 if avg > 100 else avg
        data.append(avg)
        self.update_soil_reading.emit(data)  # Signal new data
