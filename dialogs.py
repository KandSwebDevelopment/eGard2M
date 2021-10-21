import collections
import fnmatch
import glob
import os
import pprint
import socket
import sys
from datetime import *

import numpy
import serial
import serial.tools.list_ports
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextCursor
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QListWidgetItem, QTextEdit, QTableWidgetItem
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator

from class_process import ProcessClass
from defines import *
# from main import MainWindow
from plotter import *
from status_codes import FC_MESSAGE
from ui.dialogDispatchCounter import Ui_DialogDispatchCounter
from ui.dialogDispatchInternal import Ui_DialogDispatchInternal
from functions import string_to_float, m_box, auto_capital, sound_click, minutes_to_hhmm, sound_check_out, \
    sound_error, sound_ok
from ui.dialogAccess import Ui_DialogDEmodule
from ui.dialogDispatchLoadingBay import Ui_DialogDispatchLoading
from ui.dialogDispatchOverview import Ui_DialogLogistics
from ui.dialogDispatchReports import Ui_DialogDispatchReport
from ui.dialogDispatchStorage import Ui_Form
from ui.dialogElectMeter import Ui_DialogElectMeter
from ui.dialogEngineerCommandSender import Ui_DialogEngineerCommandSender
from ui.dialogEngineerIO import Ui_DialogMessage
from ui.dialogFan import Ui_DialogFan
from ui.dialogFeedMix import Ui_DialogFeedMix
from ui.area_manual import Ui_frm_area_manual
from ui.dialogGraphEnviroment import Ui_DialogGraphEnv
from ui.dialogIOVC import Ui_Dialog_IO_VC
from ui.dialogJournal import Ui_DialogJournal
from ui.dialogJournelViewer import Ui_DialogJournalViewer
from ui.dialogOutputSettings import Ui_DialogOutputSetting
from ui.dialogPatterns import Ui_DialogPatterns
from ui.dialogProcessAdjustments import Ui_DialogProcessAdjust
from ui.dialogProcessInfo import Ui_DialogProcessInfo
from ui.dialogProcessManager import Ui_dialogProcessManager
from ui.dialogProcessPerformance import Ui_DialogProcessPreformance
from ui.dialogRemoveItem import Ui_DialogRemoveItem
from ui.dialogSeedPicker import Ui_DialogSeedPicker
from ui.dialogSensorSettings import Ui_DialogSensorSettings
from ui.dialogSettings import Ui_DialogSettings
from ui.dialogSoilSensors import Ui_DialogSoilSensors
from ui.dialogStrainFinder import Ui_DialogStrainFinder
from ui.dialogStrains import Ui_DialogStrains
from ui.dialogWaterHeaterSettings import Ui_DialogWaterHeatertSetting
from ui.dialogWorkshopSettings import Ui_DialogWorkshopSetting
from ui.dialogsysInfo import Ui_DialogSysInfo


class DialogDispatchCounter(QWidget, Ui_DialogDispatchCounter):
    def __init__(self, parent=None):
        """ :type parent: MainWindow """
        super(DialogDispatchCounter, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
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
            # play_sound(SND_CHECK_OUT_ERROR)
            sound_error()
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
        sound_check_out()
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
        self.main_panel.main_window.update_stock()
        self.main_panel.coms_interface.relay_send(NWC_STOCK_TOTAL)

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
            self.pb_start.setFocus()
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
        last = self.main_panel.db.execute_single("SELECT grams FROM {} WHERE client = {} ORDER BY date DESC".
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
        self.main_panel = parent
        self.sub = None
        self.db = parent.db
        self.reading = self.reading_last = 0
        self.jar = None
        self.is_finished = False
        self.is_return = False
        self.strain_name = ""
        self.strain_id = 0
        self.scales = self.main_panel.scales
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
        sound_check_out()
        if self.is_return:
            amount = 0 - self.reading
            t_type = "INT-R"
        else:
            amount = self.reading
            t_type = "INT"
        sql = 'UPDATE {} SET weight = weight - {} WHERE jar = "{}"'.format(DB_JARS, amount, self.jar)
        print(sql)
        self.db.execute_write(sql)
        self.main_panel.logger.save_dispatch_counter("INT", "--", self.jar, self.strain_name, self.strain_id,
                                                    self.reading, self.reading)
        self.db.execute_write('INSERT INTO {} (date, type, jar, strain, grams, client) VALUES ("'
                              '{}", "{}", "{}", {}, {}, 1)'.
                              format(DB_DISPATCH, datetime.now(), t_type, self.jar, self.strain_id, amount))
        self.is_finished = True
        self.le_weight.setText("Remove")
        self.lb_info.setText("")
        self.cb_jar.setCurrentIndex(0)
        self.main_panel.main_window.update_stock()
        self.main_panel.coms_interface.relay_send(NWC_STOCK_TOTAL)
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


class DialogDispatchLoadingBay(QDialog, Ui_DialogDispatchLoading):
    def __init__(self, parent):
        """

        :type parent: MainWindow
        """
        super(DialogDispatchLoadingBay, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.sub = None
        self.db = parent.db
        self.scales = parent.scales
        self.reading = self.reading_last = 0
        self.is_finished = False
        self.is_stored = False  # Blocks readings until jar and strain set
        self.is_reading = False  # Blocks readings until jar and strain set
        self.jar = None
        self.jar_id = 0
        self.jar_nett = 0
        self.strain_total = 0
        self.strain_id = 0
        self.process_id = 0
        self.adding_to_jar = False      # True when adding to a jar with same strain
        self.step = 0  # 0=Not started, 1=item selected waiting on empty, 2=nett stored waiting on filled
        self.empty_grams = string_to_float(self.db.get_config(CFT_DISPATCH, "empty grams", 1.5))

        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_tare.clicked.connect(lambda: self.scales.tare())
        self.cb_strain.currentIndexChanged.connect(self.change_strain)
        self.pb_store.clicked.connect(self.store)
        self.scales.new_reading.connect(self.update_reading)
        self.scales.new_uid.connect(self.new_uid)
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)

        self.pb_store.setEnabled(False)

        self.load_strain_list()
        if not self.scales.is_connected:
            self.te_jar_info.setText("Scales Not Connected")
            return
        self.te_jar_info.setText("Step 1: Select Item")
        self.scales.tare()

    @pyqtSlot(str, name='newUID')
    def new_uid(self, uid):
        if self.step == 1:
            if not self.check_uid(uid):
                self.step = 10
                # self.te_jar_info.clear()
                # self.te_jar_info.setText("This jar is not empty")
                return
            self.jar = self.db.execute_one_row(
                "SELECT jar, weight, nett, UID, strain FROM {} WHERE UID ='{}'".format(DB_JARS, uid))
            self.jar_id = self.jar[0]
            # if idx != -1:
            #     self.cb_jars.setCurrentIndex(idx)
            if self.adding_to_jar:
                self.jar_nett = self.jar[1]
                # self.te_jar_info.clear()
                self.te_jar_info.append("Step 3: Store jar contents")
                # self.le_gross.setText("Waiting")
                # self.le_weight.setText("....")
            else:
                self.jar_nett = self.jar[2]
                self.te_jar_info.clear()
                self.te_jar_info.setText("Step 3: Store nett weight")
            self.pb_store.setEnabled(True)
        if self.step == 2:
            jar = self.db.execute_one_row(
                "SELECT jar, weight, nett, UID, strain FROM {} WHERE UID ='{}'".format(DB_JARS, uid))
            if jar[0] != self.jar[0]:
                self.te_jar_info.clear()
                self.te_jar_info.setText("Incorrect jar")
                return
            self.step = 3
            self.te_jar_info.clear()
            self.te_jar_info.setText("Step 5: Store total")

    @pyqtSlot(str, name='updateReading')
    def update_reading(self, value):
        self.reading = float(value)
        if self.step == 1 or self.step == 3:
            self.le_gross.setText(str(self.reading))
            self.reading_last = self.reading
            self.le_weight.setText(str(round(self.reading - self.jar_nett, 1)))
        if self.step == 10 and self.reading < 0.5:  # Jar removed
            self.te_jar_info.clear()
            self.cb_strain.setCurrentIndex(0)
            self.te_jar_info.setText("Step 1: Select Item")
            self.step = 0
            self.le_weight.setText("")
            self.le_gross.setText("")
            self.load_strain_list()

        # if self.is_stored and self.reading < 0.5:  # Jar removed
        #     self.le_weight.setText("")
        #     self.le_gross.setText("")
        #     self.te_jar_info.setText("")
        # if not self.is_reading:
        #     return
        # if self.is_finished and self.reading < 0.2:
        #     self.is_finished = False
        # if not self.is_finished:
        #     if self.reading > 1:
        #         self.te_jar_info.setText("")
        #     self.le_gross.setText(str(self.reading))
        #     self.reading_last = self.reading
        #     self.le_weight.setText(str(round(self.reading - self.jar_nett, 1)))

    # def read(self):
    #     self.is_reading = True
    #     self.pb_read.setEnabled(False)
    #     self.pb_store.setEnabled(True)
    #     self.cb_jars.setEnabled(False)
    #     self.cb_strain.setEnabled(False)
    #     self.pb_close.setEnabled(False)
    #     self.te_jar_info.setText("Place filled jar in scales")

    def load_strain_list(self):
        # Select all the items in area 3 as it will be these to be stored
        self.cb_strain.clear()
        sql = 'SELECT s.name, s.id, a.item, a.process_id FROM {} s INNER JOIN {} ps ON s.id = ps.strain_id INNER JOIN {}' \
              ' a ON ps.process_id = a.process_id AND ps.item = a.item AND a.area = 3'. \
            format(DB_STRAINS, DB_PROCESS_STRAINS, DB_AREAS)
        rows = self.db.execute(sql)
        if len(rows) == 0:
            self.cb_strain.addItem("None Incoming", 0)
        else:
            self.cb_strain.addItem("Select", 0)
            self.process_id = rows[0][3]
        for row in rows:
            self.cb_strain.addItem("No.{}  {}".format(row[2], row[0]), row[2])  # Data is item number

    def store(self):
        if self.step == 1:
            self.step = 2
            if self.adding_to_jar:
                sql = 'UPDATE {} SET weight = {}, last_recon = "{}" WHERE jar = "{}"' \
                    .format(DB_JARS, self.reading, datetime.now(), self.jar_id)
            else:
                sql = 'UPDATE {} SET nett = {}, weight = {}, last_nett = "{}" WHERE jar = "{}"' \
                    .format(DB_JARS, self.reading, self.reading, datetime.now(), self.jar_id)
            self.db.execute_write(sql)
            self.jar_nett = self.reading
            self.te_jar_info.clear()
            self.te_jar_info.setText("Step 4: Place filled jar")
            self.le_gross.setText("Waiting")
            self.le_weight.setText("....")
            return

        if self.step == 3:
            self.step = 4
            self.strain_total = round(self.reading - self.jar_nett, 1)
            # Get strain
            sql = 'SELECT s.id FROM {} s INNER JOIN {} ps ON s.id = ps.strain_id INNER JOIN {}' \
                  ' a ON ps.process_id = a.process_id AND ps.item = a.item AND a.area = 3 AND a.item = {}'. \
                format(DB_STRAINS, DB_PROCESS_STRAINS, DB_AREAS, self.cb_strain.currentData())
            strain = self.db.execute_single(sql)
            # Store in jar
            sql = 'UPDATE {} SET weight = {}, strain = {} WHERE jar = "{}"' \
                .format(DB_JARS, self.reading, strain, self.jar_id)
            print(sql)
            self.db.execute_write(sql)
            # Store plant amount
            sql = 'UPDATE {} SET yield = {} WHERE process_id = {} AND item = {}'. \
                format(DB_PROCESS_STRAINS, self.strain_total, self.process_id, self.cb_strain.currentData())
            print(sql)
            self.db.execute_write(sql)
            # Add entry in journal
            dt = datetime.strftime(datetime.now(), '%d/%m/%y %H:%M')
            self.main_panel.area_controller.get_area_process(3).journal_write(
                "{} Number {} finished drying and {} grams stored in {}".
                format(dt, self.cb_strain.currentData(), self.strain_total, self.jar_id))
            # Call the finish item
            self.main_panel.finish_item(self.cb_strain.currentData(), self.strain_total, False)
            self.te_jar_info.setText("Remove Jar")
            self.step = 10
            self.adding_to_jar = False
            # self.cb_jars.setEnabled(True)
            self.pb_store.setEnabled(False)
            # self.pb_read.setEnabled(True)
            sound_ok()
            # play_sound(SND_OK)
            # self.load_jars_list()
            self.main_panel.main_window.update_stock()
            self.main_panel.coms_interface.relay_send(NWC_STOCK_TOTAL)
            self.load_strain_list()

    def finish(self):  # Done
        self.le_weight.setText("")
        self.pb_store.setEnabled(False)
        self.pb_read.setEnabled(False)
        # self.cb_jars.setEnabled(True)
        self.cb_strain.setEnabled(True)
        self.cb_strain.setCurrentIndex(0)
        self.pb_close.setEnabled(True)
        self.te_jar_info.setText("")
        self.le_gross.setText("")
        self.strain_total = 0
        # self.main_panel.finish_item(self.cb_strain.currentData())
        self.load_jars_list()
        self.load_strain_list()
        self.pb_done.setEnabled(False)

    # def change_jar(self):
    #     sql = 'SELECT jar, strain, weight - nett as gross, nett FROM {} WHERE  jar = "{}"'. \
    #         format(DB_JARS, self.cb_jars.currentData())
    #     rows = self.db.execute_one_row(sql)
    #     if rows is None:
    #         return
    #     if rows[2] >= self.empty_grams:
    #         self.msg.setText(
    #             "This jar is not empty, it should still have {}grams.<br>Please check".format(round(rows[2], 1)))
    #         self.msg.setWindowTitle("Jar Not Empty")
    #         self.msg.setStandardButtons(QMessageBox.Cancel)
    #         self.msg.setDefaultButton(QMessageBox.Cancel)
    #         self.msg.exec_()
    #         return False
    #     self.jar_nett = rows[3]
    #     self.check_start()

    def change_strain(self):
        if self.cb_strain.currentIndex() > 0:
            self.step = 1
            self.te_jar_info.clear()
            self.te_jar_info.setText("Step 2: Place empty jar")
            sql = 'SELECT strain_id FROM {} WHERE process_id = {} AND item = {}'. \
                format(DB_PROCESS_STRAINS, self.process_id, self.cb_strain.currentData())
            self.strain_id = self.db.execute_single(sql)

    # def load_jars_list(self):
    #     self.cb_jars.clear()
    #     sql = "SELECT jar, strain FROM {} WHERE weight - nett <= 1 ORDER BY jar".format(DB_JARS)
    #     rows = self.db.execute(sql)
    #
    #     self.cb_jars.blockSignals(True)
    #     if rows is None:
    #         self.cb_jars.addItem("None Available", "000")
    #     else:
    #         self.cb_jars.addItem("Select", "000")
    #     for row in rows:
    #         self.cb_jars.addItem(row[0], row[0])
    #     self.cb_jars.blockSignals(False)

    def check_uid(self, uid) -> bool:
        """
        Checks if a jar with the UID is empty
        :param uid: The jar UID to check
        :type uid: str
        :return: True if ok to use jar
        :rtype:
        """
        row = self.db.execute_one_row("SELECT weight - nett, strain FROM {} WHERE UID = '{}'".format(DB_JARS, uid))
        gross = row[0]
        if gross is None:
            self.msg.setText("This tag has not been registered {}".format(uid))
            self.msg.setWindowTitle("Unregistered UID")
            self.msg.setStandardButtons(QMessageBox.Cancel)
            self.msg.setDefaultButton(QMessageBox.Cancel)
            self.msg.exec_()
            return False
        if gross >= self.empty_grams:
            if self.strain_id == row[1]:
                self.te_jar_info.setText("This jar contains {}g of {}, you will be adding to it".
                                         format(round(gross, 1), self.cb_strain.currentText()))
                self.adding_to_jar = True
                return True
            else:
                self.te_jar_info.setText("This jar contains a different strain and can NOT be used")
                return False
        return True

    def check_start(self):
        if self.cb_strain.currentIndex() > 0:
            self.pb_done.setEnabled(True)
            self.pb_read.setEnabled(True)
            # self.te_jar_info.setText("Place Vessel")
        else:
            self.pb_done.setEnabled(False)
            self.pb_read.setEnabled(False)


class DialogDispatchStorage(QDialog, Ui_Form):
    def __init__(self, parent):
        """

        :type parent: MainWindow
        """
        super(DialogDispatchStorage, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.main_panel = parent
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
        self.scales = self.main_panel.scales
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
        self.main_panel.main_window.update_stock()
        self.main_panel.coms_interface.relay_send(NWC_STOCK_TOTAL)

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
        sound_ok()
        # play_sound(SND_OK)
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
        self.main_panel.db.execute_write(sql)
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
        self.main_panel = parent
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
        self.le_weekly.editingFinished.connect(self.change_weekly)

    def refresh(self):
        self.load_stock()
        self.load_clients()
        # self.get_up_coming()
        self.get_future()
        self.load_available()

    def change_weekly(self):
        self.weekly_total = string_to_float(self.le_weekly.text())
        self.get_future()

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

    def get_up_coming(self):
        self.te_upcomming.clear()
        self.up_coming.clear()
        for loc in range(3, 0, -1):
            if self.main_panel.area_controller.area_has_process(loc):
                d = self.main_panel.area_controller.get_area_process(loc).end
                q = self.main_panel.area_controller.get_area_process(loc).quantity
                if d.date() > datetime.now().date():
                    getattr(self, "lbl_upcoming_{}".format(loc)).setText(
                        "{} > {}".format(datetime.strftime(d, "%d/%m/%y"), q))
                    getattr(self, "le_upcoming_total_{}".format(loc)).setText("{}".format(q * self.estimate_per_plant))
                    # getattr(self, "ck_upcoming_{}".format(loc)).setChecked(True)
                    self.up_coming.append([d, q, loc])
                    # self.up_coming_yield.append(q)

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
        self.main_panel = parent
        self.sub = None
        self.db = self.main_panel.db
        self.le_ml_1.setFixedWidth(30)
        self.feed_control = parent.feed_controller
        self.area = area  # Current area
        self.mix_number = 1  # The mix number working on
        self.is_changed = False
        self.show_next = False  # True when next recipe is to be displayed
        self.holding = None  # Holds stylesheet for mouse over event
        self.holding_1 = None  # Holds stylesheet for mouse over event
        self.pb_close.clicked.connect(self.pre_close)
        for x in range(1, 9):
            getattr(self, "ck_fed_%i" % (x + 10)).clicked.connect(self.change_qty)

        self.cb_nutrients_1.addItem("", 0)
        for n in self.feed_control.nutrients:
            self.cb_nutrients_1.addItem(self.feed_control.nutrients[n], n)

        self.tw_mixes.setStyleSheet("""QTabBar::tab:selected {background: green}""")
        # self.lbl_info.setToolTip("Next")
        self.lbl_next.installEventFilter(self)
        if 0 < self.area < 3:
            self.load(self.area)

        self.lw_recipe_1.doubleClicked.connect(self.load_item)
        self.pb_store_n_1.clicked.connect(self.store_nutrient)
        self.pb_reset_nutrients.clicked.connect(self.reset_nutrients)
        self.pb_reset_water.clicked.connect(self.reset_water)
        self.le_total_1.editingFinished.connect(self.calculate_each)
        self.le_each_1.editingFinished.connect(self.calculate_total)
        self.pb_store_w_1.clicked.connect(self.store_litres)
        self.cb_feeds.currentIndexChanged.connect(self.change_use_for)
        self.pb_add.clicked.connect(self.add_blank_tab)
        self.pb_copy.clicked.connect(self.add_mix_tab)
        self.pb_delete.clicked.connect(self.delete_mix)
        self.tw_mixes.currentChanged.connect(self.change_mix_tab)

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

    def change_mix_tab(self):
        m = self.tw_mixes.currentIndex()
        print(m)
        self.display_mix(m + 1)
        if m > 0:
            self.pb_delete.setEnabled(True)
        else:
            self.pb_delete.setEnabled(False)

    def add_mix_tab(self):
        count = self.feed_control.get_mix_count(self.area)
        idx = self.tw_mixes.addTab(QWidget(), "Feed {}".format(count + 1))
        self.feed_control.feeds[self.area].add_new_mix()
        self.tw_mixes.setCurrentIndex(idx)
        self.display_mix(count + 1)
        self.is_changed = True
        self.main_panel.update_next_feeds()

    def add_blank_tab(self):
        count = self.feed_control.get_mix_count(self.area)
        idx = self.tw_mixes.addTab(QWidget(), "Feed {}".format(count + 1))
        self.feed_control.feeds[self.area].add_blank_mix()
        self.tw_mixes.setCurrentIndex(idx)
        self.display_mix(count + 1)
        self.is_changed = True
        self.main_panel.update_next_feeds()

    def delete_mix(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Delete Mix")
        msg.setText("Confirm you wish to delete this mix")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        if msg.exec_() == QMessageBox.No:
            return

        self.feed_control.feeds[self.area].delete_mix(self.mix_number)
        self.feed_control.feeds[self.area].load_mixes()
        self.load(self.area)
        # m = self.tw_mixes.currentIndex()
        # self.tw_mixes.setCurrentIndex(0)
        # self.tw_mixes.removeTab(m)
        # for i in range(self.mix_number, self.feed_control.feeds[self.area].get_mix_count()):
        #     self.tw_mixes.setTabText(i, "Feed {}".format(i))
        self.is_changed = True

    def store_nutrient(self):
        nid = self.cb_nutrients_1.currentData()
        if nid == 0:
            return
        self.feed_control.feeds[self.area].change_recipe_item(self.mix_number, (nid, string_to_float(self.le_ml_1.text())))
        self._load()
        self.cb_nutrients_1.setCurrentIndex(0)
        self.le_ml_1.clear()
        self.is_changed = True
        # self.main_panel.coms_interface.send_data(NWC_FEED_ADJUST, MODULE_IO, self.process.location)

    def store_litres(self):
        if string_to_float(self.le_total_1.text()) == 0 or string_to_float(self.le_each_1.text()) == 0:
            sound_error()
            return
        self.feed_control.feeds[self.area].change_mix_water(self.mix_number, string_to_float(self.le_each_1.text()))
        self._load()
        self.le_each_1.clear()
        self.le_total_1.clear()
        self.is_changed = True
        self.main_panel.lbl_water_required.setText(
            str(self.main_panel.main_window.feed_controller.get_next_water_required()))

    def change_qty(self):
        count = 0
        items = collections.defaultdict()
        for x in range(1, self.feed_control.feeds[self.area].qty_org + 1):
            if getattr(self, "ck_fed_%i" % (x + 10)).isChecked():
                count += 1
                items[x] = 1
        self.feed_control.change_items(self.area, self.mix_number, items)

        for x in range(1, self.feed_control.feeds[self.area].qty_org + 1):
            self.check_included(x)

        self._load()
        self.is_changed = True

    def load_item(self):  # Loads off dbl click of list
        nid = self.lw_recipe_1.currentItem().data(Qt.UserRole)
        if nid == WATER_ONLY_IDX:
            return
        r = self.feed_control.get_recipe_item(self.area, self.mix_number, nid)
        self.le_ml_1.setText(str(r[1]))
        nid = self.cb_nutrients_1.findData(nid)
        if nid != -1:
            self.cb_nutrients_1.setCurrentIndex(nid)

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
        self.tw_mixes.clear()
        for t in range(1, count + 1):
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
            else:
                getattr(self, "ck_fed_%i" % (x + 10)).setChecked(False)
                # getattr(self, "ck_fed_%i" % (x + 10)).setEnabled(False)
            self.check_included(x)
            getattr(self, "ck_fed_%i" % (x + 10)).blockSignals(False)

        # Set number of feeds combo
        self.cb_feeds.blockSignals(True)
        self.cb_feeds.clear()
        for x in range(1, self.main_panel.feed_controller.get_feeds_remaining(self.area) + 1):
            self.cb_feeds.addItem(str(x), x)
        idx = self.cb_feeds.findData(self.main_panel.feed_controller.get_feeds_remaining(self.area))
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
            if recipe == WATER_ONLY_IDX:
                # Water only recipe
                lw_item = QListWidgetItem(str(x) + " Water only")
            else:
                # Normal recipe
                for nid in recipe:      # nid = (nid, mls)
                    # ri - 0=nid, 1=ml, 2=L, 3=nid, 4=freq, 5=adj ml, 6=adj remaining
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
                            lw_item.setForeground(Qt.lightGray)
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
                                str(x) + "   " + str(nid[1]) + "ml each (" + str(round(diff, 1)) +
                                ")   A total of " + str(
                                    round((nid[1] + 0) * feed_data[self.mix_number]["water total"], 1))
                                + "ml of " + self.feed_control.nutrients[nid[0]])
                            lw_item.setBackground(Qt.darkCyan)
                        else:  # Normal recipe item
                            lw_item = QListWidgetItem(str(x) + "   " + str(nid[1]) + "ml each.  A total of " + str(
                                round(nid[1] * feed_data[self.mix_number]["water total"], 1)) + "ml of " +
                                                      self.feed_control.nutrients[nid[0]])

                    v_item = QVariant(nid[0])
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
        cf = self.main_panel.feed_controller.check_item_included(self.area, item)
        if cf == 0:
            getattr(self, "ck_fed_%i" % (item + 10)).setStyleSheet("background-color: Yellow;")
        elif cf == 2:
            getattr(self, "ck_fed_%i" % (item + 10)).setStyleSheet("background-color: Blue;")
        elif cf == 1:
            getattr(self, "ck_fed_%i" % (item + 10)).setStyleSheet(None)

    def change_use_for(self):
        self.feed_control.feeds[self.area].change_cycles(self.mix_number, self.cb_feeds.currentData())
        self.is_changed = True

    def reset_nutrients(self):
        self.feed_control.feeds[self.area].reset_nutrients(self.mix_number)
        self._load()
        self.is_changed = True

    def reset_water(self):
        self.feed_control.feeds[self.area].reset_water(self.mix_number)
        self._load()
        self.is_changed = True

    def calculate_each(self):
        if self.le_total_1.text() == "":
            return
        v = string_to_float(self.le_total_1.text()) / len(
            self.feed_control.feeds[self.area].area_data['mixes'][self.mix_number]['items'])
        self.le_each_1.blockSignals(True)
        self.le_each_1.setText(str(v))
        self.le_each_1.blockSignals(False)

    def calculate_total(self):
        if self.le_each_1.text() == "":
            return
        v = string_to_float(self.le_each_1.text()) * len(
            self.feed_control.feeds[self.area].area_data['mixes'][self.mix_number]['items'])
        self.le_total_1.blockSignals(True)
        self.le_total_1.setText(str(v))
        self.le_total_1.blockSignals(False)

    def pre_close(self):
        # if self.is_changed:
        #     self.main_panel.coms_interface.relay_send(NWC_PROCESS_MIX_CHANGE, self.location)
        self.sub.close()


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
        self.db.set_config_both(CFT_AREA, "mode {}".format(self.area), self.manual)
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


class DialogSysInfo(QDialog, Ui_DialogSysInfo):
    def __init__(self, parent):
        super(DialogSysInfo, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.main_panel = parent
        self.coms_interface = self.main_panel.coms_interface

        if self.main_panel.master_mode == MASTER:
            text = "Master"
        else:
            text = "Slave"
        text = "<table cellpadding='3' border='0'><tr><td width='30%'>Operation Mode</td><td>{}</td></tr>".format(text)
        text += "<tr><td>PC Name</td><td>{}</td></tr>".format(socket.gethostname())
        text += "<tr><td>IP Address</td><td>{}</td></tr>"   # .format(self.server.server_ip_str)
        text += "<tr><td>Server Status</td><td>{}</td></tr>"    # .format(FC_MESSAGE[self.server.server_status]['message'])
        text += "<tr><td>Port</td><td>{}</td></tr>" # .format(self.server.port)
        text += "<tr><td colspan='2'>Interface Units</td></tr>"
        text += "<tr><td>UPD Server</td><td></td></tr>"
        text += "<tr><td>IP</td><td>{}</td></tr>".format(self.coms_interface.udp_server.remote_ip)
        text += "<tr><td>Port</td><td>{}</td></tr>".format(self.coms_interface.udp_server.remote_port)
        text += "<tr><td>UPD Client</td><td></td></tr>"
        text += "<tr><td>IP</td><td>{}</td></tr>".format(self.coms_interface.this_ip)
        text += "<tr><td>Port</td><td>{}</td></tr>".format(
            self.coms_interface.this_port + self.coms_interface.udp_client.id - 1)
        text += "<tr><td>UPD Relay</td><td></td></tr>"
        text += "<tr><td>IP</td><td>{}</td></tr>".format(self.coms_interface.this_ip)
        text += "<tr><td>Port</td><td>{}</td></tr>".format(
            self.coms_interface.this_port + self.coms_interface.udp_relay.id - 1)
        text += "<tr><td>I/O Module</td><td></td></tr>"
        text += "<tr><td>IP</td><td>{}</td></tr>".format(self.coms_interface.io_ip)
        text += "<tr><td>Port</td><td>{}</td></tr>".format(self.coms_interface.io_port)
        text += "<tr><td>D/E Module</td><td></td></tr>"
        text += "<tr><td>IP</td><td>{}</td></tr>".format(self.coms_interface.de_ip)
        text += "<tr><td>Port</td><td>{}</td></tr>".format(self.coms_interface.de_port)
        text += "<tr><td>Other PC</td><td></td></tr>"
        text += "<tr><td>IP</td><td>{}</td></tr>".format(self.coms_interface.slave_ip)
        text += "<tr><td>Port</td><td>{}</td></tr>".format(self.coms_interface.slave_port)
        text += "<tr><td>Other Relay</td><td></td></tr>"
        text += "<tr><td>IP</td><td>{}</td></tr>".format(self.coms_interface.slave_ip)
        text += "<tr><td>Port</td><td>{}</td></tr>".format(self.coms_interface.pc_relay_port)
        # text += "<tr><td>D/E</td><td>{}</td></tr>".format(self.client.de_ip)
        # text += "<tr><td>Client Status</td><td>{}</td></tr>".format(FC_MESSAGE[self.server.client_status]['message'])
        text += "</table>"
        self.te_info.setHtml(text)


class DialogJournal(QDialog, Ui_DialogJournal):
    def __init__(self, process, parent):
        super(DialogJournal, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.pbsave.clicked.connect(self.add)
        self.pbclose.clicked.connect(lambda: self.sub.close())
        self.main_panel = parent
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
        self.main_panel.coms_interface.send_command(NWC_JOURNAL_ADD, self.process.location, entry)
        self.tenew.setText("")


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
        self.cb_command.addItem("Switch", CMD_SWITCH)
        self.cb_command.addItem("Switch Position", COM_SWITCH_POS)
        self.cb_command.addItem("One Wire Scan", COM_OW_SCAN)
        self.cb_command.addItem("One Wire Query", COM_OW_COUNT)
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
        # if manual:
        self.send_(cmd, v1, v2, v3, v4, pri, to)
        return
        # if cmd == CMD_SWITCH:
        #     if v1 == "" or v2 == "":
        #         return
        #     self.my_parent.coms_interface.send_command(CMD_SWITCH, int(v1), int(v2), pri, to)
        # if cmd == CMD_VALVE:
        #     if v1 == "" or v2 == "":
        #         return
        #     if int(v2) > 90:
        #         return
        #     self.my_parent.coms_interface.send_command(CMD_VALVE, int(v1), int(v2), pri, to)

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
        self.show_io = True
        self.show_io_to = True
        self.show_de = True
        self.show_de_to = True
        self.show_relay = True
        self.show_relay_to = True
        self.show_relay_to = True
        self.show_fu = True
        self.show_fu_to = True

        self.ck_from_io.clicked.connect(self.check_to_show)
        self.ck_from_de.clicked.connect(self.check_to_show)
        self.ck_from_fu.clicked.connect(self.check_to_show)
        self.ck_from_rl.clicked.connect(self.check_to_show)
        self.ck_to_de.clicked.connect(self.check_to_show)
        self.ck_to_fu.clicked.connect(self.check_to_show)
        self.ck_to_io.clicked.connect(self.check_to_show)
        self.ck_to_rl.clicked.connect(self.check_to_show)
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_clear.clicked.connect(self.clear)

        self.my_parent.coms_interface.update_received.connect(self.incoming)
        self.my_parent.coms_interface.update_cmd_issued.connect(self.outgoing)
        self.setWindowTitle("I/O Data")
        self.te_message.append(" ")

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

    def check_incoming(self, sender) -> bool:
        port = sender[1]
        if port == self.my_parent.coms_interface.io_port and not self.show_io:
            return False
        if port == self.my_parent.coms_interface.de_port and not self.show_de:
            return False
        if port == self.my_parent.coms_interface.pc_relay_port and not self.show_relay:
            return False
        if port == self.my_parent.coms_interface.fu_port and not self.show_fu:
            return False
        return True

    def check_outgoing(self, sender) -> bool:
        # ip = sender[0]
        port = sender[1]
        if port == self.my_parent.coms_interface.io_port and not self.show_io_to:
            return False
        if port == self.my_parent.coms_interface.de_port and not self.show_de_to:
            return False
        if port == self.my_parent.coms_interface.fu_port and not self.show_fu_to:
            return False
        if port == self.my_parent.coms_interface.slave_port and not self.show_relay_to:
            return False
        return True

    def check_to_show(self):
        print(self.sender().isChecked())
        if self.ck_to_rl.isChecked():
            self.show_relay_to = True
        else:
            self.show_relay_to = False
        if self.ck_from_rl.isChecked():
            self.show_relay = True
        else:
            self.show_relay = False

        if self.ck_to_io.isChecked():
            self.show_io_to = True
        else:
            self.show_io_to = False

        if self.ck_to_de.isChecked():
            self.show_de_to = True
        else:
            self.show_de_to = False
        if self.ck_from_de.isChecked():
            self.show_de = True
        else:
            self.show_de = False

        if self.ck_to_fu.isChecked():
            self.show_fu_to = True
        else:
            self.show_fu = False
        if self.ck_from_fu.isChecked():
            self.show_fu = True
        else:
            self.show_fu = False

        if self.ck_from_io.isChecked():
            self.show_io = True
        else:
            self.show_io = False

    def clear(self):
        self.te_message.clear()
        self.te_message.append("")

    def check_for_reg(self, data) -> bool:
        if not self.ck_hide_reg.isChecked():
            return True
        for cmd in [COM_SENSOR_READ, COM_SOIL_READ, COM_OTHER_READINGS, COM_READ_KWH, COM_WATTS, COM_FANS, NWC_MESSAGE]:
            if cmd in data:
                return False
        return True

    @pyqtSlot(str, tuple)
    def incoming(self, data, sender):
        if self.check_for_reg(data):
            if self.check_incoming(sender):
                data = data.replace("<", "")
                data = data.replace(">", "")
                if sender[1] == self.my_parent.coms_interface.io_port:
                    colour = "background-color: #29A329;"
                elif sender[1] == self.my_parent.coms_interface.de_port:
                    colour = "background-color: #FF5050;"
                elif sender[1] == self.my_parent.coms_interface.fu_port:
                    colour = "background-color: #0066FF;"
                elif sender[1] == self.my_parent.coms_interface.pc_relay_port:
                    colour = "background-color: #E6E600;"
                else:
                    colour = "background-color: #999966;"
                self.te_message.append(
                    "<p style='" + colour + "'>" + str(data) + " <b>from</b> " + str(sender) + "</p>")

    @pyqtSlot(str, tuple)
    def outgoing(self, data, destination):
        if self.check_for_reg(data):
            if self.check_outgoing(destination):
                if len(data) > 0:
                    if destination[1] == self.my_parent.coms_interface.io_port:
                        colour = "background-color: #85E085;"
                    elif destination[1] == self.my_parent.coms_interface.de_port:
                        colour = "background-color: #FFB3B3;"
                    elif destination[1] == self.my_parent.coms_interface.fu_port:
                        colour = "background-color: #80B3FF;"
                    elif destination[1] == self.my_parent.coms_interface.slave_port:
                        colour = "background-color: #FFFF80;"
                    else:
                        colour = "background-color: #C2C2A3;"
                    data = data.replace('>', '')
                    data = data.replace('<', '')
                    self.te_message.append(
                        "<p style='" + colour + ";'>" + str(data) + " <b>to</b> " + str(destination) + "</p>")

    @pyqtSlot(list, list)
    def raw_update_c(self, priorities, commands):
        if len(priorities) > 0:
            self.te_message.append(
                "<p style='background-color: LightYellow;'>P > " + self.split_commands(priorities) + "</p>")
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


class DialogIOVC(QDialog, Ui_Dialog_IO_VC):
    def __init__(self, parent):
        super(DialogIOVC, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.main_window = parent
        self.db = self.main_window.db

        self.sw_que = collections.defaultdict(int)
        self.sw_que = {0, 8, 9, 30, 15, 1, 7, 4, 31, 14}
        self.main_window.coms_interface.update_switch_pos.connect(self.update_switch)
        self.get_set()
        # self.request()
        self.pb_request.clicked.connect(self.request)

    def get_set(self):
        for a in range(1, 3):
            getattr(self, "le_out_s_{}_0".format(a)).setText(
                "Off" if self.main_window.area_controller.get_light_status(a) == 0 else "On")

    @pyqtSlot(int, int, int, name="updateSwitch")
    def update_switch(self, sw, state, module):
        if module == MODULE_IO:
            if sw == OUT_LIGHT_1:
                getattr(self, "le_out_a_{}_0".format(1)).setText("Off" if state == 0 else "On")
            elif sw == OUT_LIGHT_2:
                getattr(self, "le_out_a_{}_0".format(2)).setText("Off" if state == 0 else "On")
            elif sw == OUT_HEATER_11:
                self.le_out_a_1_1.setText("Off" if state == 0 else "On")
            elif sw == OUT_HEATER_12:
                self.le_out_a_1_2.setText("Off" if state == 0 else "On")
            elif sw == OUT_AUX_1:
                self.le_out_a_1_3.setText("Off" if state == 0 else "On")
            elif sw == OUT_SPARE_1:
                self.le_out_a_1_4.setText("Off" if state == 0 else "On")

            elif sw == OUT_HEATER_21:
                self.le_out_a_2_1.setText("Off" if state == 0 else "On")
            elif sw == OUT_HEATER_22:
                self.le_out_a_2_2.setText("Off" if state == 0 else "On")
            elif sw == OUT_AUX_2:
                self.le_out_a_2_3.setText("Off" if state == 0 else "On")
            elif sw == OUT_SPARE_2:
                self.le_out_a_2_4.setText("Off" if state == 0 else "On")

    def request(self):
        return
        for sw in self.sw_que:
            self.main_window.coms_interface.send_data(COM_SWITCH_POS, True, MODULE_IO, sw)


class DialogGraphEnv(QDialog, Ui_DialogGraphEnv):
    def __init__(self, parent):
        super(DialogGraphEnv, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.main_window = parent
        self.db = self.main_window.db

        self.logger = self.main_window.logger
        self.live_timer = QTimer()
        self.live_timer.timeout.connect(self.auto_refresh)
        self.live_timer.setInterval(120000)
        self.times = []
        self.fan_times = []
        self.values = collections.defaultdict(list)
        self.output_values = collections.defaultdict(list)
        self.fan_values = collections.defaultdict(list)
        self.power_values = collections.defaultdict(list)
        self.weeks_use = collections.defaultdict()
        self.legend = []
        self.logs = []
        self.values['oh'] = []
        self.values['ot'] = []
        self.values['1h'] = []
        self.values['1t'] = []
        self.values['1c'] = []
        self.values['1r'] = []
        self.output_values['1h1'] = []
        self.output_values['1h2'] = []
        self.output_values['1a'] = []
        self.output_values['1s'] = []
        self.output_values['2h1'] = []
        self.output_values['2h2'] = []
        self.output_values['2a'] = []
        self.output_values['2s'] = []
        self.output_values['3h'] = []
        self.output_values['ws'] = []
        self.output_values['wh1'] = []
        self.output_values['wh2'] = []
        self.fan_values['1in'] = []
        self.fan_values['1sw'] = []
        self.fan_values['1rv'] = []
        self.fan_values['2in'] = []
        self.fan_values['2sw'] = []
        self.fan_values['2rv'] = []
        self.power_values['watts'] = []
        self.plot = None
        self.ax2 = None
        self.plot_outputs = None
        self.plot_fans = None
        self.plot_power = None

        self.pb_close_2.clicked.connect(lambda: self.sub.close())
        self.pb_close_3.clicked.connect(lambda: self.sub.close())
        self.pb_close_4.clicked.connect(lambda: self.sub.close())
        for y in range(2021, datetime.now().year + 1):
            self.cb_year.addItem(str(y), y)
            self.cb_year_2.addItem(str(y), y)
            self.cb_year_3.addItem(str(y), y)
            self.cb_year_4.addItem(str(y), y)
        self.cb_year.setCurrentIndex(self.cb_year.findData(datetime.now().year))
        self.cb_year_2.setCurrentIndex(self.cb_year_2.findData(datetime.now().year))
        self.cb_year_3.setCurrentIndex(self.cb_year_3.findData(datetime.now().year))
        self.cb_year_4.setCurrentIndex(self.cb_year_4.findData(datetime.now().year))
        i = 1
        for m in MONTHS:
            self.cb_month.addItem(m, i)
            self.cb_month_2.addItem(m, i)
            self.cb_month_3.addItem(m, i)
            self.cb_month_4.addItem(m, i)
            i += 1
        for c in range(1, 5):
            ctrl = getattr(self, "cb_limit_{}".format(c))
            ctrl.addItem("All", 0)
            ctrl.addItem("30", -15)
            ctrl.addItem("60", -30)
            ctrl.addItem("2hrs", -60)
            ctrl.addItem("4hrs", -120)
            ctrl.addItem("6hrs", -180)
            ctrl.addItem("8hrs", -240)
        ctrl = self.cb_limit_3
        ctrl.addItem("All", 0)
        ctrl.addItem("1", -250)
        ctrl.addItem("2", -500)
        ctrl.addItem("3", -750)
        ctrl.addItem("4", -1000)
        ctrl.addItem("5", -1500)
        ctrl.addItem("6", -2000)
        self.cb_month.setCurrentIndex(self.cb_month.findData(datetime.now().month))
        self.cb_month_2.setCurrentIndex(self.cb_month_2.findData(datetime.now().month))
        self.cb_month_3.setCurrentIndex(self.cb_month_3.findData(datetime.now().month))
        self.cb_month_4.setCurrentIndex(self.cb_month_4.findData(datetime.now().month))
        self.cb_month.currentIndexChanged.connect(lambda: self.load_available_logs("cvs"))
        self.cb_month_2.currentIndexChanged.connect(lambda: self.load_available_logs("opd"))
        self.cb_month_3.currentIndexChanged.connect(lambda: self.load_available_logs("fan"))
        self.cb_month_4.currentIndexChanged.connect(lambda: self.load_available_logs("pwr"))
        self.load_available_logs("cvs")
        self.load_available_logs("opd")
        self.load_available_logs("fan")
        self.load_available_logs("pwr")
        # self.cb_logs.currentIndexChanged.connect(self.load_log)
        self.pb_reload.clicked.connect(lambda: self.load_log(1))
        self.pb_reload_2.clicked.connect(lambda: self.load_log(2))
        self.pb_reload_3.clicked.connect(lambda: self.load_log(3))
        self.pb_reload_4.clicked.connect(lambda: self.load_log(4))
        self.pb_refresh.clicked.connect(self.plot_sensors)
        self.pb_refresh_2.clicked.connect(self.outputs_plot)
        self.pb_refresh_3.clicked.connect(self.fans_plot)
        self.pb_refresh_4.clicked.connect(self.power_plot)
        self.ck_live.clicked.connect(self.go_live)
        self.ck_tuning.clicked.connect(lambda: self.load_available_logs("fan"))

    def load_available_logs(self, f_type):
        if f_type == "cvs":
            self.cb_logs.blockSignals(True)
            self.cb_logs.clear()
            m = str(self.cb_month.currentData()).zfill(2)
        elif f_type == "opd":
            self.cb_logs_2.blockSignals(True)
            self.cb_logs_2.clear()
            m = str(self.cb_month_2.currentData()).zfill(2)
        elif f_type == "fan":
            self.cb_logs_3.blockSignals(True)
            self.cb_logs_3.clear()
            m = str(self.cb_month_3.currentData()).zfill(2)
            if self.ck_tuning.isChecked():
                f_type = "ftl"
        elif f_type == "pwr":
            self.cb_logs_4.blockSignals(True)
            self.cb_logs_4.clear()
            m = str(self.cb_month_4.currentData()).zfill(2)
        pattern = str(self.cb_year.currentData()) + m + "[0-9][0-9]." + f_type
        self.logs = fnmatch.filter(os.listdir(self.logger.log_path), pattern)
        self.logs.reverse()
        for lg in self.logs:
            s = "{}-{}-{}".format(lg[6:8], lg[4:6], lg[0:4])
            if f_type == "cvs":
                self.cb_logs.addItem(s, lg)
                self.cb_logs.blockSignals(False)
            elif f_type == "opd":
                self.cb_logs_2.addItem(s, lg)
                self.cb_logs_2.blockSignals(False)
            elif f_type == "fan" or f_type == "ftl":
                self.cb_logs_3.addItem(s, lg)
                self.cb_logs_3.blockSignals(False)
            elif f_type == "pwr":
                self.cb_logs_4.addItem(s, lg)
                self.cb_logs_4.blockSignals(False)

    def go_live(self):
        if self.ck_live.isChecked():
            self.live_timer.start()
            self.cb_logs.setEnabled(False)
        else:
            self.live_timer.stop()
            self.cb_logs.setEnabled(True)

    def auto_refresh(self):
        self._load_sensor_log(self.logger.data_filename)
        self.plot_sensors()

    def load_log(self, tab):
        if tab == 1:
            log = self.cb_logs.currentData()
            self._load_sensor_log(log)
        if tab == 2:
            log = self.cb_logs_2.currentData()
            self._load_output_log(log)
        if tab == 3:
            log = self.cb_logs_3.currentData()
            self._load_fan_log(log)
        if tab == 4:
            log = self.cb_logs_4.currentData()
            self._load_power_log(log)

    def _load_sensor_log(self, log):
        txt = self.logger.get_log(LOG_DATA, log)
        if len(txt) < 20:
            return
        values = []
        self.values.clear()
        self.times = []
        for row in txt:
            if row == "":
                break
            self.times.append(row[0: 5])
            row = row[6:]
            if row[0] == ",":
                row = row[1:]
            v = row.split(",")
            values.append(v)
        for r in values:
            if len(r) < 13:
                break
            self.values['1h'].append(string_to_float(r[0]))
            self.values['1t'].append(string_to_float(r[1]))
            self.values['1c'].append(string_to_float(r[2]))
            self.values['1r'].append(string_to_float(r[3]))
            self.values['2h'].append(string_to_float(r[4]))
            self.values['2t'].append(string_to_float(r[5]))
            self.values['2c'].append(string_to_float(r[6]))
            self.values['2r'].append(string_to_float(r[7]))
            self.values['dh'].append(string_to_float(r[8]))
            self.values['dt'].append(string_to_float(r[9]))
            self.values['ws'].append(string_to_float(r[10]))
            self.values['oh'].append(string_to_float(r[11]))
            self.values['ot'].append(string_to_float(r[12]))

    def _load_output_log(self, log):
        txt = self.logger.get_log(LOG_DATA, log)
        if len(txt) < 20:
            return
        values = []
        self.output_values.clear()
        self.times = []
        for row in txt:
            if row == "":
                break
            self.times.append(row[0: 5])
            row = row[6:]
            if row[0] == ",":
                row = row[1:]
            v = row.split(",")
            values.append(v)
        for r in values:
            if len(r) < 12:
                break
            self.output_values['1h1'].append(string_to_float(r[0]))
            self.output_values['1h2'].append(string_to_float(r[1]) + 2)
            self.output_values['1a'].append(string_to_float(r[2]) + 4)
            self.output_values['1s'].append(string_to_float(r[3]) + 6)
            self.output_values['2h1'].append(string_to_float(r[4]) + 8)
            self.output_values['2h2'].append(string_to_float(r[5]) + 10)
            self.output_values['2a'].append(string_to_float(r[6]) + 12)
            self.output_values['2s'].append(string_to_float(r[7]) + 14)
            self.output_values['h3'].append(string_to_float(r[8]) + 16)
            self.output_values['ws'].append(string_to_float(r[9]) + 18)
            self.output_values['wh1'].append(string_to_float(r[10]) + 20)
            self.output_values['wh2'].append(string_to_float(r[11]) + 22)

    def _load_power_log(self, log):
        txt = self.logger.get_log(LOG_DATA, log)
        values = []
        self.power_values.clear()
        self.times = []
        start = 0
        for row in txt:
            if row == "":
                break
            self.times.append(row[0: 5])
            row = row[6:]
            v = row.split(",")
            if start == 0:
                start = string_to_float(v[1])
            self.power_values['watts'].append(string_to_float(v[0]))
        self.le_units_used.setText(str(round(string_to_float(v[1]) - start, 2)))

    def _load_fan_log(self, log):
        txt = self.logger.get_log(LOG_DATA, log)
        # if len(txt) < 20:
        #     return
        # values = []
        self.fan_values.clear()
        self.times = []
        # self.fan_times = []
        for row in txt:
            if row == "":
                break
            self.times.append(row[0: 5])
            row = row[6:]
            v = row.split(",")
            self.fan_values['1in'].append(string_to_float(v[0]))
            self.fan_values['1sw'].append(string_to_float(v[1]))
            self.fan_values['1rv'].append(string_to_float(v[2]))
            self.fan_values['2in'].append(string_to_float(v[3]))
            self.fan_values['2sw'].append(string_to_float(v[4]))
            self.fan_values['2rv'].append(string_to_float(v[5]))

    def get_limit(self, values, limit):
        if limit == 0:
            return values
        return values[limit:]

    def plot_sensors(self):
        self.plot = MplWidget(self.wg_graph_1, 12, 4.5)
        self.plot.canvas.axes.cla()
        if self.ax2 is not None:
            self.ax2.cla()
            self.ax2 = None
        limit = self.cb_limit_1.currentData()
        times = self.get_limit(self.times, limit)

        if self.temp_1_1.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['1t'], limit), color='green', label='Area 1 Temperature')
        if self.temp_1_2.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['1c'], limit), color='green', label='Area 1 Canopy', linestyle='dotted')
        if self.temp_1_3.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['1r'], limit), color='green', label='Area 1 Root', linestyle='dashed')

        if self.temp_2_1.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['2t'], limit), color='orange', label='Area 2 Temperature')
        if self.temp_2_2.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['2c'], limit), color='orange', label='Area 2 Canopy', linestyle='dotted')
        if self.temp_2_3.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['2r'], limit), color='orange', label='Area 2 Root', linestyle='dashed')

        if self.temp_3_1.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['dt'], limit), color='olive', label='Drying Temperature')

        if self.temp_4_1.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['ws'], limit), color='brown', label='Workshop')

        if self.temp_5_1.isChecked():
            self.plot.canvas.axes.plot(times, self.get_limit(self.values['ot'], limit), color='hotpink', label='Outside Temperature')

        if self.ck_hum_1.isChecked():
            if self.ax2 is None:
                self.ax2 = self.plot.canvas.axes.twinx()
            self.ax2.plot(self.times, self.values['1h'], color='pink', label='Area 1 Humidity')
            self.ax2.yaxis.set_major_locator(MultipleLocator(10))

        if self.ck_hum_2.isChecked():
            if self.ax2 is None:
                self.ax2 = self.plot.canvas.axes.twinx()
            self.ax2.plot(self.times, self.values['2h'], color='purple', label='Area 2 Humidity')

        if self.ck_hum_3.isChecked():
            if self.ax2 is None:
                self.ax2 = self.plot.canvas.axes.twinx()
            self.ax2.plot(self.times, self.values['dh'], color='purple', label='Drying Humidity')

        if self.ck_hum_4.isChecked():
            if self.ax2 is None:
                self.ax2 = self.plot.canvas.axes.twinx()
            self.ax2.plot(self.times, self.values['oh'], color='purple', label='Outside Humidity', linestyle='dotted')

        if self.ax2 is not None:
            self.ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            # self.ax2.invert_yaxis()
            self.ax2.legend(loc='upper left')

        self.plot.canvas.axes.set_ylabel("Temperature")
        self.plot.canvas.axes.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        self.plot.canvas.axes.xaxis.set_major_locator(MultipleLocator(10))
        leg = self.plot.canvas.axes.legend()
        leg.set_draggable(state=True)
        self.plot.canvas.axes.tick_params(
            axis='x', which='major', labelcolor='Green', rotation=45, labelsize=7)
        # self.plot.canvas.axes.invert_yaxis()
        self.plot.canvas.axes.xaxis.grid(True, which='minor')
        self.plot.grid(True)
        self.plot.canvas.draw()
        self.plot.show()

    def outputs_plot(self):
        self.plot_outputs = MplWidget(self.wg_graph_2, 12, 5.3)
        self.plot_outputs.canvas.axes.cla()
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['1h1'], color='green', label='Area 1 Heater 1')
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['1h2'], color='green', label='Area 1 Heater 2', linestyle='dotted')
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['1a'], color='green', label='Area 1 Aux', linestyle='dashed')
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['1s'], color='green', label='Area 1 Socket')

        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['2h1'], color='orange', label='Area 2 Heater 1')
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['2h2'], color='orange', label='Area 2 Heater 2', linestyle='dotted')
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['2a'], color='orange', label='Area 2 Aux', linestyle='dashed')
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['2s'], color='orange', label='Area 2 Socket')

        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['h3'], color='pink', label='Area 3 Heater')

        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['ws'], color='brown', label='Workshop Heater')

        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['wh1'], color='blue', label='Water Heater 1')
        self.plot_outputs.canvas.axes.plot(self.times, self.output_values['wh2'], color='blue', label='Water Heater 2', linestyle='dashed')

        # self.plot_outputs.canvas.axes.set_ylabel("Outputs")
        # self.plot_outputs.canvas.axes.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        self.plot_outputs.canvas.axes.set_yticks(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
        self.plot_outputs.canvas.axes.set_yticklabels([
            'Off', 'H1a On', 'Off', 'H1b On', 'Off', 'A1 On', 'Off', 'S1 On', 'Off', 'H2a On', 'Off', 'H2b On',
            'Off', 'A2 On', 'Off', 'S2 On', 'Off', 'H3 On', 'Off', 'WS On', 'Off', 'WH1 On', 'Off', 'WH2 On'])
        self.plot_outputs.canvas.axes.xaxis.set_major_locator(MultipleLocator(10))
        # leg = self.plot_outputs.canvas.axes.legend()
        # leg.set_draggable(state=True)
        self.plot_outputs.canvas.axes.tick_params(
            axis='x', which='major', labelcolor='Green', rotation=45, labelsize=7)
        self.plot_outputs.canvas.axes.xaxis.grid(True, which='minor')
        self.plot_outputs.grid(True)
        self.plot_outputs.canvas.draw()
        self.plot_outputs.show()

    def fans_plot(self):
        self.plot_fans = MplWidget(self.wg_graph_3, 12, 5.3)
        self.plot_fans.canvas.axes.cla()
        limit = self.cb_limit_3.currentData()
        times = self.get_limit(self.times, limit)
        if self.ck_fan_1.isChecked():
            self.plot_fans.canvas.axes.plot(times, self.get_limit(self.fan_values['1in'], limit), color='green', label='Input 1')
            self.plot_fans.canvas.axes.plot(times, self.get_limit(self.fan_values['1rv'], limit), color='red', label='Set 1')
        if self.ck_fan_2.isChecked():
            self.plot_fans.canvas.axes.plot(times, self.get_limit(self.fan_values['2in'], limit), color='orange', label='Input 2')
            self.plot_fans.canvas.axes.plot(times, self.get_limit(self.fan_values['2rv'], limit), color='blue', label='Set 2')
        ax2 = self.plot_fans.canvas.axes.twinx()
        if self.ck_fan_1.isChecked():
            ax2.plot(times, self.get_limit(self.fan_values['1sw'], limit), color='brown', label='Speed 1', linestyle='dotted')
        if self.ck_fan_2.isChecked():
            ax2.plot(times, self.get_limit(self.fan_values['2sw'], limit), color='black', label='Speed 2', linestyle='dotted')
        # ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        self.plot_fans.canvas.axes.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax2.set_yticks([0, 1, 2, 3, 4, 5, 6])
        ax2.set_yticklabels(["Off", "1", "2", "3", "4", "5", "6"])
        self.plot_fans.canvas.axes.xaxis.set_major_locator(MultipleLocator(10))
        leg = self.plot_fans.canvas.axes.legend()
        leg.set_draggable(state=True)
        self.plot_fans.canvas.axes.tick_params(
            axis='x', which='major', labelcolor='Green', rotation=45, labelsize=7)
        self.plot_fans.canvas.axes.xaxis.grid(True, which='minor')
        self.plot_fans.grid(True)
        self.plot_fans.canvas.draw()
        self.plot_fans.show()

    def power_plot(self):
        self.plot_power = MplWidget(self.wg_graph_4, 12, 5.3)
        self.plot_power.canvas.axes.cla()
        limit = self.cb_limit_4.currentData()
        times = self.get_limit(self.times, limit)

        self.plot_power.canvas.axes.plot(times, self.get_limit(self.power_values['watts'], limit), color='green', label='Watts')

        self.plot_power.canvas.axes.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        self.plot_power.canvas.axes.xaxis.set_major_locator(MultipleLocator(10))
        # leg = self.plot_power.canvas.axes.legend()
        # leg.set_draggable(state=True)
        self.plot_power.canvas.axes.tick_params(
            axis='x', which='major', labelcolor='Green', rotation=45, labelsize=7)
        self.plot_power.canvas.axes.xaxis.grid(True, which='minor')
        self.plot_power.grid(True)
        self.plot_power.canvas.draw()
        self.plot_power.show()


class DialogPatternMaker(QDialog, Ui_DialogPatterns):
    def __init__(self, parent):
        super(DialogPatternMaker, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.main_panel = parent
        self.db = self.main_panel.db

        self.pattern_name = ""
        self.pattern_id = UNSET
        self.load_patterns()
        self.cb_patterns.editTextChanged.connect(self.check_pattern)
        self.cb_patterns.installEventFilter(self)

        self.tw_pattern_stages.resizeColumnsToContents()
        self.tw_pattern_stages.resizeRowsToContents()
        self.tw_pattern_stages.setHorizontalHeaderLabels(["Stage", "Duration", "Lighting", "Temperature", "Feeding", "Location"])

    def eventFilter(self, source, event):
        # Remember to install event filter for control first
        # print("Event ", event.type())
        if event.type() == QtCore.QEvent.FocusOut:
            if source is self.cb_patterns:
                self.add_pattern()
        return QWidget.eventFilter(self, source, event)

    def load_patterns(self):
        self.cb_patterns.blockSignals(True)
        self.cb_patterns.clear()
        rows = self.db.execute('SELECT name, id FROM {}'.format(DB_PATTERN_NAMES))
        self.cb_patterns.addItem("Select or Type", 0)
        for row in rows:
            self.cb_patterns.addItem(row[0], row[1])
        self.cb_patterns.blockSignals(False)

    def check_pattern(self, txt):
        self.pattern_id = self.cb_patterns.findText(txt)
        self.pattern_name = txt

    def add_pattern(self):
        if self.pattern_id < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Do you wish to create a new pattern " + self.pattern_name)
            msg.setWindowTitle("Confirm New Pattern")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            if msg.exec_() == QMessageBox.Cancel:
                return
        else:
            self.load_stages()

    def load_stages(self):
        rows = self.db.execute('SELECT stage, duration, lighting, temperature, feeding, location FROM {}'
                               ' WHERE pid = {}'.format(DB_STAGE_PATTERNS, self.pattern_id))
        r = 0
        for row in rows:
            for c in range(0, 7):
                ti = QTableWidgetItem(row[c])
                self.tw_pattern_stages.setItem(r, c, ti)


class DialogAccessModule(QDialog, Ui_DialogDEmodule):
    def __init__(self, parent):
        super(DialogAccessModule, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.main_panel = parent
        self.db = self.main_panel.db
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_reboot.clicked.connect(self.reboot)
        self.p_save.clicked.connect(self.save)
        self.pb_query.clicked.connect(self.query)
        self.pb_cover_open.clicked.connect(self.cover_open)
        self.pb_cover_close.clicked.connect(self.cover_close)
        self.pb_door_open.clicked.connect(self.door_open)
        self.pb_door_close.clicked.connect(self.door_lock)
        self.pb_cover_lock.clicked.connect(
            lambda: self.main_panel.coms_interface.send_switch(SW_COVER_LOCK, ON_RELAY, MODULE_DE))
        self.pb_cover_unlock.clicked.connect(
            lambda: self.main_panel.coms_interface.send_switch(SW_COVER_LOCK, OFF_RELAY, MODULE_DE))
        self.le_cover_dur.setText(str(self.main_panel.db.get_config(CFT_ACCESS, "cover time", 30)))
        self.le_auto_delay.setText(str(self.main_panel.db.get_config(CFT_ACCESS, "auto delay", 15)))
        self.cb_mute.addItem("Off", 0)
        self.cb_mute.addItem("30 Minutes", 30)
        self.cb_mute.addItem("1 Hour", 60)
        self.cb_mute.addItem("2 Hours", 120)
        self.cb_mute.currentIndexChanged.connect(self.change_mute)

    def change_mute(self):
        d = self.cb_mute.currentData()
        if d == 0:
            self.main_panel.main_window.access.mute_timeout()
        else:
            self.main_panel.main_window.access.mute_start(d)

    def query(self):
        self.main_panel.coms_interface.send_data(COM_COVER_CLOSED, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_COVER_POSITION, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_DOOR_POSITION, True, MODULE_DE)

    def re_scan(self):
        self.main_panel.coms_interface.send_data(COM_SEND_FREQ, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_KWH_DIF, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_PULSES, True, MODULE_DE)

    def cover_open(self):
        self.main_panel.coms_interface.send_switch(SW_COVER_OPEN, ON_RELAY, MODULE_DE)

    def cover_close(self):
        self.main_panel.coms_interface.send_switch(SW_COVER_CLOSE, ON_RELAY, MODULE_DE)

    def door_open(self):
        self.main_panel.coms_interface.send_switch(SW_DOOR_LOCK, OFF_RELAY, MODULE_DE)

    def door_lock(self):
        self.main_panel.coms_interface.send_switch(SW_DOOR_LOCK, ON_RELAY, MODULE_DE)

    def update(self):
        # v = float(self.le_kwh_total.text())
        # if v != self
        v = float(self.le_seconds.text())
        if v != self.send_org:
            self.main_panel.coms_interface.send_data(CMD_SEND_FREQ, False, MODULE_DE, v * 1000)

    def update_diff(self):
        v = string_to_float(self.le_watts.text())
        if v != self.watt_dif_org:
            v /= 1000  # has to be split into 2 ints as network code does not pass floats
            i = int(v)
            d = int((v - i) * 1000)
            self.main_panel.coms_interface.send_data(CMD_KWH_DIF, False, MODULE_DE, i, d)

    def update_pulses(self):
        v = string_to_float(self.le_pp_kw.text())
        if v != self.pulses_pkw:
            self.main_panel.coms_interface.send_data(CMD_SET_PULSES, False, MODULE_DE, int(v))

    def save(self):
        self.main_panel.db.set_config_both(CFT_ACCESS, "cover time", self.le_cover_dur.text())
        self.main_panel.access.cover_duration = int(self.le_cover_dur.text())
        self.main_panel.db.set_config_both(CFT_ACCESS, "auto delay", self.le_auto_delay.text())
        self.main_panel.access.auto_close_duration = int(self.le_auto_delay.text())

    def store(self):
        v = string_to_float(self.le_kwh_total.text())
        fp = int(v)
        sp = v - fp  # has to be split into 2 ints as network code does not pass floats
        sp *= 1000
        self.main_panel.coms_interface.send_data(CMD_SET_KWH, False, MODULE_DE, fp, int(sp))

    def reboot(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Confirm you wish to reboot the D/E Module")
        msg.setWindowTitle("Confirm Reboot")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Yes:
            self.main_panel.coms_interface.send_data(CMD_REBOOT, False, MODULE_DE)


class DialogElectMeter(QDialog, Ui_DialogElectMeter):
    def __init__(self, parent):
        """ :type parent: MainWindow """
        super(DialogElectMeter, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.sub = None
        self.main_panel = parent
        self.db = self.main_panel.db
        self.watt_dif_org = 0
        self.send_org = 0
        self.pulses_pkw = 0
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_reboot.clicked.connect(self.reboot)
        self.pb_update_freq.clicked.connect(self.update_freq)
        self.pb_update_diff.clicked.connect(self.update_diff)
        self.pb_update_pulses.clicked.connect(self.update_pulses)
        self.pb_scan.clicked.connect(self.re_scan)
        self.pb_store.clicked.connect(self.store)
        self.le_kwh_total.setText(self.main_panel.le_pwr_total_1.text())

        self.main_panel.coms_interface.send_data(COM_SEND_FREQ, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_KWH_DIF, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_READ_KWH, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_PULSES, True, MODULE_DE)
        self.le_pp_kw.setToolTip("Increase this value if software is ahead of actual meter, otherwise decrease")
        self.main_panel.coms_interface.update_access_settings.connect(self.setting_received)

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

    def re_scan(self):
        self.main_panel.coms_interface.send_data(COM_SEND_FREQ, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_KWH_DIF, True, MODULE_DE)
        self.main_panel.coms_interface.send_data(COM_PULSES, True, MODULE_DE)

    def update_freq(self):
        v = float(self.le_seconds.text())
        if v != self.send_org:
            self.main_panel.coms_interface.send_data(CMD_SEND_FREQ, False, MODULE_DE, v * 1000)

    def update_diff(self):
        v = string_to_float(self.le_watts.text())
        if v != self.watt_dif_org:
            v /= 1000  # has to be split into 2 ints as network code does not pass floats
            i = int(v)
            d = int((v - i) * 1000)
            self.main_panel.coms_interface.send_data(CMD_KWH_DIF, False, MODULE_DE, i, d)

    def update_pulses(self):
        v = string_to_float(self.le_pp_kw.text())
        if v != self.pulses_pkw:
            self.main_panel.coms_interface.send_data(CMD_SET_PULSES, False, MODULE_DE, int(v))

    def store(self):
        v = string_to_float(self.le_kwh_total.text())
        fp = int(v)
        sp = v - fp  # has to be split into 2 ints as network code does not pass floats
        sp *= 1000
        self.main_panel.coms_interface.send_data(CMD_SET_KWH, False, MODULE_DE, fp, int(sp))

    def reboot(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Confirm you wish to reboot the D/E Module")
        msg.setWindowTitle("Confirm Reboot")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Yes:
            self.main_panel.coms_interface.send_data(CMD_REBOOT, False, MODULE_DE)


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
        self.main_panel = parent
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.db = self.main_panel.db
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
        table += "Started on {} and is due om <b>{}</b><br> ".format(p_class.start, p_class.due_date.date())
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
        if p_class.location != 3:
            feed = self.main_panel.area_controller.main_window.feed_controller.feeds[p_class.location]
            text = "<table><tr><td>Schedule</td><td>" + feed.pattern_name + "</td><td>" + feed.pattern_id + "</td></tr>"
            text += "<tr><td>Recipe</td><td>" + feed.recipe_name + "</td><td>" + feed.recipe_id + "</td></tr>"
        #     if fs_name is not None:
        #         if feed.recipe_id == WATER_ONLY_IDX:
        #             r_name = WATER_ONLY
        #         else:
        #             sql = "SELECT name FROM {} WHERE id = {}".format(DB_RECIPE_NAMES, feed.recipe_id)
        #             r_name = self.db.execute_single(sql)
        #             if r_name is None:
        #                 r_name = "Error None"
        #         if feed.feed_schedule == 0:
        #             txt = "Error None"
        #         else:
        #             txt = str(feed.feed_schedule)
        #         table = "<table cellpadding='3' border='1'><tr><td>Current Feed Schedule</td><td><b>" + fs_name + \
        #                 "</b> [" + txt + "]</td></tr>"
        #         table += "<tr><td>Current Recipe</td><td><b>" + r_name + "</b> [" + str(
        #             feed.recipe_id) + "]</td></tr>"
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
            self.tefeed.textCursor().insertHtml(text)

        # Water supply
        table = "<table cellpadding='3' border='1'><tr><td colspan='2'><b>Total</b> Water<br>Requirement </td></tr>"
        table += '<tr><td>Tank</td><td>Litres</td></tr>'
        # table += '<tr><td> 1 </td><td>' + str(self.main_panel.water_supply.tank_required_litres[0]) + '</td></tr>'
        # table += '<tr><td> 2 </td><td>' + str(self.main_panel.water_supply.tank_required_litres[1]) + '</td></tr>'
        # table += '<tr><td> Total </td><td>' + str(self.main_panel.feed_control.get_next_water_required()) + '</td></tr>'
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
                s = self.main_panel.area_controller.sensors[row[2]]
            table += "<tr><td>{}</td><td>{}</td><td>{}<br>Low:{}  Set:{}  High:{}</td><td>{}</td></tr>" \
                .format(row[0], OUT_TYPE[row[1]], tt, s.low, s.set, s.high, row[3])
        table += "</table>"
        self.teoutputs.setHtml(table)


class DialogFan(QDialog, Ui_DialogFan):
    def __init__(self, parent, fan_id):
        super(DialogFan, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setupUi(self)
        self.sub = None
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Fan {} Settings".format(fan_id))
        self.main_panel = parent
        self.db = self.main_panel.db
        self.id = fan_id        # Also is area
        self.fan_controller = self.main_panel.area_controller.fan_controller
        self.dl_fan.valueChanged.connect(self.change_speed)
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.pb_master.clicked.connect(self.power)
        self.main_panel.main_window.coms_interface.update_fan_speed.connect(self.update_speed)
        self.main_panel.main_window.coms_interface.update_switch.connect(self.switch_update)
        self.cb_mode.addItem("Off", 0)
        self.cb_mode.addItem("Manual", 1)
        self.cb_mode.addItem("Auto", 2)
        self.cb_mode.setCurrentIndex(self.cb_mode.findData(self.fan_controller.get_mode(self.id)))
        self.cb_mode.currentIndexChanged.connect(self.change_mode)
        self.cb_sensor.addItem("Humidity", 1)   # The data is the area_range as in the sensors_config table
        self.cb_sensor.addItem("Temperature", 2)
        self.cb_sensor.addItem("Canopy", 3)
        self.cb_sensor.addItem("Root", 4)
        self.fan_sensor_id = self.fan_controller.get_fan_sensor(self.id)
        self.fan_sensor = self.db.execute_single("SELECT area_range FROM {} WHERE area = {} AND id = {}".
                                                 format(DB_SENSORS_CONFIG, self.id, self.fan_sensor_id))
        self.cb_sensor.setCurrentIndex(self.cb_sensor.findData(self.fan_sensor))
        self.cb_sensor.currentIndexChanged.connect(self.change_sensor)
        self.lbl_name.setText("Fan {}".format(self.id))
        if self.fan_controller.master_power == ON:
            self.lbl_master.setText("On")
            self.lbl_master.setStyleSheet("")
        else:
            self.lbl_master.setText("Off")
            self.lbl_master.setStyleSheet("background-color: red; color: yellow")
        self.check_mode()
        self.ck_log_tuning.setChecked(int(self.db.get_config(CFT_FANS, "log tuning", 1)))
        self.ck_log_tuning.clicked.connect(self.change_tuning_log)

    def change_tuning_log(self):
        if self.ck_log_tuning.isChecked():
            self.fan_controller._logging_t = 1
            self.db.set_config_both(CFT_FANS, "log tuning", 1)
        else:
            self.fan_controller._logging_t = 0
            self.db.set_config_both(CFT_FANS, "log tuning", 0)

    def change_sensor(self):
        new_sensor = self.cb_sensor.currentData()
        sid = self.main_panel.area_controller.get_sid_from_item(self.id, new_sensor)
        self.main_panel.area_controller.fan_controller.set_fan_sensor(self.id, sid)
        self.main_panel.area_controller.fan_controller.refresh_info(self.id)
        self.main_panel.coms_interface.relay_send(NWC_FAN_SENSOR, self.id, sid)
        # Change Arduino fan sensor
        self.main_panel.coms_interface.send_data(CMD_SET_FAN_SENSOR, True, MODULE_IO, self.id, sid)

    def power(self):
        if self.fan_controller.master_power == ON:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Confirm you wish to shut down the fan controller's power supply")
            msg.setWindowTitle("Confirm Shut Down")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            if msg.exec_() == QMessageBox.Cancel:
                return
            self.fan_controller.set_master_power(OFF)
        else:
            sound_click()
            self.fan_controller.set_master_power(ON)
        # No relay here as it will be pick up by the switch signal

    def check_mode(self):
        if self.fan_controller.master_power == OFF:
            return
        if self.fan_controller.get_mode(self.id) == 0:
            self.dl_fan.setEnabled(False)
        elif self.fan_controller.get_mode(self.id) == 2:
            self.dl_fan.setEnabled(False)
        else:
            self.dl_fan.setEnabled(True)

    def change_speed(self, speed):
        """
        Manually set speed
        @param speed:
        @type speed: int
        """
        self.fan_controller.set_speed(self.id, speed)
        # self.main_panel.coms_interface.relay_send(NWC_FAN_SPEED, self.id, speed)

    def change_mode(self):
        mode = self.cb_mode.currentData()
        self.fan_controller.set_mode(self.id, mode)
        if mode == 0:
            self.fan_controller.stop_fan(self.id)
            self.dl_fan.setEnabled(False)
        if mode == 1:
            self.fan_controller.start_manual(self.id)
            self.dl_fan.setEnabled(True)
        if mode == 2:
            self.fan_controller.start_fan(self.id)
            self.dl_fan.setEnabled(False)
        self.check_mode()
        self.main_panel.coms_interface.relay_send(NWC_FAN_MODE, self.id, mode)

    @pyqtSlot(int, int, name="updateFanSpeed")
    def update_speed(self, fan, speed):
        if fan == self.id and self.fan_controller.get_mode(self.id) == 2:
            self.dl_fan.blockSignals(True)
            self.dl_fan.setValue(speed)
            self.dl_fan.blockSignals(False)

    @pyqtSlot(int, int, int, name="updateSwitch")
    def switch_update(self, sw, state, module):
        if module != MODULE_IO:
            return
        if sw == SW_FANS_POWER:
            if state == ON:
                self.lbl_master.setText("On")
                self.lbl_master.setStyleSheet("")
            else:
                self.lbl_master.setText("Off")
                self.lbl_master.setStyleSheet("background-color: red; color: yellow")


class DialogWorkshopSettings(QWidget, Ui_DialogWorkshopSetting):
    def __init__(self, parent):
        """ :type parent: MainWindow """
        super(DialogWorkshopSettings, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.db = parent.db
        self.sub = None
        self.output = self.main_panel.area_controller.output_controller.outputs[OUT_HEATER_ROOM]
        self.ck_auto_boost.setChecked(self.output.auto_boost)
        self.cb_sensor_.addItem("Temperature")
        self.cb_mode.addItem("Off", 0)
        self.cb_mode.addItem("On", 1)
        self.cb_mode.addItem("Auto", 2)
        self.cb_mode.setCurrentIndex(self.cb_mode.findData(self.output.mode))
        self.cb_mode.currentIndexChanged.connect(self.mode_change)
        self.ck_auto_boost.clicked.connect(self.change_boost)
        self.ck_frost.setChecked(self.output.frost)
        self.ck_frost.clicked.connect(self.change_frost)
        self.le_min_frost.setText(str(self.output.min_frost))
        self.le_max_frost.setText(str(self.output.max_frost))
        if not self.output.frost:
            self.le_min_frost.setEnabled(False)
            self.le_max_frost.setEnabled(False)
        self.le_max.setText(str(self.output.max))
        self.le_min.setText(str(self.output.min))
        self.le_max.editingFinished.connect(self.change_max)
        self.le_min.editingFinished.connect(self.change_min)
        self.le_max_frost.editingFinished.connect(self.change_max_frost)
        self.le_min_frost.editingFinished.connect(self.change_min_frost)
        h = self.output.duration / 60
        m = self.output.duration % 60
        self.tm_duration.setTime(QTime(h, m))
        self.tm_duration.timeChanged.connect(self.change_duration)

    def change_max(self):
        m = string_to_float(self.le_max.text())
        if m == self.output.max:
            return
        self.output.max = m
        self.output.update_info()
        self.db.set_config_both(CFT_WORKSHOP_HEATER, "high", m)
        self.main_panel.coms_interface.relay_send(NWC_WORKSHOP_RANGES)

    def change_min(self):
        m = string_to_float(self.le_min.text())
        if m == self.output.min:
            return
        self.output.min = m
        self.output.update_info()
        self.db.set_config_both(CFT_WORKSHOP_HEATER, "low", m)
        self.main_panel.coms_interface.relay_send(NWC_WORKSHOP_RANGES)

    def change_max_frost(self):
        m = string_to_float(self.le_max_frost.text())
        if m == self.output.max_frost:
            return
        self.output.max_frost = m
        self.output.update_info()
        self.db.set_config_both(CFT_WORKSHOP_HEATER, "frost max", m)
        self.main_panel.coms_interface.relay_send(NWC_WORKSHOP_RANGES)

    def change_min_frost(self):
        m = string_to_float(self.le_min_frost.text())
        if m == self.output.min_frost:
            return
        self.output.min_frost = m
        self.output.update_info()
        self.db.set_config_both(CFT_WORKSHOP_HEATER, "frost min", m)
        self.main_panel.coms_interface.relay_send(NWC_WORKSHOP_RANGES)

    def change_frost(self):
        f = int(self.ck_frost.isChecked())
        self.output.change_frost(f)
        self.main_panel.coms_interface.relay_send(NWC_WORKSHOP_FROST, f)
        if not self.output.frost:
            self.le_min_frost.setEnabled(False)
            self.le_max_frost.setEnabled(False)
        else:
            self.le_min_frost.setEnabled(True)
            self.le_max_frost.setEnabled(True)

    def change_boost(self):
        b = int(self.ck_auto_boost.isChecked())
        self.output.change_boost(b)
        self.main_panel.coms_interface.relay_send(NWC_WORKSHOP_BOOST, b)

    def mode_change(self):
        mode = self.cb_mode.currentData()
        if mode != self.output.mode:
            self.main_panel.area_controller.output_controller.change_mode(self.output.output_pin, mode)

    def range_change(self):
        # if self.sender().hasFocus():
        #     return
        on = string_to_float(self.le_min.text())
        off = string_to_float(self.le_max.text())

        if on - 1 < off:
            off = on - 1
            self.le_max.setText(str(off))
        self.output_controller.set_limits(self.pin_id, on, off)
        self.main_panel.coms_interface.relay_send(NWC_OUTPUT_RANGE, self.pin_id)

    def change_duration(self):
        d = self.tm_duration.time()
        duration = ((d.hour() * 60) + d.minute())
        self.output.set_duration(duration)
        self.main_panel.coms_interface.relay_send(NWC_WORKSHOP_DURATION)


class DialogWaterHeaterSettings(QWidget, Ui_DialogWaterHeatertSetting):
    def __init__(self, parent, tank):
        """ :type parent: MainWindow """
        super(DialogWaterHeaterSettings, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.db = parent.db
        self.sub = None
        self.tank = tank

        self.lbl_name.setText("Water Heater {}".format(self.tank))
        sql = 'SELECT `id`, `name`, `area`, `type`, `input`, `range`, `pin`, `short_name` FROM {} WHERE ' \
              '`area` = 7 AND `item` = {}'. format(DB_OUTPUTS, self.tank)
        row = self.db.execute_one_row(sql)
        self.mode = row[3]
        self.pin_id = row[6]       # Use as index for the Outputs[] dictionary
        self.output = self.main_panel.area_controller.output_controller.outputs[self.pin_id]
        self.output_controller = self.main_panel.area_controller.output_controller
        self.frequency = int(self.db.get_config(CFT_WATER_HEATER, "frequency {}".format(self.tank), 1))
        self.use_float = int(self.db.get_config(CFT_WATER_HEATER, "float {}".format(self.tank), 1))
        self.duration = int(self.db.get_config(CFT_WATER_HEATER, "heater duration", "240"))
        self.off_time = self.db.get_config(CFT_FEEDER, "feed time", "19:00")
        self.tm_off.setTime(QTime.fromString(self.off_time))
        self.tm_off.timeChanged.connect(self.change_off_time)
        h, m = minutes_to_hhmm(self.duration)
        self.tm_duration.setTime(QTime(h, m))
        self.tm_duration.dateTimeChanged.connect(self.change_duration)
        self.ck_use_float.setChecked(self.use_float)
        self.ck_use_float.clicked.connect(self.change_float)
        self.cb_mode.addItem("Off", 0)
        self.cb_mode.addItem("Manual On", 1)
        self.cb_mode.addItem("Auto", 2)
        self.cb_mode.addItem("Timer", 3)
        self.cb_mode.setCurrentIndex(self.cb_mode.findData(row[3]))
        self.cb_frequency.addItem("As Required", 0)
        self.cb_frequency.addItem("Daily", 1)
        self.cb_frequency.addItem("2 Days", 2)
        self.cb_frequency.addItem("3 Days", 3)
        self.cb_frequency.setCurrentIndex(self.cb_frequency.findData(self.frequency))
        self.cb_frequency.currentIndexChanged.connect(self.change_frequency)
        self.cb_mode.currentIndexChanged.connect(self.mode_change)

    def change_float(self):
        f = int(self.ck_use_float.isChecked())
        if f == self.use_float:
            return
        self.output_controller.outputs[self.pin_id].set_float_use(f)
        self.main_panel.coms_interface.relay_send(NWC_WH_FLOAT_USE, self.pin_id, f)

    def change_frequency(self):
        f = self.cb_frequency.currentData()
        self.output_controller.outputs[self.pin_id].set_frequency(f)
        self.output_controller.water_heater_update_info()
        self.main_panel.coms_interface.relay_send(NWC_WH_FREQUENCY, self.pin_id, f)
        # self.main_panel.coms_interface.relay_send(NWC_FEED_DATE, self.area)

    def change_off_time(self):
        t = self.tm_off.time()
        self.main_panel.feed_controller.set_feed_time(t.toString("hh:mm"))
        self.main_panel.area_controller.output_controller.water_heater_set_off_time(t.toString("hh:mm"))

    def change_duration(self):
        d = self.tm_duration.time()
        duration = ((d.hour() * 60) + d.minute())
        self.output_controller.water_heater_set_duration(duration)
        self.main_panel.coms_interface.relay_send(NWC_WH_DURATION, self.pin_id, duration)

    def mode_change(self):
        mode = self.cb_mode.currentData()
        if mode != self.mode:
            self.mode = mode
            self.output_controller.change_mode(self.pin_id, mode)


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
        self.temperatures_active = collections.defaultdict()
        self.temperatures_inactive = collections.defaultdict()
        self.temperatures_active_org = collections.defaultdict()
        self.temperatures_inactive_org = collections.defaultdict()
        self.low_org = 0
        self.set_org = 0
        self.high_org = 0
        self.inverted = False   # True means you are working on inactive values

        # Load sensor config from db
        self.config = self.db.execute_one_row('SELECT id, name, maps_to, calibration, step, area, area_range, '
                                              'short_name FROM {} WHERE id = {}'.format(DB_SENSORS_CONFIG, self.s_id))
        if self.config is None:
            return
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
            self.pb_set_fan.setEnabled(False)
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
            txt += ""
            for row in rows:
                txt += row[0] + ", "
            txt = txt[:-2]
        self.lbl_connections.setText(txt)

        self.load_ranges()

        if self.process == 0:
            self.pb_switch.setEnabled(False)
            self.pb_set_fan.setEnabled(False)

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
        else:
            # No process so use default values which are stored in the process_temperature_adjustments
            rows = self.db.execute('SELECT item, setting, value FROM {} WHERE area = {} AND item = {}'.
                                   format(DB_PROCESS_TEMPERATURE, self.area, self.item))
            for row in rows:
                self.temperatures_active[row[1]] = row[2]
            self.temperatures_active_org = self.temperatures_inactive = self.temperatures_inactive_org = self.temperatures_active
        self.low = self.temperatures_active['low']
        self.set = self.temperatures_active['set']
        self.high = self.temperatures_active['high']
        self.low_org = self.temperatures_active_org['low']
        self.set_org = self.temperatures_active_org['set']
        self.high_org = self.temperatures_active_org['high']
        self.update_display()

    def update_display(self):
        # self.set, self.high, self.low = self.sensors[self.s_id].get_set_temperatures()
        self.le_set.setText(str(self.set))
        self.le_high.setText(str(self.high))
        self.le_low.setText(str(self.low))
        self.lbl_set.setText(str(self.set_org))
        self.lbl_high.setText(str(self.high_org))
        self.lbl_low.setText(str(self.low_org))
        if self.area < 4:
            txt = "Area {}".format(self.area)
        elif self.area == 4:
            txt = "Workshop"
        elif self.area == 5:
            txt = "Outside"
        if self.inverted:
            txt += " ({})".format("Night" if self.on_day else "Day")
            self.lbl_area.setText(txt)
            self.pb_switch.setText("Day" if self.on_day else "Night")
            stylesheet = "Color: White; background-color: red"
        else:
            if self.process != 0:
                txt += " ({})".format("Day" if self.on_day else "Night")
            self.lbl_area.setText(txt)
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
        if self.process != 0:
            self.process.load_active_temperature_ranges()
        self.main_panel.coms_interface.relay_send(NWC_SENSOR_RELOAD, self.area, self.s_id)
        self.main_panel.area_controller.sensors[self.s_id].load_range()
        self.main_panel.area_controller.sensors[self.s_id].update_status_ctrl()

    def change_set(self):
        # if self.sender().hasFocus():
        #     return
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
        self.main_panel.area_controller.fan_controller.set_req_temperature(self.area, nv)
        if self.process != 0:
            self.process.load_active_temperature_ranges()
            self.main_panel.area_controller.sensors[self.s_id].load_range()
        else:
            self.main_panel.area_controller.sensor_load_manual_ranges(self.area, self.item)
        self.main_panel.coms_interface.relay_send(NWC_SENSOR_RELOAD, self.area, self.s_id)
        self.main_panel.area_controller.sensors[self.s_id].update_status_ctrl()

    def change_high(self):
        # if self.sender().hasFocus():
        #     return
        nv = string_to_float(self.le_high.text())
        if nv == self.high:
            return
        self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                              '"high" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
        self.high = nv
        self._check_set_high(nv)
        self._check_low(self.set)
        if self.process != 0:
            self.process.load_active_temperature_ranges()
            self.main_panel.area_controller.sensors[self.s_id].load_range()
        else:
            self.main_panel.area_controller.sensor_load_manual_ranges(self.area, self.item)
        self.main_panel.coms_interface.relay_send(NWC_SENSOR_RELOAD, self.area, self.s_id)
        self.main_panel.area_controller.sensors[self.s_id].update_status_ctrl()

    def change_low(self):
        # if self.sender().hasFocus():
        #     return
        nv = string_to_float(self.le_low.text())
        if nv == self.low:
            return
        self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                              '"low" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
        self.low = nv
        self._check_set_low(nv)
        self._check_high(self.set)
        if self.process != 0:
            self.process.load_active_temperature_ranges()
            self.main_panel.area_controller.sensors[self.s_id].load_range()
        else:
            self.main_panel.area_controller.sensor_load_manual_ranges(self.area, self.item)
        self.main_panel.coms_interface.relay_send(NWC_SENSOR_RELOAD, self.area, self.s_id)
        self.main_panel.area_controller.sensors[self.s_id].update_status_ctrl()

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
            self.main_panel.area_controller.fan_controller.set_req_temperature(self.area, self.set)

    def _check_set_low(self, nv):
        # checks set value from low
        if self.set < nv + 0.5:
            self.le_set.setText(str(nv + 0.5))
            self.db.execute_write('UPDATE {} SET value = {} WHERE area= {} AND day = {} AND item = {} AND setting = '
                                  '"set" LIMIT 1'.format(DB_PROCESS_TEMPERATURE, nv, self.area, self.day_night, self.item))
            self.set = nv + 0.5
            self.main_panel.area_controller.fan_controller.set_req_temperature(self.area, self.set)

    def set_as_fan(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Confirm you wish to set this sensor as input for the fan")
        msg.setWindowTitle("Confirm Fan Setting")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        self.main_panel.area_controller.fan_controller.set_fan_sensor(self.area, self.s_id)      # Set new
        self.fan_sensor_current = self.s_id
        self.pb_set_fan.setEnabled(False)
        self.main_panel.coms_interface.send_data(CMD_SET_FAN_SENSOR, True, MODULE_IO, self.area, self.s_id)
        self.main_panel.coms_interface.relay_send(NWC_FAN_SENSOR, self.area, self.s_id)


class DialogRemoveItem(QDialog, Ui_DialogRemoveItem):
    def __init__(self, parent, process: ProcessClass):

        super(DialogRemoveItem, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.main_panel = parent
        self.sub = None
        self.db = self.main_panel.db
        self.process = process
        self.pb_cancel.clicked.connect(lambda: self.sub.close())
        self.pb_apply.clicked.connect(self.apply)
        self.lbl_info.setText("Remove item from Process {} in area {}".format(self.process.id, self.process.location))
        items = self.main_panel.area_controller.get_area_items(self.process.location)
        self.cb_item.addItem("Select", 0)
        for i in items:
            self.cb_item.addItem(str(i), i)

    def apply(self):
        reason = self.te_reason.toPlainText()
        item = self.cb_item.currentData()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        if item == 0 or len(reason) == 0:
            msg.setText("Please select an item number and enter a reason")
            msg.setWindowTitle("Invalid Selection")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        msg.setText("Confirm you wish to remove item {}".format(item))
        msg.setWindowTitle("Confirm Item Removal")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        dt = datetime.strftime(datetime.now(), '%d/%m/%y')
        self.process.journal_write(dt + "    Number " + str(item) + " Removed on day  "
                                   + str(self.process.stage_days_elapsed) + "  " + reason)
        self.process.remove(item)
        sql = "DELETE FROM {} WHERE process_id = {} AND item = {} AND area = 2".format(DB_AREAS, self.process.id, item)
        self.db.execute_write(sql)
        sql = "UPDATE {} SET location = 0, total_days = {} WHERE process_id = {} and item = {}". \
            format(DB_PROCESS_STRAINS, self.process.days_total, self.process.id, item)
        self.db.execute_write(sql)


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
        self.lbl_info.setText("Process {} in location {}".format(self.process.id, self.area))

        self.new_feed_date = self.main_panel.feed_controller.get_last_feed_date(self.area)

        if self.area < 3:
            self.cb_feed_mode.setCurrentIndex(self.cb_feed_mode.findData(self.main_panel.feed_controller.get_feed_mode(self.area)))
            self.de_feed_date.setDate(self.new_feed_date)
        else:
            self.cb_feed_mode.setEnabled(False)
            self.de_feed_date.setEnabled(False)
        self.pb_delay.clicked.connect(self.delay_feed)
        self.pb_remove.clicked.connect(self.remove)
        self.de_feed_date.dateChanged.connect(self.new_date)

    def delay_feed(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Confirm you wish to delay feeding")
        msg.setWindowTitle("Confirm Feed Delay")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        self.main_panel.feed_controller.set_last_feed_date(
            self.area, self.main_panel.feed_controller.get_last_feed_date(self.area) + timedelta(days=1))
        self.main_panel.update_next_feeds()
        # self.main_panel.area_controller.output_controller.water_heater_update_info()
        self.de_feed_date.setDate(self.main_panel.feed_controller.get_last_feed_date(self.area))
        self.main_panel.coms_interface.relay_send(NWC_FEED, self.area)  # Just send feed as it is only the feed date that is changed
        self.sub.close()

    def new_date(self):
        new_feed_date = self.de_feed_date.date().toPyDate()
        self.main_panel.feed_controller.set_last_feed_date(self.area, new_feed_date)
        self.main_panel.update_next_feeds()
        self.main_panel.area_controller.output_controller.water_heater_update_info()
        self.main_panel.coms_interface.relay_send(NWC_FEED_DATE, self.area)

    def remove(self):
        self.main_panel.main_window.wc.show(DialogRemoveItem(self.main_panel, self.process))


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

        # get day or night
        self.on_day = self.main_panel.area_controller.get_light_status(self.area)
        self.day_night = self.on_day    # Holds the day night value. Will be same as on_day unless inverted
        self.mode = 0
        self.pin_id = 0      # Use as index for the Outputs[] dictionary
        self.db_id = 0          # Id in db
        self.sensor = 0
        self.offset_on = 0
        self.offset_off = 0
        self.inverted = True    # Set true as invert() will change it

        self.load()
        self.invert()
        self.detection_mode = self.output_controller.outputs[self.pin_id].detection
        self.lbl_detection.setText("<" if self.detection_mode == DET_FALL else ">")

        self.cb_out_mode_1_1.addItem("Off", 0)
        self.cb_out_mode_1_1.addItem("Manual On", 1)
        self.cb_out_mode_1_1.addItem("Sensor", 2)
        self.cb_out_mode_1_1.addItem("Timer", 3)
        self.cb_out_mode_1_1.addItem("Both", 4)
        self.cb_out_mode_1_1.addItem("All Day", 5)
        self.cb_out_mode_1_1.addItem("All Night", 6)
        self.cb_out_mode_1_1.setCurrentIndex(self.cb_out_mode_1_1.findData(self.mode))
        self.mode_change()
        self.cb_out_mode_1_1.currentIndexChanged.connect(self.mode_change)

        sql = 'SELECT name, id FROM {} WHERE area = {}'.format(DB_SENSORS_CONFIG, self.area)
        rows = self.db.execute(sql)
        for r in rows:
            self.cb_sensor_out_1_1.addItem(r[0], r[1])
        self.cb_sensor_out_1_1.setCurrentIndex(self.cb_sensor_out_1_1.findData(self.sensor))
        self.cb_sensor_out_1_1.currentIndexChanged.connect(self.sensor_change)
        self.le_range_on_1_1.editingFinished.connect(self.range_change)
        self.le_range_off_1_1.editingFinished.connect(self.range_change)
        self.pb_reset.clicked.connect(self.reset)

        self.on, self.off = self.output_controller.get_set_temperatures(self.pin_id)

        self.cb_trigger.addItem("Falling", DET_FALL)
        self.cb_trigger.addItem("Rising", DET_RISE)
        self.cb_trigger.setCurrentIndex(self.cb_trigger.findData(self.detection_mode))
        self.cb_trigger.currentIndexChanged.connect(self.change_detection_mode)
        self.ck_lock.setChecked(self.output_controller.outputs[self.pin_id].locked)
        self.ck_lock.clicked.connect(self.change_lock)
        self.pb_switch.clicked.connect(self.invert)
        self.set_controls()

    def load(self):
        if self.day_night == DAY:
            sql = 'SELECT `id`, `name`, `area`, `type`, `input`, `range`, `pin`, `short_name` FROM {} WHERE ' \
                  '`area` = {} AND `item` = {}'. format(DB_OUTPUTS, self.area, self.item)
            dnt = "Day"
        else:
            sql = 'SELECT `id`, `name`, `area`, `type`, `input`, `range_night`, `pin`, `short_name` FROM {} WHERE ' \
                  '`area` = {} AND `item` = {}'. format(DB_OUTPUTS, self.area, self.item)
            dnt = "Night"
        row = self.db.execute_one_row(sql)
        self.db_id = row[0]
        self.mode = row[3]
        self.pin_id = row[6]       # Use as index for the Outputs[] dictionary
        self.sensor = row[4]
        t = row[5].split(',')
        self.offset_on = string_to_float(t[0])
        self.offset_off = string_to_float(t[1])
        if self.area < 4:
            self.lbl_name.setText("{} in\r\nArea {} ({})".format(row[1], self.area, dnt))
        elif self.area == 4:
            self.lbl_name.setText("Workshop Heater")
        elif self.area == 7:
            self.lbl_name.setText("Water Heater in tank {}".format(self.area))

    def invert(self):
        if self.inverted:
            self.day_night = self.on_day
            self.inverted = False
            stylesheet = ""
            self.pb_switch.setText("Night" if self.on_day else "Day")
            self.on, self.off = self.output_controller.get_set_temperatures(self.pin_id)
        else:
            self.day_night = int(not self.day_night)
            self.inverted = True
            self.pb_switch.setText("Day" if self.on_day else "Night")
            stylesheet = "Color: White; background-color: red"
            self.on, self.off = self.output_controller.get_set_temperatures_inactive(self.sensor)
        self.load()
        self.le_range_on_1_1.setText(str(self.on + self.offset_on))
        self.le_range_on_1_1.setStyleSheet(stylesheet)
        self.le_range_off_1_1.setText(str(self.off + self.offset_off))
        self.le_range_off_1_1.setStyleSheet(stylesheet)
        self.lbl_set_on_1_1.setText(str(self.on))
        self.lbl_set_off_1_1.setText(str(self.off))

    def change_lock(self):
        lock = self.ck_lock.isChecked()
        self.output_controller.change_lock(self.pin_id, lock)
        self.set_controls()

    def set_controls(self):
        if self.ck_lock.isChecked():
            self.cb_out_mode_1_1.setEnabled(False)
            self.cb_sensor_out_1_1.setEnabled(False)
            self.le_range_on_1_1.setEnabled(False)
            self.le_range_off_1_1.setEnabled(False)
            self.pb_reset.setEnabled(False)
            self.cb_trigger.setEnabled(False)
            self.cb_timer_1_1.setEnabled(False)
            self.pb_switch.setEnabled(False)
        else:
            self.cb_out_mode_1_1.setEnabled(True)
            self.cb_sensor_out_1_1.setEnabled(True)
            self.le_range_on_1_1.setEnabled(True)
            self.le_range_off_1_1.setEnabled(True)
            self.pb_reset.setEnabled(True)
            self.cb_trigger.setEnabled(True)
            self.cb_timer_1_1.setEnabled(True)
            self.pb_switch.setEnabled(True)

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
        if not self.inverted:
            self.output_controller.change_range(self.pin_id, on, off, self.day_night)
        else:
            r = "{}, {}".format(on, off)
            if self.day_night == DAY:
                sql = 'UPDATE {} SET `range` = "{}" WHERE id = {}'.format(DB_OUTPUTS, r, self.db_id)
            else:
                sql = 'UPDATE {} SET `range_night` = "{}" WHERE id = {}'.format(DB_OUTPUTS, r, self.db_id)
            self.db.execute_write(sql)

        # self.main_panel.coms_interface.relay_send(NWC_OUTPUT_RANGE, self.pin_id) --- sent by above


class DialogSettings(QDialog, Ui_DialogSettings):
    my_parent = ...  # type: MainWindow

    def __init__(self, parent):
        super(DialogSettings, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.db = parent.db
        self.sub = None
        self.mode = self.main_panel.master_mode  # 1=Master, arduino and server  2=Slave, client only
        self.running = False  # True when running an action
        self.us_tank = 1  # Tank number to operate us sensor
        self.servo_valve = 0
        self.rbustank_1.setChecked(True)

        self.pb_close.clicked.connect(lambda: self.sub.close())

        # self.pbusoperate.clicked.connect(self.us_test)
        # self.rbustank_1.clicked.connect(self.us_set_tank)
        # self.rbustank_2.clicked.connect(self.us_set_tank)
        # self.rbustank_3.clicked.connect(self.us_set_tank)
        #
        # self.rsservovalve_1.clicked.connect(self.sv_set_valve)
        # self.rsservovalve_2.clicked.connect(self.sv_set_valve)
        # self.rsservovalve_3.clicked.connect(self.sv_set_valve)
        # self.rsservovalve_4.clicked.connect(self.sv_set_valve)
        # self.rsservovalve_5.clicked.connect(self.sv_set_valve)
        # self.rsservovalve_6.clicked.connect(self.sv_set_valve)
        # self.pbsvmove.clicked.connect(self.sv_move)

        self.pbsoilread.clicked.connect(self.soil_read)
        # self.main_panel.water_control.new_data.connect(self.update_us_display)
        self.main_panel.coms_interface.update_soil_reading.connect(self.update_soil)

        # Mode
        self.cb_system_mode.addItem("Master", 1)
        self.cb_system_mode.addItem("Slave", 2)
        self.cb_system_mode.setCurrentIndex(self.main_panel.master_mode - 1)
        self.cb_system_mode.currentIndexChanged.connect(self.system_mode_change)

        # Database
        self.settings = QSettings(FN_SETTINGS, QSettings.IniFormat)
        # if self.mode == MASTER:
        self.host = self.settings.value("Database/host")
        self.db_user = self.settings.value("Database/user")
        self.db_password = self.settings.value("Database/password")
        self.db_name = self.settings.value("Database/database")
        self.pb_back_up.clicked.connect(self.db_backup)
        # else:
        #     self.host = "192.168.0.20"  # self.main_panel.server.remote_ip_str
        self.le_db_host.setText(self.host)
        self.le_db_user_name.setText(self.db_user)
        self.le_db_password.setText(self.db_password)
        self.le_db_name.setText(self.db_name)

        # Com ports
        self.pb_rescan_ports.clicked.connect(self.get_ports)
        self.le_ss_port.setText(self.db.get_config(CFT_SS_UNIT, "com", ""))
        self.pb_ss_update.clicked.connect(self.save_ss_port)
        self.le_ss_port.textChanged.connect(lambda: auto_capital(self.le_ss_port))
        self.get_ports()

        # Fans
        row = self.db.execute_one_row("SELECT sensor, mode, Kp, Ki, Kd FROM {} WHERE id = {}".format(DB_FANS, 1))
        self._sensor_1 = row[0]
        self.le_kp_1.setText(str(row[2]))
        self.le_ki_1.setText(str(row[3]))
        self.le_kd_1.setText(str(row[4]))
        row = self.db.execute_one_row("SELECT sensor, mode, Kp, Ki, Kd FROM {} WHERE id = {}".format(DB_FANS, 2))
        self._sensor_2 = row[0]
        self.le_kp_2.setText(str(row[2]))
        self.le_ki_2.setText(str(row[3]))
        self.le_kd_2.setText(str(row[4]))

        self.pb_save_fans_1.clicked.connect(lambda: self.save_fans(1))
        self.pb_reset_fan_1.clicked.connect(lambda: self.main_panel.area_controller.fan_controller.fans[1].reset())
        self.pb_save_fans_2.clicked.connect(lambda: self.save_fans(2))
        self.pb_reset_fan_2.clicked.connect(lambda: self.main_panel.area_controller.fan_controller.fans[2].reset())
        # self.pb_show_log_1.clicked.connect(lambda: self.main_panel.dialog_control("Fan 1 Log", DialogFanLog, 1))
        # self.pb_show_log_2.clicked.connect(lambda: self.main_panel.dialog_control("Fan 2 Log", DialogFanLog, 2))

        self.ck_test.clicked.connect(lambda: self.logging(1))
        self.ck_test_2.clicked.connect(lambda: self.logging(2))

    @pyqtSlot(int, int, int)
    def update_us_display(self, tank, litres, reading):
        self.leusliters.setText(str(litres))
        self.leusreading.setText(str(reading))
        self.lblusoperate.setStyleSheet("background-color: light gray;  color: white;")

    def get_ports(self):
        self.te_ports.clear()
        port_list = serial.tools.list_ports.comports()
        for port, desc, h_wid in sorted(port_list):
            print("{}: {}".format(port, desc))
            self.te_ports.append(port + ":" + desc)

    def save_ss_port(self):
        self.db.set_config(CFT_SS_UNIT, "com", self.le_ss_port.text())
        self.main_panel.scales.get_port()
        self.main_panel.scales.coms_disconnect()
        self.main_panel.scales.connect()
        # play_sound(SND_OK)
        sound_ok()

    def us_set_tank(self):
        rb = self.sender()
        if rb.text().find("1") != -1:
            self.us_tank = 1
        elif rb.text().find("2") != -1:
            self.us_tank = 2
        else:
            self.us_tank = 3

    def us_test(self):
        if self.running:
            return
        self.lblusoperate.setStyleSheet("background-color: red;  color: white;")
        self.main_panel.coms_interface.send_command(COM_US_READ, self.us_tank, None, True)

    def sv_set_valve(self):
        rb = self.sender()
        if rb.text().find("Tank 1") != -1:
            self.servo_valve = SV_TANK_1
        elif rb.text().find("Tank 2") != -1:
            self.servo_valve = SV_TANK_2
        elif rb.text().find("Feed 1") != -1:
            self.servo_valve = SV_FEED_1
        elif rb.text().find("Feed 2") != -1:
            self.servo_valve = SV_FEED_2
        elif rb.text().find("Drain 1") != -1:
            self.servo_valve = SV_DRAIN_1
        elif rb.text().find("Drain 2") != -1:
            self.servo_valve = SV_DRAIN_2

    def sv_move(self):
        pos = int(self.lesvposition.text())
        self.main_panel.coms_interface.send_data(CMD_VALVE, True, MODULE_IO, self.servo_valve, pos)

    def soil_read(self):
        self.main_panel.coms_interface.send_command(COM_SOIL_READ)
        self.running = True
        self.lblsoiloperate.setStyleSheet("background-color: red;  color: white;")

    @pyqtSlot(list)
    def update_soil(self, data):
        if not self.running:
            return
        try:
            for x in range(2, len(data)):
                var_name = "lesoil_%i" % (x - 1)
                ctrl = getattr(self, var_name)
                ctrl.setText(str(data[x]))
                self.running = False
                self.lblsoiloperate.setStyleSheet("background-color: light gray;  color: white;")
        except Exception as e:
            print(e.args)

    # System
    def system_mode_change(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Confirm you wish to change the mode of operation for this computer")
        msg.setInformativeText("The program will restart")
        msg.setWindowTitle("Confirm Mode Change")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            return
        self.settings.setValue('mode', str(self.cb_system_mode.currentData()))
        self.settings.sync()
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    # database
    def scan_ip(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.0.1", 80))
        print(s.getsockname()[0])
        s.close()

    def db_backup(self):
        self.main_panel.db.backup()

    # Fans
    def logging(self, fan):
        if fan == 1:
            self.main_panel.fans[fan].logging = self.ck_test.isChecked()
        else:
            self.main_panel.fans[fan].logging = self.ck_test_2.isChecked()

    def save_fans(self, fan):
        kp = string_to_float(getattr(self, "le_kp_{}".format(fan)).text())
        ki = string_to_float(getattr(self, "le_ki_{}".format(fan)).text())
        kd = string_to_float(getattr(self, "le_kd_{}".format(fan)).text())
        self.db.execute_write("UPDATE {} set Kp = {}, Ki = {}, Kd = {} WHERE id = {} LIMIT 1".
                              format(DB_FANS, kp, ki, kd, fan))
        self.main_panel.area_controller.fan_controller.fans[fan].set_pid(kp, ki, kd)
        self.main_panel.area_controller.fan_controller.fans[fan].reset()
        self.main_panel.coms_interface.relay_send(NWC_FAN_PID, fan)


class DialogProcessPerformance(QDialog, Ui_DialogProcessPreformance):

    def __init__(self, parent):
        super(DialogProcessPerformance, self).__init__()
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.sub = None
        self.main_panel = parent
        self.db = self.main_panel.db
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.epp = float(self.db.get_config(CFT_DISPATCH, "estimate per plant", 50))
        rows = self.db.execute(
            "SELECT DISTINCT(process_id) FROM {} ORDER BY process_id DESC".format(DB_PROCESS_STRAINS))
        self.cb_process.addItem("Select", 0)
        for row in rows:
            self.cb_process.addItem(str(row[0]), row[0])
        self.cb_process.currentIndexChanged.connect(lambda: self.load_process(self.cb_process.currentData()))

    def load_process(self, pid):
        rows = self.db.execute(
            "SELECT item, strain_id, yield FROM {} WHERE process_id = {} AND location > 0 ORDER BY item".
            format(DB_PROCESS_STRAINS, pid))
        txt = '<table cellspacing = "5"  border = "0" width = "50%">'
        total_dif = total = waiting_count = finished_count = 0
        for row in rows:
            strain = self.db.execute_single("SELECT name FROM {} WHERE id = {}".format(DB_STRAINS, row[1]))
            if row[2] == 0:
                result = "Waiting..."
                css = "background-color:white; color:green;"
                waiting_count += 1
            else:
                result = round(row[2] - self.epp, 1)
                total_dif += result
                total += row[2]
                finished_count += 1
                if result < 0:
                    css = "background-color:red; color:white;"
                else:
                    css = "background-color:green; color:black;"
            txt += '<tr><td style="width:35%">{}</td><td>{}</td><td>{}</td><td style="{}">{}</td></tr>'. \
                format(row[0], strain, row[2], css, result)
        txt += '<tr style="font-size:16px;"><td></td><td><b>Totals</td><td>{}</td><td>{}</b></td></tr>'. \
            format(round(total, 1), round(total_dif, 1))
        if finished_count > 0:
            avg = round(total / finished_count, 1)
        else:
            avg = 0
        txt += '<tr style="font-size:14px;"><td></td><td>Average per item</td><td>{}</td><td></td></tr>'. \
            format(avg)
        if waiting_count > 0:
            txt += '<tr style="font-size:14px;"><td></td><td>Waiting</td><td>{}</td><td></td></tr>'. \
                format(waiting_count * self.epp)
            txt += '<tr style="font-size:14px;"><td></td><td>New prediction</td><td>{}</td><td></td></tr>'. \
                format(waiting_count * self.epp + total)
            txt += '<tr style="font-size:14px;"><td></td><td>Avg required</td><td>{}</td><td></td></tr>'. \
                format(round((((waiting_count + finished_count) * self.epp) - total) / waiting_count), 1)
        txt += "</table>"
        self.textEdit.setHtml(txt)


class DialogProcessManager(QDialog, Ui_dialogProcessManager):
    def __init__(self, parent):
        super(DialogProcessManager, self).__init__()
        self.setupUi(self)
        self.sub = None
        self.main_panel = parent
        self.db = self.main_panel.db
        self.pb_close.clicked.connect(lambda: self.sub.close())

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
        self.earliest_start = None
        self.end = ""
        self.pattern = 0
        self.stage = 0
        self.feed_mode = 0
        self.pb_save.clicked.connect(self.save)
        self.pb_start.clicked.connect(self.start_now)
        self.de_start.setDate(datetime.now().date())
        self.de_start.dateChanged.connect(self.date_change)
        rows = self.db.execute('SELECT `name`, `id` FROM {} ORDER BY `name`'.format(DB_PATTERN_NAMES))
        self.cb_patterns.addItem("Select", 0)
        for row in rows:
            self.cb_patterns.addItem(row[0], row[1])
        self.cb_patterns.currentIndexChanged.connect(self.change_pattern)

        rows = self.db.execute_one_row("SELECT MAX(id) FROM processes")
        if rows[0] is None:
            # self.le_id.setText("1")
            self.next_id = 1
        else:
            # self.le_id.setText(str(rows[0] + 1))
            self.next_id = rows[0] + 1
        rows = self.db.execute("SELECT id FROM {} WHERE running = 1 OR location = 0".format(DB_PROCESS))
        self.cb_process.addItem("New ({})".format(self.next_id), 0)
        for row in rows:
            self.cb_process.addItem("{}".format(row[0]), row[0])

        self.cb_process.currentIndexChanged.connect(self.change_process)

        rows = self.db.execute('SELECT `name`, `breeder`, id, qty FROM {} WHERE qty > 0 ORDER BY `name`'.
                               format(DB_STRAINS))
        for i in range(1, 9):
            ctrl = getattr(self, "cb_strain_%i" % i)
            ctrl.addItem("Select", 0)
            ctrl.setEnabled(True)
            for row in rows:
                ctrl.addItem("{} x {}({})".format(row[0], row[3], row[1]), row[2])
            ctrl.currentIndexChanged.connect(self.change_strains)

    def start_now(self):
        self.main_panel.start_new_process(self.edit_id)

    def date_change(self):
        self.cal_end()
        self.start = self.de_start.date().toPyDate()

    def find_earliest_start(self):
        p = self.main_panel.area_controller.get_area_process(1)
        if p > 0:
            end = p.end
            self.earliest_start = end - timedelta(weeks=10)
        else:
            self.earliest_start = datetime.now()

    def cal_end(self):
        end_date = self.de_start.date().toPyDate()
        end_date = end_date + timedelta(days=self.total_days)
        self.le_end_date.setText(datetime.strftime(end_date, "%d/%m/%Y"))
        self.end = end_date

    def change_process(self):
        self.edit_id = int(self.cb_process.currentData())
        if self.edit_id == 0:
            # self.le_id.setText(str(self.next_id))
            # self.cb_qty.setCurrentIndex(0)
            # self.cb_location.setCurrentIndex(0)
            # self.cb_stage.setCurrentIndex(0)
            return
        # self.le_id.setText("N/A")
        rows = self.db.execute_one_row("SELECT id, running, location, start, end, pattern, "
                                       "stage, qty, feed_mode  FROM {} WHERE id = {}".
                                       format(DB_PROCESS, self.edit_id))
        self.running = rows[1]
        self.location = rows[2]
        self.start = rows[3]
        self.end = rows[4]
        self.pattern = rows[5]
        self.stage = rows[6]
        self.qty = rows[7]
        self.feed_mode = rows[8]

        self.de_start.setDate(rows[3])
        if self.running == 1:
            self.de_start.setEnabled(False)
        else:
            self.de_start.setEnabled(True)

        # Strains
        rows = self.db.execute("SELECT item, strain_id  FROM {} WHERE process_id = {}".
                               format(DB_PROCESS_STRAINS, self.edit_id))
        if len(rows) > 0:
            for row in rows:
                ctrl = getattr(self, "cb_strain_%i" % row[0])
                index = ctrl.findData(row[1])
                if index >= 0:
                    ctrl.blockSignals(True)
                    ctrl.setCurrentIndex(index)
                    # if x >= 14:
                    if self.running == 1:
                        ctrl.setEnabled(False)
                    else:
                        ctrl.setEnabled(True)
                    ctrl.blockSignals(False)
                else:
                    # No stock of seed so look up from db
                    strain = self.db.execute_one_row('SELECT name, breeder FROM {} WHERE id = {}'.format(DB_STRAINS, row[1]))
                    if len(strain) > 0:
                        ctrl.addItem("{} ({})".format(strain[0], strain[1]), row[1])
                        ctrl.setCurrentIndex(ctrl.findData(row[1]))
            self.change_strains()
        # pattern
        index = self.cb_patterns.findData(self.pattern)
        if index >= 0:
            self.cb_patterns.blockSignals(True)
            self.cb_patterns.setCurrentIndex(index)
            self.cb_patterns.blockSignals(False)
        self.calculate_duration()
        # self.pb_start.setEnabled(False)
        self.pb_find.setEnabled(False)

    def change_strains(self):
        self.strains.clear()
        for i in range(1, 9):
            ctrl = getattr(self, "cb_strain_%i" % i)
            if ctrl.currentData() != 0:
                self.strains[i] = ctrl.currentData()
        self.calculate_duration()
        self.qty = len(self.strains)
        self.le_qty.setText(str(self.qty))

    def change_pattern(self):
        self.pattern = self.cb_patterns.currentData()
        if self.pattern is None or self.pattern == 0:
            return
        self.calculate_duration()

    def calculate_duration(self):
        if self.pattern is None or self.pattern == 0:
            return

        cpt = self.cb_patterns.currentText()
        dur = self.db.execute_single(
            'SELECT SUM(duration) FROM {} WHERE pid = {}'.format(DB_STAGE_PATTERNS, self.pattern))
        self.le_dur.setText(str(dur))
        if cpt.find("Auto Cal") == 0:
            self.frm_auto_cal.setEnabled(True)
            self.le_longest.setText(str(self.max_day()))
            self.le_shortest.setText(str(self.shortest))
            self.total_days = int(dur) + self.longest
        else:
            self.frm_auto_cal.setEnabled(False)
            self.longest = 0
            self.total_days = int(dur)
        self.le_total.setText(str(self.total_days))
        self.cal_end()

    def max_day(self):
        s = ""
        for x in self.strains:
            s += str(self.strains[x]) + ", "
        s = s[:len(s) - 2]      # Remove last comma
        if len(s) == 0:     # No strains
            self.longest = 0
            self.longest = 0
            return
        sql = 'SELECT MAX(duration_max) FROM {} WHERE id IN ({})'.format(DB_STRAINS, s)
        row = self.db.execute_single(sql)
        if row is None:
            self.longest = 0
        else:
            self.longest = row
        sql = 'SELECT MIN(duration_min) FROM {} WHERE id IN ({})'.format(DB_STRAINS, s)
        row = self.db.execute_single(sql)
        # print(row)
        if row is None:
            self.longest = 0
        else:
            self.shortest = row
        return self.longest

    def save(self):
        if self.edit_id == 0:
            sql = 'INSERT INTO {} (running, location, start, end, pattern, stage, qty, feed_mode) VALUES({}, {}, "{}",' \
                  ' "{}", {}, {}, {}, {})'.\
                format(DB_PROCESS, self.running, self.location, self.start, self.end, self.pattern, self.stage,
                       self.qty, self.feed_mode)
            self.db.execute_write(sql)
            self.edit_id = self.db.execute_single('SELECT LAST_INSERT_ID()')
            # Enter strains in the process strains table
            for x in range(1, self.qty + 1):
                sid = getattr(self, "cb_strain_%i" % x).currentData()
                sql = 'INSERT INTO {} (process_id, item, strain_id) VALUES ({}, {}, {})'.\
                    format(DB_PROCESS_STRAINS, self.edit_id, x, sid)
                self.db.execute_write(sql)
                # Deduct from stock - NOT until it is started
        else:
            sql = 'UPDATE {} SET running = {}, location = {}, start = "{}", end = "{}", pattern = {}, stage = {}, ' \
                  'qty = {}, feed_mode = {} WHERE id = {}'.\
                format(DB_PROCESS, self.running, self.location, self.start, self.end, self.pattern, self.stage,
                       self.qty, self.feed_mode, self.edit_id)
            self.db.execute_write(sql)
            # Delete any entries for this
            sql = 'DELETE FROM {} WHERE process_id = {}'.format(DB_PROCESS_STRAINS, self.edit_id)
            self.db.execute_write(sql)
            for x in range(1, self.qty + 1):
                sql = 'INSERT INTO {} (strain_id, process_id, item) VALUES ({}, {}, {})'.\
                    format(DB_PROCESS_STRAINS, getattr(self, "cb_strain_%i" % x).currentData(), self.edit_id, x)
                self.db.execute_write(sql)


class DialogSoilSensors(QDialog, Ui_DialogSoilSensors):
    def __init__(self, parent, area):
        super(DialogSoilSensors, self).__init__()
        self.setupUi(self)
        self.sub = None
        self.main_panel = parent
        self.db = self.main_panel.db
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.area = area
        self.all_active = int(self.db.get_config(CFT_SOIL_SENSORS, "area {}".format(self.area), 0) == "True")
        self.lbl_name.setText("Soil Sensors Area" + str(self.area))
        items = self.main_panel.area_controller.get_area_items(self.area)
        self.cb_plant_1.addItem("Off", 0)
        self.cb_plant_2.addItem("Off", 0)
        self.cb_plant_3.addItem("Off", 0)
        self.cb_plant_4.addItem("Off", 0)
        for i in items:
            for x in range(1, 5):
                getattr(self, "cb_plant_{}".format(x)).addItem(str(i), i)
        ss = self.main_panel.area_controller.soil_sensors.get_sensor_status(self.area)
        for x in range(1, 5):
            getattr(self, "cb_plant_{}".format(x)).setCurrentIndex(ss[x - 1])
        self.cb_plant_1.currentIndexChanged.connect(lambda: self.change_item(1))
        self.cb_plant_2.currentIndexChanged.connect(lambda: self.change_item(2))
        self.cb_plant_3.currentIndexChanged.connect(lambda: self.change_item(3))
        self.cb_plant_4.currentIndexChanged.connect(lambda: self.change_item(4))

        self.pb_read.clicked.connect(lambda: self.main_panel.coms_interface.send_data(COM_SOIL_READ, True, MODULE_IO))
        # self.cb_plant_1.currentIndexChanged.connect(self.change_item)
        # self.ck_active_all.setChecked(self.all_active)
        # self.ck_active_all.clicked.connect(self.change_all_active)

    def change_item(self, sensor):
        item = self.sender().currentData()
        s = sensor + ((self.area - 1) * 4)
        self.db.set_config_both(CFT_SOIL_SENSORS, s, item)
        self.main_panel.area_controller.soil_sensors.load_status()

    def change_all_active(self):
        aa = self.ck_active_all.isChecked()
        if aa == self.all_active:
            return
        self.db.set_config_both(CFT_SOIL_SENSORS, "area {}".format(self.area), aa)
        self.main_panel.area_controller.soil_sensors.load_status()


class DialogStrains(QDialog, Ui_DialogStrains):
    def __init__(self, parent):
        super(DialogStrains, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.db = self.main_panel.db
        self.sub = None
        self.is_new = False
        self.id = None
        self.filter = "name"
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.lw_strains.doubleClicked.connect(self.load_strain)
        self.lw_strains.clicked.connect(self.show_strain)
        self.pb_new.clicked.connect(self.new)
        self.pb_save.clicked.connect(self.save)
        self.pb_today.clicked.connect(lambda: self.de_pur_date.setDate(datetime.now().date()))
        self.frame.setEnabled(False)

        # self.cw = DialogCalendar()  # Holds calendar window
        # self.cw.new_date.connect(self.calendar_callback)
        # self.le_pur_date.installEventFilter(self)
        # self.le_last_date.installEventFilter(self)

        self.cb_filter.addItem("Name", "name")
        self.cb_filter.addItem("Breeder", "breeder")
        self.cb_starting.addItem("All")
        for i in range(1, 27):
            self.cb_starting.addItem(chr(i + 64))

        self.cb_filter.currentIndexChanged.connect(self.load_list)
        self.cb_starting.currentIndexChanged.connect(self.load_list)
        self.load_list()

    # def eventFilter(self, watched, event):
    #     if watched == self.le_pur_date:
    #         ctr = 0
    #         # if event.type() == QtCore.QEvent.MouseButtonDblClick:
    #         #     if watched.isEnabled():
    #         #         self.cw.set_date(watched.text())
    #         #         self.cw.ctrlID = ctr
    #         #         self.cw.show()
    #         # if event.type() == QtCore.QEvent.KeyPress:
    #         #     key = event.key()
    #         #     if key == QtCore.Qt.Key_Return:
    #         #         self.cw.set_date(watched.text())
    #         #         self.cw.ctrlID = ctr
    #         #         self.cw.show()
    #
    #     return QWidget.eventFilter(self, watched, event)

    # @pyqtSlot(datetime, int)
    # def calendar_callback(self, d, c):
    #     print("New date sender" + str(c))
    #     if c == 0:
    #         self.le_pur_date.setText(datetime.strftime(d, '%d/%m/%y'))
    #
    def load_list(self):
        self.lw_strains.clear()
        self.filter = self.cb_filter.currentData()
        if self.filter == "name":
            nf = self.cb_starting.currentText()
            if nf == "All":
                rows = self.db.execute("SELECT name, breeder, id FROM {} ORDER BY {}".format(DB_STRAINS, self.filter))
            else:
                rows = self.db.execute("SELECT name, breeder, id FROM {} WHERE  name LIKE '{}%'".
                                       format(DB_STRAINS, nf))
            self.cb_starting.setEnabled(True)
        else:
            self.cb_starting.setEnabled(False)
            rows = self.db.execute("SELECT name, breeder, id FROM {} ORDER BY {}".format(DB_STRAINS, self.filter))
        for row in rows:
            lw_item = QListWidgetItem(row[0] + "(" + row[1] + ")")
            v_item = QVariant(row[2])
            lw_item.setData(Qt.UserRole, v_item)
            self.lw_strains.addItem(lw_item)

    def show_strain(self):
        self.id = self.lw_strains.currentItem().data(Qt.UserRole)
        if self.id is None:
            return
        strain = self.db.execute_one_row("SELECT * FROM {} WHERE id = {}".format(DB_STRAINS, self.id))
        if strain is None:
            return
        self.le_breeder.setText(strain[1])
        self.le_name.setText(strain[2])
        self.le_qty.setText(str(strain[3]))
        self.le_dur_min.setText(str(strain[4]))
        self.le_dur_max.setText(str(strain[5]))
        self.le_sativa.setText(strain[6])
        self.le_indica.setText(strain[7])
        self.le_height.setText(strain[8])
        self.le_flavour.setText(strain[9])
        self.le_effect.setText(strain[10])
        self.le_yeild.setText(strain[11])
        self.te_info.setText(strain[12])
        self.te_notes.setText(strain[13])
        self.le_supplier.setText(strain[14])
        self.le_price.setText(str(strain[15]))
        if strain[16] is not None:
            self.de_pur_date.setDate(strain[16])
        else:
            self.de_pur_date.setDate(QDate(2000, 1, 1))
        self.le_last_date.setText(str(strain[17]))
        self.le_genetics.setText(strain[18])
        self.le_thc.setText(strain[19])
        self.le_cbd.setText(strain[20])

    def load_strain(self):
        self.show_strain()
        self.frame.setEnabled(True)
        self.pb_save.setEnabled(True)

    def clear(self):
        self.le_breeder.setText("")
        self.le_name.setText("")
        self.le_qty.setText("")
        self.le_dur_min.setText("")
        self.le_dur_max.setText("")
        self.le_sativa.setText("")
        self.le_indica.setText("")
        self.le_height.setText("")
        self.le_flavour.setText("")
        self.le_effect.setText("")
        self.le_yeild.setText("")
        self.te_info.setText("")
        self.te_notes.setText("")
        self.le_supplier.setText("")
        self.le_price.setText("")
        self.de_pur_date.setDate(datetime.now().date())
        self.le_last_date.setText("")
        self.le_cbd.setText("")
        self.le_thc.setText("")
        self.le_genetics.setText("")

    def new(self):
        self.frame.setEnabled(True)
        self.clear()
        self.pb_save.setEnabled(True)
        self.is_new = True

    def save(self):
        if self.is_new:
            sql = 'INSERT INTO {} (breeder, name, qty, duration_min, duration_max, type_sativa, type_indica, height, ' \
                  'flavour, effect, yeild, info, notes, supplier, price, last_used_id, genetics, thc, cbd) ' \
                  'VALUES ("{}", "{}", {}, {}, {}, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", {}, {}, "{}", "{}", "{}") '
        else:
            sql = 'UPDATE {} SET breeder = "{}", name = "{}", qty = {}, duration_min = {}, duration_max = {}, type_sativa = "{}",' \
                  ' type_indica = "{}", height = "{}", flavour = "{}", effect = "{}", yeild = "{}", info = "{}", notes = "{}", ' \
                  'supplier = "{}", price = {}, last_used_id ={}, genetics = "{}", thc = "{}", cbd = "{}" WHERE id = {}'
        qty = self.le_qty.text()
        if qty == 'None' or qty == '':
            qty = 0
        price = self.le_price.text()
        if price == "" or price == 'None':
            price = 0
        lid = self.le_last_date.text()
        if lid == "" or lid == 'None':
            lid = 0
        min_ = self.le_dur_min.text()
        if min_ == "":
            min_ = 0
        max_ = self.le_dur_max.text()
        if max_ == "":
            max_ = 0
        sql = sql.format(DB_STRAINS, self.le_breeder.text()[:45],
                         self.le_name.text()[:45],
                         qty,
                         min_,
                         max_,
                         self.le_sativa.text()[:5],
                         self.le_indica.text()[:5],
                         self.le_height.text()[:30],
                         self.le_flavour.toPlainText(),
                         self.le_effect.toPlainText(),
                         self.le_yeild.text()[:30],
                         self.te_info.toPlainText(),
                         self.te_notes.toPlainText(),
                         self.le_supplier.text()[:30],
                         float(price),
                         lid,
                         self.le_genetics.text()[:100],
                         self.le_thc.text()[:20],
                         self.le_cbd.text()[:20],
                         self.id)

        self.db.execute_write(sql)
        # if self.de_pur_date.date() != "":
        sql = 'UPDATE {} SET date_add = "{}" WHERE id = {}'.format(DB_STRAINS, self.de_pur_date.date().toPyDate(), self.id)
        self.db.execute_write(sql)
        # if self.le_last_date.text() != "":
        #     sql = 'UPDATE {} SET last_used_id = "{}" WHERE id = {}'.format(DB_STRAINS, self.le_last_date.text(), self.id)
        #     self.db.execute_write(sql)

        self.is_new = False
        self.pb_save.setEnabled(False)
        self.frame.setEnabled(False)
        self.load_list()


class DialogProcessLogs(QDialog, Ui_DialogJournalViewer):
    def __init__(self, parent):
        """
        :type parent: MainWindow
        """
        super(DialogProcessLogs, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_window = parent
        self.sub = None
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.log_name = ""
        files = self.main_window.logger.get_log_list(LOG_JOURNAL)
        self.cb_process.clear()
        # self.cb_process.blockSignals(True)
        self.cb_process.addItem("Select", 0)
        for f in files:
            self.cb_process.addItem(f[0:-4], f)
        # self.cb_process.blockSignals(False)
        files = self.main_window.logger.get_log_list(LOG_FEED)
        self.cb_feed.clear()
        self.cb_process.addItem("Select", 0)
        for f in files:
            self.cb_feed.addItem(f[0:-4], f)
        self.cb_process.currentIndexChanged.connect(self.change_journal)
        self.cb_feed.currentIndexChanged.connect(self.change_feed)
        self.pb_save.clicked.connect(self.save_file)

    def change_journal(self):
        log = self.cb_process.currentData()
        if log == 0:
            self.te_log.setHtml("")
            return
        self.log_name = self.cb_process.currentText()
        self.te_log.setHtml(self.main_window.logger.get_log_contents(LOG_JOURNAL, log))

    def change_feed(self):
        log = self.cb_feed.currentData()
        if log == 0:
            self.te_log.setHtml("")
            return
        self.log_name = self.cb_feed.currentText()
        self.te_log.setHtml(self.main_window.logger.get_log_contents(LOG_FEED, log))

    def save_file(self):
        with open(self.main_window.logger.journal_path + "\\" + self.log_name + ".jrn", 'w') as yourFile:
            yourFile.write(str(self.te_log.toPlainText()))


class DialogSeedPicker(QDialog, Ui_DialogSeedPicker):
    def __init__(self, parent):
        """
        :type parent: MainWindow
        """
        super(DialogSeedPicker, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.main_panel = parent
        self.sub = None
        self.db = parent.db
        self.sort_order = "qty"
        self.pb_close.clicked.connect(lambda: self.sub.close())
        self.ck_in_stock.clicked.connect(self.load_list)
        self.cb_sort.addItem("Quantity", "qty")
        self.cb_sort.addItem("Name", "name")
        self.cb_sort.addItem("Min. Duration", "duration_min")
        self.cb_sort.addItem("Breeder", "breeder")
        self.print_contents = QTextEdit(self)
        self.print_contents.setVisible(False)
        self.load_list()
        self.cb_sort.currentIndexChanged.connect(self.change_sort)
        self.pb_print.clicked.connect(self.print_stock)

    def load_list(self):
        if self.ck_in_stock.isChecked():
            qty = 1
        else:
            qty = 0
        rows = self.db.execute("SELECT qty, name, breeder, duration_min, duration_max, type_indica, type_sativa,"
                               " id FROM {} WHERE qty >= {} ORDER BY {}".format(DB_STRAINS, qty, self.sort_order))
        text = p_text = '<table cellpadding = "3"  border = "1" cellspacing = "0" >'
        text += "<tr><td>Qty</td><td>Name</td><td>Breeder</td><td>Min Dur</td><td>Max Dur</td><td>Indica</td>" \
                "<td>Sativa</td><td>ID</td></tr>"
        p_text += "<tr><td>Qty</td><td>Stock</td><td>Name</td><td>Breeder</td><td>ID</td></tr>"
        for row in rows:
            text += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>"\
                .format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            p_text += "<tr><td> </td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                row[0], row[1], row[2], row[7])
        text += '</table>'
        self.te_strains.setHtml(text)
        self.print_contents.setHtml(p_text)
        qty = self.db.execute_single("SELECT SUM(qty) FROM {}".format(DB_STRAINS))
        self.le_stock.setText(str(qty))

    def change_sort(self):
        self.sort_order = self.cb_sort.currentData()
        self.load_list()

    def print_stock(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setFontEmbeddingEnabled(True)
        printer.setOrientation(QPrinter.Portrait)
        printer.setPageMargins(2, 2, 2, 2, QPrinter.Millimeter)
        printer.setFullPage(True)
        printer.setPaperSize(QPrinter.A4)
        dialog = QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle("Print Feed Schedule")
        # if dialog.exec_() == QDialog.Accepted:
        #    self.editor.print_(dialog.printer())

        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handle_paint_request)
        dialog.exec_()

    def handle_paint_request(self, printer):
        self.print_contents.print_(printer)


