# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogStrainFinder.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogStrainFinder(object):
    def setupUi(self, DialogStrainFinder):
        DialogStrainFinder.setObjectName("DialogStrainFinder")
        DialogStrainFinder.resize(400, 157)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogStrainFinder.setFont(font)
        self.cb_name = QtWidgets.QComboBox(DialogStrainFinder)
        self.cb_name.setGeometry(QtCore.QRect(30, 30, 271, 22))
        self.cb_name.setObjectName("cb_name")
        self.le_id = QtWidgets.QLineEdit(DialogStrainFinder)
        self.le_id.setGeometry(QtCore.QRect(60, 80, 71, 20))
        self.le_id.setObjectName("le_id")
        self.label = QtWidgets.QLabel(DialogStrainFinder)
        self.label.setGeometry(QtCore.QRect(32, 83, 47, 13))
        self.label.setObjectName("label")
        self.pb_close = QtWidgets.QPushButton(DialogStrainFinder)
        self.pb_close.setGeometry(QtCore.QRect(280, 80, 75, 23))
        self.pb_close.setObjectName("pb_close")

        self.retranslateUi(DialogStrainFinder)
        QtCore.QMetaObject.connectSlotsByName(DialogStrainFinder)

    def retranslateUi(self, DialogStrainFinder):
        _translate = QtCore.QCoreApplication.translate
        DialogStrainFinder.setWindowTitle(_translate("DialogStrainFinder", "Strain Finder"))
        self.label.setText(_translate("DialogStrainFinder", "ID"))
        self.pb_close.setText(_translate("DialogStrainFinder", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogStrainFinder = QtWidgets.QWidget()
    ui = Ui_DialogStrainFinder()
    ui.setupUi(DialogStrainFinder)
    DialogStrainFinder.show()
    sys.exit(app.exec_())

