# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogProcessPerformance.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogProcessPreformance(object):
    def setupUi(self, DialogProcessPreformance):
        DialogProcessPreformance.setObjectName("DialogProcessPreformance")
        DialogProcessPreformance.resize(797, 646)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogProcessPreformance.setFont(font)
        self.pb_close = QtWidgets.QPushButton(DialogProcessPreformance)
        self.pb_close.setGeometry(QtCore.QRect(710, 610, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.cb_process = QtWidgets.QComboBox(DialogProcessPreformance)
        self.cb_process.setGeometry(QtCore.QRect(100, 20, 69, 22))
        self.cb_process.setObjectName("cb_process")
        self.label = QtWidgets.QLabel(DialogProcessPreformance)
        self.label.setGeometry(QtCore.QRect(30, 20, 61, 21))
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(DialogProcessPreformance)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 761, 381))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.widget = QtWidgets.QWidget(self.horizontalLayoutWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(DialogProcessPreformance)
        QtCore.QMetaObject.connectSlotsByName(DialogProcessPreformance)

    def retranslateUi(self, DialogProcessPreformance):
        _translate = QtCore.QCoreApplication.translate
        DialogProcessPreformance.setWindowTitle(_translate("DialogProcessPreformance", "Process Preformance"))
        self.pb_close.setText(_translate("DialogProcessPreformance", "Close"))
        self.label.setText(_translate("DialogProcessPreformance", "Process"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogProcessPreformance = QtWidgets.QDialog()
    ui = Ui_DialogProcessPreformance()
    ui.setupUi(DialogProcessPreformance)
    DialogProcessPreformance.show()
    sys.exit(app.exec_())

