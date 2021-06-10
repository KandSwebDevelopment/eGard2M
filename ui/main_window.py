# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/_MDI/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1252, 805)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.horizontalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1252, 21))
        self.menubar.setObjectName("menubar")
        self.menuSystem = QtWidgets.QMenu(self.menubar)
        self.menuSystem.setObjectName("menuSystem")
        self.menuDispatch = QtWidgets.QMenu(self.menubar)
        self.menuDispatch.setObjectName("menuDispatch")
        self.menuProcess = QtWidgets.QMenu(self.menubar)
        self.menuProcess.setObjectName("menuProcess")
        self.menuFeeding = QtWidgets.QMenu(self.menubar)
        self.menuFeeding.setObjectName("menuFeeding")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSystem.menuAction())
        self.menubar.addAction(self.menuDispatch.menuAction())
        self.menubar.addAction(self.menuProcess.menuAction())
        self.menubar.addAction(self.menuFeeding.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuSystem.setTitle(_translate("MainWindow", "System"))
        self.menuDispatch.setTitle(_translate("MainWindow", "Dispatch"))
        self.menuProcess.setTitle(_translate("MainWindow", "Process"))
        self.menuFeeding.setTitle(_translate("MainWindow", "Feeding"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

