# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogsysInfo.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSysInfo(object):
    def setupUi(self, DialogSysInfo):
        DialogSysInfo.setObjectName("DialogSysInfo")
        DialogSysInfo.resize(435, 579)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogSysInfo.setFont(font)
        self.gridLayout_2 = QtWidgets.QGridLayout(DialogSysInfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.te_info = QtWidgets.QTextEdit(DialogSysInfo)
        self.te_info.setReadOnly(True)
        self.te_info.setObjectName("te_info")
        self.gridLayout.addWidget(self.te_info, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_close = QtWidgets.QPushButton(DialogSysInfo)
        self.pb_close.setObjectName("pb_close")
        self.horizontalLayout.addWidget(self.pb_close)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(DialogSysInfo)
        QtCore.QMetaObject.connectSlotsByName(DialogSysInfo)

    def retranslateUi(self, DialogSysInfo):
        _translate = QtCore.QCoreApplication.translate
        DialogSysInfo.setWindowTitle(_translate("DialogSysInfo", "System Info"))
        self.pb_close.setText(_translate("DialogSysInfo", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogSysInfo = QtWidgets.QDialog()
    ui = Ui_DialogSysInfo()
    ui.setupUi(DialogSysInfo)
    DialogSysInfo.show()
    sys.exit(app.exec_())

