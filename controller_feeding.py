from PyQt5.QtCore import QThread, pyqtSignal


class FeedControl(QThread):
    area_days = ...  # type: list[int]
    update_status_feeder = pyqtSignal(int)
    update_status_nutrients = pyqtSignal(int)
    sig1 = pyqtSignal(str)
    fault = pyqtSignal(int, int, int)  # Fault source code, Fault code, tank number

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.my_parent = parent
        self.db = self.my_parent.db

    def start_up(self):
        pid = self.my_parent.area_controller.get_area_pid(1)
        if pid != 0:
            pass
