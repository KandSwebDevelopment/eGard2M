# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogSoilLimits.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSoilLimits(object):
    def setupUi(self, DialogSoilLimits):
        DialogSoilLimits.setObjectName("DialogSoilLimits")
        DialogSoilLimits.resize(312, 236)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogSoilLimits.setFont(font)
        self.label_6 = QtWidgets.QLabel(DialogSoilLimits)
        self.label_6.setGeometry(QtCore.QRect(20, 170, 8, 24))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(DialogSoilLimits)
        self.label_5.setGeometry(QtCore.QRect(20, 140, 8, 24))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(DialogSoilLimits)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 8, 24))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(DialogSoilLimits)
        self.label_4.setGeometry(QtCore.QRect(20, 110, 8, 24))
        self.label_4.setObjectName("label_4")
        self.lbl_name = QtWidgets.QLabel(DialogSoilLimits)
        self.lbl_name.setGeometry(QtCore.QRect(10, 0, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setObjectName("lbl_name")
        self.label_12 = QtWidgets.QLabel(DialogSoilLimits)
        self.label_12.setGeometry(QtCore.QRect(50, 50, 41, 31))
        self.label_12.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(DialogSoilLimits)
        self.label_13.setGeometry(QtCore.QRect(250, 50, 41, 31))
        self.label_13.setObjectName("label_13")
        self.le_wet_1 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_wet_1.setGeometry(QtCore.QRect(40, 80, 61, 20))
        self.le_wet_1.setObjectName("le_wet_1")
        self.le_dry_1 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_dry_1.setGeometry(QtCore.QRect(110, 80, 61, 20))
        self.le_dry_1.setObjectName("le_dry_1")
        self.le_raw_1 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_raw_1.setGeometry(QtCore.QRect(240, 80, 61, 20))
        self.le_raw_1.setReadOnly(True)
        self.le_raw_1.setObjectName("le_raw_1")
        self.le_raw_2 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_raw_2.setGeometry(QtCore.QRect(240, 110, 61, 20))
        self.le_raw_2.setReadOnly(True)
        self.le_raw_2.setObjectName("le_raw_2")
        self.le_raw_3 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_raw_3.setGeometry(QtCore.QRect(240, 140, 61, 20))
        self.le_raw_3.setReadOnly(True)
        self.le_raw_3.setObjectName("le_raw_3")
        self.le_raw_4 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_raw_4.setGeometry(QtCore.QRect(240, 170, 61, 20))
        self.le_raw_4.setReadOnly(True)
        self.le_raw_4.setObjectName("le_raw_4")
        self.pb_close = QtWidgets.QPushButton(DialogSoilLimits)
        self.pb_close.setGeometry(QtCore.QRect(220, 200, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_save_1 = QtWidgets.QPushButton(DialogSoilLimits)
        self.pb_save_1.setGeometry(QtCore.QRect(174, 79, 61, 23))
        self.pb_save_1.setObjectName("pb_save_1")
        self.le_dry_2 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_dry_2.setGeometry(QtCore.QRect(110, 110, 61, 20))
        self.le_dry_2.setObjectName("le_dry_2")
        self.le_wet_2 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_wet_2.setGeometry(QtCore.QRect(40, 110, 61, 20))
        self.le_wet_2.setObjectName("le_wet_2")
        self.le_dry_3 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_dry_3.setGeometry(QtCore.QRect(110, 140, 61, 20))
        self.le_dry_3.setObjectName("le_dry_3")
        self.le_wet_3 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_wet_3.setGeometry(QtCore.QRect(40, 140, 61, 20))
        self.le_wet_3.setObjectName("le_wet_3")
        self.le_dry_4 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_dry_4.setGeometry(QtCore.QRect(110, 170, 61, 20))
        self.le_dry_4.setObjectName("le_dry_4")
        self.le_wet_4 = QtWidgets.QLineEdit(DialogSoilLimits)
        self.le_wet_4.setGeometry(QtCore.QRect(40, 170, 61, 20))
        self.le_wet_4.setObjectName("le_wet_4")
        self.label_14 = QtWidgets.QLabel(DialogSoilLimits)
        self.label_14.setGeometry(QtCore.QRect(120, 50, 41, 31))
        self.label_14.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.label_14.setObjectName("label_14")
        self.pb_save_2 = QtWidgets.QPushButton(DialogSoilLimits)
        self.pb_save_2.setGeometry(QtCore.QRect(175, 110, 61, 23))
        self.pb_save_2.setObjectName("pb_save_2")
        self.pb_save_3 = QtWidgets.QPushButton(DialogSoilLimits)
        self.pb_save_3.setGeometry(QtCore.QRect(176, 138, 61, 23))
        self.pb_save_3.setObjectName("pb_save_3")
        self.pb_save_4 = QtWidgets.QPushButton(DialogSoilLimits)
        self.pb_save_4.setGeometry(QtCore.QRect(176, 169, 61, 23))
        self.pb_save_4.setObjectName("pb_save_4")

        self.retranslateUi(DialogSoilLimits)
        QtCore.QMetaObject.connectSlotsByName(DialogSoilLimits)

    def retranslateUi(self, DialogSoilLimits):
        _translate = QtCore.QCoreApplication.translate
        DialogSoilLimits.setWindowTitle(_translate("DialogSoilLimits", "Soil Limits"))
        self.label_6.setText(_translate("DialogSoilLimits", "4"))
        self.label_5.setText(_translate("DialogSoilLimits", "3"))
        self.label_3.setText(_translate("DialogSoilLimits", "1"))
        self.label_4.setText(_translate("DialogSoilLimits", "2"))
        self.lbl_name.setText(_translate("DialogSoilLimits", "Soil Sensor Limits Area 1"))
        self.label_12.setToolTip(_translate("DialogSoilLimits", "This calculates the wet percentage value.<br>The smaller this is the wetter the soil has to be to be 100%"))
        self.label_12.setText(_translate("DialogSoilLimits", "Wet"))
        self.label_13.setText(_translate("DialogSoilLimits", "Raw"))
        self.pb_close.setText(_translate("DialogSoilLimits", "Close"))
        self.pb_save_1.setText(_translate("DialogSoilLimits", "Save"))
        self.label_14.setToolTip(_translate("DialogSoilLimits", "<html><head/><body><p>This calculates the dry percentage value.</p><p>The larger this is the drier the soil has to be to be 0% </p></body></html>"))
        self.label_14.setText(_translate("DialogSoilLimits", "Dry"))
        self.pb_save_2.setText(_translate("DialogSoilLimits", "Save"))
        self.pb_save_3.setText(_translate("DialogSoilLimits", "Save"))
        self.pb_save_4.setText(_translate("DialogSoilLimits", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogSoilLimits = QtWidgets.QWidget()
    ui = Ui_DialogSoilLimits()
    ui.setupUi(DialogSoilLimits)
    DialogSoilLimits.show()
    sys.exit(app.exec_())

