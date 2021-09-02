import sys
from datetime import timedelta

from PyQt5.QtCore import QSettings, QTimer, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from class_access import Access
from class_logger import Logger
from communication_interface import CommunicationInterface
from controller_fans import FansController
from controller_feeding import FeedControl
from controller_windows import WindowsController
from dbController import MysqlDB
from dialogs import DialogEngineerCommandSender, DialogEngineerIo, DialogDispatchInternal, DialogDispatchCounter, \
    DialogDispatchReports, DialogStrainFinder, DialogDispatchStorage, DialogDispatchOverview, DialogSysInfo, \
    DialogSettings, DialogProcessPerformance, DialogDispatchLoadingBay
from functions import multi_status_bar, get_last_friday
from functions_colors import get_css_colours
from status_codes import *
from ui.main_window import Ui_MainWindow
from controller_areas import AreaController
from message_system import MessageSystem
from main_panel import MainPanel

# Git access key
# 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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(Application)
        self.resize(1250, 975)
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
        self.master_mode = int(self.settings.value("mode"))  # 1=Master, arduino and server  2=Slave, client only

        self.main_panel = MainPanel(self)

        if self.master_mode == MASTER:
            self.update_status_bar(SBP_MODE, "Master", OK)
        else:
            self.update_status_bar(SBP_MODE, "Slave", OK)

        self.logger = Logger(self)
        self.msg_sys = MessageSystem(self, self.main_panel.listWidget)
        self.coms_interface = CommunicationInterface(self)
        self.access = Access(self)
        self.area_controller = AreaController(self)
        self.feed_controller = FeedControl(self)

        # This can only be called after the feed_control has initialised, it sets the days_till_feed
        # self.area_controller.output_controller.outputs[OUT_WATER_HEATER_1].new_day()
        # self.area_controller.output_controller.outputs[OUT_WATER_HEATER_2].new_day()

        self.connect_signals()

        self.main_panel.connect_to_main_window()
        # self.wc.show(DialogEngineerIo(self))

        self.main_panel.update_next_feeds()
        self.main_panel.check_stage(1)
        self.main_panel.check_stage(2)
        self.main_panel.check_stage(3)
        # self.main_panel.check_drying()

        self.update_stock()
        self.main_panel.check_light()

    def connect_signals(self):
        # System
        self.actionSettings.triggered.connect(lambda: self.wc.show(DialogSettings(self)))
        self.actionI_O_Data.triggered.connect(lambda: self.wc.show(DialogEngineerIo(self)))
        self.actionSend_Command.triggered.connect(lambda: self.wc.show(DialogEngineerCommandSender(self)))
        self.actionReconnect.triggered.connect(self.reconnect)
        self.actionSystem_Info.triggered.connect(lambda: self.wc.show(DialogSysInfo(self)))

        # Dispatch
        self.actionCounter.triggered.connect(lambda: self.wc.show(DialogDispatchCounter(self.main_panel)))
        self.actionInternal.triggered.connect(lambda: self.wc.show(DialogDispatchInternal(self.main_panel)))
        self.actionReport.triggered.connect(lambda: self.wc.show(DialogDispatchReports(self.main_panel)))
        self.actionStorage.triggered.connect(lambda: self.wc.show(DialogDispatchStorage(self.main_panel)))
        self.actionOverview.triggered.connect(lambda: self.wc.show(DialogDispatchOverview(self.main_panel)))
        self.actionLoading.triggered.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self.main_panel)))

        # Process
        self.actionPreformance_2.triggered.connect(lambda: self.wc.show(DialogProcessPerformance(self.main_panel)))
        # Materials
        self.actionFinder.triggered.connect(lambda: self.wc.show(DialogStrainFinder(self.main_panel)))

        self.coms_interface.update_que_status.connect(self.update_que)

        # Scales
        self.main_panel.scales.update_status.connect(self.update_scales_status)

    def reconnect(self):
        self.db.reconnect()
        self.coms_interface.reconnect()

    @pyqtSlot(int, int, int, int, name="updateQueStatus")
    def update_que(self, pri, relay, norm, lock_status):
        level = INFO
        if pri + norm > 5:
            level = WARNING
        elif pri + norm > 10:
            level = CRITICAL
        if lock_status == 2 or lock_status == 3:
            level = PENDING
        elif lock_status == 1:
            level = OPERATE
        self.update_status_bar(SBP_QUE, str(pri) + " - " + str(relay) + " - " + str(norm), level)

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

    @pyqtSlot(str, name='updateStatus')
    def update_scales_status(self, status):
        if status == 'cal1':
            pass
        elif status == 'cal2':
            pass
        elif status == 'connected':
            self.update_status_bar(SBP_REMOTE_SS, "S/S Connected", OK)
        elif status == 'disconnected':
            self.update_status_bar(SBP_REMOTE_SS, "S/S Lost", WARNING)
        elif status == 'tare':
            # self.te_info.append("Tare")
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Application = QMainWindow()
    ui = MainWindow()
    Application.show()
    sys.exit(app.exec_())
