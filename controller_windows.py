from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QAction

from dialogs import DialogJournal


class WindowsController(QObject):
    def __init__(self, parent):
        super(WindowsController, self).__init__()
        self.my_parent = parent
        self.mdiArea = parent.mdiArea
        self.__window_list_menu = parent.menuWindows
        self.__window_list_menu.aboutToShow.connect(self.__window_list_menu_about_to_show)

    def show(self, dialog_, **kwargs):
        s = self.mdiArea.addSubWindow(dialog_)
        s.setGeometry(50, 50, dialog_.frameGeometry().width() + 15, dialog_.frameGeometry().height() + 30)
        # s.setFixedSize(dialog_.frameGeometry().width() + 15, dialog_.frameGeometry().height() + 30)
        s.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        dialog_.sub = s
        dialog_.show()

    def show_journal(self, area):
        if self.my_parent.area_controller.area_has_process(area):
            self.show(DialogJournal(self.my_parent.area_controller.get_area_process(area), self))

    def __window_list_menu_about_to_show(self):
        self.__window_list_menu.clear()
        windows = self.mdiArea.subWindowList()
        index = 1
        for window in windows:
            action = QAction(str(index) + '. ' + window.windowTitle(), self.__window_list_menu)
            action.setProperty('WindowObject', window)
            action.triggered.connect(self.__on_select_window)
            self.__window_list_menu.addAction(action)
            index += 1

    def __on_select_window(self):
        action = self.sender()
        window = action.property('WindowObject')
        self.mdiArea.setActiveSubWindow(window)
