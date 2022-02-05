from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QAction, QMdiArea

from dialogs import DialogJournal, DialogProcessInfo


class WindowsController(QObject):
    def __init__(self, parent):
        super(WindowsController, self).__init__()
        self.my_parent = parent
        self.mdiArea = parent.mdiArea
        self.__window_list_menu = parent.menuWindows
        self.__window_list_menu.aboutToShow.connect(self.__window_list_menu_about_to_show)
        # self.mdiArea.windowOrder(QMdiArea.ActivationHistoryOrder)

    def show(self, dialog_, **kwargs):
        """

        :param dialog_:
        :type dialog_:
        :param kwargs:  'multi' to allow multiple copies of window
                        'resize' to allow the window to be resizable
                        'onTop' to keep window on top
        :type kwargs:
        :return:
        :rtype:
        """
        if 'multi' not in kwargs:
            if self.check_opened(dialog_):
                return
        s = self.mdiArea.addSubWindow(dialog_)
        s.setGeometry(50, 0, dialog_.frameGeometry().width() + 15, dialog_.frameGeometry().height() + 30)
        if 'resize' not in kwargs:
            s.setFixedSize(dialog_.frameGeometry().width() + 15, dialog_.frameGeometry().height() + 30)
        if 'onTop' not in kwargs:
            s.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        else:
            s.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        dialog_.sub = s
        dialog_.show()
        # s.show()

    def check_opened(self, dialog_):
        for d in self.mdiArea.subWindowList():
            if d.windowTitle() == dialog_.windowTitle():
                self.mdiArea.setActiveSubWindow(d)
                return True
        return False

    def show_journal(self, area):
        if self.my_parent.area_controller.area_has_process(area):
            self.show(DialogJournal(self.my_parent.area_controller.get_area_process(area), self))

    def show_process_info(self, area):
        if self.my_parent.area_controller.area_has_process(area):
            self.show(DialogProcessInfo(self.my_parent, self.my_parent.area_controller.get_area_process(area)))

    def __window_list_menu_about_to_show(self):
        self.__window_list_menu.clear()
        windows = self.mdiArea.subWindowList()
        index = 1
        for window in windows:
            action = QAction(str(index) + '. ' + window.windowTitle(), self.__window_list_menu)
            action.setProperty('WindowObject', window)
            action.triggered.connect(self.__on_select_window)
            self.__window_list_menu.addAction(action)
            # if index > 0:
            #     self.__window_list_menu.addAction(action)
            index += 1

    def __on_select_window(self):
        action = self.sender()
        window = action.property('WindowObject')
        self.mdiArea.setActiveSubWindow(window)
