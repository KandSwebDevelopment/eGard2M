# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogFanDry.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogFanDry(object):
    def setupUi(self, DialogFanDry):
        DialogFanDry.setObjectName("DialogFanDry")
        DialogFanDry.resize(173, 129)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogFanDry.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Users/Steven/.designer/Users/Steven/PycharmProjects/eGard001/assets/icons/003-fan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogFanDry.setWindowIcon(icon)
        self.pb_close = QtWidgets.QPushButton(DialogFanDry)
        self.pb_close.setGeometry(QtCore.QRect(80, 90, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_on = QtWidgets.QPushButton(DialogFanDry)
        self.pb_on.setGeometry(QtCore.QRect(20, 40, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pb_on.setFont(font)
        self.pb_on.setObjectName("pb_on")
        self.label_3 = QtWidgets.QLabel(DialogFanDry)
        self.label_3.setGeometry(QtCore.QRect(10, 204, 47, 13))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.lbl_name = QtWidgets.QLabel(DialogFanDry)
        self.lbl_name.setGeometry(QtCore.QRect(10, 0, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_name.setObjectName("lbl_name")
        self.pb_off = QtWidgets.QPushButton(DialogFanDry)
        self.pb_off.setGeometry(QtCore.QRect(80, 40, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pb_off.setFont(font)
        self.pb_off.setObjectName("pb_off")

        self.retranslateUi(DialogFanDry)
        QtCore.QMetaObject.connectSlotsByName(DialogFanDry)

    def retranslateUi(self, DialogFanDry):
        _translate = QtCore.QCoreApplication.translate
        DialogFanDry.setWindowTitle(_translate("DialogFanDry", "Fan"))
        self.pb_close.setText(_translate("DialogFanDry", "Close"))
        self.pb_on.setText(_translate("DialogFanDry", "On"))
        self.lbl_name.setText(_translate("DialogFanDry", "Fan"))
        self.pb_off.setText(_translate("DialogFanDry", "Off"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogFanDry = QtWidgets.QDialog()
    ui = Ui_DialogFanDry()
    ui.setupUi(DialogFanDry)
    DialogFanDry.show()
    sys.exit(app.exec_())

