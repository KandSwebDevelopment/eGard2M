# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogDispatchOverview.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogLogistics(object):
    def setupUi(self, DialogLogistics):
        DialogLogistics.setObjectName("DialogLogistics")
        DialogLogistics.resize(878, 670)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogLogistics.setFont(font)
        self.tabWidget = QtWidgets.QTabWidget(DialogLogistics)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 871, 651))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.te_stock_summary = QtWidgets.QTextEdit(self.tab)
        self.te_stock_summary.setGeometry(QtCore.QRect(370, 20, 451, 511))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.te_stock_summary.setFont(font)
        self.te_stock_summary.setObjectName("te_stock_summary")
        self.lw_available = QtWidgets.QListWidget(self.tab)
        self.lw_available.setGeometry(QtCore.QRect(10, 20, 301, 511))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lw_available.setFont(font)
        self.lw_available.setObjectName("lw_available")
        self.tabWidget.addTab(self.tab, "")
        self.jars = QtWidgets.QWidget()
        self.jars.setObjectName("jars")
        self.te_stock_list = QtWidgets.QTextEdit(self.jars)
        self.te_stock_list.setGeometry(QtCore.QRect(10, 40, 841, 551))
        self.te_stock_list.setReadOnly(True)
        self.te_stock_list.setObjectName("te_stock_list")
        self.rb_sort_1 = QtWidgets.QRadioButton(self.jars)
        self.rb_sort_1.setGeometry(QtCore.QRect(30, 10, 82, 17))
        self.rb_sort_1.setObjectName("rb_sort_1")
        self.rb_sort_2 = QtWidgets.QRadioButton(self.jars)
        self.rb_sort_2.setGeometry(QtCore.QRect(90, 10, 82, 17))
        self.rb_sort_2.setObjectName("rb_sort_2")
        self.rb_sort_3 = QtWidgets.QRadioButton(self.jars)
        self.rb_sort_3.setGeometry(QtCore.QRect(160, 10, 82, 17))
        self.rb_sort_3.setObjectName("rb_sort_3")
        self.tabWidget.addTab(self.jars, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.te_future = QtWidgets.QTextEdit(self.tab_3)
        self.te_future.setGeometry(QtCore.QRect(300, 10, 241, 601))
        self.te_future.setObjectName("te_future")
        self.te_upcomming = QtWidgets.QTextEdit(self.tab_3)
        self.te_upcomming.setGeometry(QtCore.QRect(590, 500, 161, 71))
        self.te_upcomming.setObjectName("te_upcomming")
        self.le_for = QtWidgets.QLineEdit(self.tab_3)
        self.le_for.setGeometry(QtCore.QRect(80, 530, 51, 20))
        self.le_for.setObjectName("le_for")
        self.rb_oz_g = QtWidgets.QRadioButton(self.tab_3)
        self.rb_oz_g.setGeometry(QtCore.QRect(210, 40, 82, 21))
        self.rb_oz_g.setChecked(True)
        self.rb_oz_g.setObjectName("rb_oz_g")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(140, 120, 47, 16))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.label.setObjectName("label")
        self.rb_oz_g_2 = QtWidgets.QRadioButton(self.tab_3)
        self.rb_oz_g_2.setGeometry(QtCore.QRect(210, 70, 82, 21))
        self.rb_oz_g_2.setObjectName("rb_oz_g_2")
        self.le_weekly = QtWidgets.QLineEdit(self.tab_3)
        self.le_weekly.setGeometry(QtCore.QRect(10, 110, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Oblivious font")
        font.setPointSize(12)
        self.le_weekly.setFont(font)
        # self.le_weekly.setReadOnly(True)
        self.le_weekly.setObjectName("le_weekly")
        self.le_weeks = QtWidgets.QLineEdit(self.tab_3)
        self.le_weeks.setGeometry(QtCore.QRect(100, 120, 31, 20))
        self.le_weeks.setObjectName("le_weeks")
        self.le_weight = QtWidgets.QLineEdit(self.tab_3)
        self.le_weight.setGeometry(QtCore.QRect(10, 40, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(48)
        self.le_weight.setFont(font)
        self.le_weight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_weight.setReadOnly(True)
        self.le_weight.setClearButtonEnabled(False)
        self.le_weight.setObjectName("le_weight")
        self.le_change = QtWidgets.QLineEdit(self.tab_3)
        self.le_change.setGeometry(QtCore.QRect(20, 160, 61, 20))
        self.le_change.setObjectName("le_change")
        self.pb_refresh = QtWidgets.QPushButton(self.tab_3)
        self.pb_refresh.setGeometry(QtCore.QRect(210, 110, 75, 31))
        self.pb_refresh.setObjectName("pb_refresh")
        self.te_instock = QtWidgets.QTextEdit(self.tab_3)
        self.te_instock.setGeometry(QtCore.QRect(550, 10, 311, 461))
        self.te_instock.setObjectName("te_instock")
        self.pb_reset = QtWidgets.QPushButton(self.tab_3)
        self.pb_reset.setGeometry(QtCore.QRect(180, 510, 75, 23))
        self.pb_reset.setObjectName("pb_reset")
        self.lw_clients = QtWidgets.QListWidget(self.tab_3)
        self.lw_clients.setGeometry(QtCore.QRect(10, 310, 171, 192))
        self.lw_clients.setObjectName("lw_clients")
        self.le_amount = QtWidgets.QLineEdit(self.tab_3)
        self.le_amount.setGeometry(QtCore.QRect(10, 530, 51, 20))
        self.le_amount.setObjectName("le_amount")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(10, 510, 61, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(80, 510, 61, 16))
        self.label_4.setObjectName("label_4")
        self.pb_change = QtWidgets.QPushButton(self.tab_3)
        self.pb_change.setGeometry(QtCore.QRect(20, 560, 75, 31))
        self.pb_change.setObjectName("pb_change")
        self.groupBox = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox.setGeometry(QtCore.QRect(10, 190, 271, 121))
        self.groupBox.setObjectName("groupBox")
        self.le_upcoming_total_1 = QtWidgets.QLineEdit(self.groupBox)
        self.le_upcoming_total_1.setGeometry(QtCore.QRect(180, 30, 61, 20))
        self.le_upcoming_total_1.setObjectName("le_upcoming_total_1")
        self.lbl_upcoming_1 = QtWidgets.QLabel(self.groupBox)
        self.lbl_upcoming_1.setGeometry(QtCore.QRect(50, 34, 101, 16))
        self.lbl_upcoming_1.setText("")
        self.lbl_upcoming_1.setObjectName("lbl_upcoming_1")
        self.ck_upcoming_1 = QtWidgets.QCheckBox(self.groupBox)
        self.ck_upcoming_1.setGeometry(QtCore.QRect(20, 26, 21, 31))
        self.ck_upcoming_1.setText("")
        self.ck_upcoming_1.setObjectName("ck_upcoming_1")
        self.lbl_upcoming_2 = QtWidgets.QLabel(self.groupBox)
        self.lbl_upcoming_2.setGeometry(QtCore.QRect(50, 64, 101, 16))
        self.lbl_upcoming_2.setText("")
        self.lbl_upcoming_2.setObjectName("lbl_upcoming_2")
        self.ck_upcoming_2 = QtWidgets.QCheckBox(self.groupBox)
        self.ck_upcoming_2.setGeometry(QtCore.QRect(20, 56, 21, 31))
        self.ck_upcoming_2.setText("")
        self.ck_upcoming_2.setObjectName("ck_upcoming_2")
        self.le_upcoming_total_2 = QtWidgets.QLineEdit(self.groupBox)
        self.le_upcoming_total_2.setGeometry(QtCore.QRect(180, 60, 61, 20))
        self.le_upcoming_total_2.setObjectName("le_upcoming_total_2")
        self.lbl_upcoming_3 = QtWidgets.QLabel(self.groupBox)
        self.lbl_upcoming_3.setGeometry(QtCore.QRect(50, 94, 101, 16))
        self.lbl_upcoming_3.setText("")
        self.lbl_upcoming_3.setObjectName("lbl_upcoming_3")
        self.ck_upcoming_3 = QtWidgets.QCheckBox(self.groupBox)
        self.ck_upcoming_3.setGeometry(QtCore.QRect(20, 86, 21, 31))
        self.ck_upcoming_3.setText("")
        self.ck_upcoming_3.setObjectName("ck_upcoming_3")
        self.le_upcoming_total_3 = QtWidgets.QLineEdit(self.groupBox)
        self.le_upcoming_total_3.setGeometry(QtCore.QRect(180, 90, 61, 20))
        self.le_upcoming_total_3.setObjectName("le_upcoming_total_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.pb_close = QtWidgets.QPushButton(DialogLogistics)
        self.pb_close.setGeometry(QtCore.QRect(790, 10, 75, 23))
        self.pb_close.setObjectName("pb_close")

        self.retranslateUi(DialogLogistics)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(DialogLogistics)

    def retranslateUi(self, DialogLogistics):
        _translate = QtCore.QCoreApplication.translate
        DialogLogistics.setWindowTitle(_translate("DialogLogistics", "Dialog"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("DialogLogistics", "Selection"))
        self.rb_sort_1.setText(_translate("DialogLogistics", "Jar"))
        self.rb_sort_2.setText(_translate("DialogLogistics", "Strain"))
        self.rb_sort_3.setText(_translate("DialogLogistics", "Availability"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.jars), _translate("DialogLogistics", "Jars Overview"))
        self.rb_oz_g.setText(_translate("DialogLogistics", "grams"))
        self.label_2.setText(_translate("DialogLogistics", "Weeks"))
        self.label.setText(_translate("DialogLogistics", "Total"))
        self.rb_oz_g_2.setText(_translate("DialogLogistics", "ozs"))
        self.le_weekly.setText(_translate("DialogLogistics", "000.0"))
        self.le_weight.setText(_translate("DialogLogistics", "0000.0"))
        self.pb_refresh.setText(_translate("DialogLogistics", "Refresh"))
        self.pb_reset.setText(_translate("DialogLogistics", "Reset"))
        self.label_3.setText(_translate("DialogLogistics", "Amount"))
        self.label_4.setText(_translate("DialogLogistics", "For"))
        self.pb_change.setText(_translate("DialogLogistics", "Change"))
        self.groupBox.setTitle(_translate("DialogLogistics", "Up Comming"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("DialogLogistics", "Planning"))
        self.pb_close.setText(_translate("DialogLogistics", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogLogistics = QtWidgets.QDialog()
    ui = Ui_DialogLogistics()
    ui.setupUi(DialogLogistics)
    DialogLogistics.show()
    sys.exit(app.exec_())

