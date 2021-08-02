# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogProcessAdjustments.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogProcessAdjust(object):
    def setupUi(self, DialogProcessAdjust):
        DialogProcessAdjust.setObjectName("DialogProcessAdjust")
        DialogProcessAdjust.resize(343, 193)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogProcessAdjust.setFont(font)
        self.lbl_info = QtWidgets.QLabel(DialogProcessAdjust)
        self.lbl_info.setGeometry(QtCore.QRect(9, 9, 144, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_info.setFont(font)
        self.lbl_info.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_info.setObjectName("lbl_info")
        self.pb_delay = QtWidgets.QPushButton(DialogProcessAdjust)
        self.pb_delay.setGeometry(QtCore.QRect(10, 40, 81, 26))
        self.pb_delay.setObjectName("pb_delay")
        self.label = QtWidgets.QLabel(DialogProcessAdjust)
        self.label.setGeometry(QtCore.QRect(100, 420, 55, 18))
        self.label.setObjectName("label")
        self.cb_quantity = QtWidgets.QComboBox(DialogProcessAdjust)
        self.cb_quantity.setGeometry(QtCore.QRect(170, 420, 83, 24))
        self.cb_quantity.setObjectName("cb_quantity")
        self.label_2 = QtWidgets.QLabel(DialogProcessAdjust)
        self.label_2.setGeometry(QtCore.QRect(10, 83, 73, 18))
        self.label_2.setObjectName("label_2")
        self.cb_feed_mode = QtWidgets.QComboBox(DialogProcessAdjust)
        self.cb_feed_mode.setGeometry(QtCore.QRect(90, 80, 83, 24))
        self.cb_feed_mode.setObjectName("cb_feed_mode")
        self.label_4 = QtWidgets.QLabel(DialogProcessAdjust)
        self.label_4.setGeometry(QtCore.QRect(116, 42, 100, 18))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(DialogProcessAdjust)
        self.label_3.setGeometry(QtCore.QRect(186, 84, 59, 18))
        self.label_3.setObjectName("label_3")
        self.cb_move_to = QtWidgets.QComboBox(DialogProcessAdjust)
        self.cb_move_to.setGeometry(QtCore.QRect(250, 80, 83, 24))
        self.cb_move_to.setObjectName("cb_move_to")
        self.pb_close = QtWidgets.QPushButton(DialogProcessAdjust)
        self.pb_close.setGeometry(QtCore.QRect(250, 140, 75, 26))
        self.pb_close.setAutoDefault(False)
        self.pb_close.setObjectName("pb_close")
        self.de_feed_date = QtWidgets.QDateEdit(DialogProcessAdjust)
        self.de_feed_date.setGeometry(QtCore.QRect(220, 40, 110, 22))
        self.de_feed_date.setCalendarPopup(True)
        self.de_feed_date.setObjectName("de_feed_date")
        self.pb_remove = QtWidgets.QPushButton(DialogProcessAdjust)
        self.pb_remove.setGeometry(QtCore.QRect(10, 140, 91, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pb_remove.setFont(font)
        self.pb_remove.setObjectName("pb_remove")

        self.retranslateUi(DialogProcessAdjust)
        QtCore.QMetaObject.connectSlotsByName(DialogProcessAdjust)

    def retranslateUi(self, DialogProcessAdjust):
        _translate = QtCore.QCoreApplication.translate
        DialogProcessAdjust.setWindowTitle(_translate("DialogProcessAdjust", "Process Adjustments"))
        self.lbl_info.setText(_translate("DialogProcessAdjust", "Process 0 in location 0"))
        self.pb_delay.setText(_translate("DialogProcessAdjust", "Delay Feed"))
        self.label.setText(_translate("DialogProcessAdjust", "Quantity"))
        self.label_2.setText(_translate("DialogProcessAdjust", "Feed Mode"))
        self.label_4.setText(_translate("DialogProcessAdjust", "Last Feed Date"))
        self.label_3.setText(_translate("DialogProcessAdjust", "Move To"))
        self.pb_close.setText(_translate("DialogProcessAdjust", "Cancel"))
        self.pb_remove.setText(_translate("DialogProcessAdjust", "Remove Item"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogProcessAdjust = QtWidgets.QDialog()
    ui = Ui_DialogProcessAdjust()
    ui.setupUi(DialogProcessAdjust)
    DialogProcessAdjust.show()
    sys.exit(app.exec_())

