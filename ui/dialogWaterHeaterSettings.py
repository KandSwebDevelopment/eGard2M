# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogWaterHeaterSettings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogWaterHeatertSetting(object):
    def setupUi(self, DialogWaterHeatertSetting):
        DialogWaterHeatertSetting.setObjectName("DialogWaterHeatertSetting")
        DialogWaterHeatertSetting.resize(246, 359)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogWaterHeatertSetting.setFont(font)
        self.cb_mode = QtWidgets.QComboBox(DialogWaterHeatertSetting)
        self.cb_mode.setGeometry(QtCore.QRect(80, 50, 151, 24))
        self.cb_mode.setProperty("area", 1)
        self.cb_mode.setProperty("item", 1)
        self.cb_mode.setObjectName("cb_mode")
        self.label_46 = QtWidgets.QLabel(DialogWaterHeatertSetting)
        self.label_46.setGeometry(QtCore.QRect(20, 50, 36, 18))
        self.label_46.setAlignment(QtCore.Qt.AlignCenter)
        self.label_46.setObjectName("label_46")
        self.frm_timer = QtWidgets.QFrame(DialogWaterHeatertSetting)
        self.frm_timer.setGeometry(QtCore.QRect(20, 170, 221, 141))
        self.frm_timer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_timer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frm_timer.setObjectName("frm_timer")
        self.label_47 = QtWidgets.QLabel(self.frm_timer)
        self.label_47.setGeometry(QtCore.QRect(10, 10, 38, 18))
        self.label_47.setAlignment(QtCore.Qt.AlignCenter)
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.frm_timer)
        self.label_48.setGeometry(QtCore.QRect(10, 40, 61, 18))
        self.label_48.setAlignment(QtCore.Qt.AlignCenter)
        self.label_48.setObjectName("label_48")
        self.label_49 = QtWidgets.QLabel(self.frm_timer)
        self.label_49.setGeometry(QtCore.QRect(10, 70, 71, 18))
        self.label_49.setAlignment(QtCore.Qt.AlignCenter)
        self.label_49.setObjectName("label_49")
        self.tm_off = QtWidgets.QTimeEdit(self.frm_timer)
        self.tm_off.setGeometry(QtCore.QRect(107, 70, 91, 22))
        self.tm_off.setCalendarPopup(False)
        self.tm_off.setObjectName("tm_off")
        self.tm_duration = QtWidgets.QTimeEdit(self.frm_timer)
        self.tm_duration.setGeometry(QtCore.QRect(107, 40, 91, 22))
        self.tm_duration.setMaximumTime(QtCore.QTime(6, 0, 0))
        self.tm_duration.setMinimumTime(QtCore.QTime(1, 0, 0))
        self.tm_duration.setObjectName("tm_duration")
        self.pb_set = QtWidgets.QPushButton(self.frm_timer)
        self.pb_set.setGeometry(QtCore.QRect(107, 100, 75, 25))
        self.pb_set.setObjectName("pb_set")
        self.pb_close = QtWidgets.QPushButton(DialogWaterHeatertSetting)
        self.pb_close.setGeometry(QtCore.QRect(160, 320, 75, 25))
        self.pb_close.setObjectName("pb_close")
        self.lbl_name = QtWidgets.QLabel(DialogWaterHeatertSetting)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setObjectName("lbl_name")
        self.ck_use_float = QtWidgets.QCheckBox(DialogWaterHeatertSetting)
        self.ck_use_float.setGeometry(QtCore.QRect(30, 130, 191, 21))
        self.ck_use_float.setObjectName("ck_use_float")
        self.label_50 = QtWidgets.QLabel(DialogWaterHeatertSetting)
        self.label_50.setGeometry(QtCore.QRect(13, 90, 81, 18))
        self.label_50.setAlignment(QtCore.Qt.AlignCenter)
        self.label_50.setObjectName("label_50")
        self.cb_frequency = QtWidgets.QComboBox(DialogWaterHeatertSetting)
        self.cb_frequency.setGeometry(QtCore.QRect(90, 90, 141, 24))
        self.cb_frequency.setProperty("area", 1)
        self.cb_frequency.setProperty("item", 1)
        self.cb_frequency.setObjectName("cb_frequency")

        self.retranslateUi(DialogWaterHeatertSetting)
        QtCore.QMetaObject.connectSlotsByName(DialogWaterHeatertSetting)
        DialogWaterHeatertSetting.setTabOrder(self.cb_mode, self.pb_close)

    def retranslateUi(self, DialogWaterHeatertSetting):
        _translate = QtCore.QCoreApplication.translate
        DialogWaterHeatertSetting.setWindowTitle(_translate("DialogWaterHeatertSetting", "Water Heater Settings"))
        self.label_46.setText(_translate("DialogWaterHeatertSetting", "Mode"))
        self.label_47.setText(_translate("DialogWaterHeatertSetting", "Timer"))
        self.label_48.setText(_translate("DialogWaterHeatertSetting", "Duration"))
        self.label_49.setText(_translate("DialogWaterHeatertSetting", "Off Time"))
        self.pb_set.setText(_translate("DialogWaterHeatertSetting", "Set"))
        self.pb_close.setText(_translate("DialogWaterHeatertSetting", "Close"))
        self.lbl_name.setText(_translate("DialogWaterHeatertSetting", "Water Heater 1"))
        self.ck_use_float.setText(_translate("DialogWaterHeatertSetting", "Use Float Switch"))
        self.label_50.setText(_translate("DialogWaterHeatertSetting", "Frequency"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogWaterHeatertSetting = QtWidgets.QWidget()
    ui = Ui_DialogWaterHeatertSetting()
    ui.setupUi(DialogWaterHeatertSetting)
    DialogWaterHeatertSetting.show()
    sys.exit(app.exec_())

