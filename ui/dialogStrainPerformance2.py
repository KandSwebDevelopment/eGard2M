# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogStrainPerformance2.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogStrainPreformance(object):
    def setupUi(self, DialogStrainPreformance):
        DialogStrainPreformance.setObjectName("DialogStrainPreformance")
        DialogStrainPreformance.resize(643, 542)
        self.pb_close = QtWidgets.QPushButton(DialogStrainPreformance)
        self.pb_close.setGeometry(QtCore.QRect(550, 500, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pb_close.setFont(font)
        self.pb_close.setObjectName("pb_close")
        self.tw_all = QtWidgets.QTableWidget(DialogStrainPreformance)
        self.tw_all.setGeometry(QtCore.QRect(10, 8, 621, 301))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tw_all.setFont(font)
        self.tw_all.setAlternatingRowColors(True)
        self.tw_all.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_all.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_all.setObjectName("tw_all")
        self.tw_all.setColumnCount(0)
        self.tw_all.setRowCount(0)
        self.tw_item = QtWidgets.QTableWidget(DialogStrainPreformance)
        self.tw_item.setGeometry(QtCore.QRect(10, 314, 481, 221))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tw_item.setFont(font)
        self.tw_item.setObjectName("tw_item")
        self.tw_item.setColumnCount(0)
        self.tw_item.setRowCount(0)

        self.retranslateUi(DialogStrainPreformance)
        QtCore.QMetaObject.connectSlotsByName(DialogStrainPreformance)

    def retranslateUi(self, DialogStrainPreformance):
        _translate = QtCore.QCoreApplication.translate
        DialogStrainPreformance.setWindowTitle(_translate("DialogStrainPreformance", "Strain Preformance"))
        self.pb_close.setText(_translate("DialogStrainPreformance", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogStrainPreformance = QtWidgets.QWidget()
    ui = Ui_DialogStrainPreformance()
    ui.setupUi(DialogStrainPreformance)
    DialogStrainPreformance.show()
    sys.exit(app.exec_())

