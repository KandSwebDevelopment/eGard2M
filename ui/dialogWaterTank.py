# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogWaterTank.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogWaterTank(object):
    def setupUi(self, DialogWaterTank):
        DialogWaterTank.setObjectName("DialogWaterTank")
        DialogWaterTank.resize(222, 286)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogWaterTank.setFont(font)
        self.lbl_name = QtWidgets.QLabel(DialogWaterTank)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_name.setObjectName("lbl_name")
        self.pb_close = QtWidgets.QPushButton(DialogWaterTank)
        self.pb_close.setGeometry(QtCore.QRect(120, 260, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.label = QtWidgets.QLabel(DialogWaterTank)
        self.label.setGeometry(QtCore.QRect(20, 87, 91, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(DialogWaterTank)
        self.label_2.setGeometry(QtCore.QRect(20, 117, 101, 21))
        self.label_2.setObjectName("label_2")
        self.le_current_level = QtWidgets.QLineEdit(DialogWaterTank)
        self.le_current_level.setGeometry(QtCore.QRect(130, 87, 61, 21))
        self.le_current_level.setReadOnly(True)
        self.le_current_level.setObjectName("le_current_level")
        self.le_required = QtWidgets.QLineEdit(DialogWaterTank)
        self.le_required.setGeometry(QtCore.QRect(130, 117, 61, 21))
        self.le_required.setObjectName("le_required")
        self.pb_change_level = QtWidgets.QPushButton(DialogWaterTank)
        self.pb_change_level.setGeometry(QtCore.QRect(120, 157, 75, 23))
        self.pb_change_level.setText("")
        self.pb_change_level.setObjectName("pb_change_level")
        self.pb_stop = QtWidgets.QPushButton(DialogWaterTank)
        self.pb_stop.setGeometry(QtCore.QRect(120, 226, 71, 26))
        self.pb_stop.setObjectName("pb_stop")
        self.lbl_status = QtWidgets.QLabel(DialogWaterTank)
        self.lbl_status.setGeometry(QtCore.QRect(10, 187, 201, 31))
        self.lbl_status.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_status.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lbl_status.setText("")
        self.lbl_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_status.setObjectName("lbl_status")
        self.label_3 = QtWidgets.QLabel(DialogWaterTank)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 71, 21))
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(DialogWaterTank)
        self.line.setGeometry(QtCore.QRect(0, 70, 221, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lbl_required = QtWidgets.QLabel(DialogWaterTank)
        self.lbl_required.setGeometry(QtCore.QRect(90, 49, 31, 20))
        self.lbl_required.setText("")
        self.lbl_required.setObjectName("lbl_required")
        self.label_5 = QtWidgets.QLabel(DialogWaterTank)
        self.label_5.setGeometry(QtCore.QRect(130, 54, 21, 16))
        self.label_5.setObjectName("label_5")
        self.pb_read = QtWidgets.QPushButton(DialogWaterTank)
        self.pb_read.setGeometry(QtCore.QRect(30, 160, 75, 23))
        self.pb_read.setObjectName("pb_read")
        self.pb_empty = QtWidgets.QPushButton(DialogWaterTank)
        self.pb_empty.setGeometry(QtCore.QRect(16, 227, 75, 26))
        self.pb_empty.setObjectName("pb_empty")

        self.retranslateUi(DialogWaterTank)
        QtCore.QMetaObject.connectSlotsByName(DialogWaterTank)

    def retranslateUi(self, DialogWaterTank):
        _translate = QtCore.QCoreApplication.translate
        DialogWaterTank.setWindowTitle(_translate("DialogWaterTank", "Water Tank"))
        self.lbl_name.setText(_translate("DialogWaterTank", "Tank "))
        self.pb_close.setText(_translate("DialogWaterTank", "Close"))
        self.label.setText(_translate("DialogWaterTank", "Current Level"))
        self.label_2.setText(_translate("DialogWaterTank", "Required Level"))
        self.pb_stop.setText(_translate("DialogWaterTank", "Stop"))
        self.label_3.setText(_translate("DialogWaterTank", "Required"))
        self.label_5.setText(_translate("DialogWaterTank", "L"))
        self.pb_read.setText(_translate("DialogWaterTank", "Read"))
        self.pb_empty.setText(_translate("DialogWaterTank", "Empty"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogWaterTank = QtWidgets.QWidget()
    ui = Ui_DialogWaterTank()
    ui.setupUi(DialogWaterTank)
    DialogWaterTank.show()
    sys.exit(app.exec_())

