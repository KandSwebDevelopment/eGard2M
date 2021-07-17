# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogEngineerCommandSender.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogEngineerCommandSender(object):
    def setupUi(self, DialogEngineerCommandSender):
        DialogEngineerCommandSender.setObjectName("DialogEngineerCommandSender")
        DialogEngineerCommandSender.resize(775, 110)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogEngineerCommandSender.setFont(font)
        self.cb_command = QtWidgets.QComboBox(DialogEngineerCommandSender)
        self.cb_command.setGeometry(QtCore.QRect(40, 30, 131, 22))
        self.cb_command.setObjectName("cb_command")
        self.le_value_1 = QtWidgets.QLineEdit(DialogEngineerCommandSender)
        self.le_value_1.setGeometry(QtCore.QRect(190, 30, 61, 20))
        self.le_value_1.setObjectName("le_value_1")
        self.ck_priority = QtWidgets.QCheckBox(DialogEngineerCommandSender)
        self.ck_priority.setGeometry(QtCore.QRect(520, 30, 70, 17))
        self.ck_priority.setObjectName("ck_priority")
        self.le_value_2 = QtWidgets.QLineEdit(DialogEngineerCommandSender)
        self.le_value_2.setGeometry(QtCore.QRect(270, 30, 61, 20))
        self.le_value_2.setObjectName("le_value_2")
        self.pb_send = QtWidgets.QPushButton(DialogEngineerCommandSender)
        self.pb_send.setGeometry(QtCore.QRect(680, 30, 75, 23))
        self.pb_send.setObjectName("pb_send")
        self.le_value_3 = QtWidgets.QLineEdit(DialogEngineerCommandSender)
        self.le_value_3.setGeometry(QtCore.QRect(350, 30, 61, 20))
        self.le_value_3.setObjectName("le_value_3")
        self.cb_to = QtWidgets.QComboBox(DialogEngineerCommandSender)
        self.cb_to.setGeometry(QtCore.QRect(600, 30, 69, 22))
        self.cb_to.setObjectName("cb_to")
        self.le_value_4 = QtWidgets.QLineEdit(DialogEngineerCommandSender)
        self.le_value_4.setGeometry(QtCore.QRect(430, 30, 61, 20))
        self.le_value_4.setObjectName("le_value_4")
        self.lineEdit = QtWidgets.QLineEdit(DialogEngineerCommandSender)
        self.lineEdit.setGeometry(QtCore.QRect(40, 70, 131, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pb_close = QtWidgets.QPushButton(DialogEngineerCommandSender)
        self.pb_close.setGeometry(QtCore.QRect(680, 70, 75, 23))
        self.pb_close.setObjectName("pb_close")

        self.retranslateUi(DialogEngineerCommandSender)
        QtCore.QMetaObject.connectSlotsByName(DialogEngineerCommandSender)

    def retranslateUi(self, DialogEngineerCommandSender):
        _translate = QtCore.QCoreApplication.translate
        DialogEngineerCommandSender.setWindowTitle(_translate("DialogEngineerCommandSender", "Engineer Command Sender"))
        self.ck_priority.setText(_translate("DialogEngineerCommandSender", "Priority"))
        self.pb_send.setText(_translate("DialogEngineerCommandSender", "Send"))
        self.pb_close.setText(_translate("DialogEngineerCommandSender", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogEngineerCommandSender = QtWidgets.QDialog()
    ui = Ui_DialogEngineerCommandSender()
    ui.setupUi(DialogEngineerCommandSender)
    DialogEngineerCommandSender.show()
    sys.exit(app.exec_())

