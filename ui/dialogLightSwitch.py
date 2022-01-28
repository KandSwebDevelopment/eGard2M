# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogLightSwitch.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogLightSwitch(object):
    def setupUi(self, DialogLightSwitch):
        DialogLightSwitch.setObjectName("DialogLightSwitch")
        DialogLightSwitch.resize(234, 138)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogLightSwitch.setFont(font)
        self.pb_close = QtWidgets.QPushButton(DialogLightSwitch)
        self.pb_close.setGeometry(QtCore.QRect(120, 100, 75, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pb_close.setFont(font)
        self.pb_close.setAutoDefault(False)
        self.pb_close.setObjectName("pb_close")
        self.lbl_control = QtWidgets.QLabel(DialogLightSwitch)
        self.lbl_control.setGeometry(QtCore.QRect(20, 10, 171, 21))
        self.lbl_control.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_control.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_control.setText("")
        self.lbl_control.setObjectName("lbl_control")
        self.lbl_control_2 = QtWidgets.QLabel(DialogLightSwitch)
        self.lbl_control_2.setGeometry(QtCore.QRect(20, 30, 171, 21))
        self.lbl_control_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_control_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_control_2.setText("")
        self.lbl_control_2.setObjectName("lbl_control_2")
        self.pb_on = QtWidgets.QPushButton(DialogLightSwitch)
        self.pb_on.setGeometry(QtCore.QRect(10, 70, 75, 23))
        self.pb_on.setObjectName("pb_on")
        self.pb_off = QtWidgets.QPushButton(DialogLightSwitch)
        self.pb_off.setGeometry(QtCore.QRect(10, 100, 75, 23))
        self.pb_off.setObjectName("pb_off")

        self.retranslateUi(DialogLightSwitch)
        QtCore.QMetaObject.connectSlotsByName(DialogLightSwitch)

    def retranslateUi(self, DialogLightSwitch):
        _translate = QtCore.QCoreApplication.translate
        DialogLightSwitch.setWindowTitle(_translate("DialogLightSwitch", "Light"))
        self.pb_close.setText(_translate("DialogLightSwitch", "Close"))
        self.pb_on.setText(_translate("DialogLightSwitch", "On"))
        self.pb_off.setText(_translate("DialogLightSwitch", "Off"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogLightSwitch = QtWidgets.QWidget()
    ui = Ui_DialogLightSwitch()
    ui.setupUi(DialogLightSwitch)
    DialogLightSwitch.show()
    sys.exit(app.exec_())

