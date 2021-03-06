import collections
import threading
from datetime import *
from time import strftime
import time as _time

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMdiSubWindow, QMessageBox

from defines import *
from dialogs import DialogFeedMix, DialogAreaManual, DialogAccessModule, DialogFan, DialogOutputSettings, \
    DialogSensorSettings, DialogProcessAdjustments, DialogWaterHeaterSettings, DialogWorkshopSettings, DialogElectMeter, \
    DialogJournal, DialogSoilSensors, DialogGraphEnv, DialogFanDry, DialogLogViewer, DialogDispatchLoadingBay, \
    DialogWaterTank, DialogLightSwitch
from functions import play_sound, sound_access_warn
from scales_com import ScalesComs
from ui.mainPanel import Ui_MainPanel


class MainPanel(QMdiSubWindow, Ui_MainPanel):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.main_window = args[0]
        self.db = args[0].db
        self.sub = self.main_window.mdiArea.addSubWindow(self)
        self.wc = self.main_window.wc
        self.master_mode = self.main_window.master_mode
        # self.sub.setMinimumSize(970, 500)
        # self.sub.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.setFixedSize(self.width(), self.height())
        # self.setGeometry(0, 0, self.width(), self.height())
        self.show()

        self.le_stage_1.installEventFilter(self)
        self.le_stage_2.installEventFilter(self)
        self.le_stage_3.installEventFilter(self)
        self.lbl_access_2.installEventFilter(self)
        self.lbl_fan_1.installEventFilter(self)
        self.lbl_fan_2.installEventFilter(self)
        self.lbl_fan_3.installEventFilter(self)
        self.lbl_access.installEventFilter(self)
        self.lbl_soil_1.installEventFilter(self)
        self.lbl_soil_2.installEventFilter(self)
        self.lbl_fill_tank_1.installEventFilter(self)
        self.lbl_fill_tank_2.installEventFilter(self)
        self.lbl_feed_mode_1.installEventFilter(self)
        self.lbl_feed_mode_2.installEventFilter(self)
        self.lbl_light_status_1.installEventFilter(self)
        self.lbl_light_status_2.installEventFilter(self)

        self.tesstatus_2.viewport().installEventFilter(self)
        self.tesstatus_3.viewport().installEventFilter(self)
        self.tesstatus_4.viewport().installEventFilter(self)
        self.tesstatus_5.viewport().installEventFilter(self)
        self.tesstatus_6.viewport().installEventFilter(self)
        self.tesstatus_7.viewport().installEventFilter(self)
        self.tesstatus_8.viewport().installEventFilter(self)
        self.tesstatus_9.viewport().installEventFilter(self)
        self.tesstatus_10.viewport().installEventFilter(self)
        self.tesstatus_11.viewport().installEventFilter(self)
        self.tesstatus_12.viewport().installEventFilter(self)
        for x in range(2, 13):
            getattr(self, "tesstatus_%i" % x).viewport().setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.today = datetime.now().day  # Holds today's date. Used to detect when day changes
        self.mid_day = False  # False till mid day then true till new day

        self.area_controller = None
        self.feed_controller = None
        self.coms_interface = None
        # self.fan_controller = None
        self.access = None
        self.logger = None
        self.soil_sensors = None
        self.msg_sys = None
        self.stage_change_warning_days = int(self.db.get_config(CFT_PROCESS, "stage change days", 7))
        self.unit_price = self.db.execute_single("SELECT ppu FROM {} ORDER BY date_from DESC LIMIT 1".
                                                format(DB_ELECTRIC)) / 100

        self.slave_counter = 0
        self.coms_counter = 0
        self.access_open_time = 0  # Timestamp when cover was opened
        self.timer_counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.loop_15_flag = True  # To give every other loop 15
        # self.last_sensor_data = None

        self.auto_db_backup = int(self.db.get_config(CFT_SYSTEM, "auto_db_backup", 1))
        self.nutrient_auto_stir = int(self.db.get_config(CFT_FEEDER, "auto stir", 6))
        self.has_scales = int(self.db.get_config(CFT_MODULES, "ss unit", 0))
        if self.main_window.factory:
            self.has_scales = 0
        if not self.has_scales:
            # self.panel_9.hide()
            self.main_window.actionCounter.setEnabled(False)
            self.main_window.actionInternal.setEnabled(False)
            self.main_window.actionScales.setEnabled(False)
            self.main_window.actionStorage.setEnabled(False)
            self.main_window.actionReconcilation.setEnabled(False)
            self.main_window.actionLoading.setEnabled(False)
            self.scales = None
        else:
            self.scales = ScalesComs(self)

    def eventFilter(self, source, event):
        # Remember to install event filter for control first
        # print("Event ", event.type())
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if source is self.lbl_access_2:
                self.wc.show(DialogAccessModule(self))
            elif source is self.lbl_access:
                self.wc.show(DialogElectMeter(self))
            elif source is self.lbl_fill_tank_1:
                self.wc.show(DialogWaterTank(self.main_window, 1))
            elif source is self.lbl_fill_tank_2:
                self.wc.show(DialogWaterTank(self.main_window, 2))

            # Area 1
            elif source is self.lbl_fan_1:
                self.wc.show(DialogFan(self, 1))
            elif source is self.lbl_light_status_1:
                self.wc.show(DialogLightSwitch(self, 1))
            elif source is self.le_stage_1:
                if self.area_controller.area_has_process(1):
                    self.wc.show(DialogJournal(self.area_controller.get_area_process(1), self))
                else:
                    self.wc.show(DialogAreaManual(self, 1))
            elif source is self.tesstatus_2.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 3))
            elif source is self.tesstatus_3.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 4))
            elif source is self.tesstatus_4.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 10))
            elif source is self.tesstatus_5.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 11))
            elif source is self.lbl_soil_1:
                self.wc.show(DialogSoilSensors(self, 1))
            elif source is self.lbl_feed_mode_1:
                pass

            # Area 2
            elif source is self.lbl_fan_2:
                self.wc.show(DialogFan(self, 2))
            elif source is self.lbl_light_status_2:
                self.wc.show(DialogLightSwitch(self, 2))
            elif source is self.le_stage_2:
                if self.area_controller.area_has_process(2):
                    self.wc.show(DialogJournal(self.area_controller.get_area_process(2), self))
                else:
                    self.wc.show(DialogAreaManual(self, 2))
            elif source is self.tesstatus_6.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 5))
            elif source is self.tesstatus_7.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 6))
            elif source is self.tesstatus_8.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 12))
            elif source is self.tesstatus_9.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 13))
            elif source is self.lbl_soil_2:
                self.wc.show(DialogSoilSensors(self, 2))
            elif source is self.lbl_feed_mode_2:
                pass

            # Area 3, drying
            elif source is self.le_stage_3:
                if self.area_controller.area_has_process(3):
                    self.wc.show(DialogJournal(self.area_controller.get_area_process(3), self))
                else:
                    self.wc.show(DialogAreaManual(self, 3))
            elif source is self.tesstatus_11.viewport():
                self.wc.show(DialogSensorSettings(self, 3, 7))
            elif source is self.tesstatus_12.viewport():
                self.wc.show(DialogSensorSettings(self, 3, 8))
            elif source is self.lbl_fan_3:
                self.wc.show(DialogFanDry(self))
            # Area 4, workshop
            elif source is self.tesstatus_10.viewport():
                self.wc.show(DialogSensorSettings(self, 4, 9))

        return QWidget.eventFilter(self, source, event)

    def recurring_timer(self):
        self.loop_1()
        self.timer_counter += 1
        if self.timer_counter > 360:
            self.timer_counter = 1

        if self.timer_counter % 180 == 0:
            self.loop_15()

        # Every 120
        if self.timer_counter % 120 == 0:
            self.loop_6()

        # Every 60
        if self.timer_counter % 60 == 0:
            self.loop_5()

        # Every 10
        if self.timer_counter % 15 == 0:  # 15 sec
            self.loop_3()
            return

        # Only do following every 2nd time
        if self.timer_counter % 4 == 0:
            self.loop_2()
            return

    def loop_1(self):  # 1 sec
        self.le_Clock.setText(strftime("%H" + ":" + "%M" + ":" + "%S"))
        self.le_date.setText(strftime("%a" + " " + "%d" + " " + "%b"))

    def loop_2(self):  # 2 sec
        if self.master_mode == MASTER:
            self.coms_interface.send_command(NWC_SENSOR_READ)
        self.check_light()
        if self.master_mode == SLAVE:
            self.slave_counter += 1
            if self.slave_counter > 6:
                self.msg_sys.add("Master/Slave Data link lost", MSG_DATA_LINK, CRITICAL)

    def loop_3(self):  # 10 sec
        if self.master_mode == MASTER:
            self.coms_interface.send_command(COM_OTHER_READINGS)
            self.coms_interface.send_data(COM_WATTS, False, MODULE_DE)
            self.coms_interface.send_data(COM_READ_KWH, False, MODULE_DE)
        self.area_controller.output_controller.check_water_heaters()

    def loop_5(self):  # 60 secs
        self.update_next_feeds()
        # Check for new day
        if datetime.now().day != self.today:
            self.new_day()
        if not self.mid_day and datetime.now().hour > 12:
            self.new_mid_day()
        self.db.execute("select name from " + DB_NUTRIENTS_NAMES)  # This is only to keep the database connection alive
        if self.master_mode == MASTER:
            cm = datetime.now().minute
            if cm % 2 == 0:
                #self.main_window.logger.save_log(self.area_controller.get_sensor_log_values())
                self.main_window.logger.save_output_log(self.area_controller.output_controller.get_output_log_values())
                self.main_window.logger.save_fan_log(self.area_controller.fan_controller.get_log_values())
                self.main_window.logger.save_power_log(self.le_pwr_current.text() + ", " + self.le_pwr_total_1.text())
                self.main_window.logger.save_soil_log(self.area_controller.soil_sensors.get_log_values())
        cm = datetime.now().minute
        if cm % 2 == 0:
            pass

    def loop_6(self):  # 2 min
        if self.master_mode == MASTER:
            self.coms_interface.send_command(NWC_SOIL_READ)
            if self.nutrient_auto_stir > 0 and datetime.now().hour % self.nutrient_auto_stir == 0 and datetime.now().minute < 2:
                print("Stirred Nutrients --------- ", datetime.now())
                self.coms_interface.send_data(CMD_SWITCH_TIMED, True, MODULE_FU, SW_NUTRIENT_STIR, ON,
                                              self.main_window.feeder_unit.nutrient_stir_time / 2)

    def loop_15(self):  # 3 Min
        if self.main_window.access.has_status(ACS_COVER_OPEN) and \
                self.main_window.access.mute == False and \
                self.main_window.factory == False:
            sound_access_warn()
        else:
            if self.feed_controller.feed_due_today() and \
                    self.main_window.feed_controller.mute == False and \
                    self.main_window.factory == False:
                if datetime.now().time() > (  # feed_time is a string not a datetime object
                        datetime.strptime(self.feed_controller.feed_time, "%H:%M") - timedelta(hours=2)).time():
                    play_sound(SND_ATTENTION)
        self.loop_15_flag = not self.loop_15_flag

    def connect_to_main_window(self):
        self.area_controller = self.main_window.area_controller
        self.feed_controller = self.main_window.feed_controller
        self.coms_interface = self.main_window.coms_interface
        self.logger = self.main_window.logger
        self.access = self.main_window.access
        self.msg_sys = self.main_window.msg_sys
        self.connect_signals()

        if self.has_scales:  # These have to be here to allow signals to connect
            self.scales.connect()
        self.update_duration_texts()
        self.area_controller.output_controller.water_heater_update_info()  # Required here it init things
        self.loop_15()  # Instant feed due check
        self.update_water_required()
        self.check_upcoming_starts()

    def connect_signals(self):
        self.pb_cover.clicked.connect(lambda: self.access.open())
        self.pb_cover_close.clicked.connect(lambda: self.access.close_cover())
        self.pb_graphs.clicked.connect(lambda: self.wc.show(DialogGraphEnv(self)))
        self.pb_logs.clicked.connect(lambda: self.wc.show(DialogLogViewer(self)))
        self.b1.clicked.connect(self.test)

        # Area 1
        self.pb_man_feed_1.clicked.connect(lambda: self.feed_manual(1))
        self.pb_feed_mix_1.clicked.connect(lambda: self.wc.show(DialogFeedMix(self, 1)))
        self.pb_pid_1.clicked.connect(lambda: self.wc.show_process_info(1))
        self.pb_advance_1.clicked.connect(lambda: self.stage_adjust(1, -1))
        self.pbstageadvance_1.clicked.connect(lambda: self.stage_advance(1))
        self.pb_hold_1.clicked.connect(lambda: self.stage_adjust(1, 1))
        self.pbadjust_1.clicked.connect(lambda: self.wc.show(DialogProcessAdjustments(self, 1)))
        self.pb_output_status_1.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_11))
        self.pb_output_status_2.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_12))
        self.pb_output_status_3.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_AUX_1))
        self.pb_output_status_9.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_SPARE_1))
        self.pb_output_mode_1.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 1)))
        self.pb_output_mode_2.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 2)))
        self.pb_output_mode_3.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 3)))
        self.pb_output_mode_9.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 4)))
        # Area 2
        self.pb_man_feed_2.clicked.connect(lambda: self.feed_manual(2))
        self.pb_feed_mix_2.clicked.connect(lambda: self.wc.show(DialogFeedMix(self, 2)))
        self.pb_pid_2.clicked.connect(lambda: self.wc.show_process_info(2))
        self.pbadjust_2.clicked.connect(lambda: self.wc.show(DialogProcessAdjustments(self, 2)))
        self.pb_output_status_4.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_21))
        self.pb_output_status_5.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_22))
        self.pb_output_status_6.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_AUX_2))
        self.pb_output_status_10.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_SPARE_2))
        self.pb_output_mode_4.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 1)))
        self.pb_output_mode_5.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 2)))
        self.pb_output_mode_6.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 3)))
        self.pb_output_mode_10.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 4)))
        self.pb_pm_1.clicked.connect(lambda: self.change_to_flushing(1))
        self.pb_pm_2.clicked.connect(lambda: self.change_to_flushing(2))
        self.pb_pm_3.clicked.connect(lambda: self.change_to_flushing(3))
        self.pb_pm_4.clicked.connect(lambda: self.change_to_flushing(4))
        self.pb_pm_5.clicked.connect(lambda: self.change_to_flushing(5))
        self.pb_pm_6.clicked.connect(lambda: self.change_to_flushing(6))
        self.pb_pm_7.clicked.connect(lambda: self.change_to_flushing(7))
        self.pb_pm_8.clicked.connect(lambda: self.change_to_flushing(8))
        # Area 3
        self.pb_pid_3.clicked.connect(lambda: self.wc.show_process_info(3))
        self.pb_output_status_7.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_31))
        self.pb_output_mode_7.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 3, 1)))
        self.pb_pm2_1.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 1)))
        self.pb_pm2_2.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 2)))
        self.pb_pm2_3.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 3)))
        self.pb_pm2_4.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 4)))
        self.pb_pm2_5.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 5)))
        self.pb_pm2_6.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 6)))
        self.pb_pm2_7.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 7)))
        self.pb_pm2_8.clicked.connect(lambda: self.wc.show(DialogDispatchLoadingBay(self, 8)))
        # Workshop
        self.pb_output_status_8.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_ROOM))
        self.pb_output_mode_8.clicked.connect(lambda: self.wc.show(DialogWorkshopSettings(self)))
        # Water
        self.pb_output_status_11.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_WATER_HEATER_1))
        self.pb_output_status_12.clicked.connect(
            lambda: self.area_controller.output_controller.switch_output(OUT_WATER_HEATER_2))
        self.pb_output_mode_11.clicked.connect(lambda: self.wc.show(DialogWaterHeaterSettings(self, 1)))
        self.pb_output_mode_12.clicked.connect(lambda: self.wc.show(DialogWaterHeaterSettings(self, 2)))
        # Outside

        # Signals
        self.coms_interface.update_sensors.connect(self.update_sensors)
        self.coms_interface.update_switch.connect(self.update_switch)
        self.access.update_access.connect(self.update_access)
        self.access.update_duration.connect(self.update_cover_duration)
        self.coms_interface.update_power.connect(self.update_power)
        self.coms_interface.update_other_readings.connect(self.update_others)
        self.area_controller.fan_controller.update_fans_speed.connect(self.update_fans)
        self.coms_interface.update_float_switch.connect(self.update_float)
        self.coms_interface.update_from_relay.connect(self.process_relay_command)
        self.coms_interface.update_received.connect(self.coms_indicator)
        self.coms_interface.update_feeder_unit.connect(self.update_from_fu)
        self.area_controller.fan_controller.update_fans_mode.connect(self.update_fan_mode)
        # self.db.backup_finished.connect(self.notify_backup_finished)

    def test(self):
        self.main_window.logger.save_output_log(self.area_controller.output_controller.get_output_log_values())

        pass
        # s = ["low", "set", "high"]
        # for a in range(1, 3):
        #     for i in range(1, 5):
        #         for se in range(0, 3):
        #             self.db.execute_write('INSERT INTO {} (area, `day`, `item`, `setting`, `value`)'
        #                                   ' VALUES ({}, -1, {}, "{}", 20)'.format(DB_PROCESS_TEMPERATURE, a, i, s[se]))
        #             self.db.execute_write('INSERT INTO {} (area, `day`, `item`, `setting`, `value`)'
        #                                   ' VALUES ({}, -2, {}, "{}", 20)'.format(DB_PROCESS_TEMPERATURE, a, i, s[se]))
        # self.area_controller.output_controller.outputs[OUT_HEATER_ROOM].boost_start()

    # def notify_backup_finished(self):
    #     msg = QMessageBox(QMessageBox.Information, "Complete", "The database backup has finished", QMessageBox.Ok)
    #     msg.exec_()
    #     self.msg_sys.add("Database backup complete", MSG_DATABASE_BACKUP, INFO)
    #
    def update_next_feeds(self):
        """ This updates the all feeding information for both areas  """
        for loc in range(1, 3):
            if not self.area_controller.area_has_process(loc):  # Has area no process
                getattr(self, "lbl_feed_days_" + str(loc)).setText("")
                getattr(self, "lbl_days_" + str(loc)).setText("")
                getattr(self, "lbl_feed_remaining_" + str(loc)).setText("")
                getattr(self, "lbl_feed_mixes_" + str(loc)).setText("")
                getattr(self, "pb_feed_mix_" + str(loc)).setEnabled(False)
                getattr(self, "pb_man_feed_" + str(loc)).setEnabled(False)
                continue

            days = self.feed_controller.days_till_feed(loc)
            ctrl = getattr(self, "lbl_next_feed_" + str(loc))
            if days == 0:
                # txt = " Today.."
                ctrl.setPixmap(QPixmap(":/normal/today.png"))
                ctrl.setToolTip("Feed due today")
                css = "background-color: green;  color: black;"
            elif days == 1:
                # txt = " Tomorrow"
                ctrl.setPixmap(QPixmap(":/normal/tomorrow.png"))
                ctrl.setToolTip("Feed due today")
                css = BACKGROUND_DEFAULT
            elif days == -1:
                # txt = "Yesterday"
                ctrl.setPixmap(QPixmap(":/normal/yesterday.png"))
                ctrl.setToolTip("Feed due yesterday")
                css = "background-color: red;  color: white; border-radius: 6px;"
            else:
                ctrl.setPixmap(QPixmap(":/normal/tomorrow.png"))
                css = BACKGROUND_DEFAULT
            ctrl.setStyleSheet(css)
            # show days till feed
            getattr(self, "lbl_days_%i" % loc).setText(str(days))
            if days >= 1:
                getattr(self, "lbl_days_%i" % loc).setStyleSheet("background-color: #f0f0f0;  color: Black;")
                ctrl.setToolTip("Feed due in {} day{}".format(days, "" if days == 1 else "s"))
            elif days <= -1:
                ctrl.setToolTip("Feed overdue by {} day{}".format(days, "" if days == -1 else "s"))
            elif days == 0:
                ctrl.setToolTip("Feed due Today")
                getattr(self, "lbl_days_%i" % loc).setStyleSheet("background-color: green;  color: White;")

            getattr(self, "lbl_feed_mixes_%i" % loc).setText(str(self.feed_controller.feeds[loc].get_mix_count()))

            # Recipe status
            ctrl = getattr(self, "lbl_feed_status_%i" % loc)
            if loc == 2 and self.feed_controller.feeds[loc].flush_only:
                ctrl.clear()
            else:
                rs = self.feed_controller.get_recipe_status(loc)
                if rs == 2:
                    rs = 0
                if rs == -1:
                    ctrl.setPixmap(QtGui.QPixmap(":/normal/last_feed_1.png"))
                    ctrl.setToolTip("Next feed will be last with this recipe")
                elif rs == 1:
                    ctrl.setPixmap(QPixmap(":/normal/next_feed_new.png"))
                    ctrl.setToolTip("Next feed will be new recipe")
                elif rs == 2:
                    ctrl.setPixmap(QtGui.QPixmap(":/normal/new_feed_today.png"))
                    ctrl.setToolTip("Today's feed is a new recipe")
                else:
                    ctrl.setPixmap(QtGui.QPixmap())

            # Feed frequency and number of days remaining
            ctrl = getattr(self, 'lbl_feed_days_%i' % loc)
            ctrl.setText("{}".format(self.feed_controller.feeds[loc].frequency))
            ctrl = getattr(self, 'lbl_feed_remaining_%i' % loc)
            if loc == 2 and self.feed_controller.feeds[loc].flush_only:
                ctrl.clear()
            else:
                ctrl.setText("{}".format(self.feed_controller.feeds[loc].get_recipe_days_remaining()))
                ctrl.setToolTip("Number of days the current recipe will be used for<br>Or {} feeds".
                                format(self.feed_controller.feeds[loc].get_feeds_remaining()))

            # Feed mode icon
            ctrl = getattr(self, "lbl_feed_mode_%i" % loc)
            if self.feed_controller.get_feed_mode(loc) == 1:
                ctrl.setPixmap(QtGui.QPixmap(":/normal/001-hand.png"))
                ctrl.setToolTip("Manual feed mode")
                # text = "Manual"
            elif self.feed_controller.get_feed_mode(loc) == 2:
                ctrl.setPixmap(QtGui.QPixmap(":/normal/semi_auto.png"))
                ctrl.setToolTip("Semi Auto feed mode")
                # text = "Manual"
            elif self.feed_controller.get_feed_mode(loc) == 3:
                ctrl.setPixmap(QtGui.QPixmap(":/normal/auto.png"))
                ctrl.setToolTip("Automatic feed mode")
                # text = "Semi Auto"
            elif self.feed_controller.get_feed_mode(loc) == 4:
                ctrl.setPixmap(QtGui.QPixmap(":/normal/full_auto.png"))
                ctrl.setToolTip("Fully automatic feed mode")
                # text = "Full Auto"
            # ctrl.setText(text)

    def stage_advance(self, area):
        # Advances the the process to the next stage. For Area 1 only
        if self.area_controller.area_has_process(area):
            self.area_controller.get_area_process(area).advance_stage()
            self.area_controller.reload_area(area)
            self.feed_controller.reload_area(area)
            self.update_duration_texts()
            self.check_stage(area)
            self.coms_interface.relay_send(NWC_RELOAD_PROCESSES)

    def check_stage(self, location):
        if self.area_controller.get_area_process(location) == 0:
            return
        if location == 1:
            next_stage_days = self.area_controller.get_area_process(location).stage_days_remaining
            stage_day_adjust = self.area_controller.get_area_process(location).stage_day_adjust
            if next_stage_days - stage_day_adjust <= self.stage_change_warning_days:
                self.frmstagechange_1.setEnabled(True)
                ctrl = self.pbstageadvance_1
                ctrl_le = self.lestageinfo_1
                ctrl_advance = self.pb_advance_1
                # self.process_from_location(1)
                ctrl_le.setText(str(next_stage_days))  # + day + str(
                if next_stage_days >= 1:
                    ctrl_advance.setEnabled(True)
                    ctrl.setEnabled(False)
                    ctrl_le.setStyleSheet("background-color: white;  color: black;")
                elif next_stage_days == 0:
                    ctrl_advance.setEnabled(False)
                    ctrl.setEnabled(True)
                    ctrl_le.setStyleSheet("background-color: Green;  color: black;")
                elif next_stage_days < 0:
                    ctrl.setEnabled(False)
                    ctrl_le.setStyleSheet("background-color: red;  color: white;")
                    ctrl_advance.setEnabled(False)
            else:
                self.frmstagechange_1.setEnabled(False)
                self.lestageinfo_1.setStyleSheet("background-color: white;  color: black;")

        elif location == 2:
            p = self.area_controller.get_area_process(location)
            if p.stage_days_elapsed >= p.strain_shortest - 7:
                self.frmstagechange_2.setEnabled(True)
                x = 1
                p.check_stage()
                for w in p.strain_window:
                    ctrl = getattr(self, "pb_pm_%i" % x)
                    ctrl.setText(str(x))
                    flush_start = self.db.execute_single(
                        "SELECT start FROM {} WHERE item = {}".format(DB_FLUSHING, x))
                    if flush_start is not None:
                        w = 444
                    if x in self.area_controller.get_area_items(3):
                        w = -10
                    if w == -10 or w == -100:  # Item removed or in drying
                        ctrl.setText("")
                        ctrl.setEnabled(False)
                        ctrl.setToolTip("")
                        ctrl.setStyleSheet(None)
                    elif w == 999:   # Not ready
                        ctrl.setText(str(x))
                        ctrl.setEnabled(True)
                        name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                      "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                      .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                        ctrl.setToolTip(name)

                    elif 0 > w > -7:
                        ctrl.setEnabled(True)
                        ctrl.setStyleSheet("background-color: Yellow;")
                        name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                      "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                      .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                        ctrl.setToolTip("{} Due in {} days".format(name, w))
                    elif w < 7:
                        ctrl.setEnabled(True)
                        ctrl.setStyleSheet("background-color: Green;")
                        name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                      "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                      .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                        ctrl.setToolTip("{} Due plus {} days".format(name, w))
                    elif 7 < w < 444:
                        ctrl.setEnabled(True)
                        ctrl.setStyleSheet("background-color: Orange;")
                        name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                      "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                      .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                        ctrl.setToolTip("{} Over Due by {} days".format(name, w))
                    elif w == 444:  # Item is flushing
                        ctrl.setEnabled(True)
                        ctrl.setStyleSheet("background-color: DodgerBlue;")
                        name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                      "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                      .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                        df = (datetime.now().date() - flush_start).days + 1
                        ctrl.setToolTip("Day {} flushing\n\r{}".format(df, name))

                    x += 1
                # for x in range(1, 9):
                #     if p.strain_window[x] != 999:
                #         return
                #     ctrl = getattr(self, "pb_pm_%i" % x)
                #     ctrl.setEnabled(False)
                #     ctrl.setText("")
                #     ctrl.setStyleSheet("")
            else:
                self.frmstagechange_2.setEnabled(False)
                return None

        elif location == 3:
            if self.area_controller.area_has_process(3):
                for x in range(1, 9):
                    getattr(self, "pb_pm2_%i" % x).setText("")
                self.frmstagechange_3.setEnabled(True)
                rows = self.db.execute('SELECT item, started FROM {}'.format(DB_PROCESS_DRYING))
                if len(rows) == 0:
                    self.frmstagechange_3.setEnabled(False)
                    return
                for row in rows:
                    getattr(self, "pb_pm2_%i" % row[0]).setText(str(row[0]))
                    getattr(self, "pb_pm2_%i" % row[0]).setEnabled(True)
                    days = (datetime.now().date() - row[1]).days
                    name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                  "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                  .format(DB_STRAINS, DB_PROCESS_STRAINS,
                                                          self.area_controller.areas_pid[3], row[0]))
                    getattr(self, "pb_pm2_%i" % row[0]).setToolTip("{}\r\nDay {} drying".format(name, days))
                # Show buttons disabled for all in flushing as they will be here next
                rows = self.db.execute('SELECT item, start FROM {}'.format(DB_FLUSHING))
                for row in rows:
                    getattr(self, "pb_pm2_%i" % row[0]).setText(str(row[0]))
                    getattr(self, "pb_pm2_%i" % row[0]).setEnabled(False)

    def check_light(self):
        """ This checks both area processes to see if light should be on or off. If a change is detected it sends
            switch to IO.
            Also checks to see if in transition period
            self.update_switch handles the change when it has actually switched """
        if self.area_controller.area_has_process(1):
            status = self.area_controller.get_area_process(1).check_light()
            self.area_controller.get_area_process(1).check_trans()
            if self.area_controller.light_relay_1 != status:
                self.coms_interface.send_switch(SW_LIGHT_1, status)
        else:
            if self.area_controller.light_relay_1 != OFF:
                self.coms_interface.send_switch(SW_LIGHT_1, OFF)

        if self.area_controller.area_has_process(2):
            status = self.area_controller.get_area_process(2).check_light()
            self.area_controller.get_area_process(2).check_trans()
            if self.area_controller.light_relay_2 != status or self.area_controller.light_relay_2 == -1:
                if self.master_mode == MASTER:
                    self.coms_interface.send_switch(SW_LIGHT_2, status)
                else:
                    if self.area_controller.light_relay_2 == -1:
                        self.coms_interface.relay_send(NWC_SWITCH_REQUEST, SW_LIGHT_2)
                        self.area_controller.light_relay_2 = -2
        else:
            if self.area_controller.light_relay_2 != OFF:
                self.coms_interface.send_switch(SW_LIGHT_2, OFF)

    def check_upcoming_starts(self):
        rows = self.db.execute(
            'SELECT id, start FROM {} WHERE `start` >= "{}" AND running = 0'.
            format(DB_PROCESS, datetime.now().date() - timedelta(days=10)))
        for row in rows:
            if row[1] <= (datetime.now() + timedelta(days=7)).date():
                m = ("New process No:{} is due to start on {}\n\rPre-start due on {}"
                     .format(row[0], datetime.strftime(row[1], "%a %d/%m/%y"),
                             datetime.strftime(row[1] - timedelta(days=3), "%a %d/%m/%y")))
                self.msg_sys.add(m, MSG_UPCOMING, INFO)

    def change_to_flushing(self, item):
        sql = "SELECT start FROM {} WHERE item = {}".format(DB_FLUSHING, item)
        row = self.db.execute_one_row(sql)
        if row is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Confirm you wish to flush number {} ".format(item))
            msg.setWindowTitle("Confirm Flush")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            if msg.exec_() == QMessageBox.Cancel:
                return
            sql = "INSERT into {} (item, start) VALUES ({}, '{}')".format(DB_FLUSHING, item, datetime.now().date())
            self.db.execute_write(sql)
            p = self.area_controller.get_area_process(2)
            dt = datetime.strftime(datetime.now(), '%d/%m/%y %H:%M')
            p.journal_write("{}  Number {} started flush. Day {} flowering".format(dt, item, p.stage_days_elapsed))

            self.main_window.feed_controller.feeds[2].load_mixes()
            self.check_stage(2)
            self.coms_interface.relay_send(NWC_CHANGE_TO_FLUSHING)
        else:
            self.move_to_finishing(item)

    def move_to_finishing(self, item):
        # moves a single plant into drying, if last one then advance the stage
        # the location will be area 2 ?? This may change
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Confirm you wish to move number {} into Drying".format(item))
        msg.setWindowTitle("Confirm Move to Drying")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return

        self.sender().setStyleSheet("")
        self.sender().setText("")
        self.sender().setEnabled(False)
        p = self.area_controller.get_area_process(
            2)  # Don't need to check if process at location as it should never be here unless there is a process
        p.strain_location[item - 1] = 3
        sql = "INSERT INTO {} (area, process_id, item) VALUES (3, {}, {})".format(DB_AREAS, p.id, item)
        self.db.execute_write(sql)
        sql = "DELETE FROM {} WHERE process_id = {} AND item = {} AND area = 2".format(DB_AREAS, p.id, item)
        self.db.execute_write(sql)
        # Update location and total days
        sql = "UPDATE {} SET location = 3, total_days = {} WHERE process_id = {} and item = {}". \
            format(DB_PROCESS_STRAINS, p.days_total, p.id, item)
        self.db.execute_write(sql)
        # Remove item from flushing table
        sql = "DELETE FROM {} WHERE item = {} LIMIT 1".format(DB_FLUSHING, item)
        self.db.execute_write(sql)
        # Add to drying table
        sql = "INSERT INTO {} (item, started) VALUES ({}, '{}')".format(DB_PROCESS_DRYING, item, datetime.now().date())
        self.db.execute_write(sql)
        # Enable button in area 3
        getattr(self, "pb_pm2_%i" % item).setEnabled(True)

        dt = datetime.strftime(datetime.now(), '%d/%m/%y %H:%M')
        # p.journal_write(dt + "    Number " + str(item) + " Cut and moved to drying. Days flowering "
        #                 + str(p.stage_days_elapsed) + "  ^")
        p.journal_write("{}    Number {} Cut and moved to drying. Days Veging {}   Days flowering {}  Total days {}"
                        .format(dt, item, p.days_total - p.stage_days_elapsed, p.stage_days_elapsed, p.days_total))

        self.area_controller.reload_area(2)
        # Breakpoint here as last time final item still failed below if, line above added to fix ??
        if len(self.area_controller.get_area_items(2)) == 0:  # If no items left in area 2
            # Update the processes current stage
            self.db.execute_write(
                "UPDATE " + DB_PROCESS + " SET stage = 4, location = 3 WHERE id = " + str(p.id))
            # Delete any mixes for area 2 as it will now be empty
            self.db.execute_write("DELETE FROM {} WHERE area = 2".format(DB_PROCESS_FEED_ADJUSTMENTS))
            self.db.execute_write("DELETE FROM {} WHERE area = 2".format(DB_PROCESS_MIXES))

            p.current_stage += 1
        self.area_controller.reload_area(3)
        self.check_stage(2)
        self.check_stage(3)
        self.feed_controller.reload_area(2)
        self.coms_interface.relay_send(NWC_MOVE_TO_FINISHING)

    def finish_item(self, item, amount=None, show_warn=True):
        # Drying area, when plant dried
        if show_warn:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Confirm you wish to finish number " + str(item))
            msg.setWindowTitle("Confirm Item Finish")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            if msg.exec_() == QMessageBox.Cancel:
                return
        getattr(self, "pb_pm2_%i" % item).setEnabled(False)
        p = self.area_controller.get_area_process(3)
        if p is None:  # If p is none then the process is still running in area 2
            p = self.area_controller.get_area_process(
                2)  # ??? Is this right - an item shouldn't finish unless in area 3
        p.strain_location[item - 1] = 50
        # Remove it from areas table
        sql = "DELETE FROM {} WHERE process_id = {} AND item = {} AND area = 3 LIMIT 1".format(DB_AREAS, p.id, item)
        self.db.execute_write(sql)
        # Remove it from drying table
        sql = "DELETE FROM {} WHERE item = {} LIMIT 1".format(DB_PROCESS_DRYING, item)
        self.db.execute_write(sql)
        # Update the location in the process strains table
        sql = "UPDATE {} SET location = 50 WHERE process_id = {} and item = {} LIMIT 1".format(
            DB_PROCESS_STRAINS, p.id, item)
        self.db.execute_write(sql)
        # Add journal entry
        if amount is None:
            dt = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M')
            p.journal_write(dt + "    Number " + str(item) + " Dried and finished.")

        # self.area_controller.load_areas()
        if len(self.area_controller.get_area_items(3)) == 1:    # 1 as this item not removed from areas yet... Should fix below
            # None left, so finish stage
            self.area_controller.get_area_process(3).end_process()
            # BreakPoint above is returning 0 and crashing - process already removed by load_areas ?? It is important that the end process gets called
            self.area_controller.load_areas()
            self.area_controller.load_sensors(3)
            self.area_controller.load_outputs(3)
        else:
            # self.area_controller.load_areas()
            self.check_stage(3)
            self.coms_interface.relay_send(NWC_FINISH_ITEM, item)

    def feed_manual(self, loc):
        self.feed_controller.feed(loc)
        self.update_next_feeds()
        self.coms_interface.relay_send(NWC_FEED, loc)

    def io_reboot(self):
        self.msg_sys.add("IO Reboot", MSG_DATA_LINK, CRITICAL)
        if self.master_mode == SLAVE:
            return
        th = threading.Thread(target=self.io_sync)
        th.start()
        # self.io_sync()

    def io_sync(self):
        # Send all parameters to the IO unit as it has rebooted
        # _time.sleep(1)
        if self.area_controller.area_has_process(1):
            self.coms_interface.send_switch(SW_LIGHT_1, self.area_controller.get_area_process(1).check_light())
            _time.sleep(1)
        if self.area_controller.area_has_process(2):
            self.coms_interface.send_switch(SW_LIGHT_2, self.area_controller.get_area_process(2).check_light())
            _time.sleep(1)
        if self.area_controller.area_has_process(1):
            self.coms_interface.send_switch(SW_LIGHT_1, self.area_controller.get_area_process(1).check_light())
        _time.sleep(1)
        if self.area_controller.area_has_process(2):
            self.coms_interface.send_switch(SW_LIGHT_2, self.area_controller.get_area_process(2).check_light())
            _time.sleep(1)
        self.coms_interface.send_switch(SW_FANS_POWER, self.area_controller.fan_controller.master_power)
        _time.sleep(1)
        self.coms_interface.send_data(CMD_FAN_SPEED, True, MODULE_IO, 1,
                                      self.area_controller.fan_controller.fans[1].speed)
        _time.sleep(1)
        self.coms_interface.send_data(CMD_FAN_SPEED, True, MODULE_IO, 2,
                                      self.area_controller.fan_controller.fans[2].speed)
        _time.sleep(1)
        if self.area_controller.area_has_process(1):
            self.coms_interface.send_switch(SW_FAN_1_OFF, ON)
            _time.sleep(1)
        if self.area_controller.area_has_process(2):
            self.coms_interface.send_switch(SW_FAN_2_OFF, ON)
            _time.sleep(1)
        outputs = self.area_controller.output_controller.outputs
        for o in outputs:  # o = index
            self.coms_interface.send_switch(outputs[o].output_pin, outputs[o].relay_position)
            _time.sleep(1)

    def stage_adjust(self, area, val):
        # Adjusts the current stage by val days for process in location
        if not self.area_controller.area_has_process(area):
            return
        p = self.area_controller.get_area_process(area)
        p.adjust_stage_days(val)
        self.area_controller.display_stage_icon(area)
        self.feed_controller.reload_area(area)
        self.update_duration_texts()
        self.check_stage(area)
        self.coms_interface.relay_send(NWC_STAGE_ADJUST, area)

    def start_new_process(self, pid):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        if self.area_controller.area_has_process(1):
            msg.setText("Area 1 is not free")
            msg.setWindowTitle("Start Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        msg.setText("Confirm you wish to start this process")
        msg.setWindowTitle("Confirm Stage Start")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        rsd = datetime.strftime(datetime.now(), "%Y-%m-%d")
        # rsd = self.db.reverse_date(sd)

        # Update processes table
        # Breakpoint is set so you can check the date, it seems to get put in reverse
        sql = 'UPDATE {} SET running = 1, start = "{}", location = 1, stage = 1, feed_mode = 1 WHERE id = {}'.format(
            DB_PROCESS, rsd, pid)
        self.db.execute_write(sql)

        # Set last feed date
        sql = 'UPDATE {} SET dt = "{}" WHERE item = "feed date" AND id = 1'.format(DB_PROCESS_ADJUSTMENTS, rsd)
        self.db.execute_write(sql)

        # Reset feed litres
        sql = 'UPDATE {} SET offset = 0 WHERE item = "feed litres" AND id = 1'.format(DB_PROCESS_ADJUSTMENTS)
        self.db.execute_write(sql)

        # Set process strains location
        sql = 'UPDATE {} SET location = 1 WHERE process_id = {}'.format(DB_PROCESS_STRAINS, pid)
        self.db.execute_write(sql)

        # Add to areas table
        self.db.execute_write("DELETE FROM {} WHERE area = 1".format(DB_AREAS))
        self.db.execute_write(sql)
        qty = self.db.execute_single(
            "SELECT COUNT(process_id) FROM {} WHERE process_id = {}".format(DB_PROCESS_STRAINS, pid))
        for i in range(1, qty + 1):
            self.db.execute_write("INSERT INTO {} (area, process_id, item) VALUES (1, {}, {})".format(DB_AREAS, pid, i))

            # Deduct seeds from stock
            sid = self.db.execute_single(
                "SELECT strain_id FROM {} WHERE process_id ={} and item = {}".format(DB_PROCESS_STRAINS, pid, i))
            sql = 'UPDATE {} SET qty = qty - 1 WHERE id = {} LIMIT 1'.format(DB_STRAINS, sid)
            self.db.execute_write(sql)

            # update last used
            sql = 'UPDATE {} SET last_used_id = {} WHERE id = {} LIMIT 1'.format(DB_STRAINS, pid, sid)
            self.db.execute_write(sql)

        # Remove any feed info left over for area 1
        sql = 'DELETE FROM {} WHERE area = 1'.format(DB_PROCESS_FEED_ADJUSTMENTS)
        self.db.execute_write(sql)

        self.area_controller.load_areas()
        self.area_controller.load_sensors(1)
        self.area_controller.output_controller.load_outputs(1)
        self.area_controller.load_processes()
        p = self.area_controller.get_area_process(1)
        p.journal_write("Process Number {}".format(p.id))
        p.journal_write("Started   Quantity {} on {}".format(p.quantity, datetime.now().date()))
        s = collections.OrderedDict(sorted(p.strains.items()))
        for i in range(1, p.quantity + 1):
            p.journal_write(
                "  No.{} {}  Id:{}  {} to {} days".format(s[i]['item'], s[i]['name'], s[i]['id'], s[i]['min'],
                                                          s[i]['max']))
        p.journal_write("---------------------------------")

    def coms_indicator(self):
        self.coms_counter += 1
        if self.coms_counter > 6:
            self.coms_counter = 1
        self.lbl_coms_ok.setText('.' * self.coms_counter)

    @pyqtSlot(int)
    def update_access(self, status_code):
        print("Access = ", status_code)
        if self.access.has_status(ACS_DOOR_CLOSED):
            self.lbl_door_lock.setStyleSheet("")
        else:
            self.lbl_door_lock.setStyleSheet("background-color: Red; color: White; border-radius: 6px;")

        if self.access.has_status(ACS_COVER_OPEN):  # Open limit sw
            self.le_access_status_1.setText("<  >")
            # self.lbl_cover_position.setPixmap(QtGui.QPixmap(":/normal/warning.png"))
            self.lbl_cover_lock.setStyleSheet("background-color: red; color: White; border-radius: 6px;")
            self.le_access_status_1.setStyleSheet("background-color: red; color: White; border-radius: 6px;")
            self.pb_cover.setEnabled(False)
            self.pb_cover_close.setEnabled(True)

        if self.access.has_status(ACS_COVER_CLOSED):  # Closed limit sw
            self.le_access_status_1.setStyleSheet("background-color: Green; color: White; border-radius: 6px;")
            # self.lbl_cover_position.setPixmap(QtGui.QPixmap(":/normal/locked.png"))
            self.lbl_cover_lock.setStyleSheet("")
            self.pb_cover_close.setEnabled(False)
            self.pb_cover.setEnabled(True)
        else:  # In open position or somewhere between
            if self.access.has_status(ACS_CLOSING) or self.access.has_status(ACS_OPENING):
                self.lbl_cover_lock.setStyleSheet("background-color: blue; color: White; border-radius: 6px;")
                # self.lbl_cover_position.setPixmap("")
            self.pb_cover.setEnabled(False)
            self.pb_cover_close.setEnabled(True)

        if status_code & ACS_DOOR_LOCKED == ACS_DOOR_LOCKED:
            self.lbl_door_lock.setPixmap(QtGui.QPixmap(":/normal/locked.png"))
        else:
            self.lbl_door_lock.setPixmap(QtGui.QPixmap(":/normal/011-unlock.png"))

        if status_code & ACS_COVER_LOCKED == ACS_COVER_LOCKED:
            self.lbl_cover_lock.setPixmap(QtGui.QPixmap(":/normal/locked.png"))
        else:
            self.lbl_cover_lock.setPixmap(QtGui.QPixmap(":/normal/011-unlock.png"))
            # self.le_access_status_2.setText("Open")
            # self.le_access_status_2.setStyleSheet("background-color: Red; color: White")

        if status_code & ACS_AUTO_SET == ACS_AUTO_SET:
            self.le_access_status_1.setText("Auto")
            self.le_access_status_1.setStyleSheet("background-color: Pink; color: Red")
        elif status_code & ACS_AUTO_ARMED == ACS_AUTO_ARMED:
            self.le_access_status_1.setText("ARMED")
            self.le_access_status_1.setStyleSheet("background-color: Orange; color: Red")

        if status_code & ACS_OPENING == ACS_OPENING and not status_code & ACS_STOPPED == ACS_STOPPED:
            self.access_open_time = _time.time()
            self.le_access_status_1.setStyleSheet("background-color: Yellow; color: Black")
        if status_code & ACS_CLOSING == ACS_CLOSING and \
                not status_code & ACS_STOPPED == ACS_STOPPED:
            self.le_access_status_1.setStyleSheet("background-color: Yellow; color: Black")

    @pyqtSlot(int)
    def update_cover_duration(self, d):
        if d < 0:
            d = ""
        if self.access.has_status(ACS_CLOSING):
            t = ">{}<"
        elif self.access.has_status(ACS_OPENING):
            t = "<{}>"
        else:
            t = ""

        self.le_access_status_1.setText(t.format(d))

    @pyqtSlot(int, int)
    def update_access_inputs(self, _input, _value):
        """
        Handles updates from DE Modules switch inputs
        :param _input:
        :type _input:
        :param _value:
        :type _value:
        :return:
        :rtype:
        """
        if _input == AUD_DOOR:
            if _value == 1:
                pass
                # self.le_door_pos.setStyleSheet("background-color: Green; color: White")
            else:
                self.lbl_door_lock.setStyleSheet("background-color: Red; color: White")
        elif _input == AUD_COVER_OPEN:  # Open limit sw
            if _value == 0:  # Not in open position
                if self.access.cover_closed_sw == 0:
                    self.lbl_cover_lock.setStyleSheet("")
                else:  # In open position
                    self.lbl_cover_lock.setStyleSheet("background-color: blue; color: White")
            else:
                self.lbl_cover_lock.setStyleSheet("background-color: red; color: White")
        elif _input == AUD_COVER_CLOSED:
            if _value == 0:
                self.lbl_cover_lock.setStyleSheet("")
            else:
                if self.access.cover_open_sw == 0:
                    self.lbl_cover_lock.setStyleSheet("background-color: blue; color: White")
                else:
                    self.lbl_cover_lock.setStyleSheet("background-color: red; color: White")
        elif _input == AUD_AUTO_SET:
            pass

    @pyqtSlot(list, name="updateSensors")
    def update_sensors(self, data):
        idx = 1
        try:
            for d in data:
                if idx < 8:     # Humidity and temperature
                    if idx in self.area_controller.sensors.keys():
                        self.area_controller.sensors[idx].update(d)
                else:   # One wire
                    self.area_controller.sensors[idx].update(d)

                idx += 1
        except Exception as e:
            print("Update display error - ", e.args)

    @pyqtSlot(int, int, int, name="updateSwitch")
    def update_switch(self, sw, state, module):
        if module == MODULE_IO or module == MODULE_SL:
            if sw == OUT_LIGHT_1:
                if self.area_controller.area_has_process(1):
                    self.area_controller.reload_area_ranges(1)
                if module == MODULE_SL and state == self.area_controller.light_relay_1:
                    pass
                elif state == 0:
                    self.lbl_light_status_1.setPixmap(QtGui.QPixmap(":/normal/light_off.png"))
                    self.area_controller.day_night[1] = NIGHT
                else:
                    self.area_controller.day_night[1] = DAY
                    self.lbl_light_status_1.setPixmap(QtGui.QPixmap(":/normal/light_on.png"))
                    # self.area_controller.get_area_process(1).check_trans()
                self.area_controller.light_relay_1 = state
                self.area_controller.fan_controller.load_req_temperature(1)
            # else:
            #     if self.area_controller.area_is_manual(1):
            #         self.db.set_config(CFT_AREA, "mode {}".format(1), state + 1)
            if sw == OUT_LIGHT_2:
                self.area_controller.reload_area_ranges(2)
                self.area_controller.light_relay_2 = state
                if state == 0:
                    self.area_controller.day_night[2] = NIGHT
                    self.lbl_light_status_2.setPixmap(QtGui.QPixmap(":/normal/light_off.png"))
                else:
                    self.area_controller.day_night[2] = DAY
                    self.lbl_light_status_2.setPixmap(QtGui.QPixmap(":/normal/light_on.png"))
                self.area_controller.fan_controller.load_req_temperature(2)
                # else:
                #     if self.area_controller.area_is_manual(2):
                #         self.db.set_config(CFT_AREA, "mode {}".format(2), state + 1)
            elif sw == SW_DRY_FAN:
                if state == ON:
                    self.lefanspeed_3.setText("5")
                else:
                    self.lefanspeed_3.setText("0")

    def update_trans(self, area, state):
        if area == 1:
            if state == WARM:
                # Warm
                self.lbl_transition_1.setStyleSheet("background-color: red; border-radius: 3px;")
            elif state == COOL:
                # Cool
                self.lbl_transition_1.setStyleSheet("background-color: blue; border-radius: 3px;")
            else:
                self.lbl_transition_1.setStyleSheet("")

        if area == 2:
            if state == WARM:
                # Warm
                self.lbl_transition_2.setStyleSheet("background-color: red; border-radius: 3px;")
            elif state == COOL:
                # Cool
                self.lbl_transition_2.setStyleSheet("background-color: blue; border-radius: 3px;")
            else:
                self.lbl_transition_2.setStyleSheet("")

    def update_water_required(self):
        self.lbl_water_required.setText(str(self.main_window.water_controller.get_total_required()))

    @pyqtSlot(str, float, name="updatePower")
    def update_power(self, action, val):
        if action == COM_KWH:
            self.le_pwr_total_1.setText(str(val))
            self.le_cost_total.setText(str(round(val * self.unit_price, 2)))
        if action == COM_WATTS:
            if val < 7000:
                self.le_pwr_current.setText(str(val))
                self.le_cost.setText(str(round(val / 1000 * self.unit_price, 2)))

    @pyqtSlot(int, int, name="updateFanSpeed")
    def update_fans(self, fan, speed):
        if fan == 1:
            self.lefanspeed_1.setText(str(speed))
        elif fan == 2:
            self.lefanspeed_2.setText(str(speed))

    @pyqtSlot(str, list, name="updateFeeder_unit")
    def update_from_fu(self, command, data):
        if command == CMD_FU_BOOT:
            self.msg_sys.add("FU Reboot", MSG_FU_BOOT, WARNING)

    @pyqtSlot(int, int, name="updateFloat")
    def update_float(self, tank, pos):
        ctrl = getattr(self, "lbl_float_{}".format(tank))
        if pos == FLOAT_UP:
            ctrl.setPixmap(QPixmap(":/normal/006-flood.png"))
            ctrl.setStyleSheet("background-color: None;")
        else:
            ctrl.setPixmap(QPixmap(":/normal/007-tide.png"))
            ctrl.setStyleSheet("background-color: Yellow; border-radius: 6px;")

    @pyqtSlot(int, int, int)
    def update_fan_mode(self, fan1, fan2, master_power):
        if master_power == OFF:
            if self.area_controller.area_has_process(1):
                self.lefanspeed_1.setStyleSheet("background-color: red; color: White")
                self.lefanspeed_1.setText("")
            if self.area_controller.area_has_process(2):
                self.lefanspeed_2.setStyleSheet("background-color: red; color: White")
                self.lefanspeed_2.setText("")
        else:
            self.lefanspeed_1.setStyleSheet("")
            self.lefanspeed_2.setStyleSheet("")
        for x in range(1, 3):
            if x == 1:
                ctrl = getattr(self, "lbl_fan_mode_1")
                mode = fan1
            else:
                ctrl = getattr(self, "lbl_fan_mode_2")
                mode = fan2

            if mode == 0:
                ctrl.setPixmap(QtGui.QPixmap(":/normal/002-stop.png"))
                if self.area_controller.area_has_process(x):
                    getattr(self, "lefanspeed_{}".format(x)).setStyleSheet("background-color: red; color: White")
            elif mode == 1:
                ctrl.setPixmap(QtGui.QPixmap(":/normal/output_manual_1.png"))
                getattr(self, "lefanspeed_{}".format(x)).setStyleSheet("background-color: lightblue; color: black")
            elif mode == 2:
                ctrl.setPixmap(QtGui.QPixmap(":/normal/output_auto.png"))
                getattr(self, "lefanspeed_{}".format(x)).setStyleSheet("")

    def update_duration_texts(self):
        """ Update the days elapsed and remaining for areas 1 and 2"""
        for a in range(1, 3):
            if self.area_controller.area_has_process(a):
                p = self.area_controller.get_area_process(a)
                ctrl = getattr(self, "le_day_%i" % a)
                ctrl.setText(str(p.stage_days_elapsed))
                ctrl.setToolTip("Days elapsed in current stage")
                ctrl = getattr(self, "le_remaining_%i" % a)
                if p.current_stage == 3:
                    ss = p.strain_shortest - p.stage_days_elapsed
                    if ss < 0:
                        ss = "C"
                    ctrl.setText("{}-{}".format(ss, p.strain_longest -
                                                p.stage_days_elapsed))
                    ctrl.setToolTip("This stage will finish in this range of days")
                else:
                    ctrl.setText(str(p.stage_days_remaining))
                    ctrl.setToolTip("Days remaining in current stage")
                if p.stage_day_adjust < 0:
                    ctrl = getattr(self, "lbl_over_run_%i" % a)
                    ctrl.setText("-{}".format(p.stage_day_adjust))
                    ctrl.setToolTip("Days the current stage has been shortened by")
                elif p.stage_day_adjust > 0:
                    ctrl = getattr(self, "lbl_over_run_%i" % a)
                    ctrl.setText("+{}".format(p.stage_day_adjust))
                    ctrl.setToolTip("Days the current stage has been extended by")
                else:
                    ctrl = getattr(self, "lbl_over_run_%i" % a)
                    ctrl.setText("")
                    ctrl.setToolTip(None)

    @pyqtSlot(list, name="updateOthers")
    def update_others(self, data):
        # print(data)
        try:
            self.lelightlevel_1.setText(str(round((100 / 1024) * int(data[0]), 1)))
            self.lelightlevel_2.setText(str(round((100 / 1024) * int(data[1]), 1)))
            self.update_float(1, int(data[2]))
            self.update_float(2, int(data[3]))
        except Exception as e:
            print("UPDATE OTHERS ERROR ", e.args)

    def new_day(self):
        print("*********** New day ***********")
        self.today = datetime.now().day
        self.mid_day = False
        self.logger.new_day()
        for a in range(1, 3):
            if self.area_controller.area_has_process(a):
                # Advance day in processes
                self.area_controller.get_area_process(a).day_advance()
                self.check_stage(a)
        if self.area_controller.area_has_process(3):
            self.check_stage(3)

        self.feed_controller.new_day()
        # Update next feed dates
        self.update_next_feeds()
        self.update_duration_texts()
        self.area_controller.output_controller.outputs[OUT_WATER_HEATER_1].new_day()
        self.area_controller.output_controller.outputs[OUT_WATER_HEATER_2].new_day()
        self.check_upcoming_starts()
        self.area_controller.max_min_reset_clock()  # Reset max min's that are on clock
        if self.auto_db_backup:
            self.db.backup(1, True)
        # # Reset feeder for new day
        # self.water_control.new_day()

    def new_mid_day(self):
        print("*********** Mid day ***********")
        self.mid_day = True

    @pyqtSlot(str, list, name="updateForHelper")
    def process_relay_command(self, cmd, data):
        """ For outputs use the actual output class and not the controller as it relays the action"""
        if cmd == NWC_SENSOR_RELOAD:
            self.area_controller.reload_area_process_ranges(data[0])
            # self.area_controller.sensors[data[1]].update_status_ctrl()
        elif cmd == NWC_STAGE_ADJUST:
            self.area_controller.get_area_process(data[0]).process_load_stage_info()
            self.area_controller.reload_area(data[0])
            self.feed_controller.reload_area(data[0])
            self.update_duration_texts()
            self.check_stage(data[0])
        elif cmd == NWC_CHANGE_TO_FLUSHING:
            self.check_stage(2)

        elif cmd == NWC_FAN_UPDATE:
            if data[0] == data[1] == 100:
                self.coms_interface.relay_send(NWC_FAN_UPDATE, self.area_controller.fan_controller.get_speed(1),
                                               self.area_controller.fan_controller.get_speed(2))
            else:
                self.update_fans(1, data[0] - 1)  # The -1 is because the master has added 1 for IO
                self.update_fans(2, data[1] - 1)
        elif cmd == NWC_FAN_REQUIRED:
            self.area_controller.fan_controller.set_req_temperature(data[0], data[1])
            print("Fan set point changed by remote")
        elif cmd == NWC_FAN_MODE:
            self.area_controller.fan_controller.set_mode(data[0], data[1])
        elif cmd == NWC_FAN_PID:
            self.area_controller.fan_controller.fans[data[0]].load_pid_values()
            self.area_controller.fan_controller.fans[data[0]].reset()
        elif cmd == NWC_FAN_SPEED:
            self.area_controller.fan_controller.speed_update(data[0], data[1])
        elif cmd == NWC_FAN_SENSOR:
            self.area_controller.fan_controller.set_fan_sensor(data[0], data[1])
        elif cmd == NWC_FEEDER_CONFIG:
            self.main_window.feeder_unit.load_config()
        elif cmd == NWC_FEED_DATE:
            self.feed_controller.feeds[data[0]].load_feed_date()
            self.update_next_feeds()
            self.area_controller.output_controller.water_heater_update_info()
        elif cmd == NWC_FEED_ITEMS:
            self.feed_controller.feeds[data[0]].load_mixes()
        elif cmd == NWC_FEED:
            self.feed_controller.feeds[data[0]].load_feed_date()
            self.area_controller.output_controller.water_heater_update_info()
            self.update_next_feeds()
            self.update_water_required()
        elif cmd == NWC_FINISH_ITEM:
            self.area_controller.reload_area(3)
            self.check_stage(3)

        elif cmd == NWC_MESSAGE:
            self.main_window.msg_sys.load()
        elif cmd == NWC_MOVE_TO_FINISHING:
            self.area_controller.reload_area(2)
            self.area_controller.reload_area(3)
            self.check_stage(2)
            self.check_stage(3)
            self.feed_controller.reload_area(2)

        elif cmd == NWC_NUTRIENTS_AUTO_STIR:
            self.nutrient_auto_stir = int(self.db.get_config(CFT_FEEDER, "auto stir", 6))

        elif cmd == NWC_OUTPUT_SENSOR:
            self.area_controller.output_controller.outputs[data[0]].set_input_sensor(data[1])
        elif cmd == NWC_OUTPUT_MODE:
            self.area_controller.output_controller.outputs[data[0]].set_mode(data[1])
        elif cmd == NWC_OUTPUT_TRIGGER:
            self.area_controller.output_controller.outputs[data[0]].set_detection(data[1])
        elif cmd == NWC_OUTPUT_LOCK:
            self.area_controller.output_controller.outputs[data[0]].update_locked(data[1])
        elif cmd == NWC_OUTPUT_RANGE:
            self.area_controller.output_controller.reload_range(data[0])

        elif cmd == NWC_PROCESS_MIX_CHANGE:
            self.main_window.feed_controller.reload_area(data[0])

        elif cmd == NWC_RELOAD_PROCESSES:
            self.area_controller.load_processes()
            self.update_duration_texts()
            self.check_stage(1)
            self.check_stage(2)

        elif cmd == NWC_SOIL_LOAD:
            self.area_controller.soil_sensors.load()
        elif cmd == NWC_STOCK_TOTAL:
            self.main_window.update_stock()
        elif cmd == NWC_SWITCH_REQUEST:
            self.get_switch_position(data[0])

        elif cmd == NWC_WATER_REQUIRED:
            pass
        elif cmd == NWC_WH_DURATION:
            self.area_controller.output_controller.outputs[data[0]].set_duration(data[1])
        elif cmd == NWC_WH_FREQUENCY:
            self.area_controller.output_controller.water_heater_set_frequency(data[0], data[1])
        elif cmd == NWC_WORKSHOP_RANGES:
            self.area_controller.output_controller.outputs[OUT_HEATER_ROOM].load_ranges()
        elif cmd == NWC_WORKSHOP_DURATION:
            self.area_controller.output_controller.outputs[OUT_HEATER_ROOM].set_duration()
        elif cmd == NWC_WORKSHOP_FROST:
            self.area_controller.output_controller.outputs[OUT_HEATER_ROOM].change_frost(data[0])
        elif cmd == NWC_WORKSHOP_BOOST:
            self.area_controller.output_controller.outputs[OUT_HEATER_ROOM].auto_boost = data[0]
            self.area_controller.output_controller.outputs[OUT_HEATER_ROOM].update_info()

        elif cmd == NWC_FEEDER_STATUS:
            pass  # Calibrate
        elif cmd == NWC_SWITCH_TIMED:
            pass  # Calibrate

    def get_switch_position(self, sw):
        if sw == 0:
            self.coms_interface.relay_send(NWC_SWITCH, sw, self.area_controller.light_relay_1)
        elif sw == 1:
            self.coms_interface.relay_send(NWC_SWITCH, sw, self.area_controller.light_relay_2)
        else:
            self.coms_interface.relay_send(NWC_SWITCH, sw,
                                           self.area_controller.output_controller.get_actual_position(sw))
