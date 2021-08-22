# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogAccess.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogDEmodule(object):
    def setupUi(self, DialogDEmodule):
        DialogDEmodule.setObjectName("DialogDEmodule")
        DialogDEmodule.resize(354, 226)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogDEmodule.setFont(font)
        self.label = QtWidgets.QLabel(DialogDEmodule)
        self.label.setGeometry(QtCore.QRect(20, 20, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(DialogDEmodule)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 111, 16))
        self.label_2.setObjectName("label_2")
        self.le_cover_dur = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_cover_dur.setGeometry(QtCore.QRect(140, 20, 31, 20))
        self.le_cover_dur.setObjectName("le_cover_dur")
        self.le_auto_delay = QtWidgets.QLineEdit(DialogDEmodule)
        self.le_auto_delay.setGeometry(QtCore.QRect(140, 50, 31, 20))
        self.le_auto_delay.setObjectName("le_auto_delay")
        self.pb_reboot = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_reboot.setGeometry(QtCore.QRect(10, 180, 75, 26))
        self.pb_reboot.setObjectName("pb_reboot")
        self.pb_close = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_close.setGeometry(QtCore.QRect(250, 180, 75, 26))
        self.pb_close.setObjectName("pb_close")
        self.line = QtWidgets.QFrame(DialogDEmodule)
        self.line.setGeometry(QtCore.QRect(20, 80, 321, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.p_save = QtWidgets.QPushButton(DialogDEmodule)
        self.p_save.setGeometry(QtCore.QRect(190, 30, 75, 26))
        self.p_save.setObjectName("p_save")
        self.pb_query = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_query.setGeometry(QtCore.QRect(140, 180, 75, 26))
        self.pb_query.setCheckable(False)
        self.pb_query.setChecked(False)
        self.pb_query.setAutoDefault(False)
        self.pb_query.setObjectName("pb_query")
        self.pb_cover_open = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_open.setGeometry(QtCore.QRect(120, 100, 101, 25))
        self.pb_cover_open.setObjectName("pb_cover_open")
        self.pb_cover_close = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_close.setGeometry(QtCore.QRect(120, 130, 101, 25))
        self.pb_cover_close.setObjectName("pb_cover_close")
        self.pb_door_open = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_door_open.setGeometry(QtCore.QRect(230, 100, 101, 25))
        self.pb_door_open.setObjectName("pb_door_open")
        self.pb_door_close = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_door_close.setGeometry(QtCore.QRect(230, 130, 101, 25))
        self.pb_door_close.setObjectName("pb_door_close")
        self.pb_cover_unlock = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_unlock.setGeometry(QtCore.QRect(10, 100, 101, 25))
        self.pb_cover_unlock.setObjectName("pb_cover_unlock")
        self.pb_cover_lock = QtWidgets.QPushButton(DialogDEmodule)
        self.pb_cover_lock.setGeometry(QtCore.QRect(10, 130, 101, 25))
        self.pb_cover_lock.setObjectName("pb_cover_lock")
        self.line_4 = QtWidgets.QFrame(DialogDEmodule)
        self.line_4.setGeometry(QtCore.QRect(10, 160, 331, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        self.retranslateUi(DialogDEmodule)
        QtCore.QMetaObject.connectSlotsByName(DialogDEmodule)

    def retranslateUi(self, DialogDEmodule):
        _translate = QtCore.QCoreApplication.translate
        DialogDEmodule.setWindowTitle(_translate("DialogDEmodule", "DM Module"))
        self.label.setText(_translate("DialogDEmodule", "Cover Duration"))
        self.label_2.setText(_translate("DialogDEmodule", "Auto Close Delay"))
        self.pb_reboot.setText(_translate("DialogDEmodule", "Reboot"))
        self.pb_close.setText(_translate("DialogDEmodule", "Close"))
        self.p_save.setText(_translate("DialogDEmodule", "Save"))
        self.pb_query.setToolTip(_translate("DialogDEmodule", "Requests cover position and locks status"))
        self.pb_query.setText(_translate("DialogDEmodule", "Query"))
        self.pb_cover_open.setText(_translate("DialogDEmodule", "Cover Open"))
        self.pb_cover_close.setText(_translate("DialogDEmodule", "Cover Close"))
        self.pb_door_open.setText(_translate("DialogDEmodule", "Door Unlock"))
        self.pb_door_close.setText(_translate("DialogDEmodule", "Door Lock"))
        self.pb_cover_unlock.setText(_translate("DialogDEmodule", "Cover Unlock"))
        self.pb_cover_lock.setText(_translate("DialogDEmodule", "Cover Lock"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDEmodule = QtWidgets.QDialog()
    ui = Ui_DialogDEmodule()
    ui.setupUi(DialogDEmodule)
    DialogDEmodule.show()
    sys.exit(app.exec_())

