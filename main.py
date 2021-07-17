import sys
from datetime import timedelta
from time import strftime

from PyQt5.QtCore import QSettings, QTimer, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from class_access import Access
from class_logger import Logger
from class_sensor import SensorClass
from communication_interface import CommunicationInterface
from controller_feeding import FeedControl
from controller_windows import WindowsController
from dbController import MysqlDB
from dialogs import DialogEngineerCommandSender, DialogEngineerIo
from functions import multi_status_bar, get_last_friday
from functions_colors import get_css_colours
from status_codes import *
from ui.main_window import Ui_MainWindow
from controller_areas import AreaController
from message_system import MessageSystem
from main_panel import MainPanel


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(Application)
        self.resize(2200, 1600)
        self.db = MysqlDB()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        if not self.db.connect_db():
            msg.setText("Can not connect to main data Base Server, will try localhost")
            msg.setWindowTitle("Unable to Data Base Server")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            # app.quit()
        multi_status_bar(self)

        self.wc = WindowsController(self)
        self.settings = QSettings(FN_SETTINGS, QSettings.IniFormat)
        self.mode = int(self.settings.value("mode"))  # 1=Master, arduino and server  2=Slave, client only

        self.main_panel = MainPanel(self)

        if self.mode == MASTER:
            self.update_status_bar(SBP_MODE, "Master", OK)
        else:
            self.update_status_bar(SBP_MODE, "Slave", OK)

        self.logger = Logger(self)

        self.msg_sys = MessageSystem(self, self.main_panel.listWidget)
        self.coms_interface = CommunicationInterface(self)

        self.access = Access(self)

        self.area_controller = AreaController(self)
        self.feed_controller = FeedControl(self)

        self.main_panel.connect_to_main_window()
        self.main_panel.update_next_feeds()

        self.main_panel.check_stage(1)
        self.main_panel.check_stage(2)
        self.main_panel.check_stage(3)

        self.update_stock()
        self.main_panel.check_light()

        self.connect_signals()

    def connect_signals(self):
        self.actionI_O_Data.triggered.connect(lambda: self.wc.show(DialogEngineerIo(self)))
        self.actionSend_Command.triggered.connect(lambda: self.wc.show(DialogEngineerCommandSender(self)))

    def load_sensors(self, area):
        sql = 'SELECT * FROM {} WHERE area = {}'.format(DB_SENSORS_CONFIG, area)
        rows = self.db.execute(sql)
        p = self.area_controller.get_area_process(area)
        for row in rows:
            sid = row[0]
            if sid not in self.sensors.keys():
                self.sensors[sid] = SensorClass(self, sid)
            else:
                self.sensors[sid].load_profile()
            if self.sensors[sid].area < 3:  # Only load process temperature ranges for areas 1 & 2
                if p != 0:
                    r = p.temperature_ranges_active
                    if r is not None:
                        r = r[self.sensors[sid].area_range]
                        self.sensors[sid].set_range(r)
                        if area == 1 or area == 2:
                            ro = p.temperature_ranges_active_org[self.sensors[sid].area_range]
                            self.sensors[sid].set_range_org(ro)

    def update_stock(self):
        tot = round(self.db.execute_single('SELECT SUM(weight - nett - hum_pac) FROM {}'.format(DB_JARS)), 1)
        w_tot = int(self.db.execute_single(
            'SELECT SUM(amount) FROM {} WHERE frequency = 1 ORDER BY sort_order'.format(DB_CLIENTS)))
        a_tot = self.calculate_weekly_average()
        # if a_tot > w_tot:
        #     w_tot = a_tot
        remain = int(tot / a_tot)
        if remain > 6:
            colour = OK
        elif remain > 4:
            colour = WARNING
        else:
            colour = CRITICAL
        self.update_status_bar(SBP_STOCK, "{} ({}@{}({})".
                                          format(tot, remain, a_tot, round(a_tot - w_tot, 1)), colour)

    def calculate_weekly_average(self):
        lf = get_last_friday()
        ed = lf - timedelta(days=1)
        sd = lf - timedelta(days=28)
        sql = "select ROUND(SUM(d.grams), 2) AS total " \
              'FROM dispatch d WHERE d.date >= "{}" ' \
              'AND d.date <= "{}"'.format(sd, ed)
        rows = self.db.execute(sql)
        tot = 0
        for row in rows:
            tot += row[0]
        return round(tot / 4, 1)

    def update_status_bar(self, panel, text, level=None):
        css = ""
        if level is not None:
            css = get_css_colours(level)
        ctrl = getattr(self, "panel_" + str(panel))

        ctrl.setText(text)
        ctrl.setStyleSheet(css)
        ctrl.setToolTip("Hello")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Application = QMainWindow()
    ui = MainWindow()
    Application.show()
    sys.exit(app.exec_())
