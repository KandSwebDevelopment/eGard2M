import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QMdiArea, QMdiSubWindow, QDialog, QTextEdit, QAction, QWidget, \
    QMessageBox

from dbController import MysqlDB
from functions import multi_status_bar
from ui.main_window import Ui_MainWindow
from show_functions import *
from dialogs import _Main
from controller_areas import AreaController
from message_system import MessageSystem


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(Application)

        self.db = MysqlDB()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        if not self.db.connect_db():
            msg.setText("Can not connect to main data Base Server, will try localhost")
            msg.setWindowTitle("Unable to Data Base Server")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            # app.quit()
        multi_status_bar(self)
        self.win = _Main(self)
        sub = self.mdiArea.addSubWindow(self.win)
        self.win.show()
        self.ControlBox = False
        self.TopLevel = False

        show_main(self)

        self.msg_sys = MessageSystem(self, self.win.listWidget)
        self.area_controller = AreaController(self)

    def update_stage_buttons(self, area):
        items = self.area_controller.get_area_items(area)
        if len(items) != 0:
            for i in items:
                getattr(self, "pb_pm_%i" % i).setText(str(i))
                getattr(self, "pb_pm_%i" % i).setToolTip("")
        else:  # No process in area 2
            for i in range(1, 9):
                if i not in items:
                    getattr(self, "pb_pm_%i" % i).setText("")
                    getattr(self, "pb_pm_%i" % i).setToolTip("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Application = QMainWindow()
    ui = MainWindow()
    Application.show()
    sys.exit(app.exec_())

