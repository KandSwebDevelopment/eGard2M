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
        DialogFan.resize(156, 215)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogFan.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Users/Steven/PycharmProjects/eGard001/assets/icons/003-fan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogFan.setWindowIcon(icon)
        self.frame = QtWidgets.QFrame(DialogFan)
        self.frame.setGeometry(QtCore.QRect(6, 60, 141, 121))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.dl_fan = QtWidgets.QDial(self.frame)
        self.dl_fan.setGeometry(QtCore.QRect(30, 33, 81, 71))
        self.dl_fan.setMinimum(1)
        self.dl_fan.setMaximum(5)
        self.dl_fan.setPageStep(2)
        self.dl_fan.setProperty("value", 1)
        self.dl_fan.setSliderPosition(1)
        self.dl_fan.setNotchesVisible(True)
        self.dl_fan.setObjectName("dl_fan")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(30, 40, 21, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(40, 100, 21, 16))
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(60, 10, 21, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(110, 50, 21, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(90, 100, 21, 16))
        self.label_7.setObjectName("label_7")
        self.pb_close = QtWidgets.QPushButton(DialogFan)
        self.pb_close.setGeometry(QtCore.QRect(60, 187, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_mode_off = QtWidgets.QPushButton(DialogFan)
        self.pb_mode_off.setGeometry(QtCore.QRect(4, 5, 45, 23))
        self.pb_mode_off.setObjectName("pb_mode_off")
        self.pb_mode_manual = QtWidgets.QPushButton(DialogFan)
        self.pb_mode_manual.setGeometry(QtCore.QRect(59, 5, 45, 23))
        self.pb_mode_manual.setObjectName("pb_mode_manual")
        self.pb_master = QtWidgets.QPushButton(DialogFan)
        self.pb_master.setGeometry(QtCore.QRect(10, 32, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pb_master.setFont(font)
        self.pb_master.setObjectName("pb_master")
        self.lbl_mode = QtWidgets.QLabel(DialogFan)
        self.lbl_mode.setGeometry(QtCore.QRect(70, 32, 81, 21))
        self.lbl_mode.setText("")
        self.lbl_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mode.setObjectName("lbl_mode")
        self.pb_mode_a = QtWidgets.QPushButton(DialogFan)
        self.pb_mode_a.setGeometry(QtCore.QRect(110, 5, 45, 23))
        self.pb_mode_a.setObjectName("pb_mode_a")

        self.retranslateUi(DialogFan)
        QtCore.QMetaObject.connectSlotsByName(DialogFan)

    def retranslateUi(self, DialogFan):
        _translate = QtCore.QCoreApplication.translate
        DialogFan.setWindowTitle(_translate("DialogFan", "Fan"))
        self.label.setText(_translate("DialogFan", "2"))
        self.label_2.setText(_translate("DialogFan", "1"))
        self.label_5.setText(_translate("DialogFan", "3"))
        self.label_6.setText(_translate("DialogFan", "4"))
        self.label_7.setText(_translate("DialogFan", "5"))
        self.pb_close.setText(_translate("DialogFan", "Close"))
        self.pb_mode_off.setText(_translate("DialogFan", "Off"))
        self.pb_mode_manual.setText(_translate("DialogFan", "Man"))
        self.pb_master.setText(_translate("DialogFan", "Master"))
        self.pb_mode_a.setText(_translate("DialogFan", "Auto"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogFan = QtWidgets.QDialog()
    ui = Ui_DialogFan()
    ui.setupUi(DialogFan)
    DialogFan.show()
    sys.exit(app.exec_())

