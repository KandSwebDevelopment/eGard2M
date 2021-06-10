from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

from ui.main import Ui_Form


class _Main(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.my_parent = args[0]
        self.db = args[0].db
        self.setMinimumSize(1400, 900)
        # self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        # self.setFixedSize(self.width(), self.height())
        # enable custom window hint
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)

        # disable (but not hide) close button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

