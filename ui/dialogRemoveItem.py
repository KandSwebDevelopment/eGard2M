# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogRemoveItem.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogRemoveItem(object):
    def setupUi(self, DialogRemoveItem):
        DialogRemoveItem.setObjectName("DialogRemoveItem")
        DialogRemoveItem.resize(257, 201)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogRemoveItem.setFont(font)
        self.cb_item = QtWidgets.QComboBox(DialogRemoveItem)
        self.cb_item.setGeometry(QtCore.QRect(130, 60, 69, 22))
        self.cb_item.setObjectName("cb_item")
        self.te_reason = QtWidgets.QTextEdit(DialogRemoveItem)
        self.te_reason.setGeometry(QtCore.QRect(20, 90, 211, 61))
        self.te_reason.setObjectName("te_reason")
        self.pb_apply = QtWidgets.QPushButton(DialogRemoveItem)
        self.pb_apply.setGeometry(QtCore.QRect(160, 160, 81, 28))
        self.pb_apply.setAutoDefault(False)
        self.pb_apply.setObjectName("pb_apply")
        self.pb_cancel = QtWidgets.QPushButton(DialogRemoveItem)
        self.pb_cancel.setGeometry(QtCore.QRect(40, 160, 81, 28))
        self.pb_cancel.setObjectName("pb_cancel")
        self.label = QtWidgets.QLabel(DialogRemoveItem)
        self.label.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.label.setObjectName("label")
        self.lbl_info = QtWidgets.QLabel(DialogRemoveItem)
        self.lbl_info.setGeometry(QtCore.QRect(20, 10, 221, 31))
        self.lbl_info.setText("")
        self.lbl_info.setObjectName("lbl_info")

        self.retranslateUi(DialogRemoveItem)
        QtCore.QMetaObject.connectSlotsByName(DialogRemoveItem)

    def retranslateUi(self, DialogRemoveItem):
        _translate = QtCore.QCoreApplication.translate
        DialogRemoveItem.setWindowTitle(_translate("DialogRemoveItem", "Removal"))
        self.pb_apply.setText(_translate("DialogRemoveItem", "Apply"))
        self.pb_cancel.setText(_translate("DialogRemoveItem", "Cancel"))
        self.label.setText(_translate("DialogRemoveItem", "Item Number"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogRemoveItem = QtWidgets.QDialog()
    ui = Ui_DialogRemoveItem()
    ui.setupUi(DialogRemoveItem)
    DialogRemoveItem.show()
    sys.exit(app.exec_())

