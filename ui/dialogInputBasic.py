# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogInputBasic.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogInputBasic(object):
    def setupUi(self, DialogInputBasic):
        DialogInputBasic.setObjectName("DialogInputBasic")
        DialogInputBasic.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogInputBasic.resize(400, 47)
        font = QtGui.QFont()
        font.setPointSize(10)
        DialogInputBasic.setFont(font)
        self.le_input = QtWidgets.QLineEdit(DialogInputBasic)
        self.le_input.setGeometry(QtCore.QRect(10, 10, 261, 20))
        self.le_input.setObjectName("le_input")
        self.pb_ok = QtWidgets.QPushButton(DialogInputBasic)
        self.pb_ok.setGeometry(QtCore.QRect(280, 10, 51, 23))
        self.pb_ok.setObjectName("pb_ok")
        self.pb_cancel = QtWidgets.QPushButton(DialogInputBasic)
        self.pb_cancel.setGeometry(QtCore.QRect(340, 10, 51, 23))
        self.pb_cancel.setObjectName("pb_cancel")

        self.retranslateUi(DialogInputBasic)
        QtCore.QMetaObject.connectSlotsByName(DialogInputBasic)

    def retranslateUi(self, DialogInputBasic):
        _translate = QtCore.QCoreApplication.translate
        DialogInputBasic.setWindowTitle(_translate("DialogInputBasic", "Form"))
        self.pb_ok.setText(_translate("DialogInputBasic", "Ok"))
        self.pb_cancel.setText(_translate("DialogInputBasic", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogInputBasic = QtWidgets.QWidget()
    ui = Ui_DialogInputBasic()
    ui.setupUi(DialogInputBasic)
    DialogInputBasic.show()
    sys.exit(app.exec_())

