import collections
from datetime import timedelta, datetime

from PyQt5.QtCore import QObject, QVariant, Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from defines import *


class MessageSystem(QObject):
    # control: QListWidget

    def __init__(self, parent, c_id):
        super().__init__()
        """ :type parent: MainWindow 
            :type control: QListWidget"""
        self.my_parent = parent
        self.db = self.my_parent.db
        self.control = c_id
        self.control.doubleClicked.connect(self._remove)
        self.auto_remove_list = collections.defaultdict()
        self.ck_timer = QTimer()
        self.ck_timer.setInterval(5000)
        self.ck_timer.timeout.connect(self.check)
        self.load()

    def check(self):
        # pass
        for m in self.auto_remove_list:
            if datetime.now() > self.auto_remove_list[m]['expires']:
                self._delete(m)
                self.load()

    def load(self):
        self.ck_timer.stop()
        self.control.clear()
        sql = 'SELECT mid, message, level, duration, date_added, persistent FROM {} '.format(DB_MESSAGE_SYSTEM)
        rows = self.db.execute(sql)
        for row in rows:
            if row[3] > 0:  # Check if expired
                if (datetime.now() - row[4]).seconds >= row[3]:
                    continue
                self.ck_timer.start()
                self.auto_remove_list[row[0]] = {'expires': datetime.now() + timedelta(seconds=row[3])}
            self._display(row[0], row[1], row[2])

    def add(self, msg, mid, level, **kwargs):
        """
        @param level:
        @type level:
        @param mid:
        @type mid: int
        @param msg:
        @type msg: str
        @param kwargs:
            repeat:1  1 = Will force msg to be added even if it already exists
            duration: 0 = Constant or duration in seconds
            persistent: 1 = Msg can not be removed
        @type kwargs: object
        """
        row = self._get(mid)
        if row is not None:     # msg already in system
            if 'repeat' not in kwargs:
                return
        dur = 0
        if 'duration' in kwargs:
            dur = int(kwargs['duration'])
            self.auto_remove_list[mid] = {'expires': datetime.now() + timedelta(seconds=dur)}
            self.ck_timer.start()
        if 'persistent' in kwargs:
            mid *= -1   # change id to negative to prevent removal
            if self._get(mid) is not None:  # Prevent persistent from being re-added
                return
        self._put(mid, msg, dur, level)
        self._display(mid, msg, level)
        # self.my_parent.coms_interface.relay_send(NWC_MESSAGE)

    def has_msg_id(self, mid):
        sql = 'SELECT mid FROM {} WHERE mid = {} OR mid = {}'.format(DB_MESSAGE_SYSTEM, mid, mid * -1)
        m = self.db.execute_single(sql)
        if m is None:
            return False
        return True

    def _display(self, mid, msg, level):
        font = QFont('Arial', 10)
        bg, fg, sz = self._get_colour(level)
        font.setPointSize(sz)
        lw_item = QListWidgetItem(msg)
        v_item = QVariant(mid)
        lw_item.setBackground(QColor(bg))
        lw_item.setForeground(QColor(fg))
        lw_item.setFont(font)
        lw_item.setData(Qt.UserRole, v_item)
        self.control.insertItem(0, lw_item)

    def _remove(self):
        mid = self.control.currentItem().data(Qt.UserRole)
        if mid is None or mid < 0:
            return
        self.remove(mid)

    def remove(self, mid):
        if self.has_msg_id(mid):
            self._delete(mid)
            self.load()
            self.my_parent.coms_interface.relay_send(NWC_MESSAGE)

    def _get(self, mid):
        """ Query's db and returns message with Id = mid or None"""
        sql = "SELECT duration, date_added FROM {} WHERE mid = {}".format(DB_MESSAGE_SYSTEM, mid)
        r = self.db.execute_one_row(sql)
        return r

    def _put(self, mid, msg, duration, level):
        """ Stores the message in the db"""
        sql = 'INSERT INTO {} (mid, message, duration, level, date_added) VALUES ({}, "{}", {}, {}, "{}")'.\
            format(DB_MESSAGE_SYSTEM, mid, msg, duration, level, datetime.now())
        self.db.execute_write(sql)

    def _delete(self, mid):
        sql = 'DELETE FROM {} WHERE mid = {} OR mid = {} LIMIT 1'.format(DB_MESSAGE_SYSTEM, mid, mid * -1)
        self.db.execute_write(sql)

    @staticmethod
    def _get_colour(level):
        bg = INFO_BG
        fg = INFO_FG
        sz = 10
        if level == CRITICAL:
            bg = CRITICAL_BG_QT
            fg = CRITICAL_FG_QT
            sz = 14
        elif level == ERROR:
            bg = ERROR_BG
            fg = ERROR_FG
            sz = 12
        elif level == WARNING:
            bg = WARNING_BG
            fg = WARNING_FG
            sz = 11
        elif level == INFO:
            bg = INFO_BG
            fg = INFO_FG
            sz = 10
        return bg, fg, sz
