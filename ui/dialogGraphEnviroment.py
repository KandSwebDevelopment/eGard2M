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
        DialogGraphEnv.resize(1202, 499)
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogGraphEnv.setFont(font)
        self.cb_logs = QtWidgets.QComboBox(DialogGraphEnv)
        self.cb_logs.setGeometry(QtCore.QRect(20, 20, 201, 22))
        self.cb_logs.setObjectName("cb_logs")
        self.pb_close = QtWidgets.QPushButton(DialogGraphEnv)
        self.pb_close.setGeometry(QtCore.QRect(1090, 20, 75, 23))
        self.pb_close.setObjectName("pb_close")
        self.tabWidget = QtWidgets.QTabWidget(DialogGraphEnv)
        self.tabWidget.setGeometry(QtCore.QRect(40, 60, 1141, 421))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.wg_graph_1 = QtWidgets.QWidget(self.tab)
        self.wg_graph_1.setGeometry(QtCore.QRect(10, 10, 1121, 371))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_graph_1.sizePolicy().hasHeightForWidth())
        self.wg_graph_1.setSizePolicy(sizePolicy)
        self.wg_graph_1.setObjectName("wg_graph_1")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame = QtWidgets.QFrame(self.tab_2)
        self.frame.setGeometry(QtCore.QRect(30, 20, 441, 241))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.tabWidget.addTab(self.tab_2, "")
        self.temp_1_1 = QtWidgets.QCheckBox(DialogGraphEnv)
        self.temp_1_1.setGeometry(QtCore.QRect(270, 20, 111, 17))
        self.temp_1_1.setObjectName("temp_1_1")
        self.temp_1_2 = QtWidgets.QCheckBox(DialogGraphEnv)
        self.temp_1_2.setGeometry(QtCore.QRect(270, 60, 111, 17))
        self.temp_1_2.setObjectName("temp_1_2")
        self.temp_1_3 = QtWidgets.QCheckBox(DialogGraphEnv)
        self.temp_1_3.setGeometry(QtCore.QRect(270, 40, 111, 17))
        self.temp_1_3.setObjectName("temp_1_3")
        self.temp_1_4 = QtWidgets.QCheckBox(DialogGraphEnv)
        self.temp_1_4.setGeometry(QtCore.QRect(420, 20, 111, 17))
        self.temp_1_4.setObjectName("temp_1_4")

        self.retranslateUi(DialogGraphEnv)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DialogGraphEnv)

    def retranslateUi(self, DialogGraphEnv):
        _translate = QtCore.QCoreApplication.translate
        DialogGraphEnv.setWindowTitle(_translate("DialogGraphEnv", "Enviroment Graph"))
        self.pb_close.setText(_translate("DialogGraphEnv", "Close"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("DialogGraphEnv", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("DialogGraphEnv", "Tab 2"))
        self.temp_1_1.setText(_translate("DialogGraphEnv", "Temperature"))
        self.temp_1_2.setText(_translate("DialogGraphEnv", "Root"))
        self.temp_1_3.setText(_translate("DialogGraphEnv", "Canopy"))
        self.temp_1_4.setText(_translate("DialogGraphEnv", "Temperature"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogGraphEnv = QtWidgets.QWidget()
    ui = Ui_DialogGraphEnv()
    ui.setupUi(DialogGraphEnv)
    DialogGraphEnv.show()
    sys.exit(app.exec_())

