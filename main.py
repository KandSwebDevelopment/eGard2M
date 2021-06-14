import sys
from time import strftime

from PyQt5.QtCore import QSettings, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from class_sensor import SensorClass
from communication_interface import CommunicationInterface
from controller_feeding import FeedControl
from dbController import MysqlDB
from defines import *
from functions import multi_status_bar
from status_codes import *
from ui.main_window import Ui_MainWindow
from controller_areas import AreaController
from message_system import MessageSystem
from main_window import _Main


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(Application)

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

        self.settings = QSettings(FN_SETTINGS, QSettings.IniFormat)
        self.mode = int(self.settings.value("mode"))  # 1=Master, arduino and server  2=Slave, client only

        self.main_window = _Main(self)

        self.msg_sys = MessageSystem(self, self.main_window.listWidget)
        self.area_controller = AreaController(self)
        self.feed_controller = FeedControl(self)
        self.coms_interface = CommunicationInterface(self)
        self.sensors = collections.defaultdict(SensorClass)  # Holds the sensor classes

        self.main_window.connect_to_main()
        self.main_window.update_next_feeds()

        self.timer_counter = 0
        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.recurring_timer)
        self.loop_15_flag = True  # To give every other loop 15

        self.load_sensors(1)
        self.load_sensors(2)
        self.load_sensors(3)
        self.load_sensors(4)
        self.load_sensors(5)

        self.main_window.check_stage(1)
        self.main_window.check_stage(2)
        self.main_window.check_stage(3)

        self.timer.start()

    def recurring_timer(self):
        self.loop_1()
        self.timer_counter += 1
        if self.timer_counter > 360:
            self.timer_counter = 1

        # Only do following every 2nd time
        if self.timer_counter % 2 == 0:
            self.loop_2()
            return

    def loop_1(self):  # 1 sec
        # print("Current data", self.current_data)
        self.main_window.le_Clock.setText(strftime("%H" + ":" + "%M" + ":" + "%S"))
        self.main_window.le_date.setText(strftime("%a" + " " + "%d" + " " + "%b"))

    def loop_2(self):  # 2 sec
        if self.mode == MASTER:
            self.coms_interface.send_command(NWC_SENSOR_READ)
        # self.check_light()
        # if self.mode == MASTER:
        #     if self.process_is_at_location(1):
        #         if not self.fans[1].isRunning():
        #             self.lefanspeed_1.setStyleSheet("background-color: red; color: yellow")
        #     if self.process_is_at_location(2):
        #         if not self.fans[2].isRunning():
        #             self.lefanspeed_2.setStyleSheet("background-color: red; color: yellow")
        # if self.mode == SLAVE:
        #     self.slave_counter += 1
        #     if self.slave_counter > 3:
        #         self.msg_sys.add("Master/Slave Data link lost", MSG_DATA_LINK, CRITICAL, persistent=1)

    # def update_stage_buttons(self, area):
    #     items = self.area_controller.get_area_items(area)
    #     if len(items) != 0:
    #         for i in items:
    #             getattr(self, "pb_pm_%i" % i).setText(str(i))
    #             getattr(self, "pb_pm_%i" % i).setToolTip("")
    #     else:  # No process in area 2
    #         for i in range(1, 9):
    #             if i not in items:
    #                 getattr(self, "pb_pm_%i" % i).setText("")
    #                 getattr(self, "pb_pm_%i" % i).setToolTip("")

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
                r = p.temperature_ranges_active
                if r is not None:
                    r = r[self.sensors[sid].area_range]
                    self.sensors[sid].set_range(r)
                    if area == 1 or area == 2:
                        ro = p.temperature_ranges_active_org[self.sensors[sid].area_range]
                        self.sensors[sid].set_range_org(ro)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Application = QMainWindow()
    ui = MainWindow()
    Application.show()
    sys.exit(app.exec_())
