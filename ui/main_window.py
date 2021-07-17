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
        MainWindow.resize(1434, 847)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setEnabled(True)
        self.mdiArea.setObjectName("mdiArea")
        self.horizontalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1434, 21))
        self.menubar.setObjectName("menubar")
        self.menuSystem = QtWidgets.QMenu(self.menubar)
        self.menuSystem.setObjectName("menuSystem")
        self.menuEngineer = QtWidgets.QMenu(self.menuSystem)
        self.menuEngineer.setObjectName("menuEngineer")
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
        self.actionI_O_Data = QtWidgets.QAction(MainWindow)
        self.actionI_O_Data.setObjectName("actionI_O_Data")
        self.actionSend_Command = QtWidgets.QAction(MainWindow)
        self.actionSend_Command.setObjectName("actionSend_Command")
        self.actionCounter = QtWidgets.QAction(MainWindow)
        self.actionCounter.setObjectName("actionCounter")
        self.actionInternal = QtWidgets.QAction(MainWindow)
        self.actionInternal.setObjectName("actionInternal")
        self.actionStorage = QtWidgets.QAction(MainWindow)
        self.actionStorage.setObjectName("actionStorage")
        self.actionScales = QtWidgets.QAction(MainWindow)
        self.actionScales.setObjectName("actionScales")
        self.actionReconcilation = QtWidgets.QAction(MainWindow)
        self.actionReconcilation.setObjectName("actionReconcilation")
        self.actionLogs = QtWidgets.QAction(MainWindow)
        self.actionLogs.setObjectName("actionLogs")
        self.actionReport = QtWidgets.QAction(MainWindow)
        self.actionReport.setObjectName("actionReport")
        self.actionLoading = QtWidgets.QAction(MainWindow)
        self.actionLoading.setObjectName("actionLoading")
        self.actionOverview = QtWidgets.QAction(MainWindow)
        self.actionOverview.setObjectName("actionOverview")
        self.menuEngineer.addAction(self.actionI_O_Data)
        self.menuEngineer.addAction(self.actionSend_Command)
        self.menuSystem.addAction(self.menuEngineer.menuAction())
        self.menuDispatch.addAction(self.actionCounter)
        self.menuDispatch.addAction(self.actionInternal)
        self.menuDispatch.addAction(self.actionOverview)
        self.menuDispatch.addSeparator()
        self.menuDispatch.addAction(self.actionStorage)
        self.menuDispatch.addAction(self.actionScales)
        self.menuDispatch.addAction(self.actionReconcilation)
        self.menuDispatch.addSeparator()
        self.menuDispatch.addAction(self.actionLoading)
        self.menuDispatch.addSeparator()
        self.menuDispatch.addAction(self.actionLogs)
        self.menuDispatch.addAction(self.actionReport)
        self.menuDispatch.addSeparator()
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
        self.menuSystem.setTitle(_translate("MainWindow", "System"))
        self.menuEngineer.setTitle(_translate("MainWindow", "Engineer"))
        self.menuDispatch.setTitle(_translate("MainWindow", "Dispatch"))
        self.menuProcess.setTitle(_translate("MainWindow", "Process"))
        self.menuFeeding.setTitle(_translate("MainWindow", "Feeding"))
        self.menuMaterials.setTitle(_translate("MainWindow", "Materials"))
        self.menuModules.setTitle(_translate("MainWindow", "Modules"))
        self.menuWindows.setTitle(_translate("MainWindow", "Windows"))
        self.actionCascade.setText(_translate("MainWindow", "Cascade"))
        self.actionClose_All.setText(_translate("MainWindow", "Close All"))
        self.actionI_O_Data.setText(_translate("MainWindow", "I/O Data"))
        self.actionSend_Command.setText(_translate("MainWindow", "Send Command"))
        self.actionCounter.setText(_translate("MainWindow", "Counter"))
        self.actionInternal.setText(_translate("MainWindow", "Internal"))
        self.actionStorage.setText(_translate("MainWindow", "Storage"))
        self.actionScales.setText(_translate("MainWindow", "Scales"))
        self.actionReconcilation.setText(_translate("MainWindow", "Reconciliation"))
        self.actionLogs.setText(_translate("MainWindow", "Logs"))
        self.actionReport.setText(_translate("MainWindow", "Report"))
        self.actionLoading.setText(_translate("MainWindow", "Loading"))
        self.actionOverview.setText(_translate("MainWindow", "Overview"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

