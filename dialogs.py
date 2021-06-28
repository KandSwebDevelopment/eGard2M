from datetime import *

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QDialog, QMdiSubWindow

# from main_panel import MainPanel
from defines import *
from ui.dialogFeedMix import Ui_DialogFeedMix
from ui.area_manual import Ui_frm_area_manual
from ui.dialogJournal import Ui_DialogJournal


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
        # for x in range(1, 9):
        #     getattr(self, "ck_fed_%i" % (x + 10)).clicked.connect(self.change_qty)
        #
        # self.cb_nutrients_1.addItem("", 0)
        # for n in self.feed_control.nutrients:
        #     self.cb_nutrients_1.addItem(self.feed_control.nutrients[n], n)
        #
        # self.tw_mixes.setStyleSheet("""QTabBar::tab:selected {background: green}""")
        # # self.lbl_info.setToolTip("Next")
        # self.lbl_next.installEventFilter(self)
        # if self.area > 0:
        #     self.load(self.area)

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
        for x in range(1, feed_data["qty actual"] + 1):
            getattr(self, "ck_fed_%i" % (x + 10)).blockSignals(True)
            if x in feed_data["mixes"][self.mix_number]['items']:
                getattr(self, "ck_fed_%i" % (x + 10)).setChecked(True)
            else:
                getattr(self, "ck_fed_%i" % (x + 10)).setChecked(False)
            getattr(self, "ck_fed_%i" % (x + 10)).blockSignals(False)
            self.check_included(x)
        for xx in range(x + 1, 9):
            getattr(self, "ck_fed_%i" % (xx + 10)).blockSignals(True)
            getattr(self, "ck_fed_%i" % (xx + 10)).setChecked(False)
            getattr(self, "ck_fed_%i" % (xx + 10)).setEnabled(False)
            getattr(self, "ck_fed_%i" % (xx + 10)).blockSignals(False)

        # Set number of feeds combo
        self.cb_feeds.blockSignals(True)
        self.cb_feeds.clear()
        for x in range(1, self.feed_control.max_feeds_till_change(self.area) + 1):
            self.cb_feeds.addItem(str(x), x)
        idx = self.cb_feeds.findData(self.feed_control.area_data[self.area]['mixes'][self.mix_number]['cycles'])
        self.cb_feeds.setCurrentIndex(idx)
        self.cb_feeds.blockSignals(False)

        self._load()

    def pre_close(self):
        # if self.is_changed:
        #     self.my_parent.coms_interface.relay_send(NWC_PROCESS_MIX_CHANGE, self.location)
        self.sub.close()


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
