import collections
from datetime import *

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QListWidgetItem

from class_process import ProcessClass
from defines import *
from plotter import *
from ui.dialogDispatchCounter import Ui_DialogDispatchCounter
from ui.dialogDispatchInternal import Ui_DialogDispatchInternal
from functions import string_to_float, m_box, play_sound, auto_capital
from ui.dialogAccess import Ui_DialogDEmodule
from ui.dialogDispatchOverview import Ui_DialogLogistics
from ui.dialogDispatchReports import Ui_DialogDispatchReport
from ui.dialogDispatchStorage import Ui_Form
from ui.dialogEngineerCommandSender import Ui_DialogEngineerCommandSender
from ui.dialogEngineerIO import Ui_DialogMessage
from ui.dialogFan import Ui_DialogFan
from ui.dialogFeedMix import Ui_DialogFeedMix
from ui.area_manual import Ui_frm_area_manual
from ui.dialogJournal import Ui_DialogJournal
from ui.dialogOutputSettings import Ui_DialogOutputSetting
from ui.dialogProcessAdjustments import Ui_DialogProcessAdjust
from ui.dialogProcessInfo import Ui_DialogProcessInfo
from ui.dialogSensorSettings import Ui_DialogSensorSettings
from ui.dialogStrainFinder import Ui_DialogStrainFinder


class DialogDispatchCounter(QWidget, Ui_DialogDispatchCounter):
    def __init__(self, parent=None):
        """ :type parent: MainWindow """
        super(DialogDispatchCounter, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.my_parent = parent
        self.db = parent.db
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())

        self.scales = parent.scales
        self.logger = parent.logger
        self.client = None
        self.jar = None
        self.reading = 0
        self.weight_required = 0
        self.display_factor = 1
        self.is_reading = False
        self.is_finished = True
        self.has_vessel = True
        self.strain_id = 0
        self.strain_name = ""
        self.ppg = string_to_float(self.db.get_config(CFT_DISPATCH, "ppg", 10))
        self.progress_color = "Black"
        self.zero_count = 1
        self.gross = 0
        self.factor = 1
        self.amount = 0
        self.has_got = False  # Set true when bar turns green so if you lift off it warns
        self.frame.setStyleSheet("background-color: Yellow;")
        self.frame_2.setStyleSheet("background-color: Red;")
        self.le_progress.setStyleSheet("background-color: White")
        self.l_marker_1.setStyleSheet("background-color: Orange;")
        self.l_marker_2.setStyleSheet("background-color: Salmon;")
        self.l_marker_3.setStyleSheet("background-color: Black;")
        self.l_marker_4.setStyleSheet("background-color: Black;")
        self.l_marker_last.setStyleSheet("background-color: Black;")

        self.cb_jar.currentIndexChanged.connect(self.change_jar)
        self.cb_client.currentIndexChanged.connect(self.change_client)
        self.pb_start.clicked.connect(self.start)
        self.pb_cancel.clicked.connect(self.cancel)
        self.pb_tare.clicked.connect(self.tare)

        self.scales.new_reading_p.connect(self.update_reading)
        self.scales.update_status_p.connect(self.update_status)
        self.scales.new_uid.connect(self.new_uid)

        rows = self.db.execute("SELECT jar, strain FROM {} WHERE weight - nett > 5 AND location = 0"
                               " ORDER BY jar".format(DB_JARS))
        self.cb_jar.blockSignals(True)
        self.cb_jar.addItem("Select", "000")
        for row in rows:
            strain = ""
            if row[1] > 0:
                strain = self.db.execute_single("SELECT name FROM {} WHERE id = {}".format(DB_STRAINS, row[1]))
            self.cb_jar.addItem("{} - {}".format(row[0], strain), row[0])
        self.cb_jar.blockSignals(False)

        rows = self.db.execute("SELECT name, id FROM {} ORDER BY sort_order".format(DB_CLIENTS))
        self.cb_client.blockSignals(True)
        self.cb_client.addItem("Select", "000")
        for row in rows:
            self.cb_client.addItem(row[0], row[1])
        self.cb_client.blockSignals(False)
        self.pb_start.setEnabled(False)

        self.cb_type.addItem("Select", 0)
        self.cb_type.addItem("CA", 1)  # Cash
        self.cb_type.addItem("BT", 2)  # Bank
        self.cb_type.addItem("CR", 3)  # Credit
        self.cb_type.addItem("FR", 4)  # Foc
        self.cb_type.addItem("PP", 5)  # Personal party
        self.cb_type.addItem("OP", 6)  # Other forms

        w = self.frame.size().width()
        tw = int((w / 100) * 75)
        self.frame_2.move(tw, 0)
        self.frame_2.resize(w - tw, 75)
        self.le_amount.installEventFilter(self)

        self.font = QtGui.QFont()
        self.font.setPointSize(13)
        self.connect()
        self.position_markers()
        self.le_amount.returnPressed.connect(self.enter_pressed)

    def eventFilter(self, source, event):
        # print("Event ", event.type())
        if event.type() == QtCore.QEvent.FocusOut and source is self.le_amount:
            self.check_start()
            self.check_enough()
            return False
        return False

    @pyqtSlot(str, name='updateReadingP')
    def update_reading(self, value):
        value = string_to_float(value)
        if self.has_got >= 3 and value < self.weight_required / 2:
            self.has_got = 0
            play_sound(SND_CHECK_OUT_ERROR)
            print(m_box("Warning", "This has not been checked out\n\rReplace vessel and check out before removing", 64))
            return
        # Remove any text from progress
        if (self.is_finished and value < 1) or (not self.has_vessel and value >= -0.15):
            self.le_progress.setText("")
            self.is_finished = False
            self.has_vessel = True
            self.check_start()
        # Is vessel removed
        if value < -2.00 and self.has_vessel:
            self.le_progress.setText("Replace vessel")
            self.has_vessel = False
            self.check_start()
        # Only proceed is actually weighing
        if not self.is_reading:
            return
        self.reading = value
        v = value * self.display_factor
        if value > self.weight_required - 0.15:
            self.pb_start.setEnabled(True)
            self.progress_color = "Green"
            self.has_got += 1
        else:
            self.pb_start.setEnabled(False)
            self.progress_color = "Black"
        self.update_display(v)

    @pyqtSlot(str, name='updateStatusP')
    def update_status(self, status):
        if status == "tare":
            if self.zero_count == 0:
                self.le_progress.setText("Zero scale 2 of 2.... Please wait")
                self.zero_count = 1
            else:
                self.has_vessel = True
                self.update_display(0)
                self.le_progress.setText("")
        elif status == 'connected':
            self.lb_connected.setStyleSheet("background-color: Green;")
        elif status == 'disconnected':
            self.lb_connected.setStyleSheet("background-color: Red;")

    @pyqtSlot(str, name='newUID')
    def new_uid(self, uid):
        jar = self.db.execute_single(
            "SELECT jar FROM {} WHERE UID ='{}'".format(DB_JARS, uid))
        if jar is None:
            self.cb_jar.setCurrentIndex(0)
            self.lb_info.setText("Unknown Jar")
            self.check_start()
            return
        idx = self.cb_jar.findData(jar)
        if idx != -1:
            self.cb_jar.setCurrentIndex(idx)
            self.change_jar()

    def enter_pressed(self):
        self.check_start()
        self.check_enough()

    def start(self):
        """
        Starts and finishes the weighing operation
        """
        if not self.is_reading:
            self.scales.tare_p()
            self.le_progress.setFont(self.font)
            self.le_progress.setText("Zero scale.... Please wait")
            self.calculate_weight()
            self.progress_color = "Orange"
            self.update_display(self.weight_required * self.display_factor)
            self.is_reading = True
            self.is_finished = False
            self.has_got = False
            self.pb_start.setText("Check Out")
            self.pb_start.setEnabled(False)
            self.pb_cancel.setEnabled(True)
            self.cb_jar.setEnabled(False)
            self.cb_client.setEnabled(False)
            self.cb_type.setEnabled(False)
            self.le_amount.setEnabled(False)
        else:  # BAG
            self.le_progress.setText("Remove from scale")
            self.deduct()
            self.cb_jar.setCurrentIndex(0)
            self.cb_client.setCurrentIndex(0)
            self.le_amount.setText("")
            self.lb_info.setText("")
            self.is_finished = True
            self.cancel()

    def deduct(self):
        sql = 'UPDATE {} SET weight = weight - {} WHERE jar = "{}"'.format(DB_JARS, self.reading, self.jar)
        print(sql)
        self.db.execute_write(sql)
        sql = ('INSERT INTO {} (date, type, jar, strain, grams, amount, client, p_type) VALUES '
               '("{}", "CTR", "{}", {}, {}, {}, {}, {})'.
               format(DB_DISPATCH, datetime.now(), self.jar, self.strain_id, self.reading,
                      self.le_amount.text(), self.cb_client.currentData(), self.cb_type.currentData()))
        print(sql)
        self.db.execute_write(sql)
        self.logger.save_dispatch_counter(self.client, self.le_amount.text(), self.jar, self.strain_name,
                                          self.strain_id, round(self.weight_required, 1), self.reading)
        self.has_got = 0
        self.my_parent.my_parent.update_stock()

    def cancel(self):
        self.cb_jar.setEnabled(True)
        self.cb_client.setEnabled(True)
        self.cb_type.setEnabled(True)
        self.le_amount.setEnabled(True)
        self.is_reading = False
        # self.has_vessel = True
        self.pb_start.setText("Start")
        self.pb_cancel.setEnabled(False)
        self.le_progress.setText("")
        self.weight_required = 0
        self.zero_count = 1
        self.update_display(0)
        self.cb_type.setCurrentIndex(0)

    def tare(self):
        self.zero_count = 1
        self.scales.tare_p()
        self.le_progress.setText("Zero ....")

    def check_start(self):
        if self.cb_client.currentIndex() > 0 and self.cb_jar.currentIndex() > 0 and string_to_float(
                self.le_amount.text()) and self.cb_type.currentIndex() > 0:
            self.pb_start.setEnabled(True)
        else:
            self.pb_start.setEnabled(False)

    def position_markers(self):
        w = self.le_progress.size().width()
        # Percentage
        # xp = int((w / 100) * 75)
        # mx1 = xp * 1.05
        # mx2 = xp * 1.1
        # mx3 = xp * 1.15
        # fixed weight
        if self.weight_required == 0:
            wr = 7
        else:
            wr = self.weight_required
        xp = int((w / 100) * 75)
        mx1 = xp + ((xp / wr) * 0.1)
        mx2 = xp + ((xp / wr) * 0.25)
        mx3 = xp + ((xp / wr) * 0.5)
        mx4 = xp + ((xp / wr) * 1)
        s = self.le_progress.geometry().x()
        zp = s + mx1 + 1  # 1 = half its width
        self.l_marker_1.move(zp, 0)
        zp = s + mx2 + 1  # 1 = half its width
        self.l_marker_2.move(zp, 0)
        zp = s + mx3 + 1  # 1 = half its width
        self.l_marker_3.move(zp, 0)
        zp = s + mx4 + 1  # 1 = half its width
        self.l_marker_4.move(zp, 0)

    def position_last_marker(self):
        w = self.le_progress.size().width()
        last = self.my_parent.db.execute_single("SELECT grams FROM {} WHERE client = {} ORDER BY date DESC".
                                                format(DB_DISPATCH, self.cb_client.currentData()))
        if last is None or last == 0:
            self.l_marker_last.hide()
            return
        xp = int((w / 100) * 75)
        mx1 = xp + (xp / last)
        y = self.le_progress.geometry().size().height() + self.le_progress.geometry().y()
        s = self.le_progress.geometry().x()
        zp = s + mx1 + 1  # 1 = half its width
        self.l_marker_last.move(zp, y)
        self.l_marker_last.show()

    def update_display(self, value):
        if value < 0:
            value = 0
        if value > 1:
            value = 0.999
        css = 'background: qlineargradient(x1:0, y1:0, x2:1, y2:0, '
        pos = 0
        css += 'stop: ' + str(pos) + " " + self.progress_color + ", "  # ' #000000, '
        pos = value
        css += 'stop: ' + str(pos) + " " + self.progress_color + ", "  # ' #000000, '
        pos += 0.001
        css += 'stop: ' + str(pos) + ' #ffffff, '
        css += 'stop: ' + str(1) + ' rgba(0, 0, 0, 0), stop: 1 white); color: Red;'
        self.le_progress.setStyleSheet(css)

    def calculate_weight(self):
        self.amount = string_to_float(self.le_amount.text())
        self.weight_required = round(self.amount / self.ppg, 2)
        if self.weight_required <= 0:
            return
        self.factor = self.get_factor(self.amount)
        print("Factor = ", self.factor)
        self.weight_required /= self.factor
        print("After factor ", self.weight_required)
        self.display_factor = 0.75 / self.weight_required
        self.lbl_decode.setText(str(round(self.weight_required * 100, 0))[::-1])
        self.position_markers()

    def check_enough(self):
        if self.cb_jar.currentIndex() > 0 and string_to_float(self.le_amount.text()) > 0 \
                and self.cb_client.currentIndex() > 0:
            if self.gross == 0:
                self.gross = self.db.execute_single(
                    "SELECT (weight - nett - hum_pac) as gross FROM {} WHERE jar ='{}'".format
                    (DB_JARS, self.cb_jar.currentData()))
            self.calculate_weight()
            if self.weight_required > self.gross:
                # Not enough
                amount = self.gross * self.factor * self.ppg
                amount = amount - amount % 5  # round down to next 5
                self.lb_info.setText("<b>Not Enough</b> for there amount<br>This is only enough for £{}<br>or Select"
                                     " a new jar".format(int(amount)))
                self.pb_start.setEnabled(False)
            else:
                self.load_jar()

    def get_factor(self, amount) -> float:
        """

        :param amount: Amount required in pounds
        :type amount: float
        :return: factor to apply to grams
        :rtype: float
        """
        # factor will be from tables
        sql = 'SELECT p.limit, p.factor FROM {} p INNER JOIN {} c ON p.plan = c.plan AND c.id = {} ORDER BY p.limit'. \
            format(DB_CLIENT_PLANS, DB_CLIENTS, self.cb_client.currentData())
        plan = self.db.execute(sql)
        if len(plan) == 0:
            m_box("Error", "No Account, using default", 1)
            return 1
        if plan[0][0] == 0:
            return plan[0][1]
        for row in plan:
            if row[0] > amount:
                return row[1]
        return plan[len(plan) - 1][1]

    def change_client(self):
        if self.cb_client.currentData() != "000":
            self.pb_start.setEnabled(True)
            self.client = self.cb_client.currentText()
            p_type = self.db.execute_single(
                'SELECT default_type FROM {} WHERE id = {}'.format(DB_CLIENTS, self.cb_client.currentData()))
            index = self.cb_type.findData(p_type)
            if index >= 0:
                self.cb_type.setCurrentIndex(index)
                self.position_last_marker()

        else:
            self.cb_type.setCurrentIndex(0)
            self.pb_start.setEnabled(False)
            self.client = None
        self.check_start()

    def connect(self):
        if not self.scales.is_connected:
            self.scales.connect()
        else:
            self.lb_connected.setStyleSheet("background-color: Green;")

    def change_jar(self):
        self.jar = self.cb_jar.currentData()
        self.load_jar()
        self.check_start()
        self.check_enough()

    def load_jar(self):
        strain = self.db.execute_one_row(
            'SELECT s.name, s.type_sativa, s.type_indica, s.thc, s.cbd, s.flavour, s.effect, s.id, s.info FROM {} s INNER JOIN'
            ' {} j ON s.id = j.strain AND j.jar = "{}"'.format(DB_STRAINS, DB_JARS, self.jar))
        if strain is None:
            return
        self.strain_id = strain[7]
        self.strain_name = strain[0]
        self.lb_info.setText("<b>{}</b><br>Sativa: {}  Indica: {}<br>THC: {}   CBD: {}".
                             format(strain[0], strain[1], strain[2], strain[3], strain[4]))
        txt = ""
        if strain[5] != "":
            txt += "<b>Flavour</b><br>{}<br>".format(strain[5])
        if strain[6] != "":
            txt += "<b>Effect</b><br>{}<br>".format(strain[6])
        if strain[8] != "":
            txt += "<b>Info</b><br>{}<br>".format(strain[8])
        self.lb_info.setToolTip(txt)


class DialogDispatchReports(QDialog, Ui_DialogDispatchReport):
    def __init__(self, parent=None):
        """ :type parent: MainWindow """
        super(DialogDispatchReports, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.my_parent = parent
        self.db = parent.db
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.weeks_use = collections.defaultdict()
        self.legend = []
        self.pb_refresh.clicked.connect(self.refresh)
        self.pb_search.clicked.connect(self.search)
        self.plot_by_out = None
        self.plot_by_strain = None
        self.plot_by_out_weekly = None
        self.refresh()
        self.db.fill_combo(self.cb_client, DB_CLIENTS, 1, 0, ("All", 0))
        self.cb_type.addItem("All", 0)
        self.cb_type.addItem("CA", 1)  # Cash
        self.cb_type.addItem("BT", 2)  # Bank
        self.cb_type.addItem("CR", 3)  # Credit
        self.cb_type.addItem("FR", 4)  # Foc
        self.cb_type.addItem("PP", 5)  # Personal party
        self.cb_type.addItem("OP", 5)  # Other forms
        rows = self.db.execute("SELECT jar, strain FROM {} WHERE weight - nett > 0 ORDER BY jar".format(DB_JARS))
        # self.cb_jar.blockSignals(True)
        self.cb_jar.addItem("All", 0)
        for row in rows:
            # strain = ""
            # if row[1] > 0:
            #     strain = self.db.execute_single("SELECT name, id FROM {} WHERE id = {}".format(DB_STRAINS, row[1]))
            self.cb_jar.addItem("{}".format(row[0]), row[1])
        # self.cb_jar.blockSignals(False)

    def refresh(self):
        self.plot_internal()
        self.out_going_summary()
        self.plot_output()
        self.out_totals()

    def search(self):
        sql = 'SELECT `date`, jar, strain, grams, amount, client, p_type FROM {} WHERE '.format(DB_DISPATCH)
        if self.cb_client.currentData() > 0:
            sql += 'client = {}'.format(self.cb_client.currentData())
        if self.cb_jar.currentData() > 0:
            if self.cb_client.currentData() > 0:
                sql += ' AND'
            sql += ' jar = {}'.format(self.cb_jar.currentData())
        sql += " ORDER BY `date` DESC"
        rows = self.db.execute(sql)
        table = '<table cellspacing = "5"  border = "0" width = "100%">'
        for row in rows:
            table += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'. \
                format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        table += '</table>'
        self.te_search.setHtml(table)

    def plot_internal(self):
        sql = 'SELECT d.grams, d.strain, d.date FROM dispatch d WHERE DATE >= "{}" AND client = 1 ORDER BY date' \
            .format(datetime.now() - timedelta(days=7))
        rows = self.db.execute(sql)
        for row in rows:
            if self.weeks_use.get(row[1]) is None:
                strain = self.db.execute_single("SELECT name FROM {} WHERE id = {}".format(DB_STRAINS, row[1]))
                self.weeks_use[row[1]] = [row[0], strain]
                self.legend.append(strain)
            else:
                self.weeks_use[row[1]][0] += row[0]
        amounts = []
        legend = []
        for item in self.weeks_use:
            amounts.append(round(self.weeks_use[item][0], 1))
            legend.append(self.weeks_use[item][1])

        self.plot_by_strain = MplWidget(self.frame, 3, 5)
        self.plot_by_strain.plot_bar(legend, amounts)
        self.plot_by_strain.canvas.axes.tick_params(
            axis='x', which='major', labelcolor='Green', rotation=90, labelsize=7)
        self.plot_by_strain.auto_label()
        self.plot_by_strain.grid(True)

    def out_going_summary(self):
        # Client Weekly breakdown
        query_date = self.get_date_range()
        print(query_date)
        sql = "SELECT c.name, d.`client`, ROUND(SUM(d.grams), 2) AS total, " \
              "CASE WHEN (WEEKDAY(`date`)<=3) THEN DATE(`date` + INTERVAL (3- WEEKDAY(`date`)) DAY) " \
              "ELSE DATE(`date` + INTERVAL (3+7- WEEKDAY(`date`)) DAY) END AS week_ending " \
              'FROM dispatch d INNER JOIN clients c ON d.`client` = c.id WHERE d.date >= "{}" AND d.client != 1 ' \
              "GROUP BY week_ending, d.`client` ORDER BY week_ending DESC".format(query_date)
        rows = self.db.execute(sql)
        txt = '<h2 style="color:blue;">Clients Weekly</h2><table cellspacing = "5"  border = "0" width = "100%">'
        txt += '<tr><th>Week Start</th><th>Client</th><th>Amount</th></tr>'
        lw = 0  # Tracking as when to put in date
        wt = 0  # Week total
        for row in rows:
            if row[3] != lw:
                # Put total in but not for first week
                if lw != 0:
                    txt += '<tr style="font-size:14px;"><td colspan="2"><b>Total</b></td><td style="text-align:' \
                           'center;"><b>{}</b></td></tr>'.format(round(wt, 1))
                    wt = 0
                if lw == 0:
                    # Put This Week as date
                    txt += '<tr><td><b>Current</b></td><td style="text-align:center;">{}</td>' \
                           '<td style="text-align:center;">{}</td></tr>'. \
                        format(row[0], row[2])
                else:
                    # Put line in with date
                    txt += '<tr><td><b>{}</b></td><td style="text-align:center;">{}</td>' \
                           '<td style="text-align:center;">{}</td></tr>'. \
                        format(datetime.strftime(row[3] - timedelta(days=6), "%a %d %b"), row[0], row[2])
            else:
                # Put line in without date
                txt += '<tr><td> </td><td style="text-align:center;">{}</td>' \
                       '<td style="text-align:center;">{}</td></tr>'.format(row[0], row[2])
            wt += row[2]
            lw = row[3]
        txt += "<tr style='font-size:14px;'><td>Total</td><td> </td>" \
               "<td style='text-align:center;'><b>{}</b></td></tr>" \
            .format(round(wt, 1))
        txt += "</table>"
        self.te_weeks_summary_2.setHtml(txt)

        # Weekly Totals #############################################################################

        sql = "select SUM(d.amount) AS value, ROUND(SUM(d.grams), 2) AS total, " \
              "CASE WHEN (WEEKDAY(`date`)<=3) THEN DATE(`date` + INTERVAL (3-WEEKDAY(`date`)) DAY) " \
              " ELSE DATE(`date` + INTERVAL (3+7-WEEKDAY(`date`)) DAY) " \
              "END as week_ending " \
              'FROM dispatch d WHERE CLIENT = 1 and d.date >= "{}" ' \
              "GROUP BY week_ending, d.`client` ORDER BY week_ending DESC".format(query_date)
        rows = self.db.execute(sql)
        x = 0
        t1 = t2 = t3 = 0
        wtd = []
        wt = []
        txt = '<h2>Output</h2><h3>Weekly</h3><table cellspacing = "5"  border = "0">'
        txt += '<tr><th>Week Start</th><th>Int.</th><th>Count</th><th></th></tr>'
        for row in rows:
            sql = "SELECT ROUND(SUM(d.grams), 2) total_grams, ROUND(SUM(d.amount), 2) tc " \
                  'FROM dispatch d WHERE client != 1  AND d.`date` >= "{}" AND d.date <= "{}" ' \
                .format(row[2] - timedelta(days=6), row[2])
            counter = self.db.execute_one_row(sql)
            if counter[0] is None:
                col1 = 0
                col2 = 0
            else:
                col1 = counter[0]
                col2 = counter[1]
                t1 += row[1]
                t2 += col1
                t3 += col2
                wt.append(col1 + row[1])
                wtd.append(row[2])
            if x == 0:
                txt += '<tr><td>Current</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'. \
                    format(row[1], col1, col2)
            else:
                txt += '<tr><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'. \
                    format(datetime.strftime(row[2] - timedelta(days=6), "%a %d %b"), row[1], col1, col2)
            x += 1
        txt += '<tr style="font-size:12px;"><td>Totals</td><td>{}</td><td>{}</td><td style="text-align:center;">' \
               '{}</td></tr>'.format(round(t1, 2), round(t2, 2), round(t3, 2))
        txt += "</table>"

        # Weekly total of out
        txt += '<h3>Total Out</h3><table><tr><th>Week Start</th><th>Total</th></tr>'
        x = 0
        t1 = 0
        for d in wtd:
            txt += '<tr><td>{}</td><td style="text-align:center;">{}</td></tr>'. \
                format(d, round(wt[x], 2))
            t1 += wt[x]
            x += 1
        txt += "</table>"
        txt += "<b>Average  {}</b>".format(round(t1 / len(wt), 2))

        # Monthly Counter Totals #####################################################################

        sql = "SELECT MONTHNAME(d.`date`) month_name, MONTH(d.date) month_number, ROUND(SUM(d.grams), 2) " \
              "total_grams, SUM((d.amount)) total_amount FROM dispatch d WHERE d.p_type = 1 " \
              "GROUP BY month_name ORDER BY month_number DESC"
        rows = self.db.execute(sql)
        txt += '<h3>Monthly</h3><h4>Counter</h4>' \
               '<table cellspacing = "5"  border = "0">'
        txt += '<tr><th>Month</th><th>Amount</th><th>Total</th></tr>'
        t1 = 0
        t2 = 0
        for row in rows:
            txt += '<tr><td>{}</td><td style="text-align:center;">{}</td><td>{}</td></tr>'.format(row[0], row[2],
                                                                                                  row[3])
            t1 += row[2]
            t2 += row[3]
        txt += '<tr style="font-size:12px;"><td>Totals</td><td>{}</td><td style="text-align:center;">{}</td></tr>'. \
            format(round(t1, 1), round(t2, 2))
        txt += "</table>"

        # Monthly Internal Totals
        sql = "SELECT MONTHNAME(d.`date`) month_name, MONTH(d.date) month_number, ROUND(SUM(d.grams), 2) total_grams " \
              "FROM dispatch d WHERE d.client = 1 " \
              "GROUP BY month_name ORDER BY month_number DESC"
        rows = self.db.execute(sql)
        txt += '<h4>Internal</h4><table cellspacing = "5"  border = "0">'
        txt += '<tr><th>Month</th><th>Amount</th></tr>'
        t1 = 0
        for row in rows:
            txt += '<tr><td>{}</td><td style="text-align:center;">{}</td></tr>'.format(row[0], row[2])
            t1 += row[2]
        txt += '<tr style="font-size:12px;"><td>Totals</td><td style="text-align:center;">{}</td></tr>'. \
            format(round(t1, 2))
        txt += "</table>"
        self.te_weeks_summary.setHtml(txt)
        self.monthly_totals_by_type()

    def monthly_totals_by_type(self):
        txt = '<h3>Monthly</h3><h4>Types</h4>' \
               '<table cellspacing = "5"  border = "0">'
        txt += '<tr><th>Month</th><th>Type 1</th><th>Type 2</th><th>Total</th></tr>'
        sql = "SELECT MONTHNAME(d.`date`) month_name, MONTH(d.date) month_number, ROUND(SUM(d.amount), 2) total " \
              "FROM dispatch d WHERE d.p_type = 1 " \
              "GROUP BY month_name ORDER BY month_number DESC"
        rows = self.db.execute(sql)
        sql = "SELECT MONTHNAME(d.`date`) month_name, MONTH(d.date) month_number, ROUND(SUM(d.amount), 2) total " \
              "FROM dispatch d WHERE d.p_type = 2 " \
              "GROUP BY month_name ORDER BY month_number DESC"
        rows2 = self.db.execute(sql)
        t1 = t2 = 0
        # r2 = 0
        bt = collections.defaultdict(dict)
        for row in rows2:
            bt[row[0]] = {"b": row[2]}
        for row in rows:
            b = 0
            if row[0] in bt:
                b = float(bt[row[0]]['b'])
            else:
                bt[row[0]]['b'] = 0
            txt += '<tr><td>{}</td><td style="text-align:center;">£{:0,.0f}</td>' \
                   '<td style="text-align:center;">£{:0,.0f}</td><td style="text-align:center;">£{:0,.0f}' \
                   '</td></tr>'.format(row[0], row[2], b, float(row[2]) + b).replace('£-', '-£')
            t1 += row[2]
            t2 += bt[row[0]]['b']
            # r2 += 1
        txt += '<tr style="font-size:12px;"><td>Totals</td><td style="text-align:center;">£{:0,.0f}' \
               '</td><td style="text-align:center;">£{:0,.0f}</td><td style="text-align:center;">£{:0,.0f}' \
               '</td></tr>'. \
            format(round(t1, 2), t2, t1 + t2).replace('£-', '-£')
        txt += "</table>"
        self.te_weeks_summary.append(txt)

    def plot_output(self):
        query_date = self.get_date_range(8)
        sql = "select SUM(d.amount) AS value, ROUND(SUM(d.grams), 2) AS total, " \
              "CASE WHEN (WEEKDAY(`date`)<=3) THEN DATE(`date` + INTERVAL (3-WEEKDAY(`date`)) DAY) " \
              " ELSE DATE(`date` + INTERVAL (3+7-WEEKDAY(`date`)) DAY) " \
              "END as week_ending " \
              'FROM dispatch d WHERE d.date >= "{}" ' \
              "GROUP BY week_ending ORDER BY week_ending".format(query_date)
        rows = self.db.execute(sql)
        amounts = []
        legend = []
        for row in rows:
            legend.append(row[2] - timedelta(days=6))
            amounts.append(row[1])
        self.plot_by_out = MplWidget(self.wg_graph_1, 4.75, 3)
        # plt_dates = m_dates.date2num(list(legend))
        self.plot_by_out.plot_line(legend, amounts)
        self.plot_by_out.canvas.axes.tick_params(
            axis='x', which='major', labelcolor='Green', rotation=90, labelsize=7)
        self.plot_by_out.canvas.axes.xaxis.set_major_formatter(self.plot_by_out.date_fmt)

    def out_totals(self):
        query_date = self.get_date_range(12)
        sql = "select ROUND(SUM(d.grams), 2) AS total, " \
              "CASE WHEN (WEEKDAY(`date`)<=3) THEN DATE(`date` + INTERVAL (3-WEEKDAY(`date`)) DAY) " \
              " ELSE DATE(`date` + INTERVAL (3+7-WEEKDAY(`date`)) DAY) " \
              "END as week_ending " \
              'FROM dispatch d WHERE d.date >= "{}" ' \
              "GROUP BY week_ending ORDER BY week_ending DESC".format(query_date)
        rows = self.db.execute(sql)
        amounts = []
        legend = []
        for row in rows:
            legend.append(row[1] - timedelta(days=6))
            amounts.append(row[0])
        self.plot_by_out_weekly = MplWidget(self.wg_graph_4, 10, 4.75)
        plt_dates = m_dates.date2num(list(legend))
        self.plot_by_out_weekly.plot_bar(plt_dates, amounts)
        self.plot_by_out_weekly.canvas.axes.tick_params(
            axis='x', which='major', labelcolor='Green', rotation=90, labelsize=7)
        self.plot_by_out_weekly.canvas.axes.xaxis.set_major_formatter(self.plot_by_out_weekly.date_fmt)

    @staticmethod
    def get_date_range(weeks=6):
        day = datetime.now()
        wd = day - timedelta(days=(day.weekday() - 4) % 7, weeks=0)  # Get last Friday
        return (wd - timedelta(weeks=weeks)).date()


class DialogDispatchInternal(QDialog, Ui_DialogDispatchInternal):
    def __init__(self, parent):
        """
        :type parent: MainWindow
        """
        super(DialogDispatchInternal, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.my_parent = parent
        self.sub = None
        self.db = parent.db
        self.reading = self.reading_last = 0
        self.jar = None
        self.is_finished = False
        self.is_return = False
        self.strain_name = ""
        self.strain_id = 0
        self.scales = self.my_parent.scales
        self.scales.new_reading_p.connect(self.update_reading)
        self.scales.update_status.connect(self.update_status)
        self.scales.new_uid.connect(self.new_uid)
        self.ckb_return.clicked.connect(self.check_return)
        self.tare()
        self.cb_jar.currentIndexChanged.connect(self.load_jar)
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_start.clicked.connect(self.deduct)
        self.pb_tare.clicked.connect(self.tare)

        self.load_jars_list()

    @pyqtSlot(str, name='updateReadingP')
    def update_reading(self, value):
        self.reading = float(value)
        if self.jar is not None and self.reading_last > 5 and self.reading < 1:  # Jar removed
            # self.jar = None
            # self.lb_info.setText("")
            self.cb_jar.setEnabled(True)
            # self.cb_jar.setCurrentIndex(0)
            self.pb_start.setEnabled(False)
        if self.is_finished and self.reading < 0.2:
            self.lb_info.setText("Replace vessel")
            self.is_finished = False
        if not self.is_finished:
            self.le_weight.setText(str(self.reading))
            self.reading_last = self.reading
            self.check_start()

    @pyqtSlot(str, name='updateStatusP')
    def update_status(self, status):
        if status == 'tare':
            self.le_weight.setText("Tare")

    @pyqtSlot(str, name='newUID')
    def new_uid(self, uid):
        jar = self.db.execute_single(
            "SELECT jar FROM {} WHERE UID ='{}'".format(DB_JARS, uid))
        if jar is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This tag has not been registered {}".format(uid))
            msg.setWindowTitle("Unregistered UID")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            msg.exec_()
            return False

        idx = self.cb_jar.findData(jar)
        if idx != -1:
            self.cb_jar.setCurrentIndex(idx)
            self.load_jar()

    def tare(self):
        self.scales.tare_p()

    def check_return(self):
        if self.ckb_return.isChecked():
            self.is_return = True
            self.pb_start.setText("Return")
        else:
            self.is_return = False
            self.pb_start.setText("Deduct")

    def load_jar(self):
        self.jar = self.cb_jar.currentData()
        strain = self.db.execute_one_row(
            'SELECT s.name, s.type_sativa, s.type_indica, s.thc, s.cbd, s.flavour, s.effect, s.id FROM {} s INNER JOIN {} j '
            'ON s.id = j.strain AND j.jar = "{}"'.format(DB_STRAINS, DB_JARS, self.jar))
        if strain is None:
            return
        self.strain_name = strain[0]
        self.strain_id = strain[7]
        self.lb_info.setText("<b>{}</b><br>Sativa: {}  Indica: {}<br>THC: {}   CBD: {}".
                             format(strain[0], strain[1], strain[2], strain[3], strain[4]))
        self.lb_info.setToolTip("<b>Flavour</b><br>{}<br>Effect:<br>{}".format(strain[5], strain[6]))
        self.check_start()

    def check_start(self):
        if self.cb_jar.currentIndex() > 0 and self.reading > 0.2:
            self.pb_start.setEnabled(True)
        else:
            self.pb_start.setEnabled(False)

    def deduct(self):
        if self.is_return:
            amount = 0 - self.reading
            t_type = "INT-R"
        else:
            amount = self.reading
            t_type = "INT"
        sql = 'UPDATE {} SET weight = weight - {} WHERE jar = "{}"'.format(DB_JARS, amount, self.jar)
        print(sql)
        self.db.execute_write(sql)
        self.my_parent.logger.save_dispatch_counter("INT", "--", self.jar, self.strain_name, self.strain_id,
                                                    self.reading, self.reading)
        self.db.execute_write('INSERT INTO {} (date, type, jar, strain, grams, client) VALUES ("'
                              '{}", "{}", "{}", {}, {}, 1)'.
                              format(DB_DISPATCH, datetime.now(), t_type, self.jar, self.strain_id, amount))
        self.is_finished = True
        self.le_weight.setText("Remove")
        self.lb_info.setText("")
        self.cb_jar.setCurrentIndex(0)
        self.my_parent.my_parent.update_stock()
        self.pb_start.setEnabled(False)

    def load_jars_list(self):
        self.cb_jar.clear()
        sql = "SELECT jar, strain FROM {} WHERE location = 0 AND (weight - nett - hum_pac) > 0 ORDER BY jar ".format(
            DB_JARS)
        self.cb_jar.blockSignals(True)
        self.cb_jar.addItem("Select", "000")
        rows = self.db.execute(sql)
        for row in rows:
            strain = ""
            if row[1] > 0:
                strain = self.db.execute_single("SELECT name FROM {} WHERE id = {}".format(DB_STRAINS, row[1]))
            self.cb_jar.addItem("{} - {}".format(row[0], strain), row[0])
        self.cb_jar.blockSignals(False)


class DialogDispatchStorage(QDialog, Ui_Form):
    my_parent = ...  # type: MainWindow

    def __init__(self, parent):
        """

        :type parent: MainWindow
        """
        super(DialogDispatchStorage, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.my_parent = parent
        self.db = parent.db
        self.jar = None  # jar, weight, nett, UID, strain, hum_pac
        self.is_scan = False  # When True next UID scan will be entered
        self.is_set_nett = False  # When True next weight reading will be entered as nett value
        self.is_read = False  # When True next weight reading will be entered current weight
        self.on_scale = 0  # Used in jar removal detection
        self.new_nett = False  # True when nett has been set
        self.strain = 0
        self.new_weight = 0
        self.gross = 0
        self.org_gross = 0
        self.hum_pac = 0
        self.transfer_to_jar = ""
        self.scales = self.my_parent.scales
        self.nett_tol = self.db.get_config(CFT_ACCESS, "nett set", 5)
        self.scales.new_reading.connect(self.update_reading)
        # self.scales.update_status.connect(self.update_status)
        self.scales.new_uid.connect(self.new_uid)
        self.cb_jar.currentIndexChanged.connect(self.select_jar)
        self.le_name.textChanged.connect(lambda: auto_capital(self.le_name))
        self.cb_jar_transfer.currentIndexChanged.connect(self.select_transfer_jar)

        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_add.clicked.connect(self.add)
        self.pb_remove.clicked.connect(self.remove)
        self.pb_save.clicked.connect(self.save)
        self.pb_scan.clicked.connect(self.scan)
        self.pb_set.clicked.connect(self.set_nett)
        self.pb_read.clicked.connect(self.read)
        self.pb_tare.clicked.connect(lambda: self.scales.tare())
        self.pb_empty.clicked.connect(self.empty)
        self.pb_transfer.clicked.connect(self.transfer)
        self.pb_cancel.clicked.connect(self.clear)
        self.font = QtGui.QFont()
        self.font.setPointSize(11)

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)

        self.load_jars_list()
        rows = self.db.execute("SELECT name, breeder, id FROM {} ORDER BY name, breeder".format(DB_STRAINS))
        self.cb_strain.blockSignals(True)
        self.cb_strain.addItem("Select", "0")
        for row in rows:
            self.cb_strain.addItem("{} ({})".format(row[0], row[1]), row[2])
        self.cb_strain.blockSignals(False)

        self.cb_location.addItem("", -1)
        self.cb_location.addItem("A", 0)
        self.cb_location.addItem("B", 1)
        self.cb_location.addItem("C", 2)
        self.cb_location.addItem("D", 3)

    @pyqtSlot(str, name='newUID')
    def new_uid(self, uid):
        if self.is_scan:
            if not self.check_uid(uid):
                self.le_uid.setText(uid)
                self.is_scan = False
                self.le_uid.setStyleSheet("background-color: White;  color: Black;")
                self.le_uid.setFont(self.font)
                return
        if self.jar is not None:  # Jar was select manual and then jar added to scale, check same jar
            jar = self.db.execute_single("SELECT jar FROM {} WHERE UID = '{}'".format(DB_JARS, uid))
            if jar != self.jar[0]:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("The jar placed on the scales ({}) does not match the one selected ({}).<br>Either "
                            "place correct jar of cancel the one loaded".format(jar, self.jar[0]))
                msg.setWindowTitle("Incorrect Jar")
                msg.setStandardButtons(QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Cancel)
                msg.exec_()
                return False

        if self.jar is None:
            # If you alter this do same to one below in select_jar
            self.jar = self.db.execute_one_row(
                "SELECT jar, weight, nett, UID, strain, hum_pac, last_recon, last_nett, weight - nett - hum_pac "
                "as org_gross, location, capacity FROM {} WHERE UID ='{}'".format(
                    DB_JARS, uid))
        if self.jar is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This tag has not been registered {}".format(uid))
            msg.setWindowTitle("Unregistered UID")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            msg.exec_()
        self.load_jar()

    @pyqtSlot(str, name='updateReading')
    def update_reading(self, value):
        self.le_live.setText(value)
        if self.is_set_nett:
            if float(value) < self.new_weight:
                value = str(self.new_weight)
            self.le_nett.setText(value)
            self.new_nett = True
            self.le_weight.setText(value)
            self.get_gross()
        elif self.is_read:
            if float(value) < 0:
                value = "0.0"
            self.le_weight.setText(str(value))
            self.new_weight = float(value)
            self.get_gross()
        if self.jar is not None:
            self.get_gross()
            if float(value) > self.jar[2]:
                self.on_scale = 2
            if string_to_float(value) < self.jar[2] and self.on_scale == 2:
                self.clear()
                self.on_scale = 0
                self.jar = None
            # elif string_to_float(value) < self.jar[2]:

    def read(self):  # Read weight
        if self.is_read:
            self.is_read = False
            self.le_weight.setStyleSheet("background-color: none;")
            self.le_weight.setFont(self.font)
        else:
            self.is_read = True
            self.le_weight.setStyleSheet("background-color: Orange;")
            self.le_weight.setFont(self.font)

    def set_nett(self):
        # Set nett is only available when weight is close to nett
        if not self.is_set_nett:
            if self.jar is not None and self.new_weight - self.jar[2] > self.nett_tol:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("You can not set the nett unless the contents are less the {}grams\nThis jar "
                            "has {}grams".format(1, self.new_weight - self.jar[2]))
                msg.setWindowTitle("Unable to set Nett")
                msg.setStandardButtons(QMessageBox.Cancel)
                msg.exec_()
                return
            self.le_nett.setStyleSheet("background-color: Orange;")
            self.le_nett.setFont(self.font)
            self.is_set_nett = True
        else:
            self.le_nett.setStyleSheet("background-color: none;")
            self.le_nett.setFont(self.font)
            self.is_set_nett = False

    def check_uid(self, uid) -> bool:
        # Check to see if tag scanned can be used
        jar = self.db.execute_single(
            "SELECT jar FROM {} WHERE UID = '{}'".format(
                DB_JARS, uid))
        if jar is None:
            return False
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("This UID is assigned to {}".format(jar[0]))
        msg.setWindowTitle("UID Clash")
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.exec_()
        self.le_uid.setText("")
        return True

    def select_jar(self):
        jar = self.cb_jar.currentData()
        if jar == "000" or jar is None:
            self.frame.setEnabled(False)
            self.clear()
            return
        # If you alter this do same to one above in new_uid
        self.jar = self.db.execute_one_row(
            "SELECT jar, weight, nett, UID, strain, hum_pac, last_recon, last_nett, weight - nett - hum_pac "
            "as org_gross, location, capacity FROM {} WHERE jar = '{}'".format(
                DB_JARS, jar))
        self.load_jar()

    def scan(self):
        if self.is_scan:
            self.is_scan = False
            self.le_uid.setStyleSheet("background-color: none;")
            self.le_uid.setFont(self.font)
        else:
            self.is_scan = True
            self.le_uid.setStyleSheet("background-color: Orange;")
            self.le_uid.setFont(self.font)

    def load_jars_list(self):
        self.cb_jar.blockSignals(True)
        self.cb_jar.clear()
        count = self.db.execute_single("SELECT COUNT(jar) FROM {}".format(DB_JARS))
        self.lbl_count.setText(str(count))
        sql = "SELECT jar, strain FROM {} ORDER BY jar".format(DB_JARS)
        self.cb_jar.addItem("Select", "000")
        rows = self.db.execute(sql)
        for row in rows:
            strain = ""
            if row[1] > 0:
                strain = self.db.execute_single("SELECT name FROM {} WHERE id = {}".format(DB_STRAINS, row[1]))
            self.cb_jar.addItem("{} - {}".format(row[0], strain), row[0])
        self.cb_jar.blockSignals(False)

    def load_transfer_jars(self):
        sql = "SELECT jar, strain FROM {} WHERE weight - nett <= 1 OR strain = {} ORDER BY jar".format(DB_JARS,
                                                                                                       self.jar[4])
        rows = self.db.execute(sql)

        self.cb_jar_transfer.blockSignals(True)
        self.cb_jar_transfer.clear()

        if rows is None:
            self.cb_jar_transfer.addItem("None Available", "000")
        else:
            self.cb_jar_transfer.addItem("Select", "000")
        for row in rows:
            if row[0] != self.cb_jar.currentData():  # Check not the jar selected
                self.cb_jar_transfer.addItem(row[0], row[0])
        self.cb_jar_transfer.blockSignals(False)

    def load_jar(self):
        if self.jar is None:
            return
        self.le_name.setText(self.jar[0])
        self.le_name.setReadOnly(True)
        self.le_weight.setText(str(self.jar[1]))
        self.le_weight.setToolTip(str(self.jar[6]))
        self.le_nett.setToolTip(str(self.jar[7]))
        self.new_weight = self.jar[1]
        self.le_nett.setText(str(self.jar[2]))
        self.le_uid.setText(self.jar[3])
        self.le_hum_pac.setText(str(self.jar[5]))
        self.le_size.setText(str(self.jar[10]))
        self.org_gross = round(self.jar[8], 1)
        self.le_gross_2.setText(str(self.org_gross))
        self.hum_pac = self.jar[5]
        self.strain = self.jar[4]
        index = self.cb_strain.findData(self.jar[4])
        if index >= 0:
            self.cb_strain.setCurrentIndex(index)
        index = self.cb_location.findData(self.jar[9])
        if index >= 0:
            self.cb_location.setCurrentIndex(index)
        self.frame.setEnabled(True)
        # self.pb_add.setText("Save")
        self.pb_remove.setEnabled(True)
        self.pb_add.setEnabled(False)
        self.pb_transfer.setEnabled(False)
        self.load_transfer_jars()
        if self.jar[5] > 1:  # Check if there is a hum pac
            self.pb_hum_pac.setText("Remove")
        self.get_gross()

    def get_gross(self):
        self.gross = round(string_to_float(self.le_live.text()) - string_to_float(self.le_nett.text()) -
                           string_to_float(self.le_hum_pac.text()), 1)
        if self.gross < 0:
            self.le_gross.setText("---")
            self.le_diff.setText("---")
        else:
            self.le_gross.setText(str(self.gross))
            self.le_diff.setText(str(round(self.gross - self.org_gross, 1)))

    def save(self):
        if self.jar is None:  # New
            # Check if new name is in use
            if self.db.execute_single(
                    'SELECT jar FROM {} WHERE jar = "{}"'.format(DB_JARS, self.le_name.text())) is not None:
                self.msg.setWindowTitle("Invalid Name")
                self.msg.setText("This name is already in use")
                self.msg.setStandardButtons(QMessageBox.Cancel)
                self.msg.exec_()
                return
            sql = 'INSERT INTO {} (jar, weight, nett, UID, strain, hum_pac, last_nett) VALUES ' \
                  '("{}", {}, {}, "{}", {}, {}, "{}")' \
                .format(DB_JARS, self.le_name.text(), string_to_float(self.le_weight.text()),
                        string_to_float(self.le_nett.text()), self.le_uid.text(), self.cb_strain.currentData(),
                        string_to_float(self.le_hum_pac.text()), datetime.now())
            self.db.execute_write(sql)
            self.clear()
            self.load_jars_list()
            return
        else:  # Update
            sql = "UPDATE {} SET weight = {}, nett = {}, UID = '{}', strain = {}, hum_pac = {}, location = {}, " \
                  "capacity = {} WHERE jar = '{}' LIMIT 1" \
                .format(DB_JARS, string_to_float(self.le_weight.text()), string_to_float(self.le_nett.text()),
                        self.le_uid.text(), self.cb_strain.currentData(), string_to_float(self.le_hum_pac.text()),
                        self.cb_location.currentData(),
                        string_to_float(self.le_size.text()), self.jar[0])
            self.db.execute_write(sql)
        if self.new_nett:
            self.db.execute_write('UPDATE {} SET last_nett = "{}" WHERE jar = "{}" LIMIT 1'.
                                  format(DB_JARS, datetime.now(), self.jar[0]))
        # Stop setting weight < than jar weight
        if string_to_float(self.le_weight.text()) < string_to_float(self.le_nett.text()):
            self.msg.setWindowTitle("Invalid Weight")
            self.msg.setText("You can not set the weight to less than the empty jar.")
            self.msg.setStandardButtons(QMessageBox.Cancel)
            self.msg.exec_()
            return
        self.clear()
        self.load_jars_list()
        self.my_parent.my_parent.update_stock()

    def transfer(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Do you wish to transfer {}grams from jar <b>{}</b> to jar {}".
                    format(str(self.gross), self.jar[0], self.transfer_to_jar))
        msg.setWindowTitle("Confirm")
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        move_hum_pac = 0
        if self.hum_pac > 0:
            msg.setText("This jar contains a humidity pack.<br>Do you wish to transfer it also")
            msg.setWindowTitle("Confirm")
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Cancel)
            r = msg.exec_()
            if r == QMessageBox.Cancel:
                return
            if r == QMessageBox.Yes:
                move_hum_pac = self.hum_pac
        # Zero this jar
        sql = 'UPDATE {} SET weight = nett, hum_pac = 0, strain = 0 WHERE jar = "{}" LIMIT 1'.format(DB_JARS,
                                                                                                     self.jar[0])
        print(sql)
        self.db.execute_write(sql)
        # Update new jar values
        sql = 'UPDATE {} SET weight = weight + {} + {}, hum_pac = {}, strain = {} WHERE jar = "{}" LIMIT 1'. \
            format(DB_JARS, self.gross, move_hum_pac, move_hum_pac, self.jar[4], self.transfer_to_jar)
        print(sql)
        self.db.execute_write(sql)
        play_sound(SND_OK)
        self.clear()

    def add(self):
        if self.jar is None:  # Add new jar
            self.frame.setEnabled(True)
            self.le_name.setReadOnly(False)

    def remove(self):
        if self.jar is not None:  # Remove jar
            self.msg.setText("Confirm you wish to remove this jar")
            self.msg.setWindowTitle("Confirm Removal")
            if self.msg.exec_() == QMessageBox.Cancel:
                return
            self.db.execute_write('DELETE from {} WHERE jar = "{}" LIMIT 1'.format(DB_JARS, self.jar[0]))
            self.clear()
            self.load_jars_list()
        else:  #
            pass

    def empty(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Do you wish to record this jar as empty")
        msg.setWindowTitle("Confirm")
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        sql = "UPDATE {} SET weight = {}, strain = {}, hum_pac = 0 WHERE jar = '{}' LIMIT 1". \
            format(DB_JARS, self.jar[2], 0, self.jar[0])
        self.my_parent.db.execute_write(sql)
        self.load_jars_list()
        self.cb_jar.setCurrentIndex(self.cb_jar.findData(self.jar[0]))
        # self.select_jar()

    def clear(self):
        self.le_name.setText("")
        self.le_name.setReadOnly(True)
        self.le_weight.setText("")
        self.le_nett.setText("")
        self.le_uid.setText("")
        self.le_hum_pac.setText("")
        self.le_gross.setText("")
        self.le_gross_2.setText("")
        self.le_diff.setText("")
        self.cb_strain.setCurrentIndex(0)
        self.cb_jar.setCurrentIndex(0)
        self.pb_add.setText("Add")
        self.pb_remove.setText("Remove")
        self.pb_remove.setEnabled(False)
        self.pb_add.setEnabled(True)
        self.on_scale = 0
        self.is_read = False
        self.is_scan = False
        self.is_set_nett = False
        self.jar = None
        self.frame.setEnabled(False)

    def select_transfer_jar(self):
        if self.cb_jar_transfer.currentIndex() > 0:
            self.pb_transfer.setEnabled(True)
            self.transfer_to_jar = self.cb_jar_transfer.currentData()
        else:
            self.pb_transfer.setEnabled(False)
            self.transfer_to_jar = ""


class DialogDispatchOverview(QDialog, Ui_DialogLogistics):
    def __init__(self, parent):
        """
        :type parent: MainPanel
        """
        super(DialogDispatchOverview, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.my_parent = parent
        self.db = parent.db
        self.up_coming = []
        self.up_coming_yield = []
        self.estimate_per_plant = int(self.db.get_config(CFT_DISPATCH, "estimate per plant", 50))
        self.stock = collections.defaultdict()
        self.weekly_total = 0
        self.stock_total = 0
        self.sort_order = "jar"
        self.le_weeks.setText("25")
        self.pb_refresh.clicked.connect(self.refresh)
        self.refresh()
        self.get_up_coming()
        self.rb_sort_1.toggled.connect(self.change_sort_order)
        self.rb_sort_2.toggled.connect(self.change_sort_order)
        self.rb_sort_3.toggled.connect(self.change_sort_order)
        self.lw_available.doubleClicked.connect(self.display_strain)
        self.lw_available.currentItemChanged.connect(self.display_strain)

    def refresh(self):
        self.load_stock()
        self.load_clients()
        # self.get_up_coming()
        self.get_future()
        self.load_available()

    def change_sort_order(self):
        rb_tn = self.sender()
        if rb_tn.isChecked():
            if rb_tn.text() == "Jar":
                self.sort_order = "jar"
            elif rb_tn.text() == "Strain":
                self.sort_order = "strain"
            elif rb_tn.text() == "Availability":
                self.sort_order = "gross"
            self.load_stock()

    def load_stock(self):
        self.te_stock_list.clear()
        self.stock.clear()
        total = 0
        sql = 'SELECT (weight - nett - hum_pac) as gross, jar, strain, weight, nett, UID, hum_pac, last_recon, ' \
              'last_nett, location, capacity FROM {} ORDER BY {}'.format(DB_JARS, self.sort_order)
        rows = self.db.execute(sql)
        txt = '<table cellpadding = "5"  border = "1">'
        for row in rows:
            if row[0] > 0:
                total += row[0]
                if row[9] != 0:
                    css = ' style="background-color:lightgray"'
                else:
                    css = ""
                strain = self.db.execute_single('SELECT name FROM {} WHERE id = {}'.format(DB_STRAINS, row[2]))
                txt += '<tr{}><td>{}</td><td>{}</td><td>{}</td><td>{}</td>'.format(css, strain, row[1], row[9],
                                                                                   round(row[0], 1))
                txt += '<td>{}</td><td>{}</td><td>{}</td>'.format(row[3], round(row[4], 1), row[6])
                txt += '<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(row[5], row[10], row[7], row[8])
                print("strain = ", row[2])
                if row[2] in self.stock:
                    self.stock[row[2]]['amount'] += round(row[0], 1)
                    # print("add stock =", self.stock[row[2]]['amount'])
                else:
                    self.stock[row[2]] = {'amount': round(row[0], 1), 'name': strain}
                # print("new stock =", self.stock[row[2]]['amount'])
        txt += '</table>'
        self.te_stock_list.setHtml(txt)
        self.le_weight.setText(str(round(total, 1)))
        self.stock_total = total
        self.summary()

    def summary(self):
        a_list = {}
        for key, value in self.stock.items():
            a_list[value['name']] = value['amount']
        as_list = sorted(a_list.items(), key=lambda x: x[1])    # This sorts it by weight
        txt = '<table>'
        for item in as_list:
            txt += '<tr><td>{}</td><td>{}</td></tr>'.format(item[0], round(item[1], 1))
        txt += '</table>'
        self.te_instock.setHtml(txt)

    def load_clients(self):
        total = 0
        sql = 'SELECT amount, name FROM {} WHERE frequency = 1 ORDER BY sort_order'.format(DB_CLIENTS)
        rows = self.db.execute(sql)
        self.lw_clients.clear()
        for row in rows:
            total += row[0]
            lw_item = QListWidgetItem(row[1] + "  " + str(row[0]))
            v_item = QVariant(row[0])
            lw_item.setData(Qt.UserRole, v_item)
            self.lw_clients.addItem(lw_item)

        self.le_weekly.setText(str(round(total, 1)))
        self.weekly_total = total

    def get_up_coming(self):
        self.te_upcomming.clear()
        self.up_coming.clear()
        for loc in range(3, 0, -1):
            if self.my_parent.area_controller.area_has_process(loc):
                d = self.my_parent.area_controller.get_area_process(loc).end
                q = self.my_parent.area_controller.get_area_process(loc).quantity
                if d.date() > datetime.now().date():
                    getattr(self, "lbl_upcoming_{}".format(loc)).setText(
                        "{} > {}".format(datetime.strftime(d, "%d/%m/%y"), q))
                    getattr(self, "le_upcoming_total_{}".format(loc)).setText("{}".format(q * self.estimate_per_plant))
                    # getattr(self, "ck_upcoming_{}".format(loc)).setChecked(True)
                    self.up_coming.append([d, q, loc])
                    # self.up_coming_yield.append(q)
        # for d, q in self.up_coming:
        #     self.te_upcomming.append(
        #         "{} > {} ~ {}".format(datetime.strftime(d, "%d/%m/%y"), q, q * self.estimate_per_plant))

    def get_future(self):
        self.te_future.clear()
        up_coming = self.up_coming.copy()
        txt = '<table cellpadding = "5"  border = "1" cellspacing = "0" >'
        day = datetime.now()
        wd = day - timedelta(days=(day.weekday() - 4) % 7, weeks=-1)  # Get next friday
        days = (wd - datetime.now()).days
        rt = self.stock_total
        for week in range(1, int(self.le_weeks.text()) + 1):
            rt -= self.weekly_total
            if rt > self.weekly_total:
                c = "color: Black; background: Green;"
                # if len(up_coming) > 0 and self.ck_inlude_upcomming.isChecked():
                if len(up_coming) > 0:
                    if wd.date() > up_coming[0][0].date():
                        if getattr(self, "ck_upcoming_{}".format(up_coming[0][2])).isChecked():
                            c = "color: White; background: DarkGreen;"
                            # if up_coming[0][1] > 0:
                            rt += string_to_float(getattr(self, "le_upcoming_total_{}".format(up_coming[0][2])).text())
                            up_coming.pop(0)
                            # up_coming[0][1] = 0
            else:
                c = "color: White; background: Red;"
                if len(up_coming) > 0:
                    if wd.date() > up_coming[0][0].date():
                        if getattr(self, "ck_upcoming_{}".format(up_coming[0][2])).isChecked():
                            c = "color: Black; background: Orange;"
                            # if up_coming[0][1] > 0:
                            rt += string_to_float(getattr(self, "le_upcoming_total_{}".format(up_coming[0][2])).text())
                            up_coming.pop(0)
            txt += '<tr style="{}"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'. \
                format(c, week, days + (week - 1) * 7, datetime.strftime(wd, "%d/%m/%y"), self.weekly_total, round(rt))
            wd = wd + timedelta(days=7)
        txt += '</table>'
        self.te_future.setHtml(txt)

    def load_available(self):
        self.lw_available.blockSignals(True)
        self.lw_available.clear()
        for item in self.stock:
            if item != 0:
                strain = self.db.execute_one_row('SELECT name, id FROM {} WHERE id = {}'.format(DB_STRAINS, item))
                print(item)
                lw_item = QListWidgetItem(strain[0])
                v_item = QVariant(strain[1])
                lw_item.setData(Qt.UserRole, v_item)
                self.lw_available.addItem(lw_item)
        self.lw_available.blockSignals(False)

    def display_strain(self):
        sid = self.lw_available.currentItem().data(Qt.UserRole)
        if sid is None:
            return
        strain = self.db.execute_one_row("SELECT * FROM {} WHERE id = {}".format(DB_STRAINS, sid))
        if strain is None:
            return
        jars = self.db.execute('SELECT jar FROM {} WHERE strain = {}'.format(DB_JARS, sid))
        if jars is None:
            return
        lbl = ""
        for jar in jars:
            lbl += "({})  ".format(jar[0])
        txt = '<table>'
        txt += '<tr><td> {}</td></tr>'.format(lbl)
        txt += '<tr><td><b>{}</b> by {}</td></tr>'.format(strain[2], strain[1])
        txt += '<tr><td>Sativa {}   Indica {}</td></tr>'.format(strain[6], strain[7])
        txt += '<tr><td>THC {}   CBD {}</td></tr>'.format(strain[19], strain[20])
        txt += '<tr><td><b>Genetics {}</b></td></tr>'.format(strain[18])
        if strain[9] != "":
            txt += '<tr><td><b>Flavour</b><br>{}</td></tr>'.format(strain[9])
        if strain[10] != "":
            txt += '<tr><td><b>Effect</b><br>{}</td></tr>'.format(strain[10])
        if strain[12] != "":
            txt += '<tr><td><b>Info</b><br>{}</td></tr>'.format(strain[12])
        self.te_stock_summary.setHtml(txt)


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
            if recipe is None:
                return      # Safety check, need looking into
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
                        round(self.feed_control.get_water_total(self.area, self.mix_number), 2)) + " which is " +
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
        if self.my_parent.master_mode == MASTER:
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
        self.my_parent.coms_interface.send_data(COM_READ_KWH, True, MODULE_DE)
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


class DialogStrainFinder(QWidget, Ui_DialogStrainFinder):
    def __init__(self, parent=None):
        """ :type parent: MainWindow """
        super(DialogStrainFinder, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.my_parent = parent
        self.db = parent.db
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())

        sql = 'SELECT id, name, breeder FROM {} ORDER BY name'.format(DB_STRAINS)
        rows = self.db.execute(sql)
        for row in rows:
            self.cb_name.addItem("{} ({})".format(row[1], row[2]), row[0])

        self.cb_name.currentIndexChanged.connect(lambda: self.le_id.setText(str(self.cb_name.currentData())))


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


class DialogFan(QDialog, Ui_DialogFan):
    def __init__(self, parent, fan):
        super(DialogFan, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setupUi(self)
        self.sub = None
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Fan {}".format(fan))
        self.my_parent = parent
        self.db = self.my_parent.db
        self.id = fan
        self.fan = self.my_parent.area_controller.fans[fan]
        self.dl_fan.valueChanged.connect(self.change_speed)
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_mode_off.clicked.connect(lambda: self.change_mode(0))
        self.pb_mode_manual.clicked.connect(lambda: self.change_mode(1))
        self.pb_mode_a.clicked.connect(lambda: self.change_mode(2))
        self.pb_master.clicked.connect(self.power)
        self.my_parent.coms_interface.update_fan_speed.connect(self.update_speed)
        self.check_mode()

    def power(self):
        if self.fan.master == 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Confirm you wish to shut down the fan controller's power supply")
            msg.setWindowTitle("Confirm Shut Down")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            if msg.exec_() == QMessageBox.Cancel:
                return
            self.fan.master = 0
        else:
            self.fan.master = 1

    def check_mode(self):
        if self.fan.master == 0:
            self.lbl_mode.setText("DOWN")
            return
        if self.fan.mode == 0:
            # self.dl_fan.setValue(0)
            self.lbl_mode.setText("Off")
            self.dl_fan.setEnabled(False)
        elif self.fan.mode == 2:
            self.dl_fan.setValue(self.fan.speed)
            self.lbl_mode.setText("Auto")
            self.dl_fan.setEnabled(False)
        else:
            self.lbl_mode.setText("Manual")
            self.dl_fan.setEnabled(True)

    def change_speed(self, speed):
        """
        Manually set speed
        @param speed:
        @type speed: int
        """
        self.fan.speed = speed

    def change_mode(self, mode):
        if mode == 0:
            self.fan.stop()
            self.dl_fan.setEnabled(False)
        if mode == 1:
            self.fan.start_manual()
            self.dl_fan.setEnabled(True)
            self.dl_fan.setValue(5)
        if mode == 2:
            self.fan.start_auto()
            self.dl_fan.setEnabled(False)
        # self.fan.mode = mode
        self.check_mode()

    @pyqtSlot(int, int, name="updateFanSpeed")
    def update_speed(self, fan, speed):
        if fan == self.id and self.fan.mode == 2:
            self.dl_fan.blockSignals(True)
            self.dl_fan.setValue(speed)
            self.dl_fan.blockSignals(False)


class DialogSensorSettings(QWidget, Ui_DialogSensorSettings):
    def __init__(self, parent, area, s_id):
        """ :type parent: MainWindow """
        super(DialogSensorSettings, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.db = parent.db
        self.sub = None

        self.area = area
        self.s_id = s_id

        self.process = self.main_panel.area_controller.get_area_process(self.area)
        self.sensors = self.main_panel.area_controller.sensors
        self.font_i = QtGui.QFont()
        self.font_i.setItalic(True)
        self.font_n = QtGui.QFont()
        self.font_n.setItalic(False)

        self.set = self.high = self.low = 0
        self.temperatures_active = []
        self.temperatures_inactive = []
        self.temperatures_active_org = []
        self.temperatures_inactive_org = []
        self.low_org = 0
        self.set_org = 0
        self.high_org = 0
        self.inverted = False   # True means you are working on inactive values

        # Load sensor config from db
        self.config = self.db.execute_one_row('SELECT id, name, maps_to, calibration, step, area, area_range, '
                                              'short_name FROM {} WHERE id = {}'.format(DB_SENSORS_CONFIG, self.s_id))
        self.item = self.config[6]
        self.lbl_name.setText(self.config[1])

        # get day or night
        self.on_day = self.main_panel.area_controller.get_light_status(self.area)
        self.day_night = self.on_day    # Holds the day night value. Will be same as on_day unless inverted

        # Is sensor used by fan
        self.fan_sensor_current = self.db.execute_single('SELECT sensor FROM {} WHERE id = {}'.format(DB_FANS, self.area))
        if self.fan_sensor_current == self.s_id:
            # This sensor is fan sensor
            self.fan_sensor = True
            txt = "Fan Sensor<br>"
        else:
            self.fan_sensor = False
            txt = ""

        # Is sensor controlling any outputs
        rows = self.db.execute('SELECT name FROM {} WHERE input = {}'.format(DB_OUTPUTS, self.s_id))
        if len(rows) == 0:
            if txt == "":
                txt = "None"
        else:
            txt += "Outputs<br>"
            for row in rows:
                txt += row[0] + ", "
            txt = txt[:-2]
        self.lbl_connections.setText(txt)

        self.load_ranges()

        self.pb_set_fan.clicked.connect(self.set_as_fan)
        self.le_set.editingFinished.connect(self.change_set)
        self.le_high.editingFinished.connect(self.change_high)
        self.le_low.editingFinished.connect(self.change_low)
        self.pb_reset.clicked.connect(self.reset_values)
        self.pb_switch.clicked.connect(self.invert)

    # def focusOutEvent(self):
    #     print("BYE BYE BYE BYE BYE BYE BYE BYE ")

    def eventFilter(self, source, event):
        # Remember to install event filter for control first
        print("Event ", event.type())
        if event.type() == QtCore.QEvent.FocusOut:
            if source == self:
                print("BYE BYE BYE BYE BYE BYE BYE BYE ")

        return QWidget.eventFilter(self, source, event)

    def load_ranges(self, inverted=False):
        """ From process loads the active and inactive temperature ranges used by the sensor
            inverted= True will reverse active and inactive,
                used when switched to day or night on currently active"""
        if self.process != 0:
            if inverted:
                self.temperatures_active = self.process.temperature_ranges_inactive[self.item]
                self.temperatures_inactive = self.process.temperature_ranges_active[self.item]
                self.temperatures_active_org = self.process.temperature_ranges_inactive_org[self.item]
                self.temperatures_inactive_org = self.process.temperature_ranges_active_org[self.item]
            else:
                self.temperatures_active = self.process.temperature_ranges_active[self.item]
                self.temperatures_inactive = self.process.temperature_ranges_inactive[self.item]
                self.temperatures_active_org = self.process.temperature_ranges_active_org[self.item]
                self.temperatures_inactive_org = self.process.temperature_ranges_inactive_org[self.item]
            self.low = self.temperatures_active['low']
            self.set = self.temperatures_active['set']
            self.high = self.temperatures_active['high']
            self.low_org = self.temperatures_active_org['low']
            self.set_org = self.temperatures_active_org['set']
            self.high_org = self.temperatures_active_org['high']
        else:
            # No process so use default values
            pass    # Still to be done
        self.update_display()

    def update_display(self):
        # self.set, self.high, self.low = self.sensors[self.s_id].get_set_temperatures()
        self.le_set.setText(str(self.set))
        self.le_high.setText(str(self.high))
        self.le_low.setText(str(self.low))
        self.lbl_set.setText(str(self.set_org))
        self.lbl_high.setText(str(self.high_org))
        self.lbl_low.setText(str(self.low_org))
        if self.inverted:
            self.lbl_area.setText("Area {} ({})".format(self.area, "Night" if self.on_day else "Day"))
            self.pb_switch.setText("Day" if self.on_day else "Night")
            stylesheet = "Color: White; background-color: red"
        else:
            self.lbl_area.setText("Area {} ({})".format(self.area, "Day" if self.on_day else "Night"))
            self.pb_switch.setText("Night" if self.on_day else "Day")
            stylesheet = ""
        self.le_set.setStyleSheet(stylesheet)
        self.le_high.setStyleSheet(stylesheet)
        self.le_low.setStyleSheet(stylesheet)

    def invert(self):
        self.inverted = not self.inverted
        self.day_night = int(not self.day_night)
        self.load_ranges(self.inverted)

    def reset_values(self):
        self.set = self.set_org
        self.high = self.high_org
        self.low = self.low_org
        self.le_high.setText(str(self.high))
        self.le_set.setText(str(self.set))
        self.le_low.setText(str(self.low))
        self.db.execute_write('UPDATE {} SET value = 0 WHERE area= {} AND day = {} AND item = {} '
                              'LIMIT 3'.format(DB_PROCESS_TEMPERATURE, self.area, self.day_night, self.item))
        self.process.load_active_temperature_ranges()
        self.main_panel.coms_interface.relay_send(NWC_SENSOR_RELOAD, self.area)

    def change_set(self):
        if self.sender().hasFocus():
            return
        nv = string_to_float(self.le_set.text())
        if nv == self.set:
            return
        self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                              '"set" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
        self.set = nv
        #  Check high value
        self._check_high(nv)
        # Check low value
        self._check_low(nv)
        self.process.load_active_temperature_ranges()

    def change_high(self):
        if self.sender().hasFocus():
            return
        nv = string_to_float(self.le_high.text())
        if nv == self.high:
            return
        self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                              '"high" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
        self.high = nv
        self._check_set_high(nv)
        self._check_low(self.set)
        self.process.load_active_temperature_ranges()

    def change_low(self):
        if self.sender().hasFocus():
            return
        nv = string_to_float(self.le_low.text())
        if nv == self.low:
            return
        self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                              '"low" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
        self.low = nv
        self._check_set_low(nv)
        self._check_high(self.set)
        self.process.load_active_temperature_ranges()

    def _check_high(self, nv):
        if self.high < nv + 0.5:
            self.le_high.setText(str(nv + 0.5))
            self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                                  '"high" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night,
                                                          self.item))
            self.high = nv + 0.5

    def _check_low(self, nv):
        if self.low > nv - 0.5:
            self.le_low.setText(str(nv - 0.5))
            self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                                  '"low" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
            self.low = nv - 0.5

    def _check_set_high(self, nv):
        # checks set value from high
        if self.set > nv - 0.5:
            self.le_set.setText(str(nv - 0.5))
            self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                                  '"set" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
            self.set = nv - 0.5

    def _check_set_low(self, nv):
        # checks set value from low
        if self.set < nv + 0.5:
            self.le_set.setText(str(nv + 0.5))
            self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                                  '"set" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
            self.set = nv + 0.5

    def set_as_fan(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Confirm you wish to set this sensor as input for the fan")
        msg.setWindowTitle("Confirm Fan Setting")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        self.sensors[self.fan_sensor_current].is_fan = False
        self.sensors[self.s_id].is_fan = True
        sql = 'UPDATE {} SET sensor = {} WHERE id = {}'.format(DB_FANS, self.s_id, self.area)
        self.db.execute_write(sql)
        self.main_panel.coms_interface.send_data(CMD_SET_FAN_SENSOR, True, MODULE_IO, self.area, self.s_id)
        self.main_panel.coms_interface.relay_send(NWC_FAN_SENSOR, self.area, self.s_id)


class DialogProcessAdjustments(QWidget, Ui_DialogProcessAdjust):
    def __init__(self, parent, area):
        """ :type parent: MainWindow """
        super(DialogProcessAdjustments, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.db = parent.db
        self.sub = None

        self.area = area
        self.process = self.main_panel.area_controller.get_area_process(self.area)
        self.cb_feed_mode.addItem("Manual", 1)
        self.cb_feed_mode.addItem("Semi Auto", 2)
        self.cb_feed_mode.addItem("Automatic", 3)
        self.cb_feed_mode.addItem("Full Auto", 4)
        self.cb_move_to.addItem("", 0)
        if not self.main_panel.area_controller.area_has_process(1) and self.area != 1:
            self.cb_move_to.addItem("Area 1", 1)
            # idx += 1
        if not self.main_panel.area_controller.area_has_process(2) and self.area != 2:
            self.cb_move_to.addItem("Area 2", 2)

        self.new_feed_date = self.main_panel.feed_controller.get_last_feed_date(self.area)

        if self.area != 3:
            self.cb_feed_mode.setCurrentIndex(self.main_panel.feed_controller.get_feed_mode(self.area))
            self.de_feed_date.setDate(self.new_feed_date)
        else:
            self.cb_feed_mode.setEnabled(False)
            self.de_feed_date.setEnabled(False)

    def delay_feed(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Confirm you wish to delay feeding")
        msg.setWindowTitle("Confirm Feed Delay")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        self.main_panel.feed_control.set_last_feed_date(
            self.area, self.feed_data['lfd'] + timedelta(days=1))
        # self.process.set_last_feed_date(self.process.last_feed_date + timedelta(days=1))
        self.main_panel.update_next_feeds()
        self.main_panel.coms_interface.relay_send(NWC_FEED, self.area)  # Just send feed as it is only the feed date that is changed


class DialogOutputSettings(QWidget, Ui_DialogOutputSetting):
    def __init__(self, parent, area, item):
        """ :type parent: MainWindow """
        super(DialogOutputSettings, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.db = parent.db
        self.sub = None

        self.output_controller = self.main_panel.area_controller.output_controller
        self.area = area
        self.item = item
        self.font_i = QtGui.QFont()
        self.font_i.setItalic(True)
        self.font_n = QtGui.QFont()
        self.font_n.setItalic(False)

        sql = 'SELECT `id`, `name`, `area`, `type`, `input`, `range`, `pin`, `short_name` FROM {} WHERE ' \
              '`area` = {} AND `item` = {}'. format(DB_OUTPUTS, self.area, self.item)
        row = self.db.execute_one_row(sql)
        self.mode = row[3]
        self.pin_id = row[6]       # Use as index for the Outputs[] dictionary
        self.sensor = row[4]
        t = row[5].split(',')
        self.offset_on = string_to_float(t[0])
        self.offset_off = string_to_float(t[1])
        self.detection_mode = self.output_controller.outputs[self.pin_id].detection
        self.lbl_detection.setText("<" if self.detection_mode == DET_FALL else ">")
        self.lbl_name.setText("{} in area {}".format(row[1], self.area))
        self.cb_out_mode_1_1.addItem("Off", 0)
        self.cb_out_mode_1_1.addItem("Manual On", 1)
        self.cb_out_mode_1_1.addItem("Sensor", 2)
        self.cb_out_mode_1_1.addItem("Timer", 3)
        self.cb_out_mode_1_1.addItem("Both", 4)
        self.cb_out_mode_1_1.addItem("All Day", 5)
        self.cb_out_mode_1_1.addItem("All Night", 6)
        self.cb_out_mode_1_1.setCurrentIndex(self.cb_out_mode_1_1.findData(row[3]))
        self.mode_change()
        self.cb_out_mode_1_1.currentIndexChanged.connect(self.mode_change)

        sql = 'SELECT name, id FROM {} WHERE area = {}'.format(DB_SENSORS_CONFIG, self.area)
        rows = self.db.execute(sql)
        for r in rows:
            self.cb_sensor_out_1_1.addItem(r[0], r[1])
        self.cb_sensor_out_1_1.setCurrentIndex(self.cb_sensor_out_1_1.findData(row[4]))
        self.cb_sensor_out_1_1.currentIndexChanged.connect(self.sensor_change)
        self.le_range_on_1_1.editingFinished.connect(self.range_change)
        self.le_range_off_1_1.editingFinished.connect(self.range_change)
        self.pb_reset.clicked.connect(self.reset)

        self.on, self.off = self.output_controller.get_set_temperatures(self.pin_id)

        self.le_range_on_1_1.setText(str(self.on + self.offset_on))
        self.le_range_off_1_1.setText(str(self.off + self.offset_off))
        self.lbl_set_on_1_1.setText(str(self.on))
        self.lbl_set_off_1_1.setText(str(self.off))
        self.cb_trigger.addItem("Falling", DET_FALL)
        self.cb_trigger.addItem("Rising", DET_RISE)
        self.cb_trigger.setCurrentIndex(self.cb_trigger.findData(self.change_detection_mode))
        self.cb_trigger.currentIndexChanged.connect(self.change_detection_mode)

    def change_detection_mode(self):
        self.detection_mode = self.cb_trigger.currentData()
        self.output_controller.change_trigger(self.pin_id, self.detection_mode)
        self.lbl_detection.setText("<" if self.detection_mode == DET_FALL else ">")

    def reset(self):
        self.le_range_on_1_1.setText(str(self.on))
        self.le_range_off_1_1.setText(str(self.off))
        self.range_change()

    def mode_change(self):
        self.frm_sensor.setEnabled(False)
        self.frm_timer.setEnabled(False)
        self.mode = self.cb_out_mode_1_1.currentData()
        if self.mode == 2 or self.mode == 4:  # Sensor or both
            self.frm_sensor.setEnabled(True)
        if self.mode == 3 or self.mode == 4:  # Timer or both
            self.frm_timer.setEnabled(True)
        self.output_controller.change_mode(self.pin_id, self.mode)

    def sensor_change(self):
        self.sensor = self.cb_sensor_out_1_1.currentData()
        self.output_controller.change_sensor(self.pin_id, self.sensor)

    def range_change(self):
        # if self.sender().hasFocus():
        #     return
        on = string_to_float(self.le_range_on_1_1.text())
        off = string_to_float(self.le_range_off_1_1.text())

        if self.detection_mode == DET_FALL:
            if on + 1 > off:
                off = on + 1
                self.le_range_off_1_1.setText(str(off))
        elif self.detection_mode == DET_RISE:
            if on - 1 < off:
                off = on - 1
                self.le_range_off_1_1.setText(str(off))
        on = on - self.on
        off = off - self.off
        self.output_controller.change_range(self.pin_id, on, off)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_RANGE, self.pin_id)

