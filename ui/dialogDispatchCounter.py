# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogDispatchCounter.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogDispatchCounter(object):
    def setupUi(self, DialogDispatchCounter):
        DialogDispatchCounter.setObjectName("DialogDispatchCounter")
        DialogDispatchCounter.resize(587, 268)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogDispatchCounter.setFont(font)
        self.pb_close = QtWidgets.QPushButton(DialogDispatchCounter)
        self.pb_close.setGeometry(QtCore.QRect(500, 230, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.cb_client = QtWidgets.QComboBox(DialogDispatchCounter)
        self.cb_client.setGeometry(QtCore.QRect(30, 20, 71, 22))
        self.cb_client.setObjectName("cb_client")
        self.lbl_decode = QtWidgets.QLabel(DialogDispatchCounter)
        self.lbl_decode.setGeometry(QtCore.QRect(520, 124, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lbl_decode.setFont(font)
        self.lbl_decode.setText("")
        self.lbl_decode.setObjectName("lbl_decode")
        self.lb_connected = QtWidgets.QLabel(DialogDispatchCounter)
        self.lb_connected.setGeometry(QtCore.QRect(280, 15, 21, 31))
        self.lb_connected.setText("")
        self.lb_connected.setObjectName("lb_connected")
        self.cb_type = QtWidgets.QComboBox(DialogDispatchCounter)
        self.cb_type.setGeometry(QtCore.QRect(120, 20, 91, 22))
        self.cb_type.setObjectName("cb_type")
        self.pb_cancel = QtWidgets.QPushButton(DialogDispatchCounter)
        self.pb_cancel.setEnabled(False)
        self.pb_cancel.setGeometry(QtCore.QRect(230, 100, 75, 23))
        self.pb_cancel.setAutoDefault(False)
        self.pb_cancel.setObjectName("pb_cancel")
        self.pb_start = QtWidgets.QPushButton(DialogDispatchCounter)
        self.pb_start.setEnabled(False)
        self.pb_start.setGeometry(QtCore.QRect(130, 100, 81, 31))
        self.pb_start.setObjectName("pb_start")
        self.lb_info = QtWidgets.QLabel(DialogDispatchCounter)
        self.lb_info.setGeometry(QtCore.QRect(320, 10, 251, 131))
        self.lb_info.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_info.setText("")
        self.lb_info.setObjectName("lb_info")
        self.frame = QtWidgets.QFrame(DialogDispatchCounter)
        self.frame.setGeometry(QtCore.QRect(19, 151, 551, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(370, 0, 181, 80))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.le_progress = QtWidgets.QLineEdit(self.frame)
        self.le_progress.setGeometry(QtCore.QRect(0, 20, 551, 31))
        self.le_progress.setText("")
        self.le_progress.setReadOnly(True)
        self.le_progress.setObjectName("le_progress")
        self.l_marker_1 = QtWidgets.QFrame(self.frame)
        self.l_marker_1.setGeometry(QtCore.QRect(243, 0, 2, 21))
        self.l_marker_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.l_marker_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.l_marker_1.setObjectName("l_marker_1")
        self.l_marker_2 = QtWidgets.QFrame(self.frame)
        self.l_marker_2.setGeometry(QtCore.QRect(270, 0, 2, 21))
        self.l_marker_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.l_marker_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.l_marker_2.setObjectName("l_marker_2")
        self.l_marker_3 = QtWidgets.QFrame(self.frame)
        self.l_marker_3.setGeometry(QtCore.QRect(280, 0, 2, 21))
        self.l_marker_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.l_marker_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.l_marker_3.setObjectName("l_marker_3")
        self.l_marker_4 = QtWidgets.QFrame(self.frame)
        self.l_marker_4.setGeometry(QtCore.QRect(420, 0, 2, 21))
        self.l_marker_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.l_marker_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.l_marker_4.setObjectName("l_marker_4")
        self.l_marker_last = QtWidgets.QFrame(self.frame)
        self.l_marker_last.setGeometry(QtCore.QRect(430, 50, 2, 21))
        self.l_marker_last.setFrameShape(QtWidgets.QFrame.VLine)
        self.l_marker_last.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.l_marker_last.setObjectName("l_marker_last")
        self.pb_tare = QtWidgets.QPushButton(DialogDispatchCounter)
        self.pb_tare.setGeometry(QtCore.QRect(30, 230, 75, 23))
        self.pb_tare.setAutoDefault(False)
        self.pb_tare.setObjectName("pb_tare")
        self.cb_jar = QtWidgets.QComboBox(DialogDispatchCounter)
        self.cb_jar.setGeometry(QtCore.QRect(30, 60, 271, 22))
        self.cb_jar.setObjectName("cb_jar")
        self.le_amount = QtWidgets.QLineEdit(DialogDispatchCounter)
        self.le_amount.setGeometry(QtCore.QRect(30, 100, 61, 31))
        self.le_amount.setObjectName("le_amount")

        self.retranslateUi(DialogDispatchCounter)
        QtCore.QMetaObject.connectSlotsByName(DialogDispatchCounter)

    def retranslateUi(self, DialogDispatchCounter):
        _translate = QtCore.QCoreApplication.translate
        DialogDispatchCounter.setWindowTitle(_translate("DialogDispatchCounter", "Dispatch Counter"))
        self.pb_close.setText(_translate("DialogDispatchCounter", "Close"))
        self.pb_cancel.setText(_translate("DialogDispatchCounter", "Cancel"))
        self.pb_start.setText(_translate("DialogDispatchCounter", "Start"))
        self.pb_tare.setText(_translate("DialogDispatchCounter", "Tare"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDispatchCounter = QtWidgets.QWidget()
    ui = Ui_DialogDispatchCounter()
    ui.setupUi(DialogDispatchCounter)
    DialogDispatchCounter.show()
    sys.exit(app.exec_())

