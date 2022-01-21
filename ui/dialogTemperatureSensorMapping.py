# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogTemperatureSensorMapping.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogTemperatureSensorMApping(object):
    def setupUi(self, DialogTemperatureSensorMApping):
        DialogTemperatureSensorMApping.setObjectName("DialogTemperatureSensorMApping")
        DialogTemperatureSensorMApping.resize(306, 551)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogTemperatureSensorMApping.setFont(font)
        self.pb_close = QtWidgets.QPushButton(DialogTemperatureSensorMApping)
        self.pb_close.setGeometry(QtCore.QRect(226, 510, 75, 26))
        self.pb_close.setAutoDefault(False)
        self.pb_close.setObjectName("pb_close")
        self.pb_scan = QtWidgets.QPushButton(DialogTemperatureSensorMApping)
        self.pb_scan.setGeometry(QtCore.QRect(10, 320, 71, 31))
        self.pb_scan.setObjectName("pb_scan")
        self.label_6 = QtWidgets.QLabel(DialogTemperatureSensorMApping)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 80, 18))
        self.label_6.setObjectName("label_6")
        self.tw_current = QtWidgets.QTableWidget(DialogTemperatureSensorMApping)
        self.tw_current.setGeometry(QtCore.QRect(10, 40, 231, 192))
        self.tw_current.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_current.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_current.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_current.setObjectName("tw_current")
        self.tw_current.setColumnCount(0)
        self.tw_current.setRowCount(0)
        self.tw_current.verticalHeader().setVisible(False)
        self.le_address = QtWidgets.QLineEdit(DialogTemperatureSensorMApping)
        self.le_address.setGeometry(QtCore.QRect(10, 240, 181, 26))
        self.le_address.setReadOnly(True)
        self.le_address.setObjectName("le_address")
        self.cb_position = QtWidgets.QComboBox(DialogTemperatureSensorMApping)
        self.cb_position.setEnabled(False)
        self.cb_position.setGeometry(QtCore.QRect(10, 275, 181, 25))
        self.cb_position.setObjectName("cb_position")
        self.pb_save = QtWidgets.QPushButton(DialogTemperatureSensorMApping)
        self.pb_save.setEnabled(False)
        self.pb_save.setGeometry(QtCore.QRect(210, 240, 71, 31))
        self.pb_save.setObjectName("pb_save")
        self.tw_scan = QtWidgets.QTableWidget(DialogTemperatureSensorMApping)
        self.tw_scan.setGeometry(QtCore.QRect(20, 380, 201, 161))
        self.tw_scan.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_scan.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_scan.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_scan.setObjectName("tw_scan")
        self.tw_scan.setColumnCount(0)
        self.tw_scan.setRowCount(0)
        self.tw_scan.horizontalHeader().setVisible(False)
        self.tw_scan.verticalHeader().setVisible(False)
        self.label_7 = QtWidgets.QLabel(DialogTemperatureSensorMApping)
        self.label_7.setGeometry(QtCore.QRect(20, 360, 91, 18))
        self.label_7.setObjectName("label_7")
        self.pb_delete = QtWidgets.QPushButton(DialogTemperatureSensorMApping)
        self.pb_delete.setEnabled(False)
        self.pb_delete.setGeometry(QtCore.QRect(210, 280, 71, 31))
        self.pb_delete.setObjectName("pb_delete")
        self.pb_add = QtWidgets.QPushButton(DialogTemperatureSensorMApping)
        self.pb_add.setEnabled(False)
        self.pb_add.setGeometry(QtCore.QRect(230, 390, 71, 31))
        self.pb_add.setObjectName("pb_add")
        self.lbl_current = QtWidgets.QLabel(DialogTemperatureSensorMApping)
        self.lbl_current.setGeometry(QtCore.QRect(230, 10, 41, 21))
        self.lbl_current.setText("")
        self.lbl_current.setObjectName("lbl_current")
        self.lbl_scanned = QtWidgets.QLabel(DialogTemperatureSensorMApping)
        self.lbl_scanned.setGeometry(QtCore.QRect(150, 354, 41, 21))
        self.lbl_scanned.setText("")
        self.lbl_scanned.setObjectName("lbl_scanned")
        self.pb_ckeck = QtWidgets.QPushButton(DialogTemperatureSensorMApping)
        self.pb_ckeck.setGeometry(QtCore.QRect(90, 320, 71, 31))
        self.pb_ckeck.setObjectName("pb_ckeck")

        self.retranslateUi(DialogTemperatureSensorMApping)
        QtCore.QMetaObject.connectSlotsByName(DialogTemperatureSensorMApping)

    def retranslateUi(self, DialogTemperatureSensorMApping):
        _translate = QtCore.QCoreApplication.translate
        DialogTemperatureSensorMApping.setWindowTitle(_translate("DialogTemperatureSensorMApping", "Temperature Sensor Mapping"))
        self.pb_close.setText(_translate("DialogTemperatureSensorMApping", "Close"))
        self.pb_scan.setText(_translate("DialogTemperatureSensorMApping", "Scan"))
        self.label_6.setText(_translate("DialogTemperatureSensorMApping", "Current"))
        self.pb_save.setText(_translate("DialogTemperatureSensorMApping", "Save"))
        self.label_7.setText(_translate("DialogTemperatureSensorMApping", "Scan Results"))
        self.pb_delete.setText(_translate("DialogTemperatureSensorMApping", "Delete"))
        self.pb_add.setText(_translate("DialogTemperatureSensorMApping", "Add"))
        self.pb_ckeck.setText(_translate("DialogTemperatureSensorMApping", "Check"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogTemperatureSensorMApping = QtWidgets.QWidget()
    ui = Ui_DialogTemperatureSensorMApping()
    ui.setupUi(DialogTemperatureSensorMApping)
    DialogTemperatureSensorMApping.show()
    sys.exit(app.exec_())

