import collections
from datetime import timedelta, datetime

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty, QDate
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QComboBox, QWizard, QMessageBox

from defines import *
# from eGard import MainWindow as Mw


class MagicWizard(QtWidgets.QWizard):
    def __init__(self, parent):
        """

        @type parent: Mw
        """
        super(MagicWizard, self).__init__(parent)
        uic.loadUi("ui/w_new_process.ui", self)
        self.my_parent = parent
        # self.setOptions(QWizard.IndependentPages)
        self.page1 = Page1(self)
        self.page2 = Page2(self)
        self.page3 = Page3(self)
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.addPage(self.page3)
        self.page1.new_qty()
        # self.page1 = self.addPage(Page1(self))
        self.setStartId(0)
        # func = lambda: self.page2.lb_qty.setText(self.page1.field('myField'))
        self.button(QWizard.NextButton).clicked.connect(self.process_next)
        self.button(QWizard.FinishButton).clicked.connect(self.save)
        self.page1.cb_qty.currentIndexChanged.connect(self.new_qty)
        self.show()
        # self.resize(480, 480)
        # Vars
        self.qty = 1
        self.strains = collections.defaultdict()
        self.pattern = 0
        self.longest = 0    # The number of days for longest flowering
        self.shortest = 0
        self.total_days = 0     # Total days for process
        self.edit_id = 0        # Id of process to edit
        self.running = 0
        self.location = 0
        self.start = ""
        self.end = ""
        self.pattern = 0
        self.stage = 0
        self.feed_mode = 0

        self.page3.setUpdatesEnabled(False)
        self.page3.de_start.setDate(QDate.currentDate())
        rows = self.my_parent.db.execute('SELECT `name`, `id` FROM {} ORDER BY `name`'.format(DB_PATTERN_NAMES))
        self.page3.cb_patterns.addItem("Select", 0)
        for row in rows:
            self.page3.cb_patterns.addItem(row[0], row[1])
        self.page3.setUpdatesEnabled(True)

        if self.my_parent.process_is_at_location(1):
            end = self.my_parent.process_from_location(1).end
            self.earliest_start = end - timedelta(weeks=10)
        else:
            self.earliest_start = datetime.now()
    # def nextId(self):
    #     print("WWW ")

    def new_qty(self):
        self.qty = int(self.page1.cb_qty.currentText())

    def process_next(self):
        print(self.currentId())

    def max_day(self):
        s = ""
        for x in self.strains:
            s += str(self.strains[x]) + ", "
        s = s[:len(s) - 2]      # Remove last comma
        sql = 'SELECT MAX(duration_max) FROM {} WHERE id IN ({})'.format(DB_STRAINS, s)
        row = self.my_parent.db.execute_single(sql)
        self.longest = row
        sql = 'SELECT MIN(duration_min) FROM {} WHERE id IN ({})'.format(DB_STRAINS, s)
        row = self.my_parent.db.execute_single(sql)
        print(row)
        self.shortest = row
        return self.longest

    def save(self):
        print("Finish")
        if self.edit_id == 0:
            sql = 'INSERT INTO {} (running, location, start, end, pattern, stage, qty, feed_mode) VALUES({}, {}, "{}",' \
                  ' "{}", {}, {}, {}, {})'.\
                format(DB_PROCESS, self.running, self.location, self.start, self.end, self.pattern, self.stage,
                       self.qty, self.feed_mode)
            self.my_parent.db.execute_write(sql)
            self.edit_id = self.my_parent.db.execute_single('SELECT LAST_INSERT_ID()')
            # Enter strains in the process strains table
            for x in range(1, self.qty + 1):
                sid = getattr(self.page2, "cb_strain_%i" % x).currentData()
                sql = 'INSERT INTO {} (process_id, item, strain_id) VALUES ({}, {}, {})'.\
                    format(DB_PROCESS_STRAINS, self.edit_id, x, sid)
                self.my_parent.db.execute_write(sql)
                # Deduct from stock - NOT until it is started
        else:
            sql = 'UPDATE {} SET running = {}, location = {}, start = "{}", end = "{}", pattern = {}, stage = {}, ' \
                  'qty = {}, feed_mode = {} WHERE id = {}'.\
                format(DB_PROCESS, self.running, self.location, self.start, self.end, self.pattern, self.stage,
                       self.qty, self.feed_mode, self.edit_id)
            self.my_parent.db.execute_write(sql)
            for x in range(1, self.qty + 1):
                sql = 'UPDATE {} SET strain_id = {} WHERE process_id = {} AND item = {}'.\
                    format(DB_PROCESS_STRAINS, getattr(self.page2, "cb_strain_%i" % x).currentData(), self.edit_id, x)
                self.my_parent.db.execute_write(sql)
        self.my_parent.update_info_texts()

    def start_process(self):
        self.my_parent.start_new_process(self.edit_id)

# #############################################################################################################


class Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.my_parent = parent
        uic.loadUi("ui/wp1_new_process.ui", self)
        self.registerField("my_qty", self.cb_qty, self.cb_qty.currentText(), self.cb_qty.currentIndexChanged)
        # self.registerField('myField',
        #                    self.lineEdit,
        #                    self.lineEdit.text(),
        #                    self.lineEdit.textChanged)
        self.cb_qty.currentIndexChanged.connect(self.new_qty)
        self.cb_edit_id.currentIndexChanged.connect(self.edit_id_change)
        self.next_id = 0

    def edit_id_change(self):
        self.my_parent.edit_id = int(self.cb_edit_id.currentData())
        if self.my_parent.edit_id == 0:
            self.le_id.setText(str(self.next_id))
            self.cb_qty.setCurrentIndex(0)
            self.cb_location.setCurrentIndex(0)
            self.cb_stage.setCurrentIndex(0)
            return
        self.le_id.setText("N/A")
        rows = self.my_parent.my_parent.db.execute_one_row("SELECT id, running, location, start, end, pattern, "
                                                           "stage, qty, feed_mode  FROM {} WHERE id = {}".
                                                           format(DB_PROCESS, self.my_parent.edit_id))
        self.my_parent.running = rows[1]
        self.my_parent.location = rows[2]
        self.my_parent.start = rows[3]
        self.my_parent.end = rows[4]
        self.my_parent.pattern = rows[5]
        self.my_parent.stage = rows[6]
        self.my_parent.qty = rows[7]
        self.my_parent.feed_mode = rows[8]

        self._new_qty()

        # Quantity
        index = self.cb_qty.findText(str(rows[7]), QtCore.Qt.MatchFixedString)
        if index >= 0:
            # self.cb_qty.blockSignals(True)
            self.cb_qty.setCurrentIndex(index)
            # self.cb_qty.blockSignals(False)
        # stage
        index = self.cb_stage.findData(rows[6])
        if index >= 0:
            self.cb_stage.blockSignals(True)
            self.cb_stage.setCurrentIndex(index)
            self.cb_stage.blockSignals(False)
        # location
        index = self.cb_location.findText(str(rows[2]), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.cb_location.blockSignals(True)
            self.cb_location.setCurrentIndex(index)
            self.cb_location.blockSignals(False)

        # Start
        # x = (datetime.now().date() - self.my_parent.start).days
        self.my_parent.page3.de_start.setDate(rows[3])
        # if x >= 5:
        if self.my_parent.running == 1:
            self.my_parent.page3.de_start.setEnabled(False)
        else:
            self.my_parent.page3.de_start.setEnabled(True)

        # Strains
        rows = self.my_parent.my_parent.db.execute("SELECT item, strain_id  FROM {} WHERE process_id = {}".
                                                   format(DB_PROCESS_STRAINS, self.my_parent.edit_id))
        if len(rows) > 0:
            for row in rows:
                ctrl = getattr(self.my_parent.page2, "cb_strain_%i" % row[0])
                index = ctrl.findData(row[1])
                if index >= 0:
                    ctrl.setCurrentIndex(index)
                    # if x >= 14:
                    if self.my_parent.running == 1:
                        ctrl.setEnabled(False)
                    else:
                        ctrl.setEnabled(True)

        # pattern
        index = self.my_parent.page3.cb_patterns.findData(self.my_parent.pattern)
        if index >= 0:
            # self.my_parent.page3.cb_patterns.blockSignals(True)
            self.my_parent.page3.cb_patterns.setCurrentIndex(index)
            # self.my_parent.page3.cb_patterns.blockSignals(False)

    def new_qty(self):
        self.my_parent.qty = int(self.cb_qty.currentText())
        self._new_qty()

    def _new_qty(self):
        rows = self.my_parent.my_parent.db.execute('SELECT `name`, `breeder`, id, qty FROM {} WHERE qty > 0 ORDER BY `name`'.
                                                   format(DB_STRAINS))
        for i in range(1, 9):
            ctrl = getattr(self.my_parent.page2, "cb_strain_%i" % i)
            ctrl.clear()
            if i > self.my_parent.qty:
                ctrl.setEnabled(False)
            else:
                ctrl.addItem("Select", 0)
                ctrl.setEnabled(True)
                for row in rows:
                    ctrl.addItem("{} x {} ({})".format(row[3], row[0], row[1]), row[2])

    def initializePage(self) -> None:
        rows = self.my_parent.my_parent.db.execute_one_row("SELECT MAX(id) FROM processes")
        if rows[0] is None:
            self.le_id.setText("1")
            self.next_id = 1
        else:
            self.le_id.setText(str(rows[0] + 1))
            self.next_id = rows[0] + 1
        rows = self.my_parent.my_parent.db.execute("SELECT id FROM {} WHERE running = 1 OR location = 0".
                                                   format(DB_PROCESS))
        self.cb_edit_id.blockSignals(True)
        self.cb_edit_id.addItem("N/A", 0)
        for row in rows:
            self.cb_edit_id.addItem("{}".format(row[0]), row[0])
        self.cb_edit_id.blockSignals(False)
        rows = self.my_parent.my_parent.db.execute('SELECT `name`, id FROM {} ORDER BY `id`'.format(DB_STAGE_NAMES))
        self.cb_stage.addItem("Not Started", 0)
        for row in rows:
            self.cb_stage.addItem(row[0], row[1])
        self.cb_stage.addItem("Finished", 50)
        self.cb_location.addItem("Not Started", 0)
        for row in range(1, 4):
            self.cb_location.addItem(str(row), row)
        self.cb_location.addItem("Finished", 50)

# #############################################################################################################


class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        uic.loadUi("ui/wp2_new_process.ui", self)
        self.my_parent = parent

    def validatePage(self) -> bool:
        for i in range(1, self.my_parent.qty + 1):
            ctrl = getattr(self, "cb_strain_%i" % i)
            self.my_parent.strains[i] = ctrl.currentData()
            if ctrl.currentData() < 1:
                for ii in range(i, self.my_parent.qty + 1):
                    self.my_parent.strains[ii] = 0
                return False
        print(self.my_parent.strains)
        if self.my_parent.page3.cb_patterns.currentIndex() != 0:
            self.my_parent.page3.new_pattern()
        return True

# ##############################################################################################################


class Page3(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        uic.loadUi("ui/wp3_new_process.ui", self)
        self.my_parent = parent
        self.cb_patterns.currentIndexChanged.connect(self.pattern_change)
        self.de_start.dateChanged.connect(self.date_change)
        self.pb_start.clicked.connect(lambda: self.my_parent.start_process())
        self.pb_find.clicked.connect(self.find_start)

    def find_start(self):
        self.de_start.setDate(self.my_parent.earliest_start)

    def pattern_change(self):
        cp = self.cb_patterns.currentData()
        if cp != self.my_parent.pattern:
            self.new_pattern()

    def date_change(self):
        self.cal_end()
        self.my_parent.start = datetime.strptime(datetime.strftime(self.de_start.date().toPyDate(), "%d-%m-%y"), "%d-%m-%y")

    def new_pattern(self):
        self.my_parent.pattern = self.cb_patterns.currentData()
        if self.my_parent.pattern is None or self.my_parent.pattern == 0:
            return
        cpt = self.cb_patterns.currentText()
        dur = self.my_parent.my_parent.db.execute_single(
            'SELECT SUM(duration) FROM {} WHERE pid = {}'.format(DB_STAGE_PATTERNS, self.my_parent.pattern))
        self.le_dur.setText(str(dur))
        if cpt.find("Auto Cal") == 0:
            self.frm_auto_cal.show()
            self.le_longest.setText(str(self.my_parent.max_day()))
            self.le_shortest.setText(str(self.my_parent.shortest))
            self.my_parent.total_days = int(dur) + self.my_parent.longest
        else:
            self.frm_auto_cal.hide()
            self.my_parent.longest = 0
            self.my_parent.total_days = int(dur)
        self.le_total.setText(str(self.my_parent.total_days))
        self.cal_end()

    def cal_end(self):
        end_date = datetime.strptime(datetime.strftime(self.de_start.date().toPyDate(), "%d-%m-%y"), "%d-%m-%y")
        end_date = end_date + timedelta(days=self.my_parent.total_days)
        self.le_end_date.setText(datetime.strftime(end_date, "%d/%m/%Y"))
        self.my_parent.end = end_date

    def initializePage(self):
        if self.my_parent.running == 1:
            self.pb_start.setEnabled(False)
            self.pb_end.setEnabled(True)
        else:
            self.pb_start.setEnabled(True)
            self.pb_end.setEnabled(False)

    # def isCommitPage(self) -> bool:
    #     print("Finish")
