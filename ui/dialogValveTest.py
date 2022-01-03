# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogValveTest.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialogValveTest(object):
    def setupUi(self, dialogValveTest):
        dialogValveTest.setObjectName("dialogValveTest")
        dialogValveTest.resize(293, 234)
        font = QtGui.QFont()
        font.setPointSize(11)
        dialogValveTest.setFont(font)
        self.pb_close = QtWidgets.QPushButton(dialogValveTest)
        self.pb_close.setGeometry(QtCore.QRect(200, 200, 75, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pb_close.setFont(font)
        self.pb_close.setAutoDefault(False)
        self.pb_close.setObjectName("pb_close")
        self.pb_close_all = QtWidgets.QPushButton(dialogValveTest)
        self.pb_close_all.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.pb_close_all.setObjectName("pb_close_all")
        self.ck_valve_1 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_1.setGeometry(QtCore.QRect(10, 50, 120, 31))
        self.ck_valve_1.setObjectName("ck_valve_1")
        self.ck_valve_2 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_2.setGeometry(QtCore.QRect(10, 80, 120, 31))
        self.ck_valve_2.setObjectName("ck_valve_2")
        self.ck_valve_3 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_3.setGeometry(QtCore.QRect(10, 110, 120, 31))
        self.ck_valve_3.setObjectName("ck_valve_3")
        self.ck_valve_4 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_4.setGeometry(QtCore.QRect(10, 140, 120, 31))
        self.ck_valve_4.setObjectName("ck_valve_4")
        self.ck_valve_5 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_5.setGeometry(QtCore.QRect(160, 50, 120, 31))
        self.ck_valve_5.setObjectName("ck_valve_5")
        self.ck_valve_6 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_6.setGeometry(QtCore.QRect(160, 80, 120, 31))
        self.ck_valve_6.setObjectName("ck_valve_6")
        self.ck_valve_7 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_7.setGeometry(QtCore.QRect(160, 110, 120, 31))
        self.ck_valve_7.setObjectName("ck_valve_7")
        self.ck_valve_8 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_8.setGeometry(QtCore.QRect(160, 140, 120, 31))
        self.ck_valve_8.setObjectName("ck_valve_8")
        self.ck_valve_9 = QtWidgets.QCheckBox(dialogValveTest)
        self.ck_valve_9.setGeometry(QtCore.QRect(160, 170, 120, 31))
        self.ck_valve_9.setObjectName("ck_valve_9")
        self.pushButton = QtWidgets.QPushButton(dialogValveTest)
        self.pushButton.setGeometry(QtCore.QRect(110, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(dialogValveTest)
        QtCore.QMetaObject.connectSlotsByName(dialogValveTest)

    def retranslateUi(self, dialogValveTest):
        _translate = QtCore.QCoreApplication.translate
        dialogValveTest.setWindowTitle(_translate("dialogValveTest", "Valve Test"))
        self.pb_close.setText(_translate("dialogValveTest", "Close"))
        self.pb_close_all.setText(_translate("dialogValveTest", "Close All"))
        self.ck_valve_1.setText(_translate("dialogValveTest", "Tank 1"))
        self.ck_valve_2.setText(_translate("dialogValveTest", "Tank 2"))
        self.ck_valve_3.setText(_translate("dialogValveTest", "Feeder Inlet"))
        self.ck_valve_4.setText(_translate("dialogValveTest", "Tank Drain"))
        self.ck_valve_5.setText(_translate("dialogValveTest", "Manual Feed"))
        self.ck_valve_6.setText(_translate("dialogValveTest", "Feed Area 1"))
        self.ck_valve_7.setText(_translate("dialogValveTest", "Feed Area 2"))
        self.ck_valve_8.setText(_translate("dialogValveTest", "Flush Area 1"))
        self.ck_valve_9.setText(_translate("dialogValveTest", "Flush Area 2"))
        self.pushButton.setText(_translate("dialogValveTest", "Query"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialogValveTest = QtWidgets.QWidget()
    ui = Ui_dialogValveTest()
    ui.setupUi(dialogValveTest)
    dialogValveTest.show()
    sys.exit(app.exec_())

