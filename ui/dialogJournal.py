# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogJournal.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogJournal(object):
    def setupUi(self, DialogJournal):
        DialogJournal.setObjectName("DialogJournal")
        DialogJournal.resize(677, 426)
        self.gridLayout = QtWidgets.QGridLayout(DialogJournal)
        self.gridLayout.setObjectName("gridLayout")
        self.temessage = QtWidgets.QTextEdit(DialogJournal)
        self.temessage.setReadOnly(True)
        self.temessage.setObjectName("temessage")
        self.gridLayout.addWidget(self.temessage, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(DialogJournal)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(DialogJournal)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(DialogJournal)
        self.dateTimeEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.horizontalLayout_2.addWidget(self.dateTimeEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.tenew = QtWidgets.QTextEdit(DialogJournal)
        self.tenew.setMaximumSize(QtCore.QSize(16777215, 80))
        self.tenew.setObjectName("tenew")
        self.gridLayout.addWidget(self.tenew, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbsave = QtWidgets.QPushButton(DialogJournal)
        self.pbsave.setObjectName("pbsave")
        self.horizontalLayout.addWidget(self.pbsave)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pbclose = QtWidgets.QPushButton(DialogJournal)
        self.pbclose.setObjectName("pbclose")
        self.horizontalLayout.addWidget(self.pbclose)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.retranslateUi(DialogJournal)
        QtCore.QMetaObject.connectSlotsByName(DialogJournal)

    def retranslateUi(self, DialogJournal):
        _translate = QtCore.QCoreApplication.translate
        DialogJournal.setWindowTitle(_translate("DialogJournal", "Journal"))
        self.label.setText(_translate("DialogJournal", "New Entry"))
        self.label_2.setText(_translate("DialogJournal", "Date"))
        self.pbsave.setText(_translate("DialogJournal", "Save"))
        self.pbclose.setText(_translate("DialogJournal", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogJournal = QtWidgets.QDialog()
    ui = Ui_DialogJournal()
    ui.setupUi(DialogJournal)
    DialogJournal.show()
    sys.exit(app.exec_())

