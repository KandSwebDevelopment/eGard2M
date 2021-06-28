from datetime import *
from time import strftime

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QObject, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMdiSubWindow

from controller_windows import WindowsController
from defines import *
from dialogs import DialogFeedMix, DialogAreaManual
from functions import get_last_friday
from functions_colors import get_css_colours
from ui.main import Ui_Form


def show_main(p):
    w = MainPanel(p)
    w.ControlBox = False
    w.TopLevel = True
    sub = p.mdiArea.addSubWindow(w)
    w.show()


class MainPanel(QMdiSubWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.my_parent = args[0]
        self.db = args[0].db
        self.sub = self.my_parent.mdiArea.addSubWindow(self)
        self.wc = self.my_parent.wc
        self.mode = self.my_parent.mode
        # self.sub.setMinimumSize(1600, 1200)
        self.sub.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        # sub.setFixedSize(sub.width(), sub.height())
        self.setGeometry(0, 0, self.width(), 900)
        self.my_parent.resize(self.width(), 900)
        self.show()
        # sub.show()
        self.le_stage_1.installEventFilter(self)
        self.area_controller = None
        self.feed_controller = None
        self.coms_interface = None
        self.logger = None
        self.ck_auto_boost.setChecked(int(self.db.get_config(CFT_ACCESS, "auto boost", 1)))
        self.stage_change_warning_days = int(self.db.get_config(CFT_PROCESS, "stage change days", 7))

        self.timer_counter = 0
        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.recurring_timer)
        self.loop_15_flag = True  # To give every other loop 15

        # self.timer.start()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if source is self.le_stage_1:
                self.wc.show(DialogAreaManual(self, 1))
            if source is self.le_stage_2:
                self.wc.show(DialogAreaManual(self, 2))
        return QWidget.eventFilter(self, source, event)

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
        self.le_Clock.setText(strftime("%H" + ":" + "%M" + ":" + "%S"))
        self.le_date.setText(strftime("%a" + " " + "%d" + " " + "%b"))

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

    def connect_to_main(self):
        self.area_controller = self.my_parent.area_controller
        self.feed_controller = self.my_parent.feed_controller
        self.coms_interface = self.my_parent.coms_interface
        self.logger = self.my_parent.logger
        self.connect_signals()

    def connect_signals(self):
        self.pbjournal_1.clicked.connect(lambda: self.wc.show_journal(1))
        self.pbjournal_2.clicked.connect(lambda: self.wc.show_journal(2))
        self.pbjournal_3.clicked.connect(lambda: self.wc.show_journal(3))
        self.pb_man_feed_1.clicked.connect(lambda: self.feed_manual(1))
        self.pb_man_feed_2.clicked.connect(lambda: self.feed_manual(2))
        self.pb_feed_mix_1.clicked.connect(lambda: self.wc.show(DialogFeedMix(self, 1)))
        self.pb_feed_mix_2.clicked.connect(lambda: self.wc.show(DialogFeedMix(self, 2)))
        self.b1.clicked.connect(self.test)

        self.coms_interface.update_sensors.connect(self.update_sensors)
        self.coms_interface.update_switch.connect(self.update_switch)

    def test(self):
        print(self.my_parent.mdiArea.subWindowList())
        self.my_parent.mdiArea.cascadeSubWindows()

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
            if status >= 0:
                if self.mode == MASTER:
                    self.coms_interface.send_switch(SW_LIGHT_1, status)
            self.area_controller.load_sensors(1)

        if self.area_controller.area_has_process(2):
            status = self.area_controller.get_area_process(2).check_light()
            if status >= 0:
                if self.mode == MASTER:
                    self.coms_interface.send_switch(SW_LIGHT_2, status)
            self.area_controller.load_sensors(2)

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
        if module == MODULE_IO:
            if sw == OUT_LIGHT_1:
                if state == 0:
                    self.lbl_light_status_1.setPixmap(QtGui.QPixmap(":/normal/light_off.png"))
                else:
                    self.lbl_light_status_1.setPixmap(QtGui.QPixmap(":/normal/light_on.png"))
                if self.area_controller.area_is_manual(1):
                    self.db.set_config(CFT_AREA, "mode {}".format(1), state + 1)
            if sw == OUT_LIGHT_2:
                if state == 0:
                    self.lbl_light_status_2.setPixmap(QtGui.QPixmap(":/normal/light_off.png"))
                else:
                    self.lbl_light_status_2.setPixmap(QtGui.QPixmap(":/normal/light_on.png"))
                if self.area_controller.area_is_manual(2):
                    self.db.set_config(CFT_AREA, "mode {}".format(2), state + 1)
