# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogPatterns.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogPatterns(object):
    def setupUi(self, DialogPatterns):
        DialogPatterns.setObjectName("DialogPatterns")
        DialogPatterns.resize(522, 327)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogPatterns.setFont(font)
        self.label = QtWidgets.QLabel(DialogPatterns)
        self.label.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label.setObjectName("label")
        self.cb_patterns = QtWidgets.QComboBox(DialogPatterns)
        self.cb_patterns.setGeometry(QtCore.QRect(80, 20, 241, 22))
        self.cb_patterns.setEditable(False)
        self.cb_patterns.setObjectName("cb_patterns")
        self.le_id = QtWidgets.QLineEdit(DialogPatterns)
        self.le_id.setGeometry(QtCore.QRect(380, 20, 61, 20))
        self.le_id.setReadOnly(True)
        self.le_id.setObjectName("le_id")
        self.label_2 = QtWidgets.QLabel(DialogPatterns)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 101, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(DialogPatterns)
        self.label_3.setGeometry(QtCore.QRect(70, 230, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(DialogPatterns)
        self.label_4.setGeometry(QtCore.QRect(70, 260, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(DialogPatterns)
        self.label_5.setGeometry(QtCore.QRect(350, 23, 47, 13))
        self.label_5.setObjectName("label_5")
        self.tw_pattern_stages = QtWidgets.QTableWidget(DialogPatterns)
        self.tw_pattern_stages.setGeometry(QtCore.QRect(10, 80, 501, 141))
        self.tw_pattern_stages.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_pattern_stages.setObjectName("tw_pattern_stages")
        self.tw_pattern_stages.setColumnCount(0)
        self.tw_pattern_stages.setRowCount(0)
        self.pb_close = QtWidgets.QPushButton(DialogPatterns)
        self.pb_close.setGeometry(QtCore.QRect(430, 290, 75, 23))
        self.pb_close.setObjectName("pb_close")

        self.retranslateUi(DialogPatterns)
        QtCore.QMetaObject.connectSlotsByName(DialogPatterns)

    def retranslateUi(self, DialogPatterns):
        _translate = QtCore.QCoreApplication.translate
        DialogPatterns.setWindowTitle(_translate("DialogPatterns", "Process Patterns"))
        self.label.setText(_translate("DialogPatterns", "Pattern"))
        self.label_2.setText(_translate("DialogPatterns", "Pattern Stages"))
        self.label_3.setText(_translate("DialogPatterns", "Pattern"))
        self.label_4.setText(_translate("DialogPatterns", "Pattern"))
        self.label_5.setText(_translate("DialogPatterns", "ID"))
        self.pb_close.setText(_translate("DialogPatterns", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogPatterns = QtWidgets.QWidget()
    ui = Ui_DialogPatterns()
    ui.setupUi(DialogPatterns)
    DialogPatterns.show()
    sys.exit(app.exec_())

