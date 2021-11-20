# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogMixTankCalibration.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogMixTankCalibrate(object):
    def setupUi(self, DialogMixTankCalibrate):
        DialogMixTankCalibrate.setObjectName("DialogMixTankCalibrate")
        DialogMixTankCalibrate.resize(288, 219)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogMixTankCalibrate.setFont(font)
        self.lbl_name = QtWidgets.QLabel(DialogMixTankCalibrate)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_name.setObjectName("lbl_name")
        self.pb_close = QtWidgets.QPushButton(DialogMixTankCalibrate)
        self.pb_close.setGeometry(QtCore.QRect(200, 190, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.label = QtWidgets.QLabel(DialogMixTankCalibrate)
        self.label.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label.setObjectName("label")
        self.le_current_level = QtWidgets.QLineEdit(DialogMixTankCalibrate)
        self.le_current_level.setGeometry(QtCore.QRect(110, 50, 61, 21))
        self.le_current_level.setReadOnly(True)
        self.le_current_level.setObjectName("le_current_level")
        self.pb_cal_start = QtWidgets.QPushButton(DialogMixTankCalibrate)
        self.pb_cal_start.setGeometry(QtCore.QRect(2, 130, 81, 41))
        self.pb_cal_start.setObjectName("pb_cal_start")
        self.pb_tare = QtWidgets.QPushButton(DialogMixTankCalibrate)
        self.pb_tare.setGeometry(QtCore.QRect(10, 180, 71, 31))
        self.pb_tare.setObjectName("pb_tare")
        self.lbl_status = QtWidgets.QLabel(DialogMixTankCalibrate)
        self.lbl_status.setGeometry(QtCore.QRect(90, 133, 181, 41))
        self.lbl_status.setText("")
        self.lbl_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_status.setObjectName("lbl_status")
        self.line = QtWidgets.QFrame(DialogMixTankCalibrate)
        self.line.setGeometry(QtCore.QRect(0, 70, 281, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pb_read = QtWidgets.QPushButton(DialogMixTankCalibrate)
        self.pb_read.setGeometry(QtCore.QRect(190, 50, 75, 23))
        self.pb_read.setObjectName("pb_read")
        self.label_2 = QtWidgets.QLabel(DialogMixTankCalibrate)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 121, 21))
        self.label_2.setObjectName("label_2")
        self.le_cal_weight = QtWidgets.QLineEdit(DialogMixTankCalibrate)
        self.le_cal_weight.setGeometry(QtCore.QRect(140, 90, 61, 21))
        self.le_cal_weight.setObjectName("le_cal_weight")
        self.label_3 = QtWidgets.QLabel(DialogMixTankCalibrate)
        self.label_3.setGeometry(QtCore.QRect(210, 90, 21, 21))
        self.label_3.setObjectName("label_3")
        self.pb_set_weight = QtWidgets.QPushButton(DialogMixTankCalibrate)
        self.pb_set_weight.setGeometry(QtCore.QRect(230, 90, 51, 23))
        self.pb_set_weight.setObjectName("pb_set_weight")
        self.line_2 = QtWidgets.QFrame(DialogMixTankCalibrate)
        self.line_2.setGeometry(QtCore.QRect(0, 120, 281, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.retranslateUi(DialogMixTankCalibrate)
        QtCore.QMetaObject.connectSlotsByName(DialogMixTankCalibrate)

    def retranslateUi(self, DialogMixTankCalibrate):
        _translate = QtCore.QCoreApplication.translate
        DialogMixTankCalibrate.setWindowTitle(_translate("DialogMixTankCalibrate", "Mix Tank"))
        self.lbl_name.setText(_translate("DialogMixTankCalibrate", "Mix Tank "))
        self.pb_close.setText(_translate("DialogMixTankCalibrate", "Close"))
        self.label.setText(_translate("DialogMixTankCalibrate", "Current Level"))
        self.pb_cal_start.setText(_translate("DialogMixTankCalibrate", "Calibration\n"
"Start"))
        self.pb_tare.setText(_translate("DialogMixTankCalibrate", "Tare"))
        self.pb_read.setText(_translate("DialogMixTankCalibrate", "Read"))
        self.label_2.setText(_translate("DialogMixTankCalibrate", "Calibration Weight"))
        self.label_3.setText(_translate("DialogMixTankCalibrate", "g"))
        self.pb_set_weight.setText(_translate("DialogMixTankCalibrate", "Set"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogMixTankCalibrate = QtWidgets.QWidget()
    ui = Ui_DialogMixTankCalibrate()
    ui.setupUi(DialogMixTankCalibrate)
    DialogMixTankCalibrate.show()
    sys.exit(app.exec_())

