# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogSoilSensors.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSoilSensors(object):
    def setupUi(self, DialogSoilSensors):
        DialogSoilSensors.setObjectName("DialogSoilSensors")
        DialogSoilSensors.resize(227, 241)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogSoilSensors.setFont(font)
        self.lbl_name = QtWidgets.QLabel(DialogSoilSensors)
        self.lbl_name.setGeometry(QtCore.QRect(20, 10, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_name.setObjectName("lbl_name")
        self.label_12 = QtWidgets.QLabel(DialogSoilSensors)
        self.label_12.setGeometry(QtCore.QRect(50, 70, 41, 31))
        self.label_12.setObjectName("label_12")
        self.label_3 = QtWidgets.QLabel(DialogSoilSensors)
        self.label_3.setGeometry(QtCore.QRect(16, 110, 8, 24))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(DialogSoilSensors)
        self.label_5.setGeometry(QtCore.QRect(16, 170, 8, 24))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(DialogSoilSensors)
        self.label_4.setGeometry(QtCore.QRect(16, 140, 8, 24))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(DialogSoilSensors)
        self.label_6.setGeometry(QtCore.QRect(16, 200, 8, 24))
        self.label_6.setObjectName("label_6")
        self.ck_active_all = QtWidgets.QCheckBox(DialogSoilSensors)
        self.ck_active_all.setGeometry(QtCore.QRect(130, 76, 91, 22))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ck_active_all.setFont(font)
        self.ck_active_all.setObjectName("ck_active_all")
        self.pb_close = QtWidgets.QPushButton(DialogSoilSensors)
        self.pb_close.setGeometry(QtCore.QRect(140, 200, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_advanced = QtWidgets.QPushButton(DialogSoilSensors)
        self.pb_advanced.setGeometry(QtCore.QRect(140, 160, 75, 23))
        self.pb_advanced.setObjectName("pb_advanced")
        self.cb_plant_1 = QtWidgets.QComboBox(DialogSoilSensors)
        self.cb_plant_1.setGeometry(QtCore.QRect(40, 110, 61, 22))
        self.cb_plant_1.setObjectName("cb_plant_1")
        self.cb_plant_2 = QtWidgets.QComboBox(DialogSoilSensors)
        self.cb_plant_2.setGeometry(QtCore.QRect(40, 140, 61, 22))
        self.cb_plant_2.setObjectName("cb_plant_2")
        self.cb_plant_3 = QtWidgets.QComboBox(DialogSoilSensors)
        self.cb_plant_3.setGeometry(QtCore.QRect(40, 170, 61, 22))
        self.cb_plant_3.setObjectName("cb_plant_3")
        self.cb_plant_4 = QtWidgets.QComboBox(DialogSoilSensors)
        self.cb_plant_4.setGeometry(QtCore.QRect(40, 200, 61, 22))
        self.cb_plant_4.setObjectName("cb_plant_4")
        self.pb_read = QtWidgets.QPushButton(DialogSoilSensors)
        self.pb_read.setGeometry(QtCore.QRect(140, 120, 75, 23))
        self.pb_read.setObjectName("pb_read")

        self.retranslateUi(DialogSoilSensors)
        QtCore.QMetaObject.connectSlotsByName(DialogSoilSensors)

    def retranslateUi(self, DialogSoilSensors):
        _translate = QtCore.QCoreApplication.translate
        DialogSoilSensors.setWindowTitle(_translate("DialogSoilSensors", "Soil Sensors"))
        self.lbl_name.setText(_translate("DialogSoilSensors", "Soil Sensors"))
        self.label_12.setText(_translate("DialogSoilSensors", "Item"))
        self.label_3.setText(_translate("DialogSoilSensors", "1"))
        self.label_5.setText(_translate("DialogSoilSensors", "3"))
        self.label_4.setText(_translate("DialogSoilSensors", "2"))
        self.label_6.setText(_translate("DialogSoilSensors", "4"))
        self.ck_active_all.setText(_translate("DialogSoilSensors", "Area On"))
        self.pb_close.setText(_translate("DialogSoilSensors", "Close"))
        self.pb_advanced.setText(_translate("DialogSoilSensors", "Advanced"))
        self.pb_read.setText(_translate("DialogSoilSensors", "Read"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogSoilSensors = QtWidgets.QWidget()
    ui = Ui_DialogSoilSensors()
    ui.setupUi(DialogSoilSensors)
    DialogSoilSensors.show()
    sys.exit(app.exec_())

