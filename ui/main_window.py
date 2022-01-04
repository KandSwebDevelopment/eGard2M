# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1434, 935)
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
        self.menuReports = QtWidgets.QMenu(self.menuProcess)
        self.menuReports.setObjectName("menuReports")
        self.menuFeeding = QtWidgets.QMenu(self.menubar)
        self.menuFeeding.setObjectName("menuFeeding")
        self.menuFeeder_Calibration = QtWidgets.QMenu(self.menuFeeding)
        self.menuFeeder_Calibration.setObjectName("menuFeeder_Calibration")
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
        self.actionSeeds = QtWidgets.QAction(MainWindow)
        self.actionSeeds.setObjectName("actionSeeds")
        self.actionPicker = QtWidgets.QAction(MainWindow)
        self.actionPicker.setObjectName("actionPicker")
        self.actionPreformance = QtWidgets.QAction(MainWindow)
        self.actionPreformance.setObjectName("actionPreformance")
        self.actionFinder = QtWidgets.QAction(MainWindow)
        self.actionFinder.setObjectName("actionFinder")
        self.actionReconnect = QtWidgets.QAction(MainWindow)
        self.actionReconnect.setObjectName("actionReconnect")
        self.actionSystem_Info = QtWidgets.QAction(MainWindow)
        self.actionSystem_Info.setObjectName("actionSystem_Info")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionWizzard = QtWidgets.QAction(MainWindow)
        self.actionWizzard.setObjectName("actionWizzard")
        self.actionManager = QtWidgets.QAction(MainWindow)
        self.actionManager.setObjectName("actionManager")
        self.actionPreformance_2 = QtWidgets.QAction(MainWindow)
        self.actionPreformance_2.setObjectName("actionPreformance_2")
        self.actionJournals = QtWidgets.QAction(MainWindow)
        self.actionJournals.setObjectName("actionJournals")
        self.actionStock = QtWidgets.QAction(MainWindow)
        self.actionStock.setObjectName("actionStock")
        self.actionLow_Stock = QtWidgets.QAction(MainWindow)
        self.actionLow_Stock.setObjectName("actionLow_Stock")
        self.actionCalculator = QtWidgets.QAction(MainWindow)
        self.actionCalculator.setObjectName("actionCalculator")
        self.actionManual_Feed = QtWidgets.QAction(MainWindow)
        self.actionManual_Feed.setObjectName("actionManual_Feed")
        self.actionNutrients = QtWidgets.QAction(MainWindow)
        self.actionNutrients.setObjectName("actionNutrients")
        self.actionRecipes = QtWidgets.QAction(MainWindow)
        self.actionRecipes.setObjectName("actionRecipes")
        self.actionSchedules = QtWidgets.QAction(MainWindow)
        self.actionSchedules.setObjectName("actionSchedules")
        self.actionSync_IO = QtWidgets.QAction(MainWindow)
        self.actionSync_IO.setObjectName("actionSync_IO")
        self.actionReboot_DHT_s = QtWidgets.QAction(MainWindow)
        self.actionReboot_DHT_s.setObjectName("actionReboot_DHT_s")
        self.actionPatterns = QtWidgets.QAction(MainWindow)
        self.actionPatterns.setObjectName("actionPatterns")
        self.actionI_O_VC = QtWidgets.QAction(MainWindow)
        self.actionI_O_VC.setObjectName("actionI_O_VC")
        self.actionEnviroment = QtWidgets.QAction(MainWindow)
        self.actionEnviroment.setObjectName("actionEnviroment")
        self.actionNutrient_Pumps = QtWidgets.QAction(MainWindow)
        self.actionNutrient_Pumps.setObjectName("actionNutrient_Pumps")
        self.actionWater_Tanks = QtWidgets.QAction(MainWindow)
        self.actionWater_Tanks.setObjectName("actionWater_Tanks")
        self.actionMix_Tank = QtWidgets.QAction(MainWindow)
        self.actionMix_Tank.setObjectName("actionMix_Tank")
        self.actionReload = QtWidgets.QAction(MainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionValve_Test = QtWidgets.QAction(MainWindow)
        self.actionValve_Test.setObjectName("actionValve_Test")
        self.actionValve_Test_2 = QtWidgets.QAction(MainWindow)
        self.actionValve_Test_2.setObjectName("actionValve_Test_2")
        self.menuEngineer.addAction(self.actionI_O_Data)
        self.menuEngineer.addAction(self.actionSend_Command)
        self.menuEngineer.addAction(self.actionValve_Test)
        self.menuEngineer.addSeparator()
        self.menuEngineer.addAction(self.actionReboot_DHT_s)
        self.menuEngineer.addAction(self.actionI_O_VC)
        self.menuSystem.addAction(self.actionSettings)
        self.menuSystem.addAction(self.menuEngineer.menuAction())
        self.menuSystem.addAction(self.actionReconnect)
        self.menuSystem.addAction(self.actionSystem_Info)
        self.menuSystem.addAction(self.actionSync_IO)
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
        self.menuReports.addSeparator()
        self.menuReports.addAction(self.actionPreformance_2)
        self.menuReports.addAction(self.actionJournals)
        self.menuProcess.addAction(self.actionWizzard)
        self.menuProcess.addAction(self.actionManager)
        self.menuProcess.addSeparator()
        self.menuProcess.addAction(self.menuReports.menuAction())
        self.menuProcess.addAction(self.actionPatterns)
        self.menuProcess.addSeparator()
        self.menuProcess.addAction(self.actionReload)
        self.menuFeeder_Calibration.addAction(self.actionNutrient_Pumps)
        self.menuFeeder_Calibration.addAction(self.actionWater_Tanks)
        self.menuFeeder_Calibration.addAction(self.actionMix_Tank)
        self.menuFeeder_Calibration.addAction(self.actionValve_Test_2)
        self.menuFeeding.addAction(self.actionStock)
        self.menuFeeding.addAction(self.actionLow_Stock)
        self.menuFeeding.addAction(self.actionCalculator)
        self.menuFeeding.addSeparator()
        self.menuFeeding.addAction(self.actionManual_Feed)
        self.menuFeeding.addSeparator()
        self.menuFeeding.addAction(self.actionNutrients)
        self.menuFeeding.addAction(self.actionRecipes)
        self.menuFeeding.addAction(self.actionSchedules)
        self.menuFeeding.addSeparator()
        self.menuFeeding.addAction(self.menuFeeder_Calibration.menuAction())
        self.menuMaterials.addAction(self.actionSeeds)
        self.menuMaterials.addAction(self.actionPicker)
        self.menuMaterials.addAction(self.actionPreformance)
        self.menuMaterials.addAction(self.actionFinder)
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
        self.menuReports.setTitle(_translate("MainWindow", "Reports"))
        self.menuFeeding.setTitle(_translate("MainWindow", "Feeding"))
        self.menuFeeder_Calibration.setTitle(_translate("MainWindow", "Feeder Calibration"))
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
        self.actionSeeds.setText(_translate("MainWindow", "Seeds"))
        self.actionPicker.setText(_translate("MainWindow", "Picker"))
        self.actionPreformance.setText(_translate("MainWindow", "Preformance"))
        self.actionFinder.setText(_translate("MainWindow", "Finder"))
        self.actionReconnect.setText(_translate("MainWindow", "Reconnect"))
        self.actionSystem_Info.setText(_translate("MainWindow", "System Info"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionWizzard.setText(_translate("MainWindow", "Wizzard"))
        self.actionManager.setText(_translate("MainWindow", "Manager"))
        self.actionPreformance_2.setText(_translate("MainWindow", "Preformance"))
        self.actionJournals.setText(_translate("MainWindow", "Journals"))
        self.actionStock.setText(_translate("MainWindow", "Stock"))
        self.actionLow_Stock.setText(_translate("MainWindow", "Low Stock"))
        self.actionCalculator.setText(_translate("MainWindow", "Calculator"))
        self.actionManual_Feed.setText(_translate("MainWindow", "Manual Feed"))
        self.actionNutrients.setText(_translate("MainWindow", "Nutrients"))
        self.actionRecipes.setText(_translate("MainWindow", "Recipes"))
        self.actionSchedules.setText(_translate("MainWindow", "Schedules"))
        self.actionSync_IO.setText(_translate("MainWindow", "Sync IO"))
        self.actionReboot_DHT_s.setText(_translate("MainWindow", "Reboot DHT\'s"))
        self.actionPatterns.setText(_translate("MainWindow", "Patterns"))
        self.actionI_O_VC.setText(_translate("MainWindow", "I/O VC"))
        self.actionEnviroment.setText(_translate("MainWindow", "Enviroment"))
        self.actionNutrient_Pumps.setText(_translate("MainWindow", "Nutrient Pumps"))
        self.actionWater_Tanks.setText(_translate("MainWindow", "Water Tanks"))
        self.actionMix_Tank.setText(_translate("MainWindow", "Mix Tank"))
        self.actionReload.setText(_translate("MainWindow", "Reload"))
        self.actionValve_Test.setText(_translate("MainWindow", "Valve Test"))
        self.actionValve_Test_2.setText(_translate("MainWindow", "Valve Test"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

