# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/py/dialogFeedMix.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogFeedMix(object):
    def setupUi(self, DialogFeedMix):
        DialogFeedMix.setObjectName("DialogFeedMix")
        DialogFeedMix.setWindowModality(QtCore.Qt.NonModal)
        DialogFeedMix.resize(440, 540)
        DialogFeedMix.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        DialogFeedMix.setFont(font)
        self.lbl_info = QtWidgets.QLabel(DialogFeedMix)
        self.lbl_info.setGeometry(QtCore.QRect(9, 9, 291, 18))
        self.lbl_info.setText("")
        self.lbl_info.setObjectName("lbl_info")
        self.fr_feed = QtWidgets.QFrame(DialogFeedMix)
        self.fr_feed.setGeometry(QtCore.QRect(10, 70, 421, 421))
        self.fr_feed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fr_feed.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fr_feed.setObjectName("fr_feed")
        self.lw_recipe_1 = QtWidgets.QListWidget(self.fr_feed)
        self.lw_recipe_1.setGeometry(QtCore.QRect(10, 10, 401, 141))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lw_recipe_1.setFont(font)
        self.lw_recipe_1.setObjectName("lw_recipe_1")
        self.te_water_1 = QtWidgets.QTextEdit(self.fr_feed)
        self.te_water_1.setGeometry(QtCore.QRect(10, 230, 401, 31))
        self.te_water_1.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.te_water_1.setObjectName("te_water_1")
        self.groupBox = QtWidgets.QGroupBox(self.fr_feed)
        self.groupBox.setGeometry(QtCore.QRect(10, 270, 401, 51))
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.pb_store_w_1 = QtWidgets.QPushButton(self.groupBox)
        self.pb_store_w_1.setGeometry(QtCore.QRect(270, 25, 70, 27))
        self.pb_store_w_1.setObjectName("pb_store_w_1")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(150, 30, 71, 22))
        self.label_5.setObjectName("label_5")
        self.le_total_1 = QtWidgets.QLineEdit(self.groupBox)
        self.le_total_1.setGeometry(QtCore.QRect(60, 30, 61, 20))
        self.le_total_1.setObjectName("le_total_1")
        self.le_each_1 = QtWidgets.QLineEdit(self.groupBox)
        self.le_each_1.setGeometry(QtCore.QRect(200, 30, 61, 20))
        self.le_each_1.setObjectName("le_each_1")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 30, 61, 18))
        self.label_6.setObjectName("label_6")
        self.pb_reset_water = QtWidgets.QPushButton(self.groupBox)
        self.pb_reset_water.setGeometry(QtCore.QRect(360, 27, 31, 23))
        self.pb_reset_water.setObjectName("pb_reset_water")
        self.groupBox_2 = QtWidgets.QGroupBox(self.fr_feed)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 150, 401, 61))
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.pb_store_n_1 = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_store_n_1.setGeometry(QtCore.QRect(270, 27, 70, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_store_n_1.sizePolicy().hasHeightForWidth())
        self.pb_store_n_1.setSizePolicy(sizePolicy)
        self.pb_store_n_1.setMaximumSize(QtCore.QSize(70, 16777215))
        self.pb_store_n_1.setObjectName("pb_store_n_1")
        self.le_ml_1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_ml_1.setGeometry(QtCore.QRect(160, 30, 51, 20))
        self.le_ml_1.setInputMask("")
        self.le_ml_1.setObjectName("le_ml_1")
        self.cb_nutrients_1 = QtWidgets.QComboBox(self.groupBox_2)
        self.cb_nutrients_1.setGeometry(QtCore.QRect(30, 31, 100, 20))
        self.cb_nutrients_1.setMinimumSize(QtCore.QSize(0, 0))
        self.cb_nutrients_1.setMaximumSize(QtCore.QSize(100, 16777215))
        self.cb_nutrients_1.setObjectName("cb_nutrients_1")
        self.label_24 = QtWidgets.QLabel(self.groupBox_2)
        self.label_24.setGeometry(QtCore.QRect(210, 30, 30, 20))
        self.label_24.setMinimumSize(QtCore.QSize(30, 20))
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.pb_reset_nutrients = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_reset_nutrients.setGeometry(QtCore.QRect(360, 30, 31, 23))
        self.pb_reset_nutrients.setObjectName("pb_reset_nutrients")
        self.groupBox_3 = QtWidgets.QGroupBox(self.fr_feed)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 331, 401, 51))
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.ck_fed_18 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_18.setGeometry(QtCore.QRect(310, 20, 31, 22))
        self.ck_fed_18.setChecked(True)
        self.ck_fed_18.setObjectName("ck_fed_18")
        self.ck_fed_13 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_13.setGeometry(QtCore.QRect(125, 20, 31, 22))
        self.ck_fed_13.setChecked(True)
        self.ck_fed_13.setObjectName("ck_fed_13")
        self.ck_fed_16 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_16.setGeometry(QtCore.QRect(236, 20, 31, 22))
        self.ck_fed_16.setChecked(True)
        self.ck_fed_16.setObjectName("ck_fed_16")
        self.ck_fed_17 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_17.setGeometry(QtCore.QRect(273, 20, 31, 22))
        self.ck_fed_17.setChecked(True)
        self.ck_fed_17.setObjectName("ck_fed_17")
        self.ck_fed_11 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_11.setGeometry(QtCore.QRect(51, 20, 31, 22))
        self.ck_fed_11.setChecked(True)
        self.ck_fed_11.setObjectName("ck_fed_11")
        self.ck_fed_12 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_12.setGeometry(QtCore.QRect(88, 20, 31, 22))
        self.ck_fed_12.setChecked(True)
        self.ck_fed_12.setObjectName("ck_fed_12")
        self.ck_fed_14 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_14.setGeometry(QtCore.QRect(162, 20, 31, 22))
        self.ck_fed_14.setChecked(True)
        self.ck_fed_14.setObjectName("ck_fed_14")
        self.ck_fed_15 = QtWidgets.QCheckBox(self.groupBox_3)
        self.ck_fed_15.setGeometry(QtCore.QRect(199, 20, 31, 22))
        self.ck_fed_15.setChecked(True)
        self.ck_fed_15.setObjectName("ck_fed_15")
        self.label_4 = QtWidgets.QLabel(self.fr_feed)
        self.label_4.setGeometry(QtCore.QRect(10, 390, 141, 18))
        self.label_4.setObjectName("label_4")
        self.cb_feeds = QtWidgets.QComboBox(self.fr_feed)
        self.cb_feeds.setGeometry(QtCore.QRect(90, 390, 69, 22))
        self.cb_feeds.setObjectName("cb_feeds")
        self.pb_delete = QtWidgets.QPushButton(self.fr_feed)
        self.pb_delete.setEnabled(False)
        self.pb_delete.setGeometry(QtCore.QRect(330, 390, 75, 23))
        self.pb_delete.setObjectName("pb_delete")
        self.pb_water_only = QtWidgets.QPushButton(self.fr_feed)
        self.pb_water_only.setGeometry(QtCore.QRect(200, 380, 81, 31))
        self.pb_water_only.setObjectName("pb_water_only")
        self.tw_mixes = QtWidgets.QTabWidget(DialogFeedMix)
        self.tw_mixes.setGeometry(QtCore.QRect(10, 40, 411, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.tw_mixes.setFont(font)
        self.tw_mixes.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tw_mixes.setElideMode(QtCore.Qt.ElideMiddle)
        self.tw_mixes.setDocumentMode(False)
        self.tw_mixes.setTabsClosable(False)
        self.tw_mixes.setObjectName("tw_mixes")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tw_mixes.addTab(self.tab, "")
        self.pb_add = QtWidgets.QPushButton(DialogFeedMix)
        self.pb_add.setGeometry(QtCore.QRect(360, 10, 31, 28))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pb_add.setFont(font)
        self.pb_add.setObjectName("pb_add")
        self.pb_save = QtWidgets.QPushButton(DialogFeedMix)
        self.pb_save.setGeometry(QtCore.QRect(100, 600, 61, 23))
        self.pb_save.setObjectName("pb_save")
        self.frame_3 = QtWidgets.QFrame(DialogFeedMix)
        self.frame_3.setGeometry(QtCore.QRect(510, 730, 401, 51))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.frame = QtWidgets.QFrame(DialogFeedMix)
        self.frame.setGeometry(QtCore.QRect(510, 770, 401, 51))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.label_25 = QtWidgets.QLabel(self.frame)
        self.label_25.setGeometry(QtCore.QRect(-20, 10, 101, 18))
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.label_7 = QtWidgets.QLabel(DialogFeedMix)
        self.label_7.setGeometry(QtCore.QRect(580, 550, 290, 46))
        self.label_7.setObjectName("label_7")
        self.frame_2 = QtWidgets.QFrame(DialogFeedMix)
        self.frame_2.setGeometry(QtCore.QRect(510, 640, 310, 66))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pb_close = QtWidgets.QPushButton(DialogFeedMix)
        self.pb_close.setGeometry(QtCore.QRect(340, 510, 71, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pb_close.setFont(font)
        self.pb_close.setObjectName("pb_close")
        self.lbl_next = QtWidgets.QLabel(DialogFeedMix)
        self.lbl_next.setGeometry(QtCore.QRect(310, 10, 41, 28))
        self.lbl_next.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lbl_next.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_next.setObjectName("lbl_next")
        self.pb_copy = QtWidgets.QPushButton(DialogFeedMix)
        self.pb_copy.setGeometry(QtCore.QRect(400, 10, 31, 28))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pb_copy.setFont(font)
        self.pb_copy.setObjectName("pb_copy")

        self.retranslateUi(DialogFeedMix)
        self.tw_mixes.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DialogFeedMix)
        DialogFeedMix.setTabOrder(self.cb_nutrients_1, self.le_ml_1)
        DialogFeedMix.setTabOrder(self.le_ml_1, self.pb_store_n_1)
        DialogFeedMix.setTabOrder(self.pb_store_n_1, self.le_total_1)
        DialogFeedMix.setTabOrder(self.le_total_1, self.le_each_1)
        DialogFeedMix.setTabOrder(self.le_each_1, self.pb_store_w_1)
        DialogFeedMix.setTabOrder(self.pb_store_w_1, self.lw_recipe_1)

    def retranslateUi(self, DialogFeedMix):
        _translate = QtCore.QCoreApplication.translate
        DialogFeedMix.setWindowTitle(_translate("DialogFeedMix", "Feed Mix"))
        self.groupBox.setTitle(_translate("DialogFeedMix", "Water"))
        self.pb_store_w_1.setText(_translate("DialogFeedMix", "Update"))
        self.label_5.setText(_translate("DialogFeedMix", "Each"))
        self.label_6.setText(_translate("DialogFeedMix", "Total"))
        self.pb_reset_water.setText(_translate("DialogFeedMix", "R"))
        self.groupBox_2.setTitle(_translate("DialogFeedMix", "Nutrients"))
        self.pb_store_n_1.setText(_translate("DialogFeedMix", "Update"))
        self.label_24.setText(_translate("DialogFeedMix", "ml"))
        self.pb_reset_nutrients.setText(_translate("DialogFeedMix", "R"))
        self.groupBox_3.setTitle(_translate("DialogFeedMix", "Items"))
        self.ck_fed_18.setText(_translate("DialogFeedMix", "8"))
        self.ck_fed_13.setText(_translate("DialogFeedMix", "3"))
        self.ck_fed_16.setText(_translate("DialogFeedMix", "6"))
        self.ck_fed_17.setText(_translate("DialogFeedMix", "7"))
        self.ck_fed_11.setText(_translate("DialogFeedMix", "1"))
        self.ck_fed_12.setText(_translate("DialogFeedMix", "2"))
        self.ck_fed_14.setText(_translate("DialogFeedMix", "4"))
        self.ck_fed_15.setText(_translate("DialogFeedMix", "5"))
        self.label_4.setText(_translate("DialogFeedMix", "In use for"))
        self.pb_delete.setText(_translate("DialogFeedMix", "Delete"))
        self.pb_water_only.setText(_translate("DialogFeedMix", "Water Only"))
        self.tw_mixes.setTabText(self.tw_mixes.indexOf(self.tab), _translate("DialogFeedMix", "Feed 1"))
        self.pb_add.setText(_translate("DialogFeedMix", "+"))
        self.pb_save.setText(_translate("DialogFeedMix", "Save"))
        self.label_25.setText(_translate("DialogFeedMix", "Nutrient"))
        self.label_7.setText(_translate("DialogFeedMix", "Fed"))
        self.pb_close.setText(_translate("DialogFeedMix", "Close"))
        self.lbl_next.setText(_translate("DialogFeedMix", "Next"))
        self.pb_copy.setText(_translate("DialogFeedMix", "C"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogFeedMix = QtWidgets.QDialog()
    ui = Ui_DialogFeedMix()
    ui.setupUi(DialogFeedMix)
    DialogFeedMix.show()
    sys.exit(app.exec_())

