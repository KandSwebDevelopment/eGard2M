# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogLogViewer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogLogViewer(object):
    def setupUi(self, DialogLogViewer):
        DialogLogViewer.setObjectName("DialogLogViewer")
        DialogLogViewer.resize(569, 505)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogLogViewer.setFont(font)
        self.cb_log = QtWidgets.QComboBox(DialogLogViewer)
        self.cb_log.setGeometry(QtCore.QRect(310, 20, 241, 22))
        self.cb_log.setObjectName("cb_log")
        self.te_log = QtWidgets.QTextEdit(DialogLogViewer)
        self.te_log.setGeometry(QtCore.QRect(10, 60, 541, 401))
        self.te_log.setObjectName("te_log")
        self.pb_close = QtWidgets.QPushButton(DialogLogViewer)
        self.pb_close.setGeometry(QtCore.QRect(480, 470, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.cb_log_type = QtWidgets.QComboBox(DialogLogViewer)
        self.cb_log_type.setGeometry(QtCore.QRect(20, 20, 181, 22))
        self.cb_log_type.setObjectName("cb_log_type")

        self.retranslateUi(DialogLogViewer)
        QtCore.QMetaObject.connectSlotsByName(DialogLogViewer)

    def retranslateUi(self, DialogLogViewer):
        _translate = QtCore.QCoreApplication.translate
        DialogLogViewer.setWindowTitle(_translate("DialogLogViewer", "Log Viewer"))
        self.pb_close.setText(_translate("DialogLogViewer", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogLogViewer = QtWidgets.QDialog()
    ui = Ui_DialogLogViewer()
    ui.setupUi(DialogLogViewer)
    DialogLogViewer.show()
    sys.exit(app.exec_())

