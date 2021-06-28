# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/_MDI/area_manual.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frm_area_manual(object):
    def setupUi(self, frm_area_manual):
        frm_area_manual.setObjectName("frm_area_manual")
        frm_area_manual.resize(190, 144)
        font = QtGui.QFont()
        font.setPointSize(11)
        frm_area_manual.setFont(font)
        self.pb_manual = QtWidgets.QPushButton(frm_area_manual)
        self.pb_manual.setGeometry(QtCore.QRect(80, 12, 75, 23))
        self.pb_manual.setObjectName("pb_manual")
        self.label = QtWidgets.QLabel(frm_area_manual)
        self.label.setGeometry(QtCore.QRect(10, 12, 51, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(frm_area_manual)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 51, 21))
        self.label_2.setObjectName("label_2")
        self.pb_light = QtWidgets.QPushButton(frm_area_manual)
        self.pb_light.setGeometry(QtCore.QRect(80, 40, 75, 23))
        self.pb_light.setObjectName("pb_light")
        self.pb_close = QtWidgets.QPushButton(frm_area_manual)
        self.pb_close.setGeometry(QtCore.QRect(100, 110, 75, 23))
        self.pb_close.setObjectName("pb_close")

        self.retranslateUi(frm_area_manual)
        QtCore.QMetaObject.connectSlotsByName(frm_area_manual)

    def retranslateUi(self, frm_area_manual):
        _translate = QtCore.QCoreApplication.translate
        frm_area_manual.setWindowTitle(_translate("frm_area_manual", "Form"))
        self.pb_manual.setText(_translate("frm_area_manual", "Off"))
        self.label.setText(_translate("frm_area_manual", "Manual"))
        self.label_2.setText(_translate("frm_area_manual", "Light"))
        self.pb_light.setText(_translate("frm_area_manual", "Off"))
        self.pb_close.setText(_translate("frm_area_manual", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frm_area_manual = QtWidgets.QWidget()
    ui = Ui_frm_area_manual()
    ui.setupUi(frm_area_manual)
    frm_area_manual.show()
    sys.exit(app.exec_())

