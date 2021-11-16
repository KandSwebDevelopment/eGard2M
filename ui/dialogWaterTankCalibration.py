# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogWaterTankCalibration.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dailogWaterTanksCalibrate(object):
    def setupUi(self, dailogWaterTanksCalibrate):
        dailogWaterTanksCalibrate.setObjectName("dailogWaterTanksCalibrate")
        dailogWaterTanksCalibrate.resize(324, 706)
        font = QtGui.QFont()
        font.setPointSize(11)
        dailogWaterTanksCalibrate.setFont(font)
        self.pb_close = QtWidgets.QPushButton(dailogWaterTanksCalibrate)
        self.pb_close.setGeometry(QtCore.QRect(60, 640, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.cb_tanks = QtWidgets.QComboBox(dailogWaterTanksCalibrate)
        self.cb_tanks.setGeometry(QtCore.QRect(80, 20, 69, 22))
        self.cb_tanks.setObjectName("cb_tanks")
        self.label = QtWidgets.QLabel(dailogWaterTanksCalibrate)
        self.label.setGeometry(QtCore.QRect(30, 20, 47, 13))
        self.label.setObjectName("label")
        self.tw_data = QtWidgets.QTableWidget(dailogWaterTanksCalibrate)
        self.tw_data.setGeometry(QtCore.QRect(160, 10, 151, 681))
        self.tw_data.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_data.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_data.setGridStyle(QtCore.Qt.SolidLine)
        self.tw_data.setRowCount(21)
        self.tw_data.setColumnCount(2)
        self.tw_data.setObjectName("tw_data")
        self.tw_data.horizontalHeader().setVisible(True)
        self.tw_data.verticalHeader().setVisible(False)
        self.frame = QtWidgets.QFrame(dailogWaterTanksCalibrate)
        self.frame.setGeometry(QtCore.QRect(10, 240, 141, 151))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pb_close_valve = QtWidgets.QPushButton(self.frame)
        self.pb_close_valve.setGeometry(QtCore.QRect(30, 100, 75, 23))
        self.pb_close_valve.setObjectName("pb_close_valve")
        self.pb_open = QtWidgets.QPushButton(self.frame)
        self.pb_open.setGeometry(QtCore.QRect(30, 70, 75, 23))
        self.pb_open.setObjectName("pb_open")
        self.lbl_valve = QtWidgets.QLabel(self.frame)
        self.lbl_valve.setGeometry(QtCore.QRect(20, 40, 101, 20))
        self.lbl_valve.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_valve.setObjectName("lbl_valve")
        self.lable = QtWidgets.QLabel(self.frame)
        self.lable.setGeometry(QtCore.QRect(20, 10, 101, 20))
        self.lable.setAlignment(QtCore.Qt.AlignCenter)
        self.lable.setObjectName("lable")
        self.frame_2 = QtWidgets.QFrame(dailogWaterTanksCalibrate)
        self.frame_2.setGeometry(QtCore.QRect(9, 70, 141, 161))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.label_2.setObjectName("label_2")
        self.le_litres = QtWidgets.QLineEdit(self.frame_2)
        self.le_litres.setGeometry(QtCore.QRect(80, 10, 41, 20))
        self.le_litres.setDragEnabled(True)
        self.le_litres.setObjectName("le_litres")
        self.pb_read = QtWidgets.QPushButton(self.frame_2)
        self.pb_read.setGeometry(QtCore.QRect(40, 40, 61, 23))
        self.pb_read.setObjectName("pb_read")
        self.le_reading = QtWidgets.QLineEdit(self.frame_2)
        self.le_reading.setGeometry(QtCore.QRect(40, 70, 61, 20))
        self.le_reading.setObjectName("le_reading")
        self.pb_store = QtWidgets.QPushButton(self.frame_2)
        self.pb_store.setGeometry(QtCore.QRect(40, 100, 61, 23))
        self.pb_store.setObjectName("pb_store")
        self.pb_clear = QtWidgets.QPushButton(self.frame_2)
        self.pb_clear.setGeometry(QtCore.QRect(40, 130, 61, 23))
        self.pb_clear.setObjectName("pb_clear")

        self.retranslateUi(dailogWaterTanksCalibrate)
        QtCore.QMetaObject.connectSlotsByName(dailogWaterTanksCalibrate)

    def retranslateUi(self, dailogWaterTanksCalibrate):
        _translate = QtCore.QCoreApplication.translate
        dailogWaterTanksCalibrate.setWindowTitle(_translate("dailogWaterTanksCalibrate", "Water Tank Calibration"))
        self.pb_close.setText(_translate("dailogWaterTanksCalibrate", "Close"))
        self.label.setText(_translate("dailogWaterTanksCalibrate", "Tank"))
        self.pb_close_valve.setText(_translate("dailogWaterTanksCalibrate", "Close"))
        self.pb_open.setText(_translate("dailogWaterTanksCalibrate", "Open"))
        self.lbl_valve.setText(_translate("dailogWaterTanksCalibrate", "Closed"))
        self.lable.setText(_translate("dailogWaterTanksCalibrate", "Inlet Valve"))
        self.label_2.setText(_translate("dailogWaterTanksCalibrate", "Fill Litres"))
        self.pb_read.setText(_translate("dailogWaterTanksCalibrate", "Read"))
        self.pb_store.setText(_translate("dailogWaterTanksCalibrate", "Store"))
        self.pb_clear.setText(_translate("dailogWaterTanksCalibrate", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dailogWaterTanksCalibrate = QtWidgets.QWidget()
    ui = Ui_dailogWaterTanksCalibrate()
    ui.setupUi(dailogWaterTanksCalibrate)
    dailogWaterTanksCalibrate.show()
    sys.exit(app.exec_())

