# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogEngineerIO.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogMessage(object):
    def setupUi(self, DialogMessage):
        DialogMessage.setObjectName("DialogMessage")
        DialogMessage.resize(571, 464)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogMessage.setFont(font)
        self.gridLayout_2 = QtWidgets.QGridLayout(DialogMessage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ck_to_fu = QtWidgets.QCheckBox(DialogMessage)
        self.ck_to_fu.setStyleSheet("background-color: rgb(128, 179, 255);")
        self.ck_to_fu.setChecked(True)
        self.ck_to_fu.setObjectName("ck_to_fu")
        self.horizontalLayout.addWidget(self.ck_to_fu)
        self.ck_to_rl = QtWidgets.QCheckBox(DialogMessage)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ck_to_rl.setFont(font)
        self.ck_to_rl.setStyleSheet("background-color: #ffff80")
        self.ck_to_rl.setChecked(True)
        self.ck_to_rl.setObjectName("ck_to_rl")
        self.horizontalLayout.addWidget(self.ck_to_rl)
        self.ck_to_de = QtWidgets.QCheckBox(DialogMessage)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ck_to_de.setFont(font)
        self.ck_to_de.setStyleSheet("background-color:#ffb3b3")
        self.ck_to_de.setChecked(True)
        self.ck_to_de.setObjectName("ck_to_de")
        self.horizontalLayout.addWidget(self.ck_to_de)
        self.ck_to_io = QtWidgets.QCheckBox(DialogMessage)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ck_to_io.setFont(font)
        self.ck_to_io.setStyleSheet("background-color: #85e085")
        self.ck_to_io.setChecked(True)
        self.ck_to_io.setObjectName("ck_to_io")
        self.horizontalLayout.addWidget(self.ck_to_io)
        self.pb_close = QtWidgets.QPushButton(DialogMessage)
        self.pb_close.setObjectName("pb_close")
        self.horizontalLayout.addWidget(self.pb_close)
        self.gridLayout.addLayout(self.horizontalLayout, 7, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ck_from_fu = QtWidgets.QCheckBox(DialogMessage)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ck_from_fu.setFont(font)
        self.ck_from_fu.setStyleSheet("background-color: rgb(0, 102, 255);")
        self.ck_from_fu.setChecked(True)
        self.ck_from_fu.setObjectName("ck_from_fu")
        self.horizontalLayout_2.addWidget(self.ck_from_fu)
        self.ck_from_rl = QtWidgets.QCheckBox(DialogMessage)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ck_from_rl.setFont(font)
        self.ck_from_rl.setStyleSheet("background-color:#e6e600")
        self.ck_from_rl.setChecked(True)
        self.ck_from_rl.setObjectName("ck_from_rl")
        self.horizontalLayout_2.addWidget(self.ck_from_rl)
        self.ck_from_de = QtWidgets.QCheckBox(DialogMessage)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ck_from_de.setFont(font)
        self.ck_from_de.setStyleSheet("background-color:#FF5050\n"
"")
        self.ck_from_de.setChecked(True)
        self.ck_from_de.setObjectName("ck_from_de")
        self.horizontalLayout_2.addWidget(self.ck_from_de)
        self.ck_from_io = QtWidgets.QCheckBox(DialogMessage)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ck_from_io.setFont(font)
        self.ck_from_io.setStyleSheet("background-color: #29a329\n"
"")
        self.ck_from_io.setChecked(True)
        self.ck_from_io.setObjectName("ck_from_io")
        self.horizontalLayout_2.addWidget(self.ck_from_io)
        self.pb_clear = QtWidgets.QPushButton(DialogMessage)
        self.pb_clear.setObjectName("pb_clear")
        self.horizontalLayout_2.addWidget(self.pb_clear)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.te_message = QtWidgets.QTextEdit(DialogMessage)
        self.te_message.setReadOnly(True)
        self.te_message.setObjectName("te_message")
        self.gridLayout.addWidget(self.te_message, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(DialogMessage)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(DialogMessage)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(DialogMessage)
        QtCore.QMetaObject.connectSlotsByName(DialogMessage)

    def retranslateUi(self, DialogMessage):
        _translate = QtCore.QCoreApplication.translate
        DialogMessage.setWindowTitle(_translate("DialogMessage", "Dialog"))
        self.ck_to_fu.setText(_translate("DialogMessage", "F/U"))
        self.ck_to_rl.setText(_translate("DialogMessage", "Relay"))
        self.ck_to_de.setText(_translate("DialogMessage", "D/E"))
        self.ck_to_io.setText(_translate("DialogMessage", "I/O"))
        self.pb_close.setText(_translate("DialogMessage", "Close"))
        self.ck_from_fu.setText(_translate("DialogMessage", "F/U"))
        self.ck_from_rl.setText(_translate("DialogMessage", "Relay"))
        self.ck_from_de.setText(_translate("DialogMessage", "D/E"))
        self.ck_from_io.setText(_translate("DialogMessage", "I/O"))
        self.pb_clear.setText(_translate("DialogMessage", "Clear"))
        self.label.setText(_translate("DialogMessage", "From"))
        self.label_2.setText(_translate("DialogMessage", "To"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogMessage = QtWidgets.QDialog()
    ui = Ui_DialogMessage()
    ui.setupUi(DialogMessage)
    DialogMessage.show()
    sys.exit(app.exec_())

