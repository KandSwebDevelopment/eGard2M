# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogAccess.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogDEmodule(object):
    def setupUi(self, DialogDEmodule):
        DialogDEmodule.setObjectName("DialogDEmodule")
        DialogDEmodule.resize(405, 427)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogDEmodule.setFont(font)
        self.label = QtWidgets.QLabel(DialogDEmodule)
        self.label.setGeometry(QtCore.QRect(20, 20, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(DialogDEmodule)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 111, 16))
        self.label_2.setObjectName("label_2")
        self.le_cover_dur = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_cover_dur.setGeometry(QtCore.QRect(140, 20, 31, 20))
        self.le_cover_dur.setObjectName("le_cover_dur")
        self.le_auto_delay = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_auto_delay.setGeometry(QtCore.QRect(140, 50, 31, 20))
        self.le_auto_delay.setObjectName("le_auto_delay")
        self.pb_reboot = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_reboot.setGeometry(QtCore.QRect(300, 260, 75, 26))
        self.pb_reboot.setObjectName("pb_reboot")
        self.pb_close = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_close.setGeometry(QtCore.QRect(310, 390, 75, 26))
        self.pb_close.setObjectName("pb_close")
        self.label_3 = QtWidgets.QLabel(DialogDEmodule)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pb_scan = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_scan.setGeometry(QtCore.QRect(100, 260, 75, 26))
        self.pb_scan.setCheckable(False)
        self.pb_scan.setChecked(False)
        self.pb_scan.setAutoDefault(False)
        self.pb_scan.setObjectName("pb_scan")
        self.le_kwh_total = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_kwh_total.setGeometry(QtCore.QRect(140, 100, 101, 20))
        self.le_kwh_total.setObjectName("le_kwh_total")
        self.label_4 = QtWidgets.QLabel(DialogDEmodule)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 161, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(DialogDEmodule)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 161, 16))
        self.label_5.setObjectName("label_5")
        self.le_seconds = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_seconds.setGeometry(QtCore.QRect(190, 150, 51, 20))
        self.le_seconds.setObjectName("le_seconds")
        self.le_watts = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_watts.setGeometry(QtCore.QRect(190, 190, 51, 20))
        self.le_watts.setObjectName("le_watts")
        self.label_6 = QtWidgets.QLabel(DialogDEmodule)
        self.label_6.setGeometry(QtCore.QRect(250, 150, 111, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(DialogDEmodule)
        self.label_7.setGeometry(QtCore.QRect(250, 190, 111, 16))
        self.label_7.setObjectName("label_7")
        self.line = QtWidgets.QFrame(DialogDEmodule)
        self.line.setGeometry(QtCore.QRect(20, 80, 371, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.p_save = QtWidgets.QPushButton(DialogDEmodule)
        self.p_save.setGeometry(QtCore.QRect(300, 50, 75, 26))
        self.p_save.setObjectName("p_save")
        self.pb_update_freq = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_update_freq.setGeometry(QtCore.QRect(330, 152, 61, 26))
        self.pb_update_freq.setObjectName("pb_update_freq")
        self.pb_store = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_store.setGeometry(QtCore.QRect(300, 100, 75, 26))
        self.pb_store.setObjectName("pb_store")
        self.label_8 = QtWidgets.QLabel(DialogDEmodule)
        self.label_8.setGeometry(QtCore.QRect(20, 220, 161, 16))
        self.label_8.setObjectName("label_8")
        self.le_pp_kw = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_pp_kw.setGeometry(QtCore.QRect(190, 220, 51, 20))
        self.le_pp_kw.setObjectName("le_pp_kw")
        self.line_2 = QtWidgets.QFrame(DialogDEmodule)
        self.line_2.setGeometry(QtCore.QRect(20, 130, 371, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pb_query = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_query.setGeometry(QtCore.QRect(190, 260, 75, 26))
        self.pb_query.setCheckable(False)
        self.pb_query.setChecked(False)
        self.pb_query.setAutoDefault(False)
        self.pb_query.setObjectName("pb_query")
        self.pb_cover_open = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_open.setGeometry(QtCore.QRect(130, 310, 101, 25))
        self.pb_cover_open.setObjectName("pb_cover_open")
        self.pb_cover_close = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_close.setGeometry(QtCore.QRect(130, 340, 101, 25))
        self.pb_cover_close.setObjectName("pb_cover_close")
        self.line_3 = QtWidgets.QFrame(DialogDEmodule)
        self.line_3.setGeometry(QtCore.QRect(20, 290, 371, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.pb_door_open = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_door_open.setGeometry(QtCore.QRect(240, 310, 101, 25))
        self.pb_door_open.setObjectName("pb_door_open")
        self.pb_door_close = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_door_close.setGeometry(QtCore.QRect(240, 340, 101, 25))
        self.pb_door_close.setObjectName("pb_door_close")
        self.pb_cover_unlock = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_unlock.setGeometry(QtCore.QRect(20, 310, 101, 25))
        self.pb_cover_unlock.setObjectName("pb_cover_unlock")
        self.pb_cover_lock = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_lock.setGeometry(QtCore.QRect(20, 340, 101, 25))
        self.pb_cover_lock.setObjectName("pb_cover_lock")
        self.line_4 = QtWidgets.QFrame(DialogDEmodule)
        self.line_4.setGeometry(QtCore.QRect(20, 370, 371, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.pb_update_diff = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_update_diff.setGeometry(QtCore.QRect(330, 182, 61, 26))
        self.pb_update_diff.setObjectName("pb_update_diff")
        self.pb_update_pulses = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_update_pulses.setGeometry(QtCore.QRect(330, 212, 61, 26))
        self.pb_update_pulses.setObjectName("pb_update_pulses")

        self.retranslateUi(DialogDEmodule)
        QtCore.QMetaObject.connectSlotsByName(DialogDEmodule)

    def retranslateUi(self, DialogDEmodule):
        _translate = QtCore.QCoreApplication.translate
        DialogDEmodule.setWindowTitle(_translate("DialogDEmodule", "DM Module"))
        self.label.setText(_translate("DialogDEmodule", "Cover Duration"))
        self.label_2.setText(_translate("DialogDEmodule", "Auto Close Delay"))
        self.pb_reboot.setText(_translate("DialogDEmodule", "Reboot"))
        self.pb_close.setText(_translate("DialogDEmodule", "Close"))
        self.label_3.setText(_translate("DialogDEmodule", "kWh Total"))
        self.pb_scan.setToolTip(_translate("DialogDEmodule", "Request the above information"))
        self.pb_scan.setText(_translate("DialogDEmodule", "Scan"))
        self.label_4.setText(_translate("DialogDEmodule", "watt Update frequency"))
        self.label_5.setText(_translate("DialogDEmodule", "kWh Update difference"))
        self.label_6.setText(_translate("DialogDEmodule", "seconds"))
        self.label_7.setText(_translate("DialogDEmodule", "watts"))
        self.p_save.setText(_translate("DialogDEmodule", "Save"))
        self.pb_update_freq.setText(_translate("DialogDEmodule", "Update"))
        self.pb_store.setText(_translate("DialogDEmodule", "Store"))
        self.label_8.setText(_translate("DialogDEmodule", "Pulses per Kw"))
        self.pb_query.setToolTip(_translate("DialogDEmodule", "Requests cover position and locks status"))
        self.pb_query.setText(_translate("DialogDEmodule", "Query"))
        self.pb_cover_open.setText(_translate("DialogDEmodule", "Cover Open"))
        self.pb_cover_close.setText(_translate("DialogDEmodule", "Cover Close"))
        self.pb_door_open.setText(_translate("DialogDEmodule", "Door Unlock"))
        self.pb_door_close.setText(_translate("DialogDEmodule", "Door Lock"))
        self.pb_cover_unlock.setText(_translate("DialogDEmodule", "Cover Unlock"))
        self.pb_cover_lock.setText(_translate("DialogDEmodule", "Cover Lock"))
        self.pb_update_diff.setText(_translate("DialogDEmodule", "Update"))
        self.pb_update_pulses.setText(_translate("DialogDEmodule", "Update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDEmodule = QtWidgets.QDialog()
    ui = Ui_DialogDEmodule()
    ui.setupUi(DialogDEmodule)
    DialogDEmodule.show()
    sys.exit(app.exec_())

