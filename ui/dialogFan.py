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
        DialogFan.resize(135, 182)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogFan.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Users/Steven/PycharmProjects/eGard001/assets/icons/003-fan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogFan.setWindowIcon(icon)
        self.frame = QtWidgets.QFrame(DialogFan)
        self.frame.setGeometry(QtCore.QRect(0, 30, 131, 111))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.dl_fan = QtWidgets.QDial(self.frame)
        self.dl_fan.setGeometry(QtCore.QRect(30, 23, 81, 71))
        self.dl_fan.setMinimum(0)
        self.dl_fan.setMaximum(5)
        self.dl_fan.setPageStep(2)
        self.dl_fan.setProperty("value", 0)
        self.dl_fan.setSliderPosition(0)
        self.dl_fan.setNotchesVisible(True)
        self.dl_fan.setObjectName("dl_fan")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(40, 10, 21, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 21, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(30, 90, 21, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(90, 10, 21, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(110, 50, 21, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(90, 90, 21, 16))
        self.label_7.setObjectName("label_7")
        self.pb_close = QtWidgets.QPushButton(DialogFan)
        self.pb_close.setGeometry(QtCore.QRect(30, 150, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_mode = QtWidgets.QPushButton(DialogFan)
        self.pb_mode.setGeometry(QtCore.QRect(33, 5, 75, 23))
        self.pb_mode.setText("")
        self.pb_mode.setObjectName("pb_mode")

        self.retranslateUi(DialogFan)
        QtCore.QMetaObject.connectSlotsByName(DialogFan)

    def retranslateUi(self, DialogFan):
        _translate = QtCore.QCoreApplication.translate
        DialogFan.setWindowTitle(_translate("DialogFan", "Fan"))
        self.label.setText(_translate("DialogFan", "2"))
        self.label_2.setText(_translate("DialogFan", "1"))
        self.label_3.setText(_translate("DialogFan", "Off"))
        self.label_5.setText(_translate("DialogFan", "3"))
        self.label_6.setText(_translate("DialogFan", "4"))
        self.label_7.setText(_translate("DialogFan", "5"))
        self.pb_close.setText(_translate("DialogFan", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogFan = QtWidgets.QDialog()
    ui = Ui_DialogFan()
    ui.setupUi(DialogFan)
    DialogFan.show()
    sys.exit(app.exec_())

