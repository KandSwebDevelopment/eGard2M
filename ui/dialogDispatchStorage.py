# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogDispatchStorage.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(310, 462)
        font = QtGui.QFont()
        font.setPointSize(11)
        Form.setFont(font)
        self.pb_tare = QtWidgets.QPushButton(Form)
        self.pb_tare.setGeometry(QtCore.QRect(160, 400, 75, 23))
        self.pb_tare.setObjectName("pb_tare")
        self.pb_close = QtWidgets.QPushButton(Form)
        self.pb_close.setGeometry(QtCore.QRect(230, 430, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.pb_add = QtWidgets.QPushButton(Form)
        self.pb_add.setGeometry(QtCore.QRect(20, 430, 75, 23))
        self.pb_add.setObjectName("pb_add")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.label.setObjectName("label")
        self.cb_jar = QtWidgets.QComboBox(Form)
        self.cb_jar.setGeometry(QtCore.QRect(20, 30, 231, 22))
        self.cb_jar.setObjectName("cb_jar")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setEnabled(False)
        self.frame.setGeometry(QtCore.QRect(10, 60, 281, 331))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.le_name = QtWidgets.QLineEdit(self.frame)
        self.le_name.setGeometry(QtCore.QRect(90, 10, 51, 20))
        self.le_name.setReadOnly(True)
        self.le_name.setObjectName("le_name")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(0, 14, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(0, 100, 81, 21))
        self.label_3.setObjectName("label_3")
        self.le_nett = QtWidgets.QLineEdit(self.frame)
        self.le_nett.setGeometry(QtCore.QRect(90, 100, 71, 20))
        self.le_nett.setObjectName("le_nett")
        self.pb_set = QtWidgets.QPushButton(self.frame)
        self.pb_set.setGeometry(QtCore.QRect(180, 100, 51, 23))
        self.pb_set.setObjectName("pb_set")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(0, 130, 81, 21))
        self.label_4.setObjectName("label_4")
        self.le_uid = QtWidgets.QLineEdit(self.frame)
        self.le_uid.setGeometry(QtCore.QRect(90, 130, 111, 20))
        self.le_uid.setObjectName("le_uid")
        self.pb_scan = QtWidgets.QPushButton(self.frame)
        self.pb_scan.setGeometry(QtCore.QRect(210, 130, 51, 23))
        self.pb_scan.setObjectName("pb_scan")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(0, 70, 81, 21))
        self.label_5.setObjectName("label_5")
        self.le_weight = QtWidgets.QLineEdit(self.frame)
        self.le_weight.setGeometry(QtCore.QRect(90, 70, 71, 20))
        self.le_weight.setObjectName("le_weight")
        self.pb_read = QtWidgets.QPushButton(self.frame)
        self.pb_read.setGeometry(QtCore.QRect(180, 70, 51, 23))
        self.pb_read.setObjectName("pb_read")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(230, 20, 47, 13))
        self.label_6.setObjectName("label_6")
        self.cb_strain = QtWidgets.QComboBox(self.frame)
        self.cb_strain.setGeometry(QtCore.QRect(0, 40, 281, 22))
        self.cb_strain.setObjectName("cb_strain")
        self.pb_save = QtWidgets.QPushButton(self.frame)
        self.pb_save.setGeometry(QtCore.QRect(194, 290, 81, 31))
        self.pb_save.setObjectName("pb_save")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(10, 260, 81, 16))
        self.label_7.setObjectName("label_7")
        self.cb_jar_transfer = QtWidgets.QComboBox(self.frame)
        self.cb_jar_transfer.setGeometry(QtCore.QRect(90, 260, 101, 22))
        self.cb_jar_transfer.setObjectName("cb_jar_transfer")
        self.pb_transfer = QtWidgets.QPushButton(self.frame)
        self.pb_transfer.setGeometry(QtCore.QRect(200, 260, 71, 23))
        self.pb_transfer.setObjectName("pb_transfer")
        self.pb_hum_pac = QtWidgets.QPushButton(self.frame)
        self.pb_hum_pac.setGeometry(QtCore.QRect(200, 160, 61, 23))
        self.pb_hum_pac.setObjectName("pb_hum_pac")
        self.le_hum_pac = QtWidgets.QLineEdit(self.frame)
        self.le_hum_pac.setGeometry(QtCore.QRect(110, 160, 71, 20))
        self.le_hum_pac.setObjectName("le_hum_pac")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(0, 160, 101, 21))
        self.label_9.setObjectName("label_9")
        self.le_gross = QtWidgets.QLineEdit(self.frame)
        self.le_gross.setGeometry(QtCore.QRect(30, 190, 59, 20))
        self.le_gross.setReadOnly(True)
        self.le_gross.setObjectName("le_gross")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(0, 190, 21, 21))
        self.label_10.setObjectName("label_10")
        self.le_diff = QtWidgets.QLineEdit(self.frame)
        self.le_diff.setGeometry(QtCore.QRect(220, 190, 59, 20))
        self.le_diff.setReadOnly(True)
        self.le_diff.setObjectName("le_diff")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(198, 190, 21, 21))
        self.label_11.setObjectName("label_11")
        self.le_gross_2 = QtWidgets.QLineEdit(self.frame)
        self.le_gross_2.setGeometry(QtCore.QRect(129, 190, 59, 20))
        self.le_gross_2.setReadOnly(True)
        self.le_gross_2.setObjectName("le_gross_2")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(99, 190, 31, 21))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(0, 220, 61, 21))
        self.label_13.setObjectName("label_13")
        self.cb_location = QtWidgets.QComboBox(self.frame)
        self.cb_location.setGeometry(QtCore.QRect(70, 220, 69, 22))
        self.cb_location.setObjectName("cb_location")
        self.pb_cancel = QtWidgets.QPushButton(self.frame)
        self.pb_cancel.setGeometry(QtCore.QRect(10, 290, 75, 26))
        self.pb_cancel.setObjectName("pb_cancel")
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setGeometry(QtCore.QRect(160, 220, 61, 21))
        self.label_14.setObjectName("label_14")
        self.le_size = QtWidgets.QLineEdit(self.frame)
        self.le_size.setGeometry(QtCore.QRect(200, 220, 59, 20))
        self.le_size.setReadOnly(False)
        self.le_size.setObjectName("le_size")
        self.pb_empty = QtWidgets.QPushButton(self.frame)
        self.pb_empty.setGeometry(QtCore.QRect(100, 290, 75, 26))
        self.pb_empty.setObjectName("pb_empty")
        self.lbl_count = QtWidgets.QLabel(Form)
        self.lbl_count.setGeometry(QtCore.QRect(260, 30, 31, 21))
        self.lbl_count.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_count.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbl_count.setText("")
        self.lbl_count.setObjectName("lbl_count")
        self.le_live = QtWidgets.QLineEdit(Form)
        self.le_live.setGeometry(QtCore.QRect(60, 400, 71, 20))
        self.le_live.setReadOnly(True)
        self.le_live.setObjectName("le_live")
        self.pb_remove = QtWidgets.QPushButton(Form)
        self.pb_remove.setEnabled(False)
        self.pb_remove.setGeometry(QtCore.QRect(100, 430, 75, 23))
        self.pb_remove.setObjectName("pb_remove")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(20, 400, 31, 21))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Dispatch - Storage"))
        self.pb_tare.setText(_translate("Form", "Tare"))
        self.pb_close.setText(_translate("Form", "Close"))
        self.pb_add.setText(_translate("Form", "New"))
        self.label.setText(_translate("Form", "Jar"))
        self.label_2.setText(_translate("Form", "Name"))
        self.label_3.setText(_translate("Form", "Nett Weight"))
        self.pb_set.setText(_translate("Form", "Set"))
        self.label_4.setText(_translate("Form", "UID"))
        self.pb_scan.setText(_translate("Form", "Scan"))
        self.label_5.setText(_translate("Form", "Weight"))
        self.pb_read.setText(_translate("Form", "Read"))
        self.label_6.setText(_translate("Form", "Strain"))
        self.pb_save.setText(_translate("Form", "Save"))
        self.label_7.setText(_translate("Form", "Transfer to"))
        self.pb_transfer.setText(_translate("Form", "Transfer"))
        self.pb_hum_pac.setText(_translate("Form", "Add"))
        self.label_9.setText(_translate("Form", "Humidity Pack"))
        self.label_10.setText(_translate("Form", "Cur"))
        self.label_11.setText(_translate("Form", "Dif"))
        self.label_12.setText(_translate("Form", "Org"))
        self.label_13.setText(_translate("Form", "Location"))
        self.pb_cancel.setText(_translate("Form", "Cancel"))
        self.label_14.setText(_translate("Form", "Size"))
        self.pb_empty.setText(_translate("Form", "Empty"))
        self.pb_remove.setText(_translate("Form", "Remove"))
        self.label_8.setText(_translate("Form", "Live"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

