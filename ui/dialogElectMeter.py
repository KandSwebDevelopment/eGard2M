# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogElectMeter.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogElectMeter(object):
    def setupUi(self, DialogElectMeter):
        DialogElectMeter.setObjectName("DialogElectMeter")
        DialogElectMeter.resize(410, 220)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogElectMeter.setFont(font)
        self.pb_update_diff = QtWidgets.QPushButton(DialogElectMeter)
        self.pb_update_diff.setGeometry(QtCore.QRect(330, 93, 61, 26))
        self.pb_update_diff.setObjectName("pb_update_diff")
        self.le_seconds = QtWidgets.QLineEdit(DialogElectMeter)
        self.le_seconds.setGeometry(QtCore.QRect(190, 61, 51, 20))
        self.le_seconds.setObjectName("le_seconds")
        self.label_8 = QtWidgets.QLabel(DialogElectMeter)
        self.label_8.setGeometry(QtCore.QRect(20, 131, 161, 16))
        self.label_8.setObjectName("label_8")
        self.label_7 = QtWidgets.QLabel(DialogElectMeter)
        self.label_7.setGeometry(QtCore.QRect(250, 101, 111, 16))
        self.label_7.setObjectName("label_7")
        self.pb_reboot = QtWidgets.QPushButton(DialogElectMeter)
        self.pb_reboot.setGeometry(QtCore.QRect(20, 171, 75, 26))
        self.pb_reboot.setObjectName("pb_reboot")
        self.pb_scan = QtWidgets.QPushButton(DialogElectMeter)
        self.pb_scan.setGeometry(QtCore.QRect(180, 171, 75, 26))
        self.pb_scan.setCheckable(False)
        self.pb_scan.setChecked(False)
        self.pb_scan.setAutoDefault(False)
        self.pb_scan.setObjectName("pb_scan")
        self.pb_update_pulses = QtWidgets.QPushButton(DialogElectMeter)
        self.pb_update_pulses.setGeometry(QtCore.QRect(330, 123, 61, 26))
        self.pb_update_pulses.setObjectName("pb_update_pulses")
        self.label_6 = QtWidgets.QLabel(DialogElectMeter)
        self.label_6.setGeometry(QtCore.QRect(250, 61, 111, 16))
        self.label_6.setObjectName("label_6")
        self.pb_store = QtWidgets.QPushButton(DialogElectMeter)
        self.pb_store.setGeometry(QtCore.QRect(300, 11, 75, 26))
        self.pb_store.setObjectName("pb_store")
        self.le_watts = QtWidgets.QLineEdit(DialogElectMeter)
        self.le_watts.setGeometry(QtCore.QRect(190, 101, 51, 20))
        self.le_watts.setObjectName("le_watts")
        self.label_3 = QtWidgets.QLabel(DialogElectMeter)
        self.label_3.setGeometry(QtCore.QRect(20, 21, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pb_close = QtWidgets.QPushButton(DialogElectMeter)
        self.pb_close.setGeometry(QtCore.QRect(310, 181, 75, 26))
        self.pb_close.setObjectName("pb_close")
        self.label_4 = QtWidgets.QLabel(DialogElectMeter)
        self.label_4.setGeometry(QtCore.QRect(20, 61, 161, 21))
        self.label_4.setObjectName("label_4")
        self.pb_update_freq = QtWidgets.QPushButton(DialogElectMeter)
        self.pb_update_freq.setGeometry(QtCore.QRect(330, 63, 61, 26))
        self.pb_update_freq.setObjectName("pb_update_freq")
        self.label_5 = QtWidgets.QLabel(DialogElectMeter)
        self.label_5.setGeometry(QtCore.QRect(20, 101, 161, 16))
        self.label_5.setObjectName("label_5")
        self.le_kwh_total = QtWidgets.QLineEdit(DialogElectMeter)
        self.le_kwh_total.setGeometry(QtCore.QRect(140, 16, 101, 20))
        self.le_kwh_total.setObjectName("le_kwh_total")
        self.line_2 = QtWidgets.QFrame(DialogElectMeter)
        self.line_2.setGeometry(QtCore.QRect(20, 41, 371, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.le_pp_kw = QtWidgets.QLineEdit(DialogElectMeter)
        self.le_pp_kw.setGeometry(QtCore.QRect(190, 131, 51, 20))
        self.le_pp_kw.setObjectName("le_pp_kw")

        self.retranslateUi(DialogElectMeter)
        QtCore.QMetaObject.connectSlotsByName(DialogElectMeter)

    def retranslateUi(self, DialogElectMeter):
        _translate = QtCore.QCoreApplication.translate
        DialogElectMeter.setWindowTitle(_translate("DialogElectMeter", "Electric Meter Settings"))
        self.pb_update_diff.setText(_translate("DialogElectMeter", "Update"))
        self.label_8.setText(_translate("DialogElectMeter", "Pulses per Kw"))
        self.label_7.setText(_translate("DialogElectMeter", "watts"))
        self.pb_reboot.setText(_translate("DialogElectMeter", "Reboot"))
        self.pb_scan.setToolTip(_translate("DialogElectMeter", "Request the above information"))
        self.pb_scan.setText(_translate("DialogElectMeter", "Scan"))
        self.pb_update_pulses.setText(_translate("DialogElectMeter", "Update"))
        self.label_6.setText(_translate("DialogElectMeter", "seconds"))
        self.pb_store.setText(_translate("DialogElectMeter", "Store"))
        self.label_3.setText(_translate("DialogElectMeter", "kWh Total"))
        self.pb_close.setText(_translate("DialogElectMeter", "Close"))
        self.label_4.setText(_translate("DialogElectMeter", "watt Update frequency"))
        self.pb_update_freq.setText(_translate("DialogElectMeter", "Update"))
        self.label_5.setText(_translate("DialogElectMeter", "kWh Update difference"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogElectMeter = QtWidgets.QWidget()
    ui = Ui_DialogElectMeter()
    ui.setupUi(DialogElectMeter)
    DialogElectMeter.show()
    sys.exit(app.exec_())

