# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogGraphEnviroment.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogGraphEnv(object):
    def setupUi(self, DialogGraphEnv):
        DialogGraphEnv.setObjectName("DialogGraphEnv")
        DialogGraphEnv.resize(1202, 714)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogGraphEnv.setFont(font)
        self.cb_logs = QtWidgets.QComboBox(DialogGraphEnv)
        self.cb_logs.setGeometry(QtCore.QRect(20, 20, 201, 22))
        self.cb_logs.setObjectName("cb_logs")
        self.wg_graph_1 = QtWidgets.QWidget(DialogGraphEnv)
        self.wg_graph_1.setGeometry(QtCore.QRect(10, 60, 1171, 541))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_graph_1.sizePolicy().hasHeightForWidth())
        self.wg_graph_1.setSizePolicy(sizePolicy)
        self.wg_graph_1.setObjectName("wg_graph_1")
        self.pb_close = QtWidgets.QPushButton(DialogGraphEnv)
        self.pb_close.setGeometry(QtCore.QRect(1090, 20, 75, 23))
        self.pb_close.setObjectName("pb_close")

        self.retranslateUi(DialogGraphEnv)
        QtCore.QMetaObject.connectSlotsByName(DialogGraphEnv)

    def retranslateUi(self, DialogGraphEnv):
        _translate = QtCore.QCoreApplication.translate
        DialogGraphEnv.setWindowTitle(_translate("DialogGraphEnv", "Enviroment Graph"))
        self.pb_close.setText(_translate("DialogGraphEnv", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogGraphEnv = QtWidgets.QWidget()
    ui = Ui_DialogGraphEnv()
    ui.setupUi(DialogGraphEnv)
    DialogGraphEnv.show()
    sys.exit(app.exec_())

