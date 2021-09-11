# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogSeedPicker.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSeedPicker(object):
    def setupUi(self, DialogSeedPicker):
        DialogSeedPicker.setObjectName("DialogSeedPicker")
        DialogSeedPicker.resize(673, 719)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogSeedPicker.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(DialogSeedPicker)
        self.gridLayout.setObjectName("gridLayout")
        self.le_stock = QtWidgets.QLineEdit(DialogSeedPicker)
        self.le_stock.setMaximumSize(QtCore.QSize(75, 16777215))
        self.le_stock.setReadOnly(True)
        self.le_stock.setObjectName("le_stock")
        self.gridLayout.addWidget(self.le_stock, 0, 4, 1, 1)
        self.ck_in_stock = QtWidgets.QCheckBox(DialogSeedPicker)
        self.ck_in_stock.setChecked(True)
        self.ck_in_stock.setTristate(False)
        self.ck_in_stock.setObjectName("ck_in_stock")
        self.gridLayout.addWidget(self.ck_in_stock, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.cb_sort = QtWidgets.QComboBox(DialogSeedPicker)
        self.cb_sort.setObjectName("cb_sort")
        self.gridLayout.addWidget(self.cb_sort, 0, 0, 1, 1)
        self.te_strains = QtWidgets.QTextEdit(DialogSeedPicker)
        self.te_strains.setReadOnly(True)
        self.te_strains.setObjectName("te_strains")
        self.gridLayout.addWidget(self.te_strains, 1, 0, 1, 5)
        self.label = QtWidgets.QLabel(DialogSeedPicker)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.pb_close = QtWidgets.QPushButton(DialogSeedPicker)
        self.pb_close.setObjectName("pb_close")
        self.gridLayout.addWidget(self.pb_close, 2, 4, 1, 1)
        self.pb_print = QtWidgets.QPushButton(DialogSeedPicker)
        self.pb_print.setObjectName("pb_print")
        self.gridLayout.addWidget(self.pb_print, 2, 0, 1, 1)

        self.retranslateUi(DialogSeedPicker)
        QtCore.QMetaObject.connectSlotsByName(DialogSeedPicker)

    def retranslateUi(self, DialogSeedPicker):
        _translate = QtCore.QCoreApplication.translate
        DialogSeedPicker.setWindowTitle(_translate("DialogSeedPicker", "Seed Picker"))
        self.ck_in_stock.setText(_translate("DialogSeedPicker", "In stock only"))
        self.label.setText(_translate("DialogSeedPicker", "Stock"))
        self.pb_close.setText(_translate("DialogSeedPicker", "Close"))
        self.pb_print.setText(_translate("DialogSeedPicker", "Print Stock"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogSeedPicker = QtWidgets.QDialog()
    ui = Ui_DialogSeedPicker()
    ui.setupUi(DialogSeedPicker)
    DialogSeedPicker.show()
    sys.exit(app.exec_())

