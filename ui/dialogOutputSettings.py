# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogOutputSettings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogOutputSetting(object):
    def setupUi(self, DialogOutputSetting):
        DialogOutputSetting.setObjectName("DialogOutputSetting")
        DialogOutputSetting.resize(246, 327)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogOutputSetting.setFont(font)
        self.cb_out_mode_1_1 = QtWidgets.QComboBox(DialogOutputSetting)
        self.cb_out_mode_1_1.setGeometry(QtCore.QRect(80, 50, 151, 24))
        self.cb_out_mode_1_1.setProperty("area", 1)
        self.cb_out_mode_1_1.setProperty("item", 1)
        self.cb_out_mode_1_1.setObjectName("cb_out_mode_1_1")
        self.label_46 = QtWidgets.QLabel(DialogOutputSetting)
        self.label_46.setGeometry(QtCore.QRect(30, 50, 36, 18))
        self.label_46.setAlignment(QtCore.Qt.AlignCenter)
        self.label_46.setObjectName("label_46")
        self.frm_sensor = QtWidgets.QFrame(DialogOutputSetting)
        self.frm_sensor.setGeometry(QtCore.QRect(20, 80, 221, 151))
        self.frm_sensor.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_sensor.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frm_sensor.setObjectName("frm_sensor")
        self.le_range_off_1_1 = QtWidgets.QLineEdit(self.frm_sensor)
        self.le_range_off_1_1.setGeometry(QtCore.QRect(130, 70, 41, 21))
        self.le_range_off_1_1.setObjectName("le_range_off_1_1")
        self.cb_sensor_out_1_1 = QtWidgets.QComboBox(self.frm_sensor)
        self.cb_sensor_out_1_1.setGeometry(QtCore.QRect(59, 10, 151, 24))
        self.cb_sensor_out_1_1.setMinimumSize(QtCore.QSize(140, 0))
        self.cb_sensor_out_1_1.setProperty("area", 1)
        self.cb_sensor_out_1_1.setProperty("item", 1)
        self.cb_sensor_out_1_1.setObjectName("cb_sensor_out_1_1")
        self.lbl_set_off_1_1 = QtWidgets.QLabel(self.frm_sensor)
        self.lbl_set_off_1_1.setGeometry(QtCore.QRect(135, 96, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_set_off_1_1.setFont(font)
        self.lbl_set_off_1_1.setText("")
        self.lbl_set_off_1_1.setObjectName("lbl_set_off_1_1")
        self.le_range_on_1_1 = QtWidgets.QLineEdit(self.frm_sensor)
        self.le_range_on_1_1.setGeometry(QtCore.QRect(60, 70, 41, 21))
        self.le_range_on_1_1.setObjectName("le_range_on_1_1")
        self.lbl_set_on_1_1 = QtWidgets.QLabel(self.frm_sensor)
        self.lbl_set_on_1_1.setGeometry(QtCore.QRect(63, 96, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_set_on_1_1.setFont(font)
        self.lbl_set_on_1_1.setText("")
        self.lbl_set_on_1_1.setObjectName("lbl_set_on_1_1")
        self.label_49 = QtWidgets.QLabel(self.frm_sensor)
        self.label_49.setGeometry(QtCore.QRect(66, 40, 101, 20))
        self.label_49.setAlignment(QtCore.Qt.AlignCenter)
        self.label_49.setObjectName("label_49")
        self.label_48 = QtWidgets.QLabel(self.frm_sensor)
        self.label_48.setGeometry(QtCore.QRect(10, 10, 44, 18))
        self.label_48.setAlignment(QtCore.Qt.AlignCenter)
        self.label_48.setObjectName("label_48")
        self.label = QtWidgets.QLabel(self.frm_sensor)
        self.label.setGeometry(QtCore.QRect(10, 71, 47, 13))
        self.label.setObjectName("label")
        self.pb_reset = QtWidgets.QPushButton(self.frm_sensor)
        self.pb_reset.setGeometry(QtCore.QRect(180, 70, 31, 23))
        self.pb_reset.setObjectName("pb_reset")
        self.lbl_detection = QtWidgets.QLabel(self.frm_sensor)
        self.lbl_detection.setGeometry(QtCore.QRect(105, 70, 21, 21))
        self.lbl_detection.setText("")
        self.lbl_detection.setObjectName("lbl_detection")
        self.label_2 = QtWidgets.QLabel(self.frm_sensor)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.cb_trigger = QtWidgets.QComboBox(self.frm_sensor)
        self.cb_trigger.setGeometry(QtCore.QRect(70, 120, 89, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cb_trigger.setFont(font)
        self.cb_trigger.setProperty("area", 1)
        self.cb_trigger.setProperty("item", 1)
        self.cb_trigger.setObjectName("cb_trigger")
        self.frm_timer = QtWidgets.QFrame(DialogOutputSetting)
        self.frm_timer.setGeometry(QtCore.QRect(20, 240, 221, 41))
        self.frm_timer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_timer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frm_timer.setObjectName("frm_timer")
        self.cb_timer_1_1 = QtWidgets.QComboBox(self.frm_timer)
        self.cb_timer_1_1.setGeometry(QtCore.QRect(70, 10, 83, 24))
        self.cb_timer_1_1.setObjectName("cb_timer_1_1")
        self.label_47 = QtWidgets.QLabel(self.frm_timer)
        self.label_47.setGeometry(QtCore.QRect(10, 10, 38, 18))
        self.label_47.setAlignment(QtCore.Qt.AlignCenter)
        self.label_47.setObjectName("label_47")
        self.pb_close = QtWidgets.QPushButton(DialogOutputSetting)
        self.pb_close.setGeometry(QtCore.QRect(160, 290, 75, 25))
        self.pb_close.setObjectName("pb_close")
        self.lbl_name = QtWidgets.QLabel(DialogOutputSetting)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setObjectName("lbl_name")
        self.ck_lock = QtWidgets.QCheckBox(DialogOutputSetting)
        self.ck_lock.setGeometry(QtCore.QRect(30, 290, 71, 20))
        self.ck_lock.setObjectName("ck_lock")

        self.retranslateUi(DialogOutputSetting)
        QtCore.QMetaObject.connectSlotsByName(DialogOutputSetting)
        DialogOutputSetting.setTabOrder(self.cb_out_mode_1_1, self.cb_sensor_out_1_1)
        DialogOutputSetting.setTabOrder(self.cb_sensor_out_1_1, self.le_range_on_1_1)
        DialogOutputSetting.setTabOrder(self.le_range_on_1_1, self.le_range_off_1_1)
        DialogOutputSetting.setTabOrder(self.le_range_off_1_1, self.pb_reset)
        DialogOutputSetting.setTabOrder(self.pb_reset, self.cb_timer_1_1)
        DialogOutputSetting.setTabOrder(self.cb_timer_1_1, self.pb_close)

    def retranslateUi(self, DialogOutputSetting):
        _translate = QtCore.QCoreApplication.translate
        DialogOutputSetting.setWindowTitle(_translate("DialogOutputSetting", "Output Settings"))
        self.label_46.setText(_translate("DialogOutputSetting", "Mode"))
        self.label_49.setText(_translate("DialogOutputSetting", "On         Off"))
        self.label_48.setText(_translate("DialogOutputSetting", "Sensor"))
        self.label.setText(_translate("DialogOutputSetting", "Offset"))
        self.pb_reset.setText(_translate("DialogOutputSetting", "R"))
        self.label_2.setText(_translate("DialogOutputSetting", "Trigger"))
        self.label_47.setText(_translate("DialogOutputSetting", "Timer"))
        self.pb_close.setText(_translate("DialogOutputSetting", "Close"))
        self.lbl_name.setText(_translate("DialogOutputSetting", "Socket"))
        self.ck_lock.setText(_translate("DialogOutputSetting", "Lock"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogOutputSetting = QtWidgets.QWidget()
    ui = Ui_DialogOutputSetting()
    ui.setupUi(DialogOutputSetting)
    DialogOutputSetting.show()
    sys.exit(app.exec_())

