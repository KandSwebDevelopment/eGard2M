# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogDispatchLoadingBay.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogDispatchLoading(object):
    def setupUi(self, DialogDispatchLoading):
        DialogDispatchLoading.setObjectName("DialogDispatchLoading")
        DialogDispatchLoading.resize(285, 250)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogDispatchLoading.setFont(font)
        self.le_gross = QtWidgets.QLineEdit(DialogDispatchLoading)
        self.le_gross.setGeometry(QtCore.QRect(190, 120, 71, 20))
        self.le_gross.setReadOnly(True)
        self.le_gross.setObjectName("le_gross")
        self.pb_close = QtWidgets.QPushButton(DialogDispatchLoading)
        self.pb_close.setGeometry(QtCore.QRect(190, 150, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_store = QtWidgets.QPushButton(DialogDispatchLoading)
        self.pb_store.setEnabled(False)
        self.pb_store.setGeometry(QtCore.QRect(100, 130, 81, 31))
        self.pb_store.setObjectName("pb_store")
        self.te_jar_info = QtWidgets.QTextEdit(DialogDispatchLoading)
        self.te_jar_info.setGeometry(QtCore.QRect(10, 190, 251, 51))
        self.te_jar_info.setReadOnly(True)
        self.te_jar_info.setObjectName("te_jar_info")
        self.le_weight = QtWidgets.QLineEdit(DialogDispatchLoading)
        self.le_weight.setGeometry(QtCore.QRect(10, 10, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(48)
        self.le_weight.setFont(font)
        self.le_weight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_weight.setReadOnly(True)
        self.le_weight.setClearButtonEnabled(False)
        self.le_weight.setObjectName("le_weight")
        self.pb_tare = QtWidgets.QPushButton(DialogDispatchLoading)
        self.pb_tare.setGeometry(QtCore.QRect(200, 20, 75, 23))
        self.pb_tare.setObjectName("pb_tare")
        self.cb_jars = QtWidgets.QComboBox(DialogDispatchLoading)
        self.cb_jars.setGeometry(QtCore.QRect(200, 50, 71, 22))
        self.cb_jars.setObjectName("cb_jars")
        self.cb_strain = QtWidgets.QComboBox(DialogDispatchLoading)
        self.cb_strain.setGeometry(QtCore.QRect(10, 80, 261, 26))
        self.cb_strain.setObjectName("cb_strain")
        self.pb_done = QtWidgets.QPushButton(DialogDispatchLoading)
        self.pb_done.setEnabled(False)
        self.pb_done.setGeometry(QtCore.QRect(10, 150, 81, 31))
        self.pb_done.setObjectName("pb_done")
        self.pb_read = QtWidgets.QPushButton(DialogDispatchLoading)
        self.pb_read.setEnabled(False)
        self.pb_read.setGeometry(QtCore.QRect(10, 110, 81, 31))
        self.pb_read.setObjectName("pb_read")

        self.retranslateUi(DialogDispatchLoading)
        QtCore.QMetaObject.connectSlotsByName(DialogDispatchLoading)

    def retranslateUi(self, DialogDispatchLoading):
        _translate = QtCore.QCoreApplication.translate
        DialogDispatchLoading.setWindowTitle(_translate("DialogDispatchLoading", "Dispatch - Loading Bay"))
        self.pb_close.setText(_translate("DialogDispatchLoading", "Close"))
        self.pb_store.setText(_translate("DialogDispatchLoading", "Store"))
        self.le_weight.setText(_translate("DialogDispatchLoading", "000.00"))
        self.pb_tare.setText(_translate("DialogDispatchLoading", "Tare"))
        self.pb_done.setText(_translate("DialogDispatchLoading", "Done"))
        self.pb_read.setText(_translate("DialogDispatchLoading", "Read"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDispatchLoading = QtWidgets.QDialog()
    ui = Ui_DialogDispatchLoading()
    ui.setupUi(DialogDispatchLoading)
    DialogDispatchLoading.show()
    sys.exit(app.exec_())

