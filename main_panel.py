import collections
from datetime import *
from time import strftime
import time as _time

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMdiSubWindow

from class_fan import FanController
from class_soil_sensors import SoilSensorClass
from defines import *
from dialogs import DialogFeedMix, DialogAreaManual, DialogAccessModule, DialogFan, DialogOutputSettings, \
    DialogSensorSettings
from scales_com import ScalesComs
from ui.main import Ui_Form


class MainPanel(QMdiSubWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.my_parent = args[0]
        self.db = args[0].db
        self.sub = self.my_parent.mdiArea.addSubWindow(self)
        self.wc = self.my_parent.wc
        self.master_mode = self.my_parent.master_mode
        # self.sub.setMinimumSize(1600, 1200)
        self.sub.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        # sub.setFixedSize(sub.width(), sub.height())
        self.setGeometry(0, 0, self.width(), 900)
        self.my_parent.resize(self.width(), 900)
        self.show()

        self.le_stage_1.installEventFilter(self)
        self.le_stage_2.installEventFilter(self)
        self.le_stage_3.installEventFilter(self)
        self.lbl_access_2.installEventFilter(self)
        self.lbl_fan_1.installEventFilter(self)
        self.lbl_fan_2.installEventFilter(self)

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
        for x in range(0, 13):
            getattr(self, "tesstatus_%i" % x).viewport().setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.today = datetime.now().day  # Holds today's date. Used to detect when day changes

        self.area_controller = None
        self.feed_controller = None
        self.coms_interface = None
        self.access = None
        self.logger = None
        self.soil_sensors = None
        self.msg_sys = None
        self.ck_auto_boost.setChecked(int(self.db.get_config(CFT_ACCESS, "auto boost", 1)))
        self.stage_change_warning_days = int(self.db.get_config(CFT_PROCESS, "stage change days", 7))
        self.unit_price = float(self.db.get_config(CFT_ACCESS, "unit price", 20)) / 100

        self.slave_counter = 0
        self.access_open_time = 0  # Timestamp when cover was opened
        self.timer_counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.loop_15_flag = True  # To give every other loop 15

        self.ck_auto_boost.setChecked(int(self.db.get_config(CFT_ACCESS, "auto boost", 1)))

        self.has_scales = int(self.db.get_config(CFT_MODULES, "ss unit", 0))
        self.scales = ScalesComs(self)
        if not self.has_scales:
            self.panel_9.hide()
            self.my_parent.actionCounter.setEnabled(False)
            self.my_parent.actionInternal.setEnabled(False)
            self.my_parent.actionScales.setEnabled(False)
            self.my_parent.actionStorage.setEnabled(False)
            self.my_parent.actionReconciliation.setEnabled(False)
            self.my_parent.actionLoading.setEnabled(False)

    def eventFilter(self, source, event):
        # Remember to install event filter for control first
        # print("Event ", event.type())
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if source is self.le_stage_1:
                self.wc.show(DialogAreaManual(self, 1))
            elif source is self.le_stage_2:
                self.wc.show(DialogAreaManual(self, 2))
            elif source is self.le_stage_3:
                self.wc.show(DialogAreaManual(self, 3))
            elif source is self.lbl_access_2:
                self.wc.show(DialogAccessModule(self))
            elif source is self.lbl_fan_1:
                self.wc.show(DialogFan(self, 1))
            elif source is self.lbl_fan_2:
                self.wc.show(DialogFan(self, 2))
            # Area 1
            elif source is self.tesstatus_2.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 3))
            elif source is self.tesstatus_3.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 4))
            elif source is self.tesstatus_4.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 10))
            elif source is self.tesstatus_5.viewport():
                self.wc.show(DialogSensorSettings(self, 1, 11))
            # Area 2
            elif source is self.tesstatus_6.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 5))
            elif source is self.tesstatus_7.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 6))
            elif source is self.tesstatus_8.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 12))
            elif source is self.tesstatus_9.viewport():
                self.wc.show(DialogSensorSettings(self, 2, 13))
            # Area 3
            elif source is self.tesstatus_11.viewport():
                self.wc.show(DialogSensorSettings(self, 3, 1))
            elif source is self.tesstatus_12.viewport():
                self.wc.show(DialogSensorSettings(self, 3, 2))
            # Area 3
            elif source is self.tesstatus_10.viewport():
                self.wc.show(DialogSensorSettings(self, 4, 1))

        return QWidget.eventFilter(self, source, event)

    def recurring_timer(self):
        self.loop_1()
        self.timer_counter += 1
        if self.timer_counter > 360:
            self.timer_counter = 1

        # Every 60
        if self.timer_counter % 60 == 0:
            self.loop_5()

        # Every 10
        if self.timer_counter % 10 == 0:
            self.loop_3()
            return

        # Only do following every 2nd time
        if self.timer_counter % 2 == 0:
            self.loop_2()
            return

    def loop_1(self):  # 1 sec
        # print("Current data", self.current_data)
        self.le_Clock.setText(strftime("%H" + ":" + "%M" + ":" + "%S"))
        self.le_date.setText(strftime("%a" + " " + "%d" + " " + "%b"))

    def loop_2(self):  # 2 sec
        if self.master_mode == MASTER:
            self.coms_interface.send_command(NWC_SENSOR_READ)
        self.check_light()
        # if self.master_mode == MASTER:
        #     if self.process_is_at_location(1):
        #         if not self.fans[1].isRunning():
        #             self.lefanspeed_1.setStyleSheet("background-color: red; color: yellow")
        #     if self.process_is_at_location(2):
        #         if not self.fans[2].isRunning():
        #             self.lefanspeed_2.setStyleSheet("background-color: red; color: yellow")
        # if self.master_mode == SLAVE:
        #     self.slave_counter += 1
        #     if self.slave_counter > 6:
        #         self.msg_sys.add("Master/Slave Data link lost", MSG_DATA_LINK, CRITICAL, persistent=1)

    def loop_3(self):  # 10 sec
        if self.master_mode == MASTER:
            self.coms_interface.send_command(NWC_SOIL_READ)
            self.coms_interface.send_command(COM_OTHER_READINGS)
            self.coms_interface.send_data(COM_WATTS, False, MODULE_DE)
            self.coms_interface.send_data(COM_READ_KWH, False, MODULE_DE)

    def loop_5(self):  # 60 secs
        # if NWC_SOIL_READ in self.current_data:
        #     self.logger.save_log(NWC_SOIL_READ + " " + self.current_data[NWC_SOIL_READ])
        # if NWC_US_READ in self.current_data:
        #     self.logger.save_log(NWC_US_READ + self.current_data[NWC_US_READ])
        self.update_next_feeds()
        # Check for new day
        if datetime.now().day != self.today:
            self.new_day()
        self.db.execute("select name from " + DB_NUTRIENTS_NAMES)  # This is only to keep the database connection alive

    def connect_to_main_window(self):
        self.area_controller = self.my_parent.area_controller
        self.feed_controller = self.my_parent.feed_controller
        self.coms_interface = self.my_parent.coms_interface
        self.logger = self.my_parent.logger
        self.access = self.my_parent.access
        self.msg_sys = self.my_parent.msg_sys
        self.connect_signals()

        if self.has_scales:     # These have to be here to allow signals to connect
            self.scales.connect()
        self.update_duration_texts()

    def connect_signals(self):
        self.pb_cover.clicked.connect(lambda: self.access.open())
        self.pb_cover_close.clicked.connect(lambda: self.access.close_cover())
        self.b1.clicked.connect(self.test)

        # Area 1
        self.pbjournal_1.clicked.connect(lambda: self.wc.show_journal(1))
        self.pb_man_feed_1.clicked.connect(lambda: self.feed_manual(1))
        self.pb_feed_mix_1.clicked.connect(lambda: self.wc.show(DialogFeedMix(self, 1)))
        self.pbinfo_1.clicked.connect(lambda: self.wc.show_process_info(1))
        self.pb_advance_1.clicked.connect(lambda: self.stage_adjust(1, -1))
        self.pb_hold_1.clicked.connect(lambda: self.stage_adjust(1, 1))
        self.pb_output_status_1.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_11))
        self.pb_output_status_2.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_12))
        self.pb_output_status_3.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_AREA_1))
        self.pb_output_status_9.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_SPARE_1))
        self.pb_output_mode_1.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 1)))
        self.pb_output_mode_2.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 2)))
        self.pb_output_mode_3.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 3)))
        self.pb_output_mode_9.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 1, 4)))
        # Area 2
        self.pbjournal_2.clicked.connect(lambda: self.wc.show_journal(2))
        self.pb_man_feed_2.clicked.connect(lambda: self.feed_manual(2))
        self.pb_feed_mix_2.clicked.connect(lambda: self.wc.show(DialogFeedMix(self, 2)))
        self.pbinfo_2.clicked.connect(lambda: self.wc.show_process_info(2))
        self.pb_output_status_4.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_21))
        self.pb_output_status_5.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_22))
        self.pb_output_status_6.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_AREA_2))
        self.pb_output_status_10.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_SPARE_2))
        self.pb_output_mode_4.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 1)))
        self.pb_output_mode_5.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 2)))
        self.pb_output_mode_6.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 3)))
        self.pb_output_mode_10.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 2, 4)))
        # Area 3
        self.pbjournal_3.clicked.connect(lambda: self.wc.show_journal(3))
        self.pbinfo_3.clicked.connect(lambda: self.wc.show_process_info(3))
        self.pb_output_status_7.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_31))
        self.pb_output_mode_7.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 3, 1)))
        # Workshop
        self.pb_output_status_8.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_HEATER_ROOM))
        self.pb_output_mode_8.clicked.connect(lambda: self.wc.show(DialogOutputSettings(self, 4, 1)))
        # Water
        self.pb_output_status_11.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_WATER_HEATER_1))
        self.pb_output_status_12.clicked.connect(lambda: self.area_controller.output_controller.switch_output(OUT_WATER_HEATER_2))

        self.coms_interface.update_sensors.connect(self.update_sensors)
        self.coms_interface.update_switch.connect(self.update_switch)
        self.access.update_access.connect(self.update_access)
        self.access.update_duration.connect(self.update_cover_duration)
        self.coms_interface.update_power.connect(self.update_power)
        self.coms_interface.update_other_readings.connect(self.update_others)
        self.area_controller.soil_sensors.update_soil_reading.connect(self.update_soil_display)
        self.coms_interface.update_fan_speed.connect(self.update_fans)
        self.coms_interface.update_float_switch.connect(self.update_float)
        self.coms_interface.update_from_relay.connect(self.process_relay_command)

    def test(self):
        print(self.my_parent.mdiArea.subWindowList())
        # self.my_parent.mdiArea.cascadeSubWindows()

    def update_next_feeds(self):
        """
        This updates the all feeding information for both areas
        :return: None
        :rtype: None
        """
        for loc in range(1, 3):
            if not self.area_controller.area_has_process(loc):  # Has area a process
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
                css = "background-color: green;  color: black; border-radius: 6px;"
            elif days == 1:
                # txt = " Tomorrow"
                ctrl.setPixmap(QPixmap(":/normal/tomorrow.png"))
                ctrl.setToolTip("Feed due today")
                css = ""
            elif days == -1:
                # txt = "Yesterday"
                ctrl.setPixmap(QPixmap(":/normal/yesterday.png"))
                ctrl.setToolTip("Feed due yesterday")
                css = "background-color: red;  color: white; border-radius: 6px;"
            # elif days < -1:
            #     txt = "-{} Days".format(days)
            #     css = "background-color: red;  color: white;"
            else:
                ctrl.setPixmap(QPixmap(":/normal/tomorrow.png"))
                css = ""
            ctrl.setStyleSheet(css)
            if days >= 1:
                ctrl.setToolTip("Feed due in {} day{}".format(days, "" if days == 1 else "s"))
                getattr(self, "lbl_days_%i" % loc).setText(str(days))
            elif days <= -1:
                ctrl.setToolTip("Feed due in {} day{}".format(days, "" if days == 1 else "s"))
                getattr(self, "lbl_days_%i" % loc).setText(str(days))
            else:
                getattr(self, "lbl_days_%i" % loc).setText("")

            getattr(self, "lbl_feed_mixes_%i" % loc).setText(str(self.feed_controller.feeds[loc].get_mix_count()))

            ctrl = getattr(self, "lbl_feed_status_%i" % loc)
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

            ctrl = getattr(self, 'lbl_feed_days_%i' % loc)
            ctrl.setText("{}".format(self.feed_controller.feeds[loc].frequency))
            ctrl = getattr(self, 'lbl_feed_remaining_%i' % loc)
            ctrl.setText("{}".format(self.feed_controller.feeds[loc].get_recipe_days_remaining()))
            ctrl.setToolTip("Number of days the current recipe will be used for<br>Or {} feeds".
                            format(self.feed_controller.feeds[loc].get_feeds_remaining()))

            # ctrl = getattr(self, "lblsp_%i_1" % loc)
            # text = "Not Set"
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

    def check_stage(self, location):
        if self.area_controller.get_area_process(location) == 0:
            return
            # next_stage_days = None
        else:
            next_stage_days = self.area_controller.get_area_process(location).stage_days_remaining
            if location == 1:
                if next_stage_days <= self.stage_change_warning_days:
                    self.frmstagechange_1.setEnabled(True)
                    ctrl = self.pbstageadvance_1
                    ctrl_le = self.lestageinfo_1
                    ctrl_advance = self.pb_advance_1
                    # self.process_from_location(1)
                    ctrl_le.setText(str(next_stage_days))    # + day + str(
                    if next_stage_days > 1:
                        ctrl_advance.setEnabled(True)
                        ctrl.setEnabled(False)
                        ctrl_le.setStyleSheet("background-color: white;  color: black;")
                    elif next_stage_days == 0:
                        ctrl_advance.setEnabled(False)
                        ctrl.setEnabled(True)
                        ctrl_le.setStyleSheet("background-color: light green;  color: black;")
                    elif next_stage_days < 0:
                        ctrl.setEnabled(False)
                        ctrl_le.setStyleSheet("background-color: red;  color: white;")
                        ctrl_advance.setEnabled(False)
                else:
                    self.frmstagechange_1.setEnabled(False)

            elif location == 2:
                p = self.area_controller.get_area_process(location)
                if p.stage_days_elapsed >= p.strain_shortest - 7:
                    self.frmstagechange_2.setEnabled(True)
                    x = 1
                    p.check_stage()
                    for w in p.strain_window:
                        ctrl = getattr(self, "pb_pm_%i" % x)
                        ctrl.setText(str(x))
                        if w == -1:     # Item removed
                            ctrl.setText("")
                            ctrl.setEnabled(False)
                            ctrl.setToolTip("")
                            continue
                        flush_start = self.db.execute_single("SELECT start FROM {} WHERE item = {}".format(DB_FLUSHING, x))
                        if flush_start is None:
                            if p.strain_location[x - 1] != location:
                                ctrl.setText("")
                            if p.strain_location[x - 1] != location or w == 0:
                                ctrl.setEnabled(False)
                                ctrl.setToolTip("")
                            elif w == 1:
                                ctrl.setEnabled(True)
                                ctrl.setStyleSheet("background-color: Yellow;")
                                name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                              "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                              .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                                ctrl.setToolTip(name)
                            elif w == 2:
                                ctrl.setEnabled(True)
                                ctrl.setStyleSheet("background-color: Green;")
                                name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                              "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                              .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                                ctrl.setToolTip(name)
                            elif w == 3:
                                ctrl.setEnabled(True)
                                ctrl.setStyleSheet("background-color: Orange;")
                                name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                              "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                              .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                                ctrl.setToolTip(name)
                        else:   # Item is flushing
                            ctrl.setEnabled(True)
                            ctrl.setStyleSheet("background-color: DodgerBlue;")
                            name = self.db.execute_single("SELECT s.name FROM {} s INNER JOIN {} ps ON s.id = "
                                                          "ps.strain_id AND ps.process_id = {} AND ps.item = {}"
                                                          .format(DB_STRAINS, DB_PROCESS_STRAINS, p.id, x))
                            df = (datetime.now().date() - flush_start).days + 1
                            ctrl.setToolTip("Day {} flushing\n\r{}".format(df, name))

                        x += 1
                    for x in range(len(p.strain_window) + 1, 9):
                        ctrl = getattr(self, "pb_pm_%i" % x)
                        ctrl.setEnabled(False)
                        ctrl.setText("")
            else:
                self.frmstagechange_2.setEnabled(False)
                return None

    def feed_manual(self, loc):
        self.feed_controller.feed(loc)
        # self.update_next_feeds()
        # self.coms_interface.relay_send(NWC_FEED, loc)

    def check_light(self):
        if self.area_controller.area_has_process(1):
            status = self.area_controller.get_area_process(1).check_light()
            if self.area_controller.light_relay_1 != status:
                if self.master_mode == MASTER:
                    self.coms_interface.send_switch(SW_LIGHT_1, status)
                else:
                    self.coms_interface.relay_send(NWC_SWITCH_REQUEST, SW_LIGHT_1)

        if self.area_controller.area_has_process(2):
            status = self.area_controller.get_area_process(2).check_light()
            if self.area_controller.light_relay_2 != status:
                if self.master_mode == MASTER:
                    self.coms_interface.send_switch(SW_LIGHT_2, status)
                else:
                    self.coms_interface.relay_send(NWC_SWITCH_REQUEST, SW_LIGHT_2)

    def stage_advance(self, area):
        # Advances the the process to the next stage
        if self.area_controller.area_has_process(area):
            self.area_controller.get_area_process(area).advance_stage()
            self.update_duration_texts()
            self.check_stage(area)
            self.coms_interface.relay_send(NWC_RELOAD_PROCESSES)

    def stage_adjust(self, area, val):
        # Adjusts the current stage by val days for process in location
        if not self.area_controller.area_has_process(area):
            return
        p = self.area_controller.get_area_process(area)
        current_stage = p.current_stage
        p.adjust_stage_days(val)
        if p.current_stage is not current_stage:
            self.area_controller.display_stage_icon(area)
        # self.area_controller.display_stage_icon(area)
        self.update_duration_texts()
        self.check_stage(area)
        self.coms_interface.relay_send(NWC_STAGE_ADJUST)

    @pyqtSlot(int)
    def update_access(self, status_code):
        print("Access = ", status_code)
        if self.access.has_status(ACS_DOOR_CLOSED):
            self.le_door_pos.setStyleSheet("background-color: Green; color: White")
        else:
            self.le_door_pos.setStyleSheet("background-color: Red; color: White")

        if self.access.has_status(ACS_COVER_OPEN):  # Open limit sw
            self.le_access_status_1.setText("Open")
            self.le_cover_pos_2.setStyleSheet("background-color: red; color: White")
            self.le_access_status_1.setStyleSheet("background-color: red; color: White")
            self.pb_cover.setEnabled(False)
            self.pb_cover_close.setEnabled(True)

        if self.access.has_status(ACS_COVER_CLOSED):    # Closed limit sw
            self.le_cover_pos_2.setStyleSheet("background-color: green; color: White")
            self.le_access_status_1.setStyleSheet("background-color: Green; color: White")
            self.le_access_status_1.setText("Closed")
            self.pb_cover_close.setEnabled(False)
            self.pb_cover.setEnabled(True)
        else:  # In open position or somewhere between
            if self.access.has_status(ACS_CLOSING) or self.access.has_status(ACS_OPENING):
                self.le_cover_pos_2.setStyleSheet("background-color: blue; color: White")
                self.le_access_status_1.setText("Closing")
            self.pb_cover.setEnabled(False)
            self.pb_cover_close.setEnabled(True)

        if status_code & ACS_DOOR_LOCKED == ACS_DOOR_LOCKED:
            self.le_access_status_3.setText("Locked")
            self.le_access_status_3.setStyleSheet("background-color: Green; color: White")
        else:
            self.le_access_status_3.setText("Open")
            self.le_access_status_3.setStyleSheet("background-color: Red; color: White")

        if status_code & ACS_COVER_LOCKED == ACS_COVER_LOCKED:
            self.le_access_status_2.setText("Locked")
            self.le_access_status_2.setStyleSheet("background-color: Green; color: White")
        else:
            self.le_access_status_2.setText("Open")
            self.le_access_status_2.setStyleSheet("background-color: Red; color: White")

        if status_code & ACS_AUTO_SET == ACS_AUTO_SET:
            self.le_access_status_1.setText("Auto")
            self.le_access_status_1.setStyleSheet("background-color: Pink; color: Red")
        elif status_code & ACS_AUTO_ARMED == ACS_AUTO_ARMED:
            self.le_access_status_1.setText("ARMED")
            self.le_access_status_1.setStyleSheet("background-color: Orange; color: Red")

        if status_code & ACS_OPENING == ACS_OPENING and not status_code & ACS_STOPPED == ACS_STOPPED:
            self.le_access_status_1.setText("Opening")
            self.le_cover_duration.show()
            self.access_open_time = _time.time()
            # self.pb_cover_rev.hide()
            self.le_access_status_1.setStyleSheet("background-color: Yellow; color: Black")
        if status_code & ACS_CLOSING == ACS_CLOSING and \
                not status_code & ACS_STOPPED == ACS_STOPPED:
            self.le_access_status_1.setText("Closing")
            self.le_cover_duration.show()
            # self.pb_cover_rev.hide()
            self.le_access_status_1.setStyleSheet("background-color: Yellow; color: Black")
        # elif status_code & ACS_COVER_LOCKED == ACS_COVER_LOCKED:
        #     self.le_access_status_1.setText("Closed")
        #     self.access_open_time = 0
        #     self.pb_cover.setText("Open")
        #     self.le_cover_duration.hide()
        #     self.le_access_status_1.setStyleSheet("background-color: Green; color: White")
        # elif status_code & ACS_STOPPED == ACS_STOPPED:
        #     if status_code & ACS_OPENING == ACS_OPENING:
        #         self.le_access_status_1.setText("Stopped O")
        #         self.pb_cover.setText("Open")
        #         self.pb_cover_rev.setText("Close")
        #     else:
        #         self.le_access_status_1.setText("Stopped C")
        #         self.pb_cover.setText("Close")
        #         self.pb_cover_rev.setText("Open")
        #     self.pb_cover_rev.show()
        #     self.le_cover_duration.show()
        #     self.le_access_status_1.setStyleSheet("background-color: Yellow; color: Black")
        # else:
        #     self.le_access_status_1.setText("Open")
        #     if self.access_open_time == 0:
        #         self.access_open_time = _time.time()
        #     self.le_cover_duration.hide()
        #     self.le_access_status_1.setStyleSheet("background-color: Red; color: White")

    @pyqtSlot(int)
    def update_cover_duration(self, d):
        if d < 0:
            d = ""
        self.le_cover_duration.setText(str(d))

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
                self.le_door_pos.setStyleSheet("background-color: Green; color: White")
            else:
                self.le_door_pos.setStyleSheet("background-color: Red; color: White")
        elif _input == AUD_COVER_OPEN:  # Open limit sw
            if _value == 0:  # Not in open position
                if self.access.cover_closed_sw == 0:
                    self.le_cover_pos_2.setStyleSheet("background-color: green; color: White")
                else:  # In open position
                    self.le_cover_pos_2.setStyleSheet("background-color: blue; color: White")
            else:
                self.le_cover_pos_2.setStyleSheet("background-color: red; color: White")
        elif _input == AUD_COVER_CLOSED:
            if _value == 0:
                self.le_cover_pos_2.setStyleSheet("background-color: Green; color: White")
            else:
                if self.access.cover_open_sw == 0:
                    self.le_cover_pos_2.setStyleSheet("background-color: blue; color: White")
                else:
                    self.le_cover_pos_2.setStyleSheet("background-color: red; color: White")
        elif _input == AUD_AUTO_SET:
            pass

    @pyqtSlot(list, name="updateSoil")
    def update_soil_display(self, lst):
        try:
            self.le_avg_soil_1.setText(str(lst[8]))
            self.le_avg_soil_2.setText(str(lst[9]))
            for a in range(1, 3):
                for c in range(1, 5):
                    idx = ((a - 1) * 4) + c
                    if int(lst[idx - 1]) > 1020:
                        getattr(self, "le_soil_{}_{}".format(a, c)).setText("--")
                    else:
                        getattr(self, "le_soil_{}_{}".format(a, c)).setText(lst[idx - 1])
        except Exception as e:
            print("Update soil display - ", e.args)

    @pyqtSlot(list, name="updateSensors")
    def update_sensors(self, data):
        idx = 1
        try:
            for d in data:
                if idx in self.area_controller.sensors.keys():
                    self.area_controller.sensors[idx].update(d)
                idx += 1
            # print("Data in ", self.current_data)
        except Exception as e:
            print("Update display error - ", e.args)

    @pyqtSlot(int, int, int, name="updateSwitch")
    def update_switch(self, sw, state, module):
        if module == MODULE_IO or module == MODULE_SL:
            if sw == OUT_LIGHT_1:
                if state == 0:
                    self.lbl_light_status_1.setPixmap(QtGui.QPixmap(":/normal/light_off.png"))
                    self.area_controller.light_relay_1 = state
                else:
                    self.lbl_light_status_1.setPixmap(QtGui.QPixmap(":/normal/light_on.png"))
                    self.area_controller.light_relay_1 = state
                if self.area_controller.area_is_manual(1):
                    self.db.set_config(CFT_AREA, "mode {}".format(1), state + 1)
            if sw == OUT_LIGHT_2:
                if state == 0:
                    self.lbl_light_status_2.setPixmap(QtGui.QPixmap(":/normal/light_off.png"))
                    self.area_controller.light_relay_2 = state
                else:
                    self.lbl_light_status_2.setPixmap(QtGui.QPixmap(":/normal/light_on.png"))
                    self.area_controller.light_relay_2 = state
                if self.area_controller.area_is_manual(2):
                    self.db.set_config(CFT_AREA, "mode {}".format(2), state + 1)

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

    @pyqtSlot(int, int, name="updateFloat")
    def update_float(self, tank, pos):
        ctrl = getattr(self, "lbl_float_{}".format(tank))
        if pos == FLOAT_UP:
            ctrl.setPixmap(QPixmap(":/normal/006-flood.png"))
            ctrl.setStyleSheet("background-color: None;")
        else:
            ctrl.setPixmap(QPixmap(":/normal/007-tide.png"))
            ctrl.setStyleSheet("background-color: Yellow; border-radius: 6px;")

    def update_fan_mode(self, fan, mode):
        if fan == 1:
            ctrl = self.lbl_fan_mode_1
        else:
            ctrl = self.lbl_fan_mode_2
        if mode == 0:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/002-stop.png"))
            ctrl.setStyleSheet("background-color: red; color: White")
        elif mode == 1:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/output_manual_1.png"))
            ctrl.setStyleSheet("background-color: lightblue; color: White")
        elif mode == 2:
            ctrl.setPixmap(QtGui.QPixmap(":/normal/output_auto.png"))
            ctrl.setStyleSheet("")

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
            # self.outputs[OP_W_HEATER_1].float_update(int(data[2]), int(data[3]))
            self.update_float(2, int(data[3]))
        except Exception as e:
            print("UPDATE OTHERS ERROR ", e.args)

    def new_day(self):
        print("*********** New day ***********")
        self.today = datetime.now().day
        # if self.master_mode == MASTER:
        #     self.logger.new_day()
        # self.outputs[OP_W_HEATER_1].new_day()
        # self.outputs[OP_W_HEATER_2].new_day()
        for a in range(1, 4):
            if self.area_controller.area_has_process(a):
                # Advance day in processes
                p = self.area_controller.get_area_process(a)
                p.day_advance()
                self.check_stage(a)
                # if p.is_feed_due_today():
                #     self.feed_today = True
        self.feed_controller.new_day()
        # Update next feed dates
        self.update_next_feeds()
        self.update_duration_texts()
        # # Reset feeder for new day
        # self.water_control.new_day()
        # self.water_control.start()

    @pyqtSlot(str, list, name="updateForHelper")
    def process_relay_command(self, cmd, data):
        if cmd == NWC_SENSOR_RELOAD:
            if self.area_controller.area_has_process(data[0]):
                self.area_controller.get_area_process(data[0]).load_active_temperature_ranges()
            else:
                # No process, load defaults
                pass
        elif cmd == NWC_STAGE_ADJUST:

        elif cmd == NWC_OUTPUT_MODE:
            self.area_controller.output_controller.outputs[data[0]].set_mode(data[1])
        elif cmd == NWC_FAN_SENSOR:
            self.area_controller.fans[data[0]].reload_sensor(data[1])
        elif cmd == NWC_OUTPUT_RANGE:
            self.area_controller.output_controller.outputs[data[0]].load_profile()
        elif cmd == NWC_RELOAD_PROCESSES:
            self.area_controller.load_processes()
            self.update_duration_texts()
            self.check_stage(1)
            self.check_stage(2)
        elif cmd == NWC_SWITCH_REQUEST:
            self.get_switch_position(data[0])

    def get_switch_position(self, sw):
        if sw == 0:
            self.coms_interface.relay_send(NWC_SWITCH, sw, self.area_controller.light_relay_1)
        elif sw == 1:
            self.coms_interface.relay_send(NWC_SWITCH, sw, self.area_controller.light_relay_2)
        else:
            self.coms_interface.relay_send(NWC_SWITCH, sw, self.area_controller.output_controller.get_actual_position(sw))
