# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogFeedSchedules.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSchedules(object):
    def setupUi(self, DialogSchedules):
        DialogSchedules.setObjectName("DialogSchedules")
        DialogSchedules.resize(473, 300)
        font = QtGui.QFont()
        font.setPointSize(10)
        DialogSchedules.setFont(font)
        self.label_2 = QtWidgets.QLabel(DialogSchedules)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 101, 21))
        self.label_2.setObjectName("label_2")
        self.le_id = QtWidgets.QLineEdit(DialogSchedules)
        self.le_id.setGeometry(QtCore.QRect(360, 10, 61, 20))
        self.le_id.setMouseTracking(False)
        self.le_id.setReadOnly(True)
        self.le_id.setObjectName("le_id")
        self.label_5 = QtWidgets.QLabel(DialogSchedules)
        self.label_5.setGeometry(QtCore.QRect(340, 13, 47, 13))
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(DialogSchedules)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label.setObjectName("label")
        self.cb_schedules = QtWidgets.QComboBox(DialogSchedules)
        self.cb_schedules.setGeometry(QtCore.QRect(80, 10, 241, 22))
        self.cb_schedules.setEditable(False)
        self.cb_schedules.setObjectName("cb_schedules")
        self.tw_schedule = QtWidgets.QTableWidget(DialogSchedules)
        self.tw_schedule.setGeometry(QtCore.QRect(5, 70, 271, 221))
        self.tw_schedule.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_schedule.setAlternatingRowColors(True)
        self.tw_schedule.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_schedule.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_schedule.setObjectName("tw_schedule")
        self.tw_schedule.setColumnCount(0)
        self.tw_schedule.setRowCount(0)
        self.tw_schedule.verticalHeader().setVisible(True)
        self.pb_close = QtWidgets.QPushButton(DialogSchedules)
        self.pb_close.setGeometry(QtCore.QRect(350, 260, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_add_item = QtWidgets.QPushButton(DialogSchedules)
        self.pb_add_item.setGeometry(QtCore.QRect(210, 47, 31, 23))
        self.pb_add_item.setObjectName("pb_add_item")
        self.pb_remove_item = QtWidgets.QPushButton(DialogSchedules)
        self.pb_remove_item.setGeometry(QtCore.QRect(240, 48, 31, 23))
        self.pb_remove_item.setObjectName("pb_remove_item")
        self.frm_edit = QtWidgets.QFrame(DialogSchedules)
        self.frm_edit.setEnabled(False)
        self.frm_edit.setGeometry(QtCore.QRect(280, 140, 181, 111))
        self.frm_edit.setFrameShape(QtWidgets.QFrame.Box)
        self.frm_edit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_edit.setObjectName("frm_edit")
        self.le_frequency = QtWidgets.QLineEdit(self.frm_edit)
        self.le_frequency.setGeometry(QtCore.QRect(133, 20, 31, 20))
        self.le_frequency.setObjectName("le_frequency")
        self.le_start = QtWidgets.QLineEdit(self.frm_edit)
        self.le_start.setGeometry(QtCore.QRect(13, 20, 31, 20))
        self.le_start.setObjectName("le_start")
        self.le_lpp = QtWidgets.QLineEdit(self.frm_edit)
        self.le_lpp.setGeometry(QtCore.QRect(87, 20, 31, 20))
        self.le_lpp.setObjectName("le_lpp")
        self.le_end = QtWidgets.QLineEdit(self.frm_edit)
        self.le_end.setGeometry(QtCore.QRect(50, 20, 31, 20))
        self.le_end.setObjectName("le_end")
        self.cb_recipe = QtWidgets.QComboBox(self.frm_edit)
        self.cb_recipe.setGeometry(QtCore.QRect(4, 50, 141, 22))
        self.cb_recipe.setObjectName("cb_recipe")
        self.pb_open = QtWidgets.QPushButton(self.frm_edit)
        self.pb_open.setGeometry(QtCore.QRect(144, 49, 31, 24))
        self.pb_open.setObjectName("pb_open")
        self.pb_save = QtWidgets.QPushButton(self.frm_edit)
        self.pb_save.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.pb_save.setObjectName("pb_save")
        self.pb_save_as = QtWidgets.QPushButton(self.frm_edit)
        self.pb_save_as.setGeometry(QtCore.QRect(100, 80, 75, 23))
        self.pb_save_as.setObjectName("pb_save_as")
        self.label_6 = QtWidgets.QLabel(self.frm_edit)
        self.label_6.setGeometry(QtCore.QRect(10, 5, 47, 13))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frm_edit)
        self.label_7.setGeometry(QtCore.QRect(55, 6, 47, 13))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.frm_edit)
        self.label_8.setGeometry(QtCore.QRect(97, 6, 47, 13))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.frm_edit)
        self.label_9.setGeometry(QtCore.QRect(137, 5, 47, 13))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(DialogSchedules)
        self.label_10.setGeometry(QtCore.QRect(276, 41, 71, 20))
        self.label_10.setObjectName("label_10")
        self.te_info = QtWidgets.QTextEdit(DialogSchedules)
        self.te_info.setGeometry(QtCore.QRect(280, 60, 171, 71))
        self.te_info.setReadOnly(False)
        self.te_info.setObjectName("te_info")
        self.lbl_error = QtWidgets.QLabel(DialogSchedules)
        self.lbl_error.setEnabled(True)
        self.lbl_error.setGeometry(QtCore.QRect(120, 43, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_error.setFont(font)
        self.lbl_error.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 0);")
        self.lbl_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_error.setObjectName("lbl_error")

        self.retranslateUi(DialogSchedules)
        QtCore.QMetaObject.connectSlotsByName(DialogSchedules)
        DialogSchedules.setTabOrder(self.le_start, self.le_end)
        DialogSchedules.setTabOrder(self.le_end, self.le_lpp)
        DialogSchedules.setTabOrder(self.le_lpp, self.le_frequency)
        DialogSchedules.setTabOrder(self.le_frequency, self.cb_recipe)
        DialogSchedules.setTabOrder(self.cb_recipe, self.pb_save)
        DialogSchedules.setTabOrder(self.pb_save, self.tw_schedule)
        DialogSchedules.setTabOrder(self.tw_schedule, self.pb_close)
        DialogSchedules.setTabOrder(self.pb_close, self.le_id)
        DialogSchedules.setTabOrder(self.le_id, self.te_info)
        DialogSchedules.setTabOrder(self.te_info, self.cb_schedules)
        DialogSchedules.setTabOrder(self.cb_schedules, self.pb_add_item)
        DialogSchedules.setTabOrder(self.pb_add_item, self.pb_open)
        DialogSchedules.setTabOrder(self.pb_open, self.pb_remove_item)
        DialogSchedules.setTabOrder(self.pb_remove_item, self.pb_save_as)

    def retranslateUi(self, DialogSchedules):
        _translate = QtCore.QCoreApplication.translate
        DialogSchedules.setWindowTitle(_translate("DialogSchedules", "Feed Schedules"))
        self.label_2.setText(_translate("DialogSchedules", "Schedule Items"))
        self.label_5.setText(_translate("DialogSchedules", "ID"))
        self.label.setText(_translate("DialogSchedules", "Schedule"))
        self.pb_close.setText(_translate("DialogSchedules", "Close"))
        self.pb_add_item.setText(_translate("DialogSchedules", "+"))
        self.pb_remove_item.setText(_translate("DialogSchedules", "-"))
        self.pb_open.setText(_translate("DialogSchedules", "..."))
        self.pb_save.setText(_translate("DialogSchedules", "Save"))
        self.pb_save_as.setText(_translate("DialogSchedules", "Save As"))
        self.label_6.setText(_translate("DialogSchedules", "Start"))
        self.label_7.setText(_translate("DialogSchedules", "To"))
        self.label_8.setText(_translate("DialogSchedules", "LPP"))
        self.label_9.setText(_translate("DialogSchedules", "Freq"))
        self.label_10.setText(_translate("DialogSchedules", "Description"))
        self.lbl_error.setText(_translate("DialogSchedules", "Error"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogSchedules = QtWidgets.QWidget()
    ui = Ui_DialogSchedules()
    ui.setupUi(DialogSchedules)
    DialogSchedules.show()
    sys.exit(app.exec_())

