# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogDispatchInternal.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogDispatchInternal(object):
    def setupUi(self, DialogDispatchInternal):
        DialogDispatchInternal.setObjectName("DialogDispatchInternal")
        DialogDispatchInternal.resize(400, 186)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogDispatchInternal.setFont(font)
        self.cb_jar = QtWidgets.QComboBox(DialogDispatchInternal)
        self.cb_jar.setGeometry(QtCore.QRect(20, 20, 211, 22))
        self.cb_jar.setObjectName("cb_jar")
        self.lb_info = QtWidgets.QLabel(DialogDispatchInternal)
        self.lb_info.setGeometry(QtCore.QRect(30, 90, 241, 81))
        self.lb_info.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_info.setText("")
        self.lb_info.setObjectName("lb_info")
        self.le_weight = QtWidgets.QLineEdit(DialogDispatchInternal)
        self.le_weight.setGeometry(QtCore.QRect(240, 10, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(48)
        self.le_weight.setFont(font)
        self.le_weight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_weight.setReadOnly(True)
        self.le_weight.setClearButtonEnabled(False)
        self.le_weight.setObjectName("le_weight")
        self.pb_tare = QtWidgets.QPushButton(DialogDispatchInternal)
        self.pb_tare.setGeometry(QtCore.QRect(30, 50, 75, 23))
        self.pb_tare.setAutoDefault(False)
        self.pb_tare.setObjectName("pb_tare")
        self.pb_start = QtWidgets.QPushButton(DialogDispatchInternal)
        self.pb_start.setEnabled(False)
        self.pb_start.setGeometry(QtCore.QRect(290, 80, 81, 31))
        self.pb_start.setObjectName("pb_start")
        self.pb_close = QtWidgets.QPushButton(DialogDispatchInternal)
        self.pb_close.setGeometry(QtCore.QRect(300, 140, 75, 23))
        self.pb_close.setAutoDefault(False)
        self.pb_close.setObjectName("pb_close")
        self.ckb_return = QtWidgets.QCheckBox(DialogDispatchInternal)
        self.ckb_return.setGeometry(QtCore.QRect(140, 52, 70, 21))
        self.ckb_return.setObjectName("ckb_return")

        self.retranslateUi(DialogDispatchInternal)
        QtCore.QMetaObject.connectSlotsByName(DialogDispatchInternal)

    def retranslateUi(self, DialogDispatchInternal):
        _translate = QtCore.QCoreApplication.translate
        DialogDispatchInternal.setWindowTitle(_translate("DialogDispatchInternal", "Dispatch - Internal"))
        self.le_weight.setText(_translate("DialogDispatchInternal", "00.00"))
        self.pb_tare.setText(_translate("DialogDispatchInternal", "Tare"))
        self.pb_start.setText(_translate("DialogDispatchInternal", "Deduct"))
        self.pb_close.setText(_translate("DialogDispatchInternal", "Close"))
        self.ckb_return.setText(_translate("DialogDispatchInternal", "Return"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDispatchInternal = QtWidgets.QDialog()
    ui = Ui_DialogDispatchInternal()
    ui.setupUi(DialogDispatchInternal)
    DialogDispatchInternal.show()
    sys.exit(app.exec_())

