# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogJournelViewer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogJournalViewer(object):
    def setupUi(self, DialogJournalViewer):
        DialogJournalViewer.setObjectName("DialogJournalViewer")
        DialogJournalViewer.resize(789, 514)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogJournalViewer.setFont(font)
        self.pb_close = QtWidgets.QPushButton(DialogJournalViewer)
        self.pb_close.setGeometry(QtCore.QRect(700, 480, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pb_close.setFont(font)
        self.pb_close.setObjectName("pb_close")
        self.cb_process = QtWidgets.QComboBox(DialogJournalViewer)
        self.cb_process.setGeometry(QtCore.QRect(90, 10, 141, 22))
        self.cb_process.setObjectName("cb_process")
        self.label_12 = QtWidgets.QLabel(DialogJournalViewer)
        self.label_12.setGeometry(QtCore.QRect(20, 4, 51, 31))
        self.label_12.setObjectName("label_12")
        self.pb_save = QtWidgets.QPushButton(DialogJournalViewer)
        self.pb_save.setGeometry(QtCore.QRect(10, 480, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pb_save.setFont(font)
        self.pb_save.setObjectName("pb_save")
        self.te_log = QtWidgets.QTextEdit(DialogJournalViewer)
        self.te_log.setGeometry(QtCore.QRect(10, 40, 771, 431))
        self.te_log.setObjectName("te_log")
        self.label_13 = QtWidgets.QLabel(DialogJournalViewer)
        self.label_13.setGeometry(QtCore.QRect(260, 0, 61, 31))
        self.label_13.setObjectName("label_13")
        self.cb_feed = QtWidgets.QComboBox(DialogJournalViewer)
        self.cb_feed.setGeometry(QtCore.QRect(320, 10, 141, 22))
        self.cb_feed.setObjectName("cb_feed")

        self.retranslateUi(DialogJournalViewer)
        QtCore.QMetaObject.connectSlotsByName(DialogJournalViewer)

    def retranslateUi(self, DialogJournalViewer):
        _translate = QtCore.QCoreApplication.translate
        DialogJournalViewer.setWindowTitle(_translate("DialogJournalViewer", "Process Log Viewer"))
        self.pb_close.setText(_translate("DialogJournalViewer", "Close"))
        self.label_12.setText(_translate("DialogJournalViewer", "Journal"))
        self.pb_save.setText(_translate("DialogJournalViewer", "Save"))
        self.label_13.setText(_translate("DialogJournalViewer", "Feeding"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogJournalViewer = QtWidgets.QWidget()
    ui = Ui_DialogJournalViewer()
    ui.setupUi(DialogJournalViewer)
    DialogJournalViewer.show()
    sys.exit(app.exec_())

