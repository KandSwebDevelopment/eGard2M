# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogSettingsAll.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialogSettingsAll(object):
    def setupUi(self, dialogSettingsAll):
        dialogSettingsAll.setObjectName("dialogSettingsAll")
        dialogSettingsAll.resize(944, 697)
        self.toolBox = QtWidgets.QToolBox(dialogSettingsAll)
        self.toolBox.setGeometry(QtCore.QRect(10, 10, 921, 441))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.toolBox.setFont(font)
        self.toolBox.setObjectName("toolBox")
        self.page_9 = QtWidgets.QWidget()
        self.page_9.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_9.setObjectName("page_9")
        self.groupBox_3 = QtWidgets.QGroupBox(self.page_9)
        self.groupBox_3.setGeometry(QtCore.QRect(140, 0, 481, 121))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_22 = QtWidgets.QLabel(self.groupBox_3)
        self.label_22.setGeometry(QtCore.QRect(7, 30, 81, 16))
        self.label_22.setObjectName("label_22")
        self.pb_db_open = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_db_open.setGeometry(QtCore.QRect(270, 30, 75, 23))
        self.pb_db_open.setObjectName("pb_db_open")
        self.le_db_host = QtWidgets.QLineEdit(self.groupBox_3)
        self.le_db_host.setGeometry(QtCore.QRect(73, 30, 132, 20))
        self.le_db_host.setObjectName("le_db_host")
        self.le_db_user_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.le_db_user_name.setGeometry(QtCore.QRect(73, 60, 132, 20))
        self.le_db_user_name.setObjectName("le_db_user_name")
        self.le_db_password = QtWidgets.QLineEdit(self.groupBox_3)
        self.le_db_password.setGeometry(QtCore.QRect(73, 90, 132, 20))
        self.le_db_password.setObjectName("le_db_password")
        self.le_db_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.le_db_name.setGeometry(QtCore.QRect(220, 90, 131, 20))
        self.le_db_name.setObjectName("le_db_name")
        self.label_23 = QtWidgets.QLabel(self.groupBox_3)
        self.label_23.setGeometry(QtCore.QRect(7, 90, 81, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_3)
        self.label_24.setGeometry(QtCore.QRect(220, 60, 81, 16))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.groupBox_3)
        self.label_25.setGeometry(QtCore.QRect(7, 60, 81, 16))
        self.label_25.setObjectName("label_25")
        self.pb_back_up = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_back_up.setGeometry(QtCore.QRect(380, 20, 81, 25))
        self.pb_back_up.setAutoDefault(False)
        self.pb_back_up.setObjectName("pb_back_up")
        self.ck_db_compress = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_db_compress.setGeometry(QtCore.QRect(385, 50, 91, 17))
        self.ck_db_compress.setChecked(True)
        self.ck_db_compress.setObjectName("ck_db_compress")
        self.ck_db_auto = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_db_auto.setGeometry(QtCore.QRect(387, 70, 101, 17))
        self.ck_db_auto.setObjectName("ck_db_auto")
        self.groupBox = QtWidgets.QGroupBox(self.page_9)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 131, 61))
        self.groupBox.setObjectName("groupBox")
        self.cb_system_mode = QtWidgets.QComboBox(self.groupBox)
        self.cb_system_mode.setGeometry(QtCore.QRect(10, 30, 111, 22))
        self.cb_system_mode.setObjectName("cb_system_mode")
        self.groupBox_14 = QtWidgets.QGroupBox(self.page_9)
        self.groupBox_14.setGeometry(QtCore.QRect(800, 0, 120, 121))
        self.groupBox_14.setObjectName("groupBox_14")
        self.label_26 = QtWidgets.QLabel(self.groupBox_14)
        self.label_26.setGeometry(QtCore.QRect(10, 24, 91, 16))
        self.label_26.setObjectName("label_26")
        self.le_ppu = QtWidgets.QLineEdit(self.groupBox_14)
        self.le_ppu.setGeometry(QtCore.QRect(10, 50, 61, 20))
        self.le_ppu.setObjectName("le_ppu")
        self.label_27 = QtWidgets.QLabel(self.groupBox_14)
        self.label_27.setGeometry(QtCore.QRect(80, 44, 21, 22))
        self.label_27.setObjectName("label_27")
        self.pb_electeric_update = QtWidgets.QPushButton(self.groupBox_14)
        self.pb_electeric_update.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.pb_electeric_update.setObjectName("pb_electeric_update")
        self.toolBox.addItem(self.page_9, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_2.setObjectName("page_2")
        self.groupBox_8 = QtWidgets.QGroupBox(self.page_2)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 0, 251, 121))
        self.groupBox_8.setObjectName("groupBox_8")
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_12.setGeometry(QtCore.QRect(10, 20, 221, 91))
        self.groupBox_12.setObjectName("groupBox_12")
        self.label_2 = QtWidgets.QLabel(self.groupBox_12)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_12)
        self.label_4.setGeometry(QtCore.QRect(10, 65, 47, 13))
        self.label_4.setObjectName("label_4")
        self.le_area_trans_cool_1 = QtWidgets.QLineEdit(self.groupBox_12)
        self.le_area_trans_cool_1.setGeometry(QtCore.QRect(60, 30, 61, 24))
        self.le_area_trans_cool_1.setObjectName("le_area_trans_cool_1")
        self.le_area_trans_warm_1 = QtWidgets.QLineEdit(self.groupBox_12)
        self.le_area_trans_warm_1.setGeometry(QtCore.QRect(60, 60, 61, 24))
        self.le_area_trans_warm_1.setObjectName("le_area_trans_warm_1")
        self.label_5 = QtWidgets.QLabel(self.groupBox_12)
        self.label_5.setGeometry(QtCore.QRect(130, 33, 61, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_12)
        self.label_6.setGeometry(QtCore.QRect(130, 64, 61, 16))
        self.label_6.setObjectName("label_6")
        self.groupBox_11 = QtWidgets.QGroupBox(self.page_2)
        self.groupBox_11.setGeometry(QtCore.QRect(280, 0, 251, 121))
        self.groupBox_11.setObjectName("groupBox_11")
        self.groupBox_13 = QtWidgets.QGroupBox(self.groupBox_11)
        self.groupBox_13.setGeometry(QtCore.QRect(10, 20, 221, 91))
        self.groupBox_13.setObjectName("groupBox_13")
        self.label_7 = QtWidgets.QLabel(self.groupBox_13)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 47, 13))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_13)
        self.label_8.setGeometry(QtCore.QRect(10, 65, 47, 13))
        self.label_8.setObjectName("label_8")
        self.le_area_trans_cool_2 = QtWidgets.QLineEdit(self.groupBox_13)
        self.le_area_trans_cool_2.setGeometry(QtCore.QRect(60, 30, 61, 24))
        self.le_area_trans_cool_2.setObjectName("le_area_trans_cool_2")
        self.le_area_trans_warm_2 = QtWidgets.QLineEdit(self.groupBox_13)
        self.le_area_trans_warm_2.setGeometry(QtCore.QRect(60, 60, 61, 24))
        self.le_area_trans_warm_2.setObjectName("le_area_trans_warm_2")
        self.label_9 = QtWidgets.QLabel(self.groupBox_13)
        self.label_9.setGeometry(QtCore.QRect(130, 33, 61, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_13)
        self.label_10.setGeometry(QtCore.QRect(130, 64, 61, 16))
        self.label_10.setObjectName("label_10")
        self.pb_area_save = QtWidgets.QPushButton(self.page_2)
        self.pb_area_save.setGeometry(QtCore.QRect(550, 90, 75, 23))
        self.pb_area_save.setObjectName("pb_area_save")
        self.toolBox.addItem(self.page_2, "")
        self.page_14 = QtWidgets.QWidget()
        self.page_14.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_14.setObjectName("page_14")
        self.groupBox_2 = QtWidgets.QGroupBox(self.page_14)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 401, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.te_ports = QtWidgets.QTextEdit(self.groupBox_2)
        self.te_ports.setGeometry(QtCore.QRect(10, 20, 281, 91))
        self.te_ports.setObjectName("te_ports")
        self.pb_rescan_ports = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_rescan_ports.setGeometry(QtCore.QRect(310, 20, 75, 23))
        self.pb_rescan_ports.setObjectName("pb_rescan_ports")
        self.groupBox_4 = QtWidgets.QGroupBox(self.page_14)
        self.groupBox_4.setGeometry(QtCore.QRect(420, 10, 120, 80))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pb_ss_update = QtWidgets.QPushButton(self.groupBox_4)
        self.pb_ss_update.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.pb_ss_update.setObjectName("pb_ss_update")
        self.le_ss_port = QtWidgets.QLineEdit(self.groupBox_4)
        self.le_ss_port.setGeometry(QtCore.QRect(10, 20, 61, 20))
        self.le_ss_port.setObjectName("le_ss_port")
        self.toolBox.addItem(self.page_14, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_3.setObjectName("page_3")
        self.groupBox_7 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_7.setGeometry(QtCore.QRect(110, 10, 131, 61))
        self.groupBox_7.setObjectName("groupBox_7")
        self.le_dispatch_empty = QtWidgets.QLineEdit(self.groupBox_7)
        self.le_dispatch_empty.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.le_dispatch_empty.setObjectName("le_dispatch_empty")
        self.label = QtWidgets.QLabel(self.groupBox_7)
        self.label.setGeometry(QtCore.QRect(80, 30, 51, 21))
        self.label.setObjectName("label")
        self.groupBox_9 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_9.setGeometry(QtCore.QRect(250, 10, 131, 61))
        self.groupBox_9.setObjectName("groupBox_9")
        self.le_dispatch_per_item = QtWidgets.QLineEdit(self.groupBox_9)
        self.le_dispatch_per_item.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.le_dispatch_per_item.setObjectName("le_dispatch_per_item")
        self.label_3 = QtWidgets.QLabel(self.groupBox_9)
        self.label_3.setGeometry(QtCore.QRect(80, 30, 51, 21))
        self.label_3.setObjectName("label_3")
        self.groupBox_10 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_10.setGeometry(QtCore.QRect(10, 10, 81, 61))
        self.groupBox_10.setObjectName("groupBox_10")
        self.le_dispatch_ppg = QtWidgets.QLineEdit(self.groupBox_10)
        self.le_dispatch_ppg.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.le_dispatch_ppg.setObjectName("le_dispatch_ppg")
        self.pb_save_dispatch = QtWidgets.QPushButton(self.page_3)
        self.pb_save_dispatch.setGeometry(QtCore.QRect(410, 50, 75, 23))
        self.pb_save_dispatch.setObjectName("pb_save_dispatch")
        self.toolBox.addItem(self.page_3, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_5.setObjectName("page_5")
        self.groupBox_5 = QtWidgets.QGroupBox(self.page_5)
        self.groupBox_5.setGeometry(QtCore.QRect(0, 0, 251, 121))
        self.groupBox_5.setObjectName("groupBox_5")
        self.le_kd_1 = QtWidgets.QLineEdit(self.groupBox_5)
        self.le_kd_1.setGeometry(QtCore.QRect(50, 90, 51, 20))
        self.le_kd_1.setObjectName("le_kd_1")
        self.label_16 = QtWidgets.QLabel(self.groupBox_5)
        self.label_16.setGeometry(QtCore.QRect(20, 30, 31, 21))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.groupBox_5)
        self.label_17.setGeometry(QtCore.QRect(20, 60, 31, 21))
        self.label_17.setObjectName("label_17")
        self.le_kp_1 = QtWidgets.QLineEdit(self.groupBox_5)
        self.le_kp_1.setGeometry(QtCore.QRect(50, 30, 51, 20))
        self.le_kp_1.setObjectName("le_kp_1")
        self.le_ki_1 = QtWidgets.QLineEdit(self.groupBox_5)
        self.le_ki_1.setGeometry(QtCore.QRect(50, 60, 51, 20))
        self.le_ki_1.setObjectName("le_ki_1")
        self.label_18 = QtWidgets.QLabel(self.groupBox_5)
        self.label_18.setGeometry(QtCore.QRect(20, 90, 31, 21))
        self.label_18.setObjectName("label_18")
        self.pb_reset_fan_1 = QtWidgets.QPushButton(self.groupBox_5)
        self.pb_reset_fan_1.setGeometry(QtCore.QRect(120, 30, 61, 23))
        self.pb_reset_fan_1.setObjectName("pb_reset_fan_1")
        self.pb_save_fans_1 = QtWidgets.QPushButton(self.groupBox_5)
        self.pb_save_fans_1.setGeometry(QtCore.QRect(120, 60, 61, 23))
        self.pb_save_fans_1.setObjectName("pb_save_fans_1")
        self.ck_test = QtWidgets.QCheckBox(self.groupBox_5)
        self.ck_test.setGeometry(QtCore.QRect(120, 90, 61, 21))
        self.ck_test.setObjectName("ck_test")
        self.pb_show_log_1 = QtWidgets.QPushButton(self.groupBox_5)
        self.pb_show_log_1.setGeometry(QtCore.QRect(180, 60, 75, 31))
        self.pb_show_log_1.setObjectName("pb_show_log_1")
        self.groupBox_6 = QtWidgets.QGroupBox(self.page_5)
        self.groupBox_6.setGeometry(QtCore.QRect(270, 0, 251, 121))
        self.groupBox_6.setObjectName("groupBox_6")
        self.le_kd_2 = QtWidgets.QLineEdit(self.groupBox_6)
        self.le_kd_2.setGeometry(QtCore.QRect(50, 90, 51, 20))
        self.le_kd_2.setObjectName("le_kd_2")
        self.label_19 = QtWidgets.QLabel(self.groupBox_6)
        self.label_19.setGeometry(QtCore.QRect(20, 30, 31, 21))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_6)
        self.label_20.setGeometry(QtCore.QRect(20, 60, 31, 21))
        self.label_20.setObjectName("label_20")
        self.le_kp_2 = QtWidgets.QLineEdit(self.groupBox_6)
        self.le_kp_2.setGeometry(QtCore.QRect(50, 30, 51, 20))
        self.le_kp_2.setObjectName("le_kp_2")
        self.le_ki_2 = QtWidgets.QLineEdit(self.groupBox_6)
        self.le_ki_2.setGeometry(QtCore.QRect(50, 60, 51, 20))
        self.le_ki_2.setObjectName("le_ki_2")
        self.label_21 = QtWidgets.QLabel(self.groupBox_6)
        self.label_21.setGeometry(QtCore.QRect(20, 90, 31, 21))
        self.label_21.setObjectName("label_21")
        self.pb_reset_fan_2 = QtWidgets.QPushButton(self.groupBox_6)
        self.pb_reset_fan_2.setGeometry(QtCore.QRect(120, 30, 61, 23))
        self.pb_reset_fan_2.setObjectName("pb_reset_fan_2")
        self.pb_save_fans_2 = QtWidgets.QPushButton(self.groupBox_6)
        self.pb_save_fans_2.setGeometry(QtCore.QRect(120, 60, 61, 23))
        self.pb_save_fans_2.setObjectName("pb_save_fans_2")
        self.ck_test_2 = QtWidgets.QCheckBox(self.groupBox_6)
        self.ck_test_2.setGeometry(QtCore.QRect(130, 90, 61, 21))
        self.ck_test_2.setObjectName("ck_test_2")
        self.pb_show_log_2 = QtWidgets.QPushButton(self.groupBox_6)
        self.pb_show_log_2.setGeometry(QtCore.QRect(190, 50, 75, 31))
        self.pb_show_log_2.setObjectName("pb_show_log_2")
        self.toolBox.addItem(self.page_5, "")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_6.setObjectName("page_6")
        self.groupBox_16 = QtWidgets.QGroupBox(self.page_6)
        self.groupBox_16.setGeometry(QtCore.QRect(0, 0, 341, 91))
        self.groupBox_16.setObjectName("groupBox_16")
        self.label_13 = QtWidgets.QLabel(self.groupBox_16)
        self.label_13.setGeometry(QtCore.QRect(9, 28, 71, 16))
        self.label_13.setObjectName("label_13")
        self.le_feeder_feed_litres = QtWidgets.QLineEdit(self.groupBox_16)
        self.le_feeder_feed_litres.setGeometry(QtCore.QRect(89, 25, 49, 20))
        self.le_feeder_feed_litres.setObjectName("le_feeder_feed_litres")
        self.label_14 = QtWidgets.QLabel(self.groupBox_16)
        self.label_14.setGeometry(QtCore.QRect(9, 58, 71, 16))
        self.label_14.setObjectName("label_14")
        self.le_feeder_soak = QtWidgets.QLineEdit(self.groupBox_16)
        self.le_feeder_soak.setGeometry(QtCore.QRect(89, 56, 49, 20))
        self.le_feeder_soak.setObjectName("le_feeder_soak")
        self.label_15 = QtWidgets.QLabel(self.groupBox_16)
        self.label_15.setGeometry(QtCore.QRect(185, 27, 71, 16))
        self.label_15.setObjectName("label_15")
        self.le_mix_max = QtWidgets.QLineEdit(self.groupBox_16)
        self.le_mix_max.setGeometry(QtCore.QRect(265, 25, 49, 20))
        self.le_mix_max.setObjectName("le_mix_max")
        self.label_31 = QtWidgets.QLabel(self.groupBox_16)
        self.label_31.setGeometry(QtCore.QRect(144, 30, 16, 16))
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.groupBox_16)
        self.label_32.setGeometry(QtCore.QRect(315, 29, 16, 16))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.groupBox_16)
        self.label_33.setGeometry(QtCore.QRect(144, 60, 31, 16))
        self.label_33.setObjectName("label_33")
        self.label_42 = QtWidgets.QLabel(self.groupBox_16)
        self.label_42.setGeometry(QtCore.QRect(315, 62, 16, 16))
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.groupBox_16)
        self.label_43.setGeometry(QtCore.QRect(183, 60, 81, 16))
        self.label_43.setObjectName("label_43")
        self.le_feeder_man_max = QtWidgets.QLineEdit(self.groupBox_16)
        self.le_feeder_man_max.setGeometry(QtCore.QRect(265, 58, 49, 20))
        self.le_feeder_man_max.setObjectName("le_feeder_man_max")
        self.groupBox_17 = QtWidgets.QGroupBox(self.page_6)
        self.groupBox_17.setGeometry(QtCore.QRect(350, 0, 171, 61))
        self.groupBox_17.setObjectName("groupBox_17")
        self.label_28 = QtWidgets.QLabel(self.groupBox_17)
        self.label_28.setGeometry(QtCore.QRect(9, 28, 71, 16))
        self.label_28.setObjectName("label_28")
        self.le_feeder_flush = QtWidgets.QLineEdit(self.groupBox_17)
        self.le_feeder_flush.setGeometry(QtCore.QRect(89, 25, 61, 20))
        self.le_feeder_flush.setObjectName("le_feeder_flush")
        self.label_34 = QtWidgets.QLabel(self.groupBox_17)
        self.label_34.setGeometry(QtCore.QRect(153, 30, 16, 16))
        self.label_34.setObjectName("label_34")
        self.groupBox_18 = QtWidgets.QGroupBox(self.page_6)
        self.groupBox_18.setGeometry(QtCore.QRect(530, 0, 201, 121))
        self.groupBox_18.setObjectName("groupBox_18")
        self.label_39 = QtWidgets.QLabel(self.groupBox_18)
        self.label_39.setGeometry(QtCore.QRect(9, 28, 71, 16))
        self.label_39.setObjectName("label_39")
        self.le_feeder_stir_nutrients = QtWidgets.QLineEdit(self.groupBox_18)
        self.le_feeder_stir_nutrients.setGeometry(QtCore.QRect(89, 25, 49, 20))
        self.le_feeder_stir_nutrients.setObjectName("le_feeder_stir_nutrients")
        self.label_40 = QtWidgets.QLabel(self.groupBox_18)
        self.label_40.setGeometry(QtCore.QRect(10, 94, 71, 16))
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.groupBox_18)
        self.label_41.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.label_41.setObjectName("label_41")
        self.le_feeder_stri_mix = QtWidgets.QLineEdit(self.groupBox_18)
        self.le_feeder_stri_mix.setGeometry(QtCore.QRect(90, 90, 49, 20))
        self.le_feeder_stri_mix.setObjectName("le_feeder_stri_mix")
        self.label_44 = QtWidgets.QLabel(self.groupBox_18)
        self.label_44.setGeometry(QtCore.QRect(142, 30, 31, 16))
        self.label_44.setObjectName("label_44")
        self.label_45 = QtWidgets.QLabel(self.groupBox_18)
        self.label_45.setGeometry(QtCore.QRect(143, 95, 31, 16))
        self.label_45.setObjectName("label_45")
        self.cb_feeder_auto_stir = QtWidgets.QComboBox(self.groupBox_18)
        self.cb_feeder_auto_stir.setGeometry(QtCore.QRect(90, 60, 69, 22))
        self.cb_feeder_auto_stir.setObjectName("cb_feeder_auto_stir")
        self.toolBox.addItem(self.page_6, "")
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_7.setObjectName("page_7")
        self.groupBox_19 = QtWidgets.QGroupBox(self.page_7)
        self.groupBox_19.setGeometry(QtCore.QRect(0, 10, 381, 61))
        self.groupBox_19.setObjectName("groupBox_19")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.groupBox_19)
        self.lineEdit_19.setGeometry(QtCore.QRect(30, 24, 341, 24))
        self.lineEdit_19.setText("")
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.groupBox_20 = QtWidgets.QGroupBox(self.page_7)
        self.groupBox_20.setGeometry(QtCore.QRect(390, 0, 271, 121))
        self.groupBox_20.setObjectName("groupBox_20")
        self.toolBox.addItem(self.page_7, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page.setObjectName("page")
        self.groupBox_21 = QtWidgets.QGroupBox(self.page)
        self.groupBox_21.setGeometry(QtCore.QRect(0, 0, 481, 91))
        self.groupBox_21.setTitle("")
        self.groupBox_21.setObjectName("groupBox_21")
        self.label_52 = QtWidgets.QLabel(self.groupBox_21)
        self.label_52.setGeometry(QtCore.QRect(9, 28, 71, 16))
        self.label_52.setObjectName("label_52")
        self.lineEdit_23 = QtWidgets.QLineEdit(self.groupBox_21)
        self.lineEdit_23.setGeometry(QtCore.QRect(110, 25, 101, 24))
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.label_54 = QtWidgets.QLabel(self.groupBox_21)
        self.label_54.setGeometry(QtCore.QRect(9, 58, 101, 16))
        self.label_54.setObjectName("label_54")
        self.lineEdit_24 = QtWidgets.QLineEdit(self.groupBox_21)
        self.lineEdit_24.setGeometry(QtCore.QRect(110, 56, 49, 24))
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.label_55 = QtWidgets.QLabel(self.groupBox_21)
        self.label_55.setGeometry(QtCore.QRect(239, 15, 91, 16))
        self.label_55.setObjectName("label_55")
        self.lineEdit_25 = QtWidgets.QLineEdit(self.groupBox_21)
        self.lineEdit_25.setGeometry(QtCore.QRect(340, 13, 49, 24))
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.label_58 = QtWidgets.QLabel(self.groupBox_21)
        self.label_58.setGeometry(QtCore.QRect(165, 60, 31, 16))
        self.label_58.setObjectName("label_58")
        self.label_59 = QtWidgets.QLabel(self.groupBox_21)
        self.label_59.setGeometry(QtCore.QRect(390, 50, 41, 16))
        self.label_59.setObjectName("label_59")
        self.label_60 = QtWidgets.QLabel(self.groupBox_21)
        self.label_60.setGeometry(QtCore.QRect(237, 48, 91, 16))
        self.label_60.setObjectName("label_60")
        self.lineEdit_26 = QtWidgets.QLineEdit(self.groupBox_21)
        self.lineEdit_26.setGeometry(QtCore.QRect(340, 46, 49, 24))
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.toolBox.addItem(self.page, "")
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_8.setObjectName("page_8")
        self.groupBox_23 = QtWidgets.QGroupBox(self.page_8)
        self.groupBox_23.setGeometry(QtCore.QRect(0, 0, 291, 61))
        self.groupBox_23.setObjectName("groupBox_23")
        self.label_56 = QtWidgets.QLabel(self.groupBox_23)
        self.label_56.setGeometry(QtCore.QRect(9, 28, 47, 13))
        self.label_56.setObjectName("label_56")
        self.lineEdit_27 = QtWidgets.QLineEdit(self.groupBox_23)
        self.lineEdit_27.setGeometry(QtCore.QRect(30, 24, 121, 24))
        self.lineEdit_27.setText("")
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.label_57 = QtWidgets.QLabel(self.groupBox_23)
        self.label_57.setGeometry(QtCore.QRect(166, 28, 61, 16))
        self.label_57.setObjectName("label_57")
        self.lineEdit_28 = QtWidgets.QLineEdit(self.groupBox_23)
        self.lineEdit_28.setGeometry(QtCore.QRect(210, 24, 71, 24))
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.groupBox_24 = QtWidgets.QGroupBox(self.page_8)
        self.groupBox_24.setGeometry(QtCore.QRect(0, 60, 291, 61))
        self.groupBox_24.setObjectName("groupBox_24")
        self.label_61 = QtWidgets.QLabel(self.groupBox_24)
        self.label_61.setGeometry(QtCore.QRect(9, 28, 47, 13))
        self.label_61.setObjectName("label_61")
        self.lineEdit_29 = QtWidgets.QLineEdit(self.groupBox_24)
        self.lineEdit_29.setGeometry(QtCore.QRect(30, 24, 121, 24))
        self.lineEdit_29.setText("")
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.label_62 = QtWidgets.QLabel(self.groupBox_24)
        self.label_62.setGeometry(QtCore.QRect(166, 28, 61, 16))
        self.label_62.setObjectName("label_62")
        self.lineEdit_30 = QtWidgets.QLineEdit(self.groupBox_24)
        self.lineEdit_30.setGeometry(QtCore.QRect(210, 24, 71, 24))
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.groupBox_15 = QtWidgets.QGroupBox(self.page_8)
        self.groupBox_15.setGeometry(QtCore.QRect(300, 10, 161, 91))
        self.groupBox_15.setObjectName("groupBox_15")
        self.label_11 = QtWidgets.QLabel(self.groupBox_15)
        self.label_11.setGeometry(QtCore.QRect(9, 28, 47, 13))
        self.label_11.setObjectName("label_11")
        self.le_feeder_ip = QtWidgets.QLineEdit(self.groupBox_15)
        self.le_feeder_ip.setGeometry(QtCore.QRect(30, 24, 121, 24))
        self.le_feeder_ip.setText("")
        self.le_feeder_ip.setObjectName("le_feeder_ip")
        self.label_12 = QtWidgets.QLabel(self.groupBox_15)
        self.label_12.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.label_12.setObjectName("label_12")
        self.le_feeder_port = QtWidgets.QLineEdit(self.groupBox_15)
        self.le_feeder_port.setGeometry(QtCore.QRect(54, 56, 71, 24))
        self.le_feeder_port.setObjectName("le_feeder_port")
        self.toolBox.addItem(self.page_8, "")
        self.page_11 = QtWidgets.QWidget()
        self.page_11.setGeometry(QtCore.QRect(0, 0, 921, 141))
        self.page_11.setObjectName("page_11")
        self.groupBox_22 = QtWidgets.QGroupBox(self.page_11)
        self.groupBox_22.setGeometry(QtCore.QRect(10, 0, 181, 121))
        self.groupBox_22.setObjectName("groupBox_22")
        self.label_47 = QtWidgets.QLabel(self.groupBox_22)
        self.label_47.setGeometry(QtCore.QRect(9, 28, 71, 16))
        self.label_47.setObjectName("label_47")
        self.lineEdit_20 = QtWidgets.QLineEdit(self.groupBox_22)
        self.lineEdit_20.setGeometry(QtCore.QRect(89, 25, 49, 24))
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.label_48 = QtWidgets.QLabel(self.groupBox_22)
        self.label_48.setGeometry(QtCore.QRect(9, 58, 71, 16))
        self.label_48.setObjectName("label_48")
        self.lineEdit_21 = QtWidgets.QLineEdit(self.groupBox_22)
        self.lineEdit_21.setGeometry(QtCore.QRect(89, 56, 49, 24))
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.label_49 = QtWidgets.QLabel(self.groupBox_22)
        self.label_49.setGeometry(QtCore.QRect(10, 89, 71, 16))
        self.label_49.setObjectName("label_49")
        self.lineEdit_22 = QtWidgets.QLineEdit(self.groupBox_22)
        self.lineEdit_22.setGeometry(QtCore.QRect(90, 87, 49, 24))
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.label_50 = QtWidgets.QLabel(self.groupBox_22)
        self.label_50.setGeometry(QtCore.QRect(144, 30, 16, 16))
        self.label_50.setObjectName("label_50")
        self.label_51 = QtWidgets.QLabel(self.groupBox_22)
        self.label_51.setGeometry(QtCore.QRect(140, 91, 16, 16))
        self.label_51.setObjectName("label_51")
        self.label_53 = QtWidgets.QLabel(self.groupBox_22)
        self.label_53.setGeometry(QtCore.QRect(140, 60, 16, 16))
        self.label_53.setObjectName("label_53")
        self.toolBox.addItem(self.page_11, "")
        self.pb_close = QtWidgets.QPushButton(dialogSettingsAll)
        self.pb_close.setGeometry(QtCore.QRect(860, 10, 75, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pb_close.setFont(font)
        self.pb_close.setAutoDefault(False)
        self.pb_close.setObjectName("pb_close")

        self.retranslateUi(dialogSettingsAll)
        self.toolBox.setCurrentIndex(5)
        self.toolBox.layout().setSpacing(6)
        QtCore.QMetaObject.connectSlotsByName(dialogSettingsAll)

    def retranslateUi(self, dialogSettingsAll):
        _translate = QtCore.QCoreApplication.translate
        dialogSettingsAll.setWindowTitle(_translate("dialogSettingsAll", "Settings"))
        self.groupBox_3.setTitle(_translate("dialogSettingsAll", "Database"))
        self.label_22.setText(_translate("dialogSettingsAll", "Host"))
        self.pb_db_open.setText(_translate("dialogSettingsAll", "Save"))
        self.label_23.setText(_translate("dialogSettingsAll", "Password"))
        self.label_24.setText(_translate("dialogSettingsAll", "DB Name"))
        self.label_25.setText(_translate("dialogSettingsAll", "User Name"))
        self.pb_back_up.setText(_translate("dialogSettingsAll", "Back Up Now"))
        self.ck_db_compress.setText(_translate("dialogSettingsAll", "Compress"))
        self.ck_db_auto.setText(_translate("dialogSettingsAll", "Auto Backup"))
        self.groupBox.setTitle(_translate("dialogSettingsAll", "Operation Mode"))
        self.groupBox_14.setTitle(_translate("dialogSettingsAll", "Electrict"))
        self.label_26.setText(_translate("dialogSettingsAll", "Price per unit"))
        self.label_27.setText(_translate("dialogSettingsAll", "p"))
        self.pb_electeric_update.setText(_translate("dialogSettingsAll", "Update"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_9), _translate("dialogSettingsAll", "General"))
        self.groupBox_8.setTitle(_translate("dialogSettingsAll", "Area 1"))
        self.groupBox_12.setTitle(_translate("dialogSettingsAll", "Transition time"))
        self.label_2.setText(_translate("dialogSettingsAll", "Cool"))
        self.label_4.setText(_translate("dialogSettingsAll", "Warm"))
        self.label_5.setText(_translate("dialogSettingsAll", "minutes"))
        self.label_6.setText(_translate("dialogSettingsAll", "minutes"))
        self.groupBox_11.setTitle(_translate("dialogSettingsAll", "Area 2"))
        self.groupBox_13.setTitle(_translate("dialogSettingsAll", "Transition time"))
        self.label_7.setText(_translate("dialogSettingsAll", "Cool"))
        self.label_8.setText(_translate("dialogSettingsAll", "Warm"))
        self.label_9.setText(_translate("dialogSettingsAll", "minutes"))
        self.label_10.setText(_translate("dialogSettingsAll", "minutes"))
        self.pb_area_save.setText(_translate("dialogSettingsAll", "Save"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("dialogSettingsAll", "Areas"))
        self.groupBox_2.setTitle(_translate("dialogSettingsAll", "Ports"))
        self.pb_rescan_ports.setText(_translate("dialogSettingsAll", "Rescan"))
        self.groupBox_4.setTitle(_translate("dialogSettingsAll", "Scales Unit Port"))
        self.pb_ss_update.setText(_translate("dialogSettingsAll", "Update"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_14), _translate("dialogSettingsAll", "Com Ports"))
        self.groupBox_7.setToolTip(_translate("dialogSettingsAll", "The number of grams a jar must contain less than to be classed as empty"))
        self.groupBox_7.setTitle(_translate("dialogSettingsAll", "Empty"))
        self.label.setText(_translate("dialogSettingsAll", "grams"))
        self.groupBox_9.setToolTip(_translate("dialogSettingsAll", "The number of grams a jar must contain less than to be classed as empty"))
        self.groupBox_9.setTitle(_translate("dialogSettingsAll", "Estimate per item"))
        self.label_3.setText(_translate("dialogSettingsAll", "grams"))
        self.groupBox_10.setToolTip(_translate("dialogSettingsAll", "The number of grams a jar must contain less than to be classed as empty"))
        self.groupBox_10.setTitle(_translate("dialogSettingsAll", "PPG"))
        self.pb_save_dispatch.setText(_translate("dialogSettingsAll", "Save"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("dialogSettingsAll", "Dispatch"))
        self.groupBox_5.setTitle(_translate("dialogSettingsAll", "Fan 1"))
        self.label_16.setText(_translate("dialogSettingsAll", "Kp"))
        self.label_17.setText(_translate("dialogSettingsAll", "Ki"))
        self.label_18.setText(_translate("dialogSettingsAll", "Kd"))
        self.pb_reset_fan_1.setText(_translate("dialogSettingsAll", "Reset"))
        self.pb_save_fans_1.setText(_translate("dialogSettingsAll", "Save"))
        self.ck_test.setText(_translate("dialogSettingsAll", "Log"))
        self.pb_show_log_1.setText(_translate("dialogSettingsAll", "Show Log"))
        self.groupBox_6.setTitle(_translate("dialogSettingsAll", "Fan 2"))
        self.label_19.setText(_translate("dialogSettingsAll", "Kp"))
        self.label_20.setText(_translate("dialogSettingsAll", "Ki"))
        self.label_21.setText(_translate("dialogSettingsAll", "Kd"))
        self.pb_reset_fan_2.setText(_translate("dialogSettingsAll", "Reset"))
        self.pb_save_fans_2.setText(_translate("dialogSettingsAll", "Save"))
        self.ck_test_2.setText(_translate("dialogSettingsAll", "Log"))
        self.pb_show_log_2.setText(_translate("dialogSettingsAll", "Show Log"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), _translate("dialogSettingsAll", "Fans"))
        self.groupBox_16.setTitle(_translate("dialogSettingsAll", "Feeding"))
        self.label_13.setText(_translate("dialogSettingsAll", "Feed litres"))
        self.le_feeder_feed_litres.setProperty("table", _translate("dialogSettingsAll", "config"))
        self.le_feeder_feed_litres.setProperty("title", _translate("dialogSettingsAll", "feeder"))
        self.le_feeder_feed_litres.setProperty("key", _translate("dialogSettingsAll", "feed L"))
        self.label_14.setText(_translate("dialogSettingsAll", "Soak time"))
        self.le_feeder_soak.setProperty("table", _translate("dialogSettingsAll", "config"))
        self.le_feeder_soak.setProperty("title", _translate("dialogSettingsAll", "feeder"))
        self.le_feeder_soak.setProperty("key", _translate("dialogSettingsAll", "soak time"))
        self.label_15.setText(_translate("dialogSettingsAll", "Max Mix"))
        self.le_mix_max.setProperty("table", _translate("dialogSettingsAll", "config"))
        self.le_mix_max.setProperty("title", _translate("dialogSettingsAll", "feeder"))
        self.le_mix_max.setProperty("key", _translate("dialogSettingsAll", "max mix litres"))
        self.label_31.setText(_translate("dialogSettingsAll", "L"))
        self.label_32.setText(_translate("dialogSettingsAll", "L"))
        self.label_33.setText(_translate("dialogSettingsAll", "sec"))
        self.label_42.setText(_translate("dialogSettingsAll", "L"))
        self.label_43.setText(_translate("dialogSettingsAll", "Manual max"))
        self.le_feeder_man_max.setProperty("table", _translate("dialogSettingsAll", "config"))
        self.le_feeder_man_max.setProperty("title", _translate("dialogSettingsAll", "feeder"))
        self.le_feeder_man_max.setProperty("key", _translate("dialogSettingsAll", "max manual feed"))
        self.groupBox_17.setTitle(_translate("dialogSettingsAll", "Flushing"))
        self.label_28.setText(_translate("dialogSettingsAll", "Flush litres"))
        self.le_feeder_flush.setProperty("table", _translate("dialogSettingsAll", "config"))
        self.le_feeder_flush.setProperty("title", _translate("dialogSettingsAll", "feeder"))
        self.le_feeder_flush.setProperty("key", _translate("dialogSettingsAll", "flush litres"))
        self.label_34.setText(_translate("dialogSettingsAll", "L"))
        self.groupBox_18.setTitle(_translate("dialogSettingsAll", "Stiring"))
        self.label_39.setText(_translate("dialogSettingsAll", "Nutrients"))
        self.le_feeder_stir_nutrients.setProperty("table", _translate("dialogSettingsAll", "config"))
        self.le_feeder_stir_nutrients.setProperty("title", _translate("dialogSettingsAll", "feeder"))
        self.le_feeder_stir_nutrients.setProperty("key", _translate("dialogSettingsAll", "nutrient stir time"))
        self.label_40.setText(_translate("dialogSettingsAll", "Mix"))
        self.label_41.setText(_translate("dialogSettingsAll", "Auto stir"))
        self.le_feeder_stri_mix.setProperty("table", _translate("dialogSettingsAll", "config"))
        self.le_feeder_stri_mix.setProperty("title", _translate("dialogSettingsAll", "feeder"))
        self.le_feeder_stri_mix.setProperty("key", _translate("dialogSettingsAll", "mix stir time"))
        self.label_44.setText(_translate("dialogSettingsAll", "sec"))
        self.label_45.setText(_translate("dialogSettingsAll", "sec"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_6), _translate("dialogSettingsAll", "Feeder Unit"))
        self.groupBox_19.setTitle(_translate("dialogSettingsAll", "Log path"))
        self.groupBox_20.setTitle(_translate("dialogSettingsAll", "Message system"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_7), _translate("dialogSettingsAll", "Logs"))
        self.label_52.setText(_translate("dialogSettingsAll", "Feed time"))
        self.label_54.setText(_translate("dialogSettingsAll", "Time tolerance"))
        self.label_55.setText(_translate("dialogSettingsAll", "Max quantity"))
        self.label_58.setText(_translate("dialogSettingsAll", "hrs"))
        self.label_59.setText(_translate("dialogSettingsAll", "Days"))
        self.label_60.setText(_translate("dialogSettingsAll", "Stage change"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("dialogSettingsAll", "Process"))
        self.groupBox_23.setTitle(_translate("dialogSettingsAll", "DE Module"))
        self.label_56.setText(_translate("dialogSettingsAll", "IP"))
        self.label_57.setText(_translate("dialogSettingsAll", "Port"))
        self.groupBox_24.setTitle(_translate("dialogSettingsAll", "IO Module"))
        self.label_61.setText(_translate("dialogSettingsAll", "IP"))
        self.label_62.setText(_translate("dialogSettingsAll", "Port"))
        self.groupBox_15.setTitle(_translate("dialogSettingsAll", "Network"))
        self.label_11.setText(_translate("dialogSettingsAll", "IP"))
        self.label_12.setText(_translate("dialogSettingsAll", "Port"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_8), _translate("dialogSettingsAll", "Network"))
        self.groupBox_22.setTitle(_translate("dialogSettingsAll", "Tanks"))
        self.label_47.setText(_translate("dialogSettingsAll", "Max litres"))
        self.label_48.setText(_translate("dialogSettingsAll", "Min litres"))
        self.label_49.setText(_translate("dialogSettingsAll", "Fill extra"))
        self.label_50.setText(_translate("dialogSettingsAll", "L"))
        self.label_51.setText(_translate("dialogSettingsAll", "L"))
        self.label_53.setText(_translate("dialogSettingsAll", "L"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_11), _translate("dialogSettingsAll", "Water"))
        self.pb_close.setText(_translate("dialogSettingsAll", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialogSettingsAll = QtWidgets.QWidget()
    ui = Ui_dialogSettingsAll()
    ui.setupUi(dialogSettingsAll)
    dialogSettingsAll.show()
    sys.exit(app.exec_())

