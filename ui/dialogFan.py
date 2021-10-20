# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogFan.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogFan(object):
    def setupUi(self, DialogFan):
        DialogFan.setObjectName("DialogFan")
        DialogFan.resize(173, 358)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogFan.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Users/Steven/.designer/Users/Steven/PycharmProjects/eGard001/assets/icons/003-fan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogFan.setWindowIcon(icon)
        self.frame = QtWidgets.QFrame(DialogFan)
        self.frame.setGeometry(QtCore.QRect(20, 56, 131, 121))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.dl_fan = QtWidgets.QDial(self.frame)
        self.dl_fan.setGeometry(QtCore.QRect(30, 33, 81, 71))
        self.dl_fan.setMinimum(1)
        self.dl_fan.setMaximum(6)
        self.dl_fan.setPageStep(2)
        self.dl_fan.setProperty("value", 1)
        self.dl_fan.setSliderPosition(1)
        self.dl_fan.setNotchesVisible(True)
        self.dl_fan.setObjectName("dl_fan")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 60, 21, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(40, 100, 21, 16))
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(40, 20, 21, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(91, 30, 21, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(90, 100, 21, 16))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(110, 60, 21, 16))
        self.label_9.setObjectName("label_9")
        self.pb_close = QtWidgets.QPushButton(DialogFan)
        self.pb_close.setGeometry(QtCore.QRect(80, 320, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_master = QtWidgets.QPushButton(DialogFan)
        self.pb_master.setGeometry(QtCore.QRect(60, 200, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pb_master.setFont(font)
        self.pb_master.setObjectName("pb_master")
        self.label_3 = QtWidgets.QLabel(DialogFan)
        self.label_3.setGeometry(QtCore.QRect(10, 204, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(DialogFan)
        self.label_4.setGeometry(QtCore.QRect(10, 234, 47, 13))
        self.label_4.setObjectName("label_4")
        self.cb_sensor = QtWidgets.QComboBox(DialogFan)
        self.cb_sensor.setGeometry(QtCore.QRect(60, 230, 101, 22))
        self.cb_sensor.setObjectName("cb_sensor")
        self.cb_mode = QtWidgets.QComboBox(DialogFan)
        self.cb_mode.setGeometry(QtCore.QRect(60, 40, 101, 21))
        self.cb_mode.setObjectName("cb_mode")
        self.label_8 = QtWidgets.QLabel(DialogFan)
        self.label_8.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.label_8.setObjectName("label_8")
        self.line = QtWidgets.QFrame(DialogFan)
        self.line.setGeometry(QtCore.QRect(10, 180, 151, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lbl_master = QtWidgets.QLabel(DialogFan)
        self.lbl_master.setGeometry(QtCore.QRect(120, 200, 31, 22))
        self.lbl_master.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_master.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_master.setText("")
        self.lbl_master.setObjectName("lbl_master")
        self.lbl_name = QtWidgets.QLabel(DialogFan)
        self.lbl_name.setGeometry(QtCore.QRect(10, 0, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_name.setObjectName("lbl_name")
        self.ck_log = QtWidgets.QCheckBox(DialogFan)
        self.ck_log.setGeometry(QtCore.QRect(10, 280, 70, 24))
        self.ck_log.setObjectName("ck_log")
        self.ck_log_tuning = QtWidgets.QCheckBox(DialogFan)
        self.ck_log_tuning.setGeometry(QtCore.QRect(70, 280, 101, 24))
        self.ck_log_tuning.setObjectName("ck_log_tuning")
        self.line_2 = QtWidgets.QFrame(DialogFan)
        self.line_2.setGeometry(QtCore.QRect(10, 260, 151, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.retranslateUi(DialogFan)
        QtCore.QMetaObject.connectSlotsByName(DialogFan)

    def retranslateUi(self, DialogFan):
        _translate = QtCore.QCoreApplication.translate
        DialogFan.setWindowTitle(_translate("DialogFan", "Fan"))
        self.label.setText(_translate("DialogFan", "2"))
        self.label_2.setText(_translate("DialogFan", "1"))
        self.label_5.setText(_translate("DialogFan", "3"))
        self.label_6.setText(_translate("DialogFan", "4"))
        self.label_7.setText(_translate("DialogFan", "6"))
        self.label_9.setText(_translate("DialogFan", "5"))
        self.pb_close.setText(_translate("DialogFan", "Close"))
        self.pb_master.setText(_translate("DialogFan", "Power"))
        self.label_3.setText(_translate("DialogFan", "Master"))
        self.label_4.setText(_translate("DialogFan", "Sensor"))
        self.label_8.setText(_translate("DialogFan", "Mode"))
        self.lbl_name.setText(_translate("DialogFan", "Fan"))
        self.ck_log.setText(_translate("DialogFan", "Log"))
        self.ck_log_tuning.setText(_translate("DialogFan", "Log Tuning"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogFan = QtWidgets.QDialog()
    ui = Ui_DialogFan()
    ui.setupUi(DialogFan)
    DialogFan.show()
    sys.exit(app.exec_())

