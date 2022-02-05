# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogFeedSchedules.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSchedules(object):
    def setupUi(self, DialogSchedules):
        DialogSchedules.setObjectName("DialogSchedules")
        DialogSchedules.resize(444, 300)
        font = QtGui.QFont()
        font.setPointSize(10)
        DialogSchedules.setFont(font)
        self.label_2 = QtWidgets.QLabel(DialogSchedules)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 101, 21))
        self.label_2.setObjectName("label_2")
        self.le_id = QtWidgets.QLineEdit(DialogSchedules)
        self.le_id.setGeometry(QtCore.QRect(360, 10, 61, 20))
        self.le_id.setMouseTracking(False)
        self.le_id.setReadOnly(True)
        self.le_id.setObjectName("le_id")
        self.label_5 = QtWidgets.QLabel(DialogSchedules)
        self.label_5.setGeometry(QtCore.QRect(340, 13, 47, 13))
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(DialogSchedules)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label.setObjectName("label")
        self.cb_schedules = QtWidgets.QComboBox(DialogSchedules)
        self.cb_schedules.setGeometry(QtCore.QRect(80, 10, 241, 22))
        self.cb_schedules.setEditable(False)
        self.cb_schedules.setObjectName("cb_schedules")
        self.tw_schedule = QtWidgets.QTableWidget(DialogSchedules)
        self.tw_schedule.setGeometry(QtCore.QRect(10, 70, 241, 221))
        self.tw_schedule.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_schedule.setAlternatingRowColors(True)
        self.tw_schedule.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_schedule.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_schedule.setObjectName("tw_schedule")
        self.tw_schedule.setColumnCount(0)
        self.tw_schedule.setRowCount(0)
        self.pb_close = QtWidgets.QPushButton(DialogSchedules)
        self.pb_close.setGeometry(QtCore.QRect(350, 260, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.le_end = QtWidgets.QLineEdit(DialogSchedules)
        self.le_end.setGeometry(QtCore.QRect(300, 120, 31, 20))
        self.le_end.setObjectName("le_end")
        self.le_start = QtWidgets.QLineEdit(DialogSchedules)
        self.le_start.setGeometry(QtCore.QRect(260, 120, 31, 20))
        self.le_start.setObjectName("le_start")
        self.le_lpp = QtWidgets.QLineEdit(DialogSchedules)
        self.le_lpp.setGeometry(QtCore.QRect(340, 120, 51, 20))
        self.le_lpp.setObjectName("le_lpp")
        self.cb_recipe = QtWidgets.QComboBox(DialogSchedules)
        self.cb_recipe.setGeometry(QtCore.QRect(260, 160, 141, 22))
        self.cb_recipe.setObjectName("cb_recipe")
        self.lineEdit = QtWidgets.QLineEdit(DialogSchedules)
        self.lineEdit.setGeometry(QtCore.QRect(400, 120, 31, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(DialogSchedules)
        self.pushButton.setGeometry(QtCore.QRect(270, 200, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(DialogSchedules)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 200, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(DialogSchedules)
        self.pushButton_3.setGeometry(QtCore.QRect(250, 70, 31, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(DialogSchedules)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 90, 31, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(DialogSchedules)
        self.pushButton_5.setGeometry(QtCore.QRect(400, 160, 31, 23))
        self.pushButton_5.setObjectName("pushButton_5")

        self.retranslateUi(DialogSchedules)
        QtCore.QMetaObject.connectSlotsByName(DialogSchedules)

    def retranslateUi(self, DialogSchedules):
        _translate = QtCore.QCoreApplication.translate
        DialogSchedules.setWindowTitle(_translate("DialogSchedules", "Feed Schedules"))
        self.label_2.setText(_translate("DialogSchedules", "Schedule Items"))
        self.label_5.setText(_translate("DialogSchedules", "ID"))
        self.label.setText(_translate("DialogSchedules", "Schedule"))
        self.pb_close.setText(_translate("DialogSchedules", "Close"))
        self.pushButton.setText(_translate("DialogSchedules", "Save"))
        self.pushButton_2.setText(_translate("DialogSchedules", "Save As"))
        self.pushButton_3.setText(_translate("DialogSchedules", "+"))
        self.pushButton_4.setText(_translate("DialogSchedules", "-"))
        self.pushButton_5.setText(_translate("DialogSchedules", "+"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogSchedules = QtWidgets.QWidget()
    ui = Ui_DialogSchedules()
    ui.setupUi(DialogSchedules)
    DialogSchedules.show()
    sys.exit(app.exec_())

