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
        self.mdiArea.setEnabled(True)
        self.mdiArea.setObjectName("mdiArea")
        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("subwindow")
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
        self.menuMaterials = QtWidgets.QMenu(self.menubar)
        self.menuMaterials.setObjectName("menuMaterials")
        self.menuModules = QtWidgets.QMenu(self.menubar)
        self.menuModules.setObjectName("menuModules")
        self.menuWindows = QtWidgets.QMenu(self.menubar)
        self.menuWindows.setObjectName("menuWindows")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCascade = QtWidgets.QAction(MainWindow)
        self.actionCascade.setObjectName("actionCascade")
        self.actionClose_All = QtWidgets.QAction(MainWindow)
        self.actionClose_All.setObjectName("actionClose_All")
        self.menuWindows.addAction(self.actionCascade)
        self.menuWindows.addAction(self.actionClose_All)
        self.menuWindows.addSeparator()
        self.menubar.addAction(self.menuSystem.menuAction())
        self.menubar.addAction(self.menuDispatch.menuAction())
        self.menubar.addAction(self.menuProcess.menuAction())
        self.menubar.addAction(self.menuFeeding.menuAction())
        self.menubar.addAction(self.menuMaterials.menuAction())
        self.menubar.addAction(self.menuModules.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.subwindow.setWindowTitle(_translate("MainWindow", "Main Panel"))
        self.menuSystem.setTitle(_translate("MainWindow", "System"))
        self.menuDispatch.setTitle(_translate("MainWindow", "Dispatch"))
        self.menuProcess.setTitle(_translate("MainWindow", "Process"))
        self.menuFeeding.setTitle(_translate("MainWindow", "Feeding"))
        self.menuMaterials.setTitle(_translate("MainWindow", "Materials"))
        self.menuModules.setTitle(_translate("MainWindow", "Modules"))
        self.menuWindows.setTitle(_translate("MainWindow", "Windows"))
        self.actionCascade.setText(_translate("MainWindow", "Cascade"))
        self.actionClose_All.setText(_translate("MainWindow", "Close All"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

