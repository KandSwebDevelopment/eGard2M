import collections
from datetime import *

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QDialog, QMdiSubWindow, QMessageBox, QListWidgetItem

from class_process import ProcessClass
from defines import *
from functions import string_to_float
from ui.dialogAccess import Ui_DialogDEmodule
from ui.dialogEngineerCommandSender import Ui_DialogEngineerCommandSender
from ui.dialogEngineerIO import Ui_DialogMessage
from ui.dialogFeedMix import Ui_DialogFeedMix
from ui.area_manual import Ui_frm_area_manual
from ui.dialogJournal import Ui_DialogJournal
from ui.dialogProcessInfo import Ui_DialogProcessInfo


class DialogFeedMix(QWidget, Ui_DialogFeedMix):

    def __init__(self, parent, area=0):

        super(DialogFeedMix, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setupUi(self)
        self.my_parent = parent
        self.sub = None
        # self.sub = self.my_parent.my_parent.mdiArea.addSubWindow(self)
        # # self.sub.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        # self.sub.setFixedSize(440, 640)
        # self.sub.setGeometry(0, 0, 440, 640)
        # self.show()
        self.db = self.my_parent.db
        self.le_ml_1.setFixedWidth(30)
        self.feed_control = parent.feed_controller
        self.area = area  # Current area
        self.mix_number = 1  # The mix number working on
        self.is_changed = False
        self.show_next = False  # True when next recipe is to be displayed
        self.holding = None  # Holds stylesheet for mouse over event
        self.holding_1 = None  # Holds stylesheet for mouse over event
        # self.lw_recipe_1.doubleClicked.connect(self.load_item)
        # self.pb_store_n_1.clicked.connect(self.store_nutrient)
        # self.le_total_1.editingFinished.connect(self.calculate_each)
        # self.le_each_1.editingFinished.connect(self.calculate_total)
        # self.pb_store_w_1.clicked.connect(self.store_litres)
        # self.cb_feeds.currentIndexChanged.connect(self.change_use_for)
        # self.pb_water_only.clicked.connect(self.water_only)
        # self.pb_add.clicked.connect(self.add_mix_tab)
        self.pb_close.clicked.connect(self.pre_close)
        # self.pb_reset_nutrients.clicked.connect(self.reset_nutrients)
        # self.pb_reset_water.clicked.connect(self.reset_water)
        # self.pb_delete.clicked.connect(self.delete_mix)
        # self.tw_mixes.currentChanged.connect(self.change_mix_tab)
        for x in range(1, 9):
            getattr(self, "ck_fed_%i" % (x + 10)).clicked.connect(self.change_qty)

        self.cb_nutrients_1.addItem("", 0)
        for n in self.feed_control.nutrients:
            self.cb_nutrients_1.addItem(self.feed_control.nutrients[n], n)

        self.tw_mixes.setStyleSheet("""QTabBar::tab:selected {background: green}""")
        # self.lbl_info.setToolTip("Next")
        self.lbl_next.installEventFilter(self)
        if self.area > 0:
            self.load(self.area)

    def eventFilter(self, source, event):
        print("Event ", event.type())
        if event.type() == QtCore.QEvent.Enter and source is self.lbl_next:
            self.holding = self.lw_recipe_1.styleSheet()
            self.holding_1 = self.te_water_1.styleSheet()
            self.lw_recipe_1.setStyleSheet("background-color: LightSalmon;")
            self.te_water_1.setStyleSheet("background-color: LightSalmon;")
            font = QtGui.QFont()
            font.setPointSize(11)
            self.te_water_1.setFont(font)
            self.show_next = True
            self._load()
            # self.display_next_mix()
        if event.type() == QtCore.QEvent.Leave and source is self.lbl_next:
            # self.display_mix(self.mix_number)
            self.lw_recipe_1.setStyleSheet(None)
            self.te_water_1.setStyleSheet("background-color: White;")
            font = QtGui.QFont()
            font.setPointSize(11)
            self.te_water_1.setFont(font)
            self.show_next = False
            self._load()
        return QWidget.eventFilter(self, source, event)

    def load(self, location):
        self.area = location
        self.setWindowTitle("Feed Recipe for Area " + str(location))
        # feed_data = self.feed_control.area_data[location]
        days = self.feed_control.get_recipe_days_remaining(location)
        s = "" if days == 1 else "s"
        fd = self.feed_control.get_feeds_remaining(location)
        fds = "" if fd == 1 else "s"
        self.lbl_info.setText("{} Day{} ({} Feed{}) Remaining".
                              format(days, s, fd, fds))
        rs = self.feed_control.get_recipe_status(location)
        if rs == 1:
            if (self.feed_control.get_next_feed_date(location).date() - datetime.now().date()).days \
                    < self.feed_control.get_feed_frequency(location):
                pass  # Hasn't been feed last feed
            else:
                self.lw_recipe_1.setStyleSheet("background-color: orange;")
                self.lbl_info.setText("The next feed will be using this new recipe")
                self.show_next = True
        if rs == 2:
            self.lw_recipe_1.setStyleSheet("background-color: springgreen;")

        count = self.feed_control.get_mix_count(location)
        for t in range(2, count + 1):
            self.tw_mixes.addTab(QWidget(), "Feed {}".format(t))

        self.display_mix(self.mix_number)

    def display_mix(self, mix_num):
        self.mix_number = mix_num
        feed_data = self.feed_control.feeds[self.area].get_mixes()
        # Set check boxes
        x = 0
        for x in range(1, 9):   # Loop through all check boxes and tick if in items
            getattr(self, "ck_fed_%i" % (x + 10)).blockSignals(True)
            if x in feed_data[self.mix_number]['items']:
                getattr(self, "ck_fed_%i" % (x + 10)).setChecked(True)
                self.check_included(x)
            else:
                getattr(self, "ck_fed_%i" % (x + 10)).setChecked(False)
                getattr(self, "ck_fed_%i" % (x + 10)).setEnabled(False)
            getattr(self, "ck_fed_%i" % (x + 10)).blockSignals(False)

        # Set number of feeds combo
        self.cb_feeds.blockSignals(True)
        self.cb_feeds.clear()
        for x in range(1, self.my_parent.feed_controller.get_feeds_remaining(self.area) + 1):
            self.cb_feeds.addItem(str(x), x)
        idx = self.cb_feeds.findData(self.my_parent.feed_controller.get_feeds_remaining(self.area))
        self.cb_feeds.setCurrentIndex(idx)
        self.cb_feeds.blockSignals(False)

        self._load()

    def _load(self):
        """ Displays the mix and the water """
        feed_data = self.feed_control.feeds[self.area].get_mixes()
        self.lw_recipe_1.clear()
        if self.show_next:
            recipe = self.feed_control.get_next_recipe(self.area)
        else:
            recipe = self.feed_control.get_recipe(self.area, self.mix_number)
        # Loop through recipe
        x = 1  # Just a counter for display
        if recipe == WATER_ONLY_IDX:
            lw_item = QListWidgetItem(str(x) + " Water only")
            v_item = QVariant(WATER_ONLY_IDX)
            lw_item.setData(Qt.UserRole, v_item)
            self.lw_recipe_1.addItem(lw_item)
        else:
            for nid in recipe:      # nid = (nid, mls)
                # ri - 0=nid, 1=ml, 2=L, 3=rid, 4=freq, 5=adj ml, 6=adj remaining
                rs, diff = self.feed_control.recipe_item_status(self.area, self.mix_number, (nid[0], nid[1]))
                if nid[0] == WATER_ONLY_IDX:
                    lw_item = QListWidgetItem(str(x) + " Water only")
                else:
                    if nid[1] == 0:  # mls is 0 show as a no add
                        lw_item = QListWidgetItem(
                            str(x) + "   " + str(nid[1]) + "ml each (" + str(0) + ") x" + str(
                                0) + ".  A total of " + str(
                                round(nid[1] * feed_data[self.mix_number]["water total"], 1)) + "ml of "
                            + self.feed_control.nutrients[nid[0]])
                        lw_item.setBackground(Qt.darkGray)
                    elif rs == 2:
                        # This item is not part of normal recipe
                        lw_item = QListWidgetItem(
                            str(x) + "   " + str(nid[1] + 0) + "ml each.   A total of " +
                            str(round((nid[1] + 0) * feed_data[self.mix_number]["water total"], 1))
                            + "ml of " + self.feed_control.nutrients[nid[0]])
                        lw_item.setBackground(Qt.lightGray)
                    elif rs == 1 and diff != 0:
                        # This item is part of normal recipe but has been altered
                        lw_item = QListWidgetItem(
                            str(x) + "   " + str(nid[1]) + "ml each (" + str(diff) +
                            ")   A total of " + str(
                                round((nid[1] + 0) * feed_data[self.mix_number]["water total"], 1))
                            + "ml of " + self.feed_control.nutrients[nid[0]])
                        lw_item.setBackground(Qt.darkCyan)
                    else:  # Normal recipe item
                        lw_item = QListWidgetItem(str(x) + "   " + str(nid[1]) + "ml each.  A total of " + str(
                            round(nid[1] * feed_data[self.mix_number]["water total"], 1)) + "ml of " +
                                                  self.feed_control.nutrients[nid[0]])

                v_item = QVariant(nid)
                lw_item.setData(Qt.UserRole, v_item)
                self.lw_recipe_1.addItem(lw_item)
                x += 1

        if self.show_next:
            lpp = self.feed_control.get_next_lpp(self.area)
            self.te_water_1.setText(
                "Recommended water " + str(
                    round(lpp * feed_data[self.mix_number]["water total"], 2)) + " which is " +
                str(lpp) + "L each")

        else:
            lpp = self.feed_control.get_lpp(self.area, self.mix_number)
            if self.feed_control.get_lpp_org(self.area) == lpp:
                self.te_water_1.setText(
                    "Recommended water " + str(
                        round(self.feed_control.get_water_total, 2)) + " which is " +
                    str(lpp) + "L each")
            else:
                self.te_water_1.setText("Adjusted water {} which is {}L each. ({}L each)".format(
                    round(self.feed_control.get_water_total(self.area, self.mix_number), 2),
                    lpp, lpp - self.feed_control.get_lpp_org(self.area)))

    def display_next_mix(self):
        """ Displays the next mix and the water """
        feed_data = self.feed_control.feeds[self.area].get_mixes()
        self.lw_recipe_1.clear()
        recipe = self.feed_control.get_next_recipe(self.area)
        # Loop through recipe
        x = 1  # Just a counter for display
        for nid in recipe:
            # ri - 0=nid, 1=ml, 2=L, 3=rid, 4=freq, 5=adj ml, 6=adj remaining
            rs, diff = self.feed_control.recipe_item_status(self.area, self.mix_number, (nid[0], nid[1]))
            if nid[0] == WATER_ONLY_IDX:
                lw_item = QListWidgetItem(str(x) + " Water only")
                v_item = QVariant(WATER_ONLY_IDX)
                lw_item.setData(Qt.UserRole, v_item)
                self.lw_recipe_1.addItem(lw_item)
            else:
                if nid[1] == 0:  # mls is 0 show as a no add
                    lw_item = QListWidgetItem(str(x) + "   " + str(nid[1]) + "ml each (" + str(0) + ") x" + str(
                        0) + ".  A total of " + str(
                        round(nid[1] * feed_data[self.mix_number]["water total"], 1)) + "ml of "
                                              + self.feed_control.nutrients[nid[0]])
                    lw_item.setBackground(Qt.darkGray)
                elif rs == 2:
                    # This item is not part of normal recipe
                    lw_item = QListWidgetItem(
                        str(x) + "   " + str(recipe[nid] + 0) + "ml each.   A total of " +
                        str(round((recipe[nid] + 0) * feed_data['mixes'][self.mix_number]["water total"], 1))
                        + "ml of " + self.feed_control.nutrients[nid])
                    lw_item.setBackground(Qt.lightGray)
                elif rs == 1 and diff != 0:
                    # This item is part of normal recipe but has been altered
                    lw_item = QListWidgetItem(
                        str(x) + "   " + str(recipe[nid]) + "ml each (" + str(round(diff, 1)) +
                        ")   A total of " + str(
                            round((recipe[nid] + 0) * feed_data['mixes'][self.mix_number]["water total"], 1))
                        + "ml of " + self.feed_control.nutrients[nid])
                    lw_item.setBackground(Qt.darkCyan)
                else:  # Normal recipe item
                    lw_item = QListWidgetItem(str(x) + "   " + str(recipe[nid]) + "ml each.  A total of " + str(
                        round(recipe[nid] * feed_data['mixes'][self.mix_number]["water total"], 1)) + "ml of " +
                                              self.feed_control.nutrients[nid])

            v_item = QVariant(nid)
            lw_item.setData(Qt.UserRole, v_item)
            self.lw_recipe_1.addItem(lw_item)
            x += 1

        lpp = feed_data['lpp_next']
        self.te_water_1.setText(
            "Next water " + str(
                round(lpp * feed_data['qty actual'], 2)) + " which is " +
            str(lpp) + "L each")

    def check_included(self, item):
        cf = self.my_parent.feed_controller.check_item_included(self.area, item)
        if cf == 0:
            getattr(self, "ck_fed_%i" % (item + 10)).setStyleSheet("background-color: Yellow;")
        elif cf == 2:
            getattr(self, "ck_fed_%i" % (item + 10)).setStyleSheet("background-color: Blue;")
        elif cf == 1:
            getattr(self, "ck_fed_%i" % (item + 10)).setStyleSheet(None)

    def pre_close(self):
        # if self.is_changed:
        #     self.my_parent.coms_interface.relay_send(NWC_PROCESS_MIX_CHANGE, self.location)
        self.sub.close()

    def change_qty(self):
        count = 0
        items = collections.defaultdict()
        for x in range(1, 9):
            if getattr(self, "ck_fed_%i" % (x + 10)).isChecked():
                count += 1
                items[x] = 1
        self.feed_control.change_items(self.area, self.mix_number, items)

        for x in self.feed_control.get_all_items(self.area):
            self.check_included(x)

        self._load()
        self.is_changed = True


class DialogAreaManual(QWidget, Ui_frm_area_manual):
    my_parent = ...  # type: MainPanel

    def __init__(self, parent, area=0):
        """
        :type parent: MainPanel
        """

        super(DialogAreaManual, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setupUi(self)
        self.my_parent = parent
        self.sub = None
        self.setWindowTitle("Area {} Manual Controls".format(area))
        self.area = area
        self.db = self.my_parent.db
        self.manual = int(self.db.get_config(CFT_AREA, "mode {}".format(area), 0))

        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_manual.clicked.connect(self.manual_click)
        self.pb_light.clicked.connect(self.light_click)
        self.set_buttons()
        self.my_parent.coms_interface.update_switch.connect(self.update_switch)

    @pyqtSlot(int, int, int, name="updateSwitch")
    def update_switch(self, sw, state, module):
        if module == MODULE_IO:
            if sw == OUT_LIGHT_1 or sw == OUT_LIGHT_2:
                if state == 0:
                    self.pb_light.setText("Switch On")
                else:
                    self.pb_light.setText("Switch Off")
        self.manual = int(self.db.get_config(CFT_AREA, "mode {}".format(self.area), 0))

    def manual_click(self):
        if self.manual > 0:
            self.manual = 0
            self.my_parent.coms_interface.send_switch(OUT_LIGHT_1 - 1 + self.area, 0, MODULE_IO)
        else:
            self.manual = 1
        self.db.set_config(CFT_AREA, "mode {}".format(self.area), self.manual)
        self.my_parent.area_controller.load_areas()
        self.my_parent.area_controller.load_sensors(self.area)
        self.set_buttons()

    def light_click(self):
        if self.manual == 0:
            return
        if self.manual == 1:
            self.my_parent.coms_interface.send_switch(OUT_LIGHT_1 - 1 + self.area, 1, MODULE_IO)
        else:
            self.my_parent.coms_interface.send_switch(OUT_LIGHT_1 - 1 + self.area, 0, MODULE_IO)

    def set_buttons(self):
        if self.manual > 0:
            self.pb_manual.setText("Switch Off")
            self.pb_light.setEnabled(True)
        else:
            self.pb_manual.setText("Switch On")
            self.pb_light.setEnabled(False)
        if self.manual > 1:
            self.pb_light.setText("Switch Off")
        else:
            self.pb_light.setText("Switch On")


class DialogJournal(QDialog, Ui_DialogJournal):
    def __init__(self, process, parent):
        super(DialogJournal, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.pbsave.clicked.connect(self.add)
        self.pbclose.clicked.connect(self.close_)
        self.my_parent = parent
        self.process = process
        self.new_line = '\n'

        self.temessage.setText(self.process.journal_read())
        self.stage = self.process.current_stage
        self.days = self.process.stage_days_elapsed
        self.dateTimeEdit.setDateTime(datetime.now())

    def add(self):
        entry = self.tenew.toPlainText()
        if entry == "":
            return
        dt = self.dateTimeEdit.dateTime()
        dt_string = dt.toString(self.dateTimeEdit.displayFormat())
        entry = dt_string + "  Stage:{} Day:{}   ".format(self.stage, self.days) + entry
        self.process.journal_write(entry)

        self.temessage.setText(self.process.journal_read())
        self.my_parent.my_parent.coms_interface.send_command(NWC_JOURNAL_ADD, self.process.location, entry)
        self.tenew.setText("")

    def close_(self):
        self.sub.close()


class DialogEngineerCommandSender(QDialog, Ui_DialogEngineerCommandSender):
    def __init__(self, parent):
        super(DialogEngineerCommandSender, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.my_parent = parent
        self.db = self.my_parent.db
        self.pb_send.clicked.connect(self.send)
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.cb_command.addItem("Manual Entry", "")
        self.cb_command.addItem("Sensor Read", COM_SENSOR_READ)
        self.cb_command.addItem("Soil Read", COM_SOIL_READ)
        self.cb_command.addItem("Other Read", COM_OTHER_READINGS)
        self.cb_command.addItem("Tank Read", COM_US_READ)
        self.cb_command.addItem("Switch", CMD_SWITCH)
        self.cb_command.addItem("Valve", CMD_VALVE)
        self.cb_command.addItem("Valve Cluster", CMD_VALVE_CLUSTER)
        if self.my_parent.mode == MASTER:
            self.cb_to.addItem("Slave", MODULE_SL)
        else:
            self.cb_to.addItem("Master", MODULE_SL)
        self.cb_to.addItem("I/O", MODULE_IO)
        self.cb_to.addItem("D/E", MODULE_DE)
        self.cb_to.addItem("F/U", MODULE_FU)
        # self.cb_to.addItem("NWC", MODULE_NWC)

    def send(self):
        cmd = self.cb_command.currentData()
        manual = False
        if cmd == "":
            cmd = self.lineEdit.text()
            manual = True
        pri = self.ck_priority.isChecked()
        if cmd == COM_SENSOR_READ or cmd == COM_SOIL_READ or cmd == COM_OTHER_READINGS:
            self.my_parent.coms_interface.send_command(cmd)
        v1 = self.le_value_1.text()
        v2 = self.le_value_2.text()
        v3 = self.le_value_3.text()
        v4 = self.le_value_4.text()
        to = self.cb_to.currentData()
        if manual:
            self.send_(cmd, v1, v2, v3, v4, pri, to)
            return
        if cmd == CMD_SWITCH:
            if v1 == "" or v2 == "":
                return
            self.my_parent.coms_interface.send_command(CMD_SWITCH, int(v1), int(v2), pri, to)
        if cmd == CMD_VALVE:
            if v1 == "" or v2 == "":
                return
            if int(v2) > 90:
                return
            self.my_parent.coms_interface.send_command(CMD_VALVE, int(v1), int(v2), pri, to)

    def send_(self, cmd, v1, v2, v3, v4, p, to):
        if v4 != "":
            if to == MODULE_SL:
                self.my_parent.coms_interface.relay_send(cmd, v1, v2, v3, v4)
            else:
                self.my_parent.coms_interface.send_data(cmd, p, to, v1, v2, v3, v4)
            return
        if v3 != "":
            if to == MODULE_SL:
                self.my_parent.coms_interface.relay_send(cmd, v1, v2, v3)
            else:
                self.my_parent.coms_interface.send_data(cmd, p, to, v1, v2, v3)
            return
        if v2 != "":
            if to == MODULE_SL:
                self.my_parent.coms_interface.relay_send(cmd, v1, v2)
            else:
                self.my_parent.coms_interface.send_data(cmd, p, to, v1, v2)
            return
        if v1 != "":
            if to == MODULE_SL:
                self.my_parent.coms_interface.relay_send(cmd, v1)
            else:
                self.my_parent.coms_interface.send_command(cmd, v1, None, p, to)
            return
        if to == MODULE_SL:
            self.my_parent.coms_interface.relay_send(cmd)
        else:
            self.my_parent.coms_interface.send_command(cmd, None, None, p, to)


class DialogEngineerIo(QDialog, Ui_DialogMessage):
    def __init__(self, parent=None):
        """ :type parent: MainWindow """
        super(DialogEngineerIo, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.my_parent = parent
        self.mode = 0
        self.show_m_server = True
        self.show_m_server_out = True
        self.show_m_relay = True
        self.show_m_client = True
        self.show_m_client_to = True
        self.show_io = True
        self.show_io_to = True
        self.show_de = True
        self.show_de_to = True
        self.show_relay = True
        self.show_this_to = True
        self.show_relay_to = True

        self.ckb_io.clicked.connect(self.change_show)
        self.ckb_de.clicked.connect(self.change_show)
        self.ckb_other.clicked.connect(self.change_show)
        self.ckb_this.clicked.connect(self.change_show)
        self.ckb_io_2.clicked.connect(self.change_show)
        self.ckb_de_2.clicked.connect(self.change_show)
        self.ckb_other_2.clicked.connect(self.change_show)
        self.ckb_this_2.clicked.connect(self.change_show)
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_clear.clicked.connect(lambda: self.te_message.clear())

        self.my_parent.coms_interface.update_received.connect(self.raw_update_a)
        self.my_parent.coms_interface.update_cmd_issued.connect(self.outgoing)
        self.setWindowTitle("I/O Data")

    def set_kwargs(self, **kwargs):
        if 'mode' in kwargs.keys():
            self.mode = kwargs['mode']
            self.te_message.append("<p style='background-color: White;'> </p>")
            # self.my_parent.client.update_que.connect(self.raw_update_c)
            # self.my_parent.server.update_received.connect(self.raw_update_b)
            self.resize(500, 700)

        if 'title' in kwargs.keys():
            self.setWindowTitle(kwargs['title'])

    def load(self, message, title):
        self.te_message.setText(message)
        self.setWindowTitle(title)

    def check_show(self, sender) -> bool:
        ip = sender[0]
        port = sender[1]
        if port == self.my_parent.coms_interface.io_port and not self.show_io:
            return False
        if port == self.my_parent.coms_interface.de_port and not self.show_de:
            return False
        if port == self.my_parent.coms_interface.slave_port and not self.show_m_client:
            return False
        if port == self.my_parent.coms_interface.pc_relay_port and not self.show_relay:
            return False
        if port == self.my_parent.coms_interface.this_port and not self.show_m_relay:
            return False
        return True

    def check_outgoing(self, sender) -> bool:
        # ip = sender[0]
        port = sender[1]
        if port == self.my_parent.coms_interface.io_port and not self.show_io_to:
            return False
        if port == self.my_parent.coms_interface.de_port and not self.show_de_to:
            return False
        if port == self.my_parent.coms_interface.slave_port and not self.show_m_client_to:
            return False
            # if port == self.my_parent.coms_interface.this_relay_port and not self.show_relay:
            #     return False
        if port == self.my_parent.coms_interface.pc_relay_port and not self.show_relay_to:
            return False
        if port == self.my_parent.coms_interface.this_port and not self.show_this_to:
            return False
        return True

    def change_show(self):
        if self.ckb_this.isChecked():
            self.show_m_server = True
        else:
            self.show_m_server = False
        if self.ckb_this_2.isChecked():
            self.show_m_server_out = True
        else:
            self.show_m_server = False

        if self.ckb_relay.isChecked():
            self.show_relay = True
        else:
            self.show_relay = False
        if self.ckb_relay_2.isChecked():
            self.show_relay_to = True
        else:
            self.show_relay_to = False

        if self.ckb_other.isChecked():
            self.show_m_client = True
        else:
            self.show_m_client = False
        if self.ckb_other_2.isChecked():
            self.show_m_client_to = True
        else:
            self.show_m_client_to = False

        if self.ckb_io.isChecked():
            self.show_io = True
        else:
            self.show_io = False
        if self.ckb_io_2.isChecked():
            self.show_io_to = True
        else:
            self.show_io_to = False

        if self.ckb_de.isChecked():
            self.show_de = True
        else:
            self.show_de = False
        if self.ckb_de_2.isChecked():
            self.show_de_to = True
        else:
            self.show_de_to = False

    @pyqtSlot(str, tuple)
    def raw_update_a(self, data, sender):
        if self.check_show(sender):
            data = data.replace("<", "")
            data = data.replace(">", "")
            self.te_message.append(
                "<p style='background-color: tan;'>" + str(data) + " (" + str(sender[1]) + ")</p>")

    @pyqtSlot(str, tuple)
    def outgoing(self, data, sender):
        if self.check_outgoing(sender):
            if len(data) > 0:
                data = data.replace('>', '')
                data = data.replace('<', '')
                self.te_message.append(
                    "<p style='background-color: LightSkyBlue;'>" + str(data) + " (" + str(sender) + ")</p>")

    @pyqtSlot(list, list)
    def raw_update_c(self, priorities, commands):
        if len(priorities) > 0:
            self.te_message.append(
                "<p style='background-color: LightGreen;'>P > " + self.split_commands(priorities) + "</p>")
        if len(commands) > 0:
            self.te_message.append(
                "<p style='background-color: Lime;'>C > " + self.split_commands(commands) + "</p>")

    @staticmethod
    def split_commands(data) -> str:
        t = ""
        for x in data:
            # print(x)
            cmd = x['cmd'].replace("<", " ")
            cmd = cmd.replace(">", ", ")
            t += "[" + str(x['client']) + "] " + cmd
        return t


class DialogAccessModule(QDialog, Ui_DialogDEmodule):
    def __init__(self, parent):
        """ :type parent: MainWindow """
        super(DialogAccessModule, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.my_parent = parent
        self.db = self.my_parent.db
        self.watt_dif_org = 0
        self.send_org = 0
        self.pulses_pkw = 0
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_reboot.clicked.connect(self.reboot)
        self.pb_update_freq.clicked.connect(self.update)
        self.pb_update_diff.clicked.connect(self.update_diff)
        self.pb_update_pulses.clicked.connect(self.update_pulses)
        self.pb_scan.clicked.connect(self.re_scan)
        self.p_save.clicked.connect(self.save)
        self.pb_store.clicked.connect(self.store)
        self.pb_query.clicked.connect(self.query)
        self.pb_cover_open.clicked.connect(self.cover_open)
        self.pb_cover_close.clicked.connect(self.cover_close)
        self.pb_door_open.clicked.connect(self.door_open)
        self.pb_door_close.clicked.connect(self.door_lock)
        self.pb_cover_lock.clicked.connect(
            lambda: self.my_parent.coms_interface.send_switch(SW_COVER_LOCK, ON_RELAY, MODULE_DE))
        self.pb_cover_unlock.clicked.connect(
            lambda: self.my_parent.coms_interface.send_switch(SW_COVER_LOCK, OFF_RELAY, MODULE_DE))
        self.le_cover_dur.setText(str(self.my_parent.db.get_config(CFT_ACCESS, "cover time", 30)))
        self.le_auto_delay.setText(str(self.my_parent.db.get_config(CFT_ACCESS, "auto delay", 15)))
        self.le_kwh_total.setText(self.my_parent.le_pwr_total_1.text())

        self.my_parent.coms_interface.update_access_settings.connect(self.setting_received)

        self.my_parent.coms_interface.send_data(COM_SEND_FREQ, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_KWH_DIF, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_KWH, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_PULSES, True, MODULE_DE)

    @pyqtSlot(str, float)
    def setting_received(self, cmd, value):
        if cmd == COM_KWH_DIF:
            self.le_watts.setText(str(value * 1000))
            self.watt_dif_org = value * 1000
        elif cmd == COM_SEND_FREQ:
            self.le_seconds.setText(str(value / 1000))
            self.send_org = value / 1000
        elif cmd == COM_PULSES:
            self.pulses_pkw = int(value)
            self.le_pp_kw.setText(str(self.pulses_pkw))

    def query(self):
        self.my_parent.coms_interface.send_data(COM_COVER_CLOSED, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_COVER_POSITION, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_DOOR_POSITION, True, MODULE_DE)

    def re_scan(self):
        self.my_parent.coms_interface.send_data(COM_SEND_FREQ, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_KWH_DIF, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_PULSES, True, MODULE_DE)

    def cover_open(self):
        self.my_parent.coms_interface.send_switch(SW_COVER_OPEN, ON_RELAY, MODULE_DE)

    def cover_close(self):
        self.my_parent.coms_interface.send_switch(SW_COVER_CLOSE, ON_RELAY, MODULE_DE)

    def door_open(self):
        self.my_parent.coms_interface.send_switch(SW_DOOR_LOCK, OFF_RELAY, MODULE_DE)

    def door_lock(self):
        self.my_parent.coms_interface.send_switch(SW_DOOR_LOCK, ON_RELAY, MODULE_DE)

    def update(self):
        # v = float(self.le_kwh_total.text())
        # if v != self
        v = float(self.le_seconds.text())
        if v != self.send_org:
            self.my_parent.coms_interface.send_data(CMD_SEND_FREQ, False, MODULE_DE, v * 1000)

    def update_diff(self):
        v = string_to_float(self.le_watts.text())
        if v != self.watt_dif_org:
            v /= 1000  # has to be split into 2 ints as network code does not pass floats
            i = int(v)
            d = int((v - i) * 1000)
            self.my_parent.coms_interface.send_data(CMD_KWH_DIF, False, MODULE_DE, i, d)

    def update_pulses(self):
        v = string_to_float(self.le_pp_kw.text())
        if v != self.pulses_pkw:
            self.my_parent.coms_interface.send_data(CMD_SET_PULSES, False, MODULE_DE, int(v))

    def save(self):
        self.my_parent.db.set_config(CFT_ACCESS, "cover time", self.le_cover_dur.text())
        self.my_parent.access.cover_duration = int(self.le_cover_dur.text())
        self.my_parent.db.set_config(CFT_ACCESS, "auto delay", self.le_auto_delay.text())
        self.my_parent.access.auto_close_duration = int(self.le_auto_delay.text())

    def store(self):
        v = string_to_float(self.le_kwh_total.text())
        fp = int(v)
        sp = v - fp  # has to be split into 2 ints as network code does not pass floats
        sp *= 1000
        self.my_parent.coms_interface.send_data(CMD_SET_KWH, False, MODULE_DE, fp, int(sp))

    def reboot(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Confirm you wish to reboot the D/E Module")
        msg.setWindowTitle("Confirm Reboot")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Yes:
            self.my_parent.coms_interface.send_data(CMD_REBOOT, False, MODULE_DE)


class DialogProcessInfo(QDialog, Ui_DialogProcessInfo):
    def __init__(self, parent, process=None):
        super(DialogProcessInfo, self).__init__()
        self.sub = None
        self.my_parent = parent
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.db = self.my_parent.db
        self.pb_close.clicked.connect(lambda: self.sub.close())

        if process is not None:
            self.load(process)

    def load(self, p_class):
        if type(p_class) is not ProcessClass:
            return
        self.lbltitle.setText("Process " + str(p_class.id))
        table = "Day {}, week {} of {} days, {} weeks in stage {} {} {} days remaining<br>".format(
            p_class.stage_days_elapsed, round(p_class.running_days / 7, 1), p_class.stage_total_duration,
            round(p_class.stage_total_duration / 7, 1), p_class.current_stage, p_class.stage_name,
            p_class.stage_days_remaining)
        table += "Started on {} and is due om <b>{}</b> ".format(p_class.start, p_class.due_date)
        table += "It has been running a total of {} days or {} weeks".format(p_class.running_days,
                                                                             round(p_class.running_days / 7, 1))
        self.tetime.setHtml(table)

        # Pattern
        line = '<table cellpadding = "3"  border = "1">'
        for x in range(0, len(p_class.stages)):
            # sn = p_class.get_stage_name(x + 1)
            # for z in range(len(sn), 14):
            #     sn += "&nbsp;"
            line += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                p_class.stages[x][0], p_class.get_stage_name(x + 1),
                p_class.datetime_to_string(p_class.stages_start[x], "%d-%m-%y"), p_class.stages[x][1],
                round(p_class.stages[x][1] / 7, 1), p_class.stages_len_adjustment[x + 1]
            )
            # line = str(p_class.stages[x][0]) + \
            #     " " + sn + p_class.datetime_to_string(p_class.stages_start[x], "%d-%m-%y") + " | " + \
            #     str(p_class.stages[x][1]) + " (" + str(round(p_class.stages[x][1] / 7, 1)) + ") + " + \
            #     str(p_class.stages_len_adjustment[x + 1]) + "<br>"
            # self.teStages.moveCursor(QTextCursor.End)
        line += "</table>"
        self.teStages.textCursor().insertHtml(line)

        # Strains
        sql = 'SELECT strain_id FROM {} WHERE process_id = {} ORDER BY item'.format(DB_PROCESS_STRAINS, p_class.id)
        rows = self.db.execute(sql)
        text = "<table>"
        idx = 1
        for row in rows:
            sql = 'SELECT name, breeder, duration_min, duration_max FROM {} WHERE id = {}'.format(DB_STRAINS, row[0])
            strain = self.db.execute_one_row(sql)
            text += "<tr><td style='padding:0 15px 0 px;'>" + str(idx) + "</td><td style='padding:0 15px 0 px;'>" \
                    + strain[0] + "</td><td style='padding:0 15px 0 px;'>" + strain[
                        1] + "</td><td style='padding:0 15px 0 px;'>" + str(strain[2]) \
                    + "</td><td > To </td><td style='padding:0 15px 0 px;'>" + str(strain[3]) + "</td></tr>"
            idx += 1
        text += "</table>"
        self.te_strains.insertHtml(text)

        # temperatures
        self.teTemperatures.moveCursor(QTextCursor.End)
        temps = p_class.temperature_ranges_active
        if p_class.light_status:
            title = "Day"
            alt = "Night"
            # idx = 1
        else:
            title = "Night"
            alt = "Day"
            # idx = 2
        self.teTemperatures.textCursor().insertHtml("<font size = '4'><b>" + title + "</b><br>")
        if temps is None:
            self.teTemperatures.textCursor().insertHtml("<font size = '5'><b>Temperature schedule is missing</b><br>")
            self.teTemperatures.textCursor().insertHtml("<hr><font size = '4'><b>" + alt + "</b><br>")
        else:
            self.teTemperatures.textCursor().insertHtml(
                "Humidity&nbsp;" + str(temps[1]['low']) + "&deg;  &lt;  <b>" + str(
                    temps[1]['set']) + "&deg;</b>  &gt;  " + str(temps[1]['high']) + "&deg;<br>")
            self.teTemperatures.textCursor().insertHtml(
                "Room&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; " + str(temps[2]['low']) + "&deg;  &lt;  <b>" + str(
                    temps[2]['set']) + "&deg;</b>  &gt;  " + str(temps[2]['high']) + "&deg;<br>")
            if p_class.location != 3:
                self.teTemperatures.textCursor().insertHtml(
                    "Process&nbsp;&nbsp;&nbsp;" + str(temps[3]['low']) + "&deg;  &lt;  <b>" + str(
                        temps[3]['set']) + "&deg;</b>  &gt;  " + str(temps[3]['high']) + "&deg;<br>")
                self.teTemperatures.textCursor().insertHtml(
                    "Core&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; " + str(temps[4]['low']) + "&deg;  &lt;  <b>" + str(
                        temps[4]['set']) + "&deg;</b>  &gt;  " + str(temps[4]['high']) + "&deg;<br>")

            temps = p_class.temperature_ranges_inactive
            if not p_class.light_status:
                title = "Day"
                # alt = "Night"
                # idx = 1
            else:
                title = "Night"
                # alt = "Day"
                # idx = 2
            self.teTemperatures.textCursor().insertHtml("<font size = '4'><b>" + title + "</b><br>")
            self.teTemperatures.textCursor().insertHtml(
                "Humidity&nbsp;" + str(temps[1]['low']) + "&deg;  &lt;  <b>" + str(
                    temps[1]['set']) + "&deg;</b>  &gt;  " + str(temps[1]['high']) + "&deg;<br>")
            self.teTemperatures.textCursor().insertHtml(
                "Room&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; " + str(temps[2]['low']) + "&deg;  &lt;  <b>" + str(
                    temps[2]['set']) + "&deg;</b>  &gt;  " + str(temps[2]['high']) + "&deg;<br>")
            if p_class.location != 3:
                self.teTemperatures.textCursor().insertHtml(
                    "Process&nbsp;&nbsp;&nbsp;" + str(temps[3]['low']) + "&deg;  &lt;  <b>" + str(
                        temps[3]['set']) + "&deg;</b>  &gt;  " + str(temps[3]['high']) + "&deg;<br>")
                self.teTemperatures.textCursor().insertHtml(
                    "Core&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; " + str(temps[4]['low']) + "&deg;  &lt;  <b>" + str(
                        temps[4]['set']) + "&deg;</b>  &gt;  " + str(temps[4]['high']) + "&deg;<br>")

        # Feed
        # if p_class.location != 3:
        #     sql = "SELECT name FROM {} WHERE id = {}".format(DB_FEED_SCHEDULE_NAMES, p_class.current_feed_schedule_id)
        #     fs_name = self.db.execute_single(sql)
        #     if fs_name is not None:
        #         if p_class.recipe_id == WATER_ONLY_IDX:
        #             r_name = WATER_ONLY
        #         else:
        #             sql = "SELECT name FROM {} WHERE id = {}".format(DB_RECIPE_NAMES, p_class.recipe_id)
        #             r_name = self.db.execute_single(sql)
        #             if r_name is None:
        #                 r_name = "Error None"
        #         if p_class.current_feed_schedule_id == 0:
        #             txt = "Error None"
        #         else:
        #             txt = str(p_class.current_feed_schedule_id)
        #         table = "<table cellpadding='3' border='1'><tr><td>Current Feed Schedule</td><td><b>" + fs_name + \
        #                 "</b> [" + txt + "]</td></tr>"
        #         table += "<tr><td>Current Recipe</td><td><b>" + r_name + "</b> [" + str(
        #             p_class.recipe_id) + "]</td></tr>"
        #         table += "<tr><td>Recipe changes on day</td><td><b>" + str(
        #             p_class.recipe_expires_day) + "</b></td></tr>"
        #         if p_class.recipe_next_id == WATER_ONLY_IDX:
        #             r_name = WATER_ONLY
        #         elif p_class.recipe_next_id is None:
        #             r_name = "None"
        #         else:
        #             sql = "SELECT name FROM {} WHERE id = {}".format(DB_RECIPE_NAMES, p_class.recipe_next_id)
        #             r_name = self.db.execute_single(sql)
        #         table += "<tr><td>Next Recipe</td><td><b>" + r_name + "</b> [" + str(
        #             p_class.recipe_next_id) + "]</td></tr>"
        #         table += "<tr><td>Starts in</td><td><b>" + str(
        #             p_class.recipe_expires_day - p_class.stage_days_elapsed) + "</b> days</td></tr>"
        #         table += "</table><br>"
        #         # Today
        #         table += "<table cellpadding='3' border='1'><tr><td colspan='3'>Current Recipe " + str(
        #             p_class.recipe_original[0][2]) + "Litre(s) Each</td></tr>"
        #         table += '<tr><td>Nutrient</td><td>Amount</td><td>Freq</td></tr>'
        #         for row in p_class.recipe_final:
        #             if row[0] == 100:
        #                 table += '<tr><td colspan="3" Font="3">Water Only</td></tr>'
        #                 continue
        #             sql = "SELECT name FROM {} WHERE id = {}".format(DB_NUTRIENTS_NAMES, row[0])
        #             n_name = self.db.execute_single(sql)
        #             colour = ""
        #             if row[5] != 0:
        #                 colour = " bgcolor='light gray'"
        #             table += '<tr><td>' + n_name + '</td><td' + colour + '>' + str(
        #                 row[1] + row[5]) + 'ml</td><td>' + str(
        #                 row[4]) + '</td></tr>'
        #         table += "</table><br><br>"
        #
        #         if len(p_class.recipe_next) > 0:
        #             table += "<table cellpadding='3' border='1'><tr><td colspan='3'>Next Recipe " + str(
        #                 p_class.recipe_next[0][2]) + "Litre(s) Each</td></tr>"
        #             table += '<tr><td>Nutrient</td><td>Amount</td><td>Freq</td></tr>'
        #             for row in p_class.recipe_next:
        #                 if row[3] == 100:
        #                     table += '<tr><td colspan="3" Font="3">Water Only</td></tr>'
        #                     continue
        #                 sql = "SELECT name FROM {} WHERE id = {}".format(DB_NUTRIENTS_NAMES, row[0])
        #                 n_name = self.db.execute_single(sql)
        #                 colour = ""
        #                 if row[5] != 0:
        #                     colour = " bgcolor='#00FF00'"
        #                 table += '<tr><td>' + n_name + '</td><td' + colour + '>' + str(
        #                     row[1] + row[5]) + 'ml</td><td>' + str(
        #                     row[4]) + '</td></tr>'
        #             table += "</table><br><br>"
        #         self.tefeed.textCursor().insertHtml(table)
        #     else:
        #         table = "<table cellpadding='3' border='1'><tr><td>Current Feed Schedule</td><td><b>Missing</b> </td></tr>"
        #         table += "</table><br><br>"
        #         self.tefeed.textCursor().insertHtml(table)

        # Water supply
        table = "<table cellpadding='3' border='1'><tr><td colspan='2'><b>Total</b> Water<br>Requirement </td></tr>"
        table += '<tr><td>Tank</td><td>Litres</td></tr>'
        # table += '<tr><td> 1 </td><td>' + str(self.my_parent.water_supply.tank_required_litres[0]) + '</td></tr>'
        # table += '<tr><td> 2 </td><td>' + str(self.my_parent.water_supply.tank_required_litres[1]) + '</td></tr>'
        # table += '<tr><td> Total </td><td>' + str(self.my_parent.feed_control.get_next_water_required()) + '</td></tr>'
        table += "</table>"
        self.tewater.textCursor().insertHtml(table)

        # Outputs
        s = ""
        table = "<table cellpadding='3' border='1'><tr><td>Output</td><td>Mode</td><td>Sensor</td><td>Range</td></tr>"
        rows = self.db.execute(
            'SELECT `name`, `type`, `input`, `range` FROM {} WHERE `area` = {}'.format(DB_OUTPUTS, p_class.location))
        for row in rows:
            if row[3] == 'NULL':
                # t = ""
                pass
            else:
                pass
                # t = row[3]
            if row[2] == -1:
                tt = "None"
            else:
                tt = self.db.execute_single("SELECT `name` FROM {} WHERE `id` = {}".format(DB_SENSORS_CONFIG, row[2]))
                s = self.my_parent.area_controller.sensors[row[2]]
            table += "<tr><td>{}</td><td>{}</td><td>{}<br>Low:{}  Set:{}  High:{}</td><td>{}</td></tr>" \
                .format(row[0], OUT_TYPE[row[1]], tt, s.low, s.set, s.high, row[3])
        table += "</table>"
        self.teoutputs.setHtml(table)





