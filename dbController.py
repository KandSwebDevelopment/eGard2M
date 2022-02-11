import os
import pipes
import threading
from sqlite3 import OperationalError

from PyQt5.QtCore import QSettings, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox, QComboBox
from datetime import datetime
import mysql.connector
from defines import *


class MysqlDB(QObject):
    backup_finished = pyqtSignal(int, name="backupFinished")    # Silent = True or False

    def __init__(self, parent=None):
        # super(MysqlDB, self).__init__()
        QObject.__init__(self, parent)
        self.main_window = parent
        self.settings = QSettings(FN_SETTINGS, QSettings.IniFormat)
        self.master_mode = int(self.settings.value("mode"))  # 1=Master  2=Slave
        if self.master_mode == MASTER:
            self.is_master = True
            self.config_col = "value_m"
        else:
            self.config_col = "value_s"
            self.is_master = False
        self.host = self.settings.value("Database/host")
        self.user = self.settings.value("Database/user")
        self.password = self.settings.value("Database/password")
        self.database = self.settings.value("Database/database")
        self.con = None
        self.cur = None
        self.err_count = 0
        self.is_connected = False
        self.gzip = 0   # Set 1 to zip db backup
        self.silent_backup = 0
        self.backup_finished.connect(self.notify_finished)

    def reconnect(self):
        if self.is_connected:
            self.con.close()
        self.connect_db()
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Database Connection")
        if self.is_connected:
            msg.setIcon(QMessageBox.Information)
            msg.setText("The database has been connected")
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The database has NOT been connected")
        msg.exec_()

    def connect_db(self):
        try:
            self.con = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database,
                autocommit=True
            )
            # self.con.autocommit(True)
            self.cur = self.con.cursor(buffered=True)
            self.is_connected = True
            print("connected to mySql at ", self.host)
            return True
        except Exception as e:
            print("Sql failed to connect")
            print("Error %s:" % e.args[0], e.args[2])
            self.is_connected = False
            return False

    def disconnect(self):
        self.con.close()

    def execute(self, query):
        rows = []
        if self._execute(query):
            rows = self.cur.fetchall()
        return rows

    def execute_one_row(self, query):  # As above but only return one row
        if self._execute(query):
            row = self.cur.fetchone()
            return row
        return []

    def execute_single(self, query):  # As above but only return one item
        if self._execute(query):
            row = self.execute_one_row(query)
            if row is None:
                return None
            try:
                return row[0]
            except Exception as e:
                print(e)

    def execute_write(self, query):  # Use for edits and new
        if self._execute(query):
            self.con.commit()

    def execute_record_exists(self, query):
        r = self.execute(query)
        if r is None or len(r) == 0:
            return False
        return True

    def _execute(self, query):
        if self.cur is None:
            print("NO DB cursor")
            return False
        try:
            self.cur.execute(query)
            return True
        except OperationalError as e:
            if 'MySQL server has gone away' in str(e) or \
                    'Lost connection to MySQL server during query' in str(e):
                self.connect_db()
                if not self.is_connected:
                    print(e.args)
                    return False
                else:
                    try:
                        self.cur.execute(query)
                        return True
                    except Exception as e:
                        print(e.args)
                        return False
            else:
                print(e)
                return False
        except Exception as e:
            print("Unhandled DB ERROR ", e)
            self.connect_db()

    def load_pattern(self, pid=None, name=None):
        if pid is None:
            rows = self.execute("SELECT * FROM " + DB_PATTERN_NAMES + " WHERE id = " + str(pid) + "")
        elif name is not None:
            rows = self.execute("SELECT * FROM " + DB_PATTERN_NAMES + " WHERE name = '" + name + "'")
        else:
            rows = None
        return rows

    def load_stages(self, name):
        rows = self.execute("SELECT * FROM " + DB_PATTERN_NAMES + " WHERE name = '" + name + "'")
        if not rows:
            return rows
        pid = rows[0][0]
        sql = "SELECT * FROM stages WHERE pid = {}".format(pid)
        rows = self.execute(sql)
        return rows

    def name_from_id(self, id_, table_name):
        sql = "SELECT * FROM {} WHERE id = {}".format(table_name, id_)
        return self.execute_one_row(sql)

    def id_from_name(self, name, table_name):
        sql = "SELECT * FROM {} WHERE name = '{}'".format(table_name, name)
        row = self.execute_one_row(sql)
        if row is None:
            return 0
        return row[0]

    def save_temperature_ranges(self, name, lst):  # Saves the 12 temperature values for a range
        row = self.execute_one_row('SELECT * FROM temperatureranges WHERE name = "' + name + '"')
        trid = row[0]
        sql = "SELECT value FROM rangevalues WHERE trid = {}".format(trid)
        rows = self.execute(sql)
        displayid = 0
        isnew = False
        if rows is None:  # Insert
            sql = "INSERT INTO temperatureranges (name) VALUES ('" + name + "')"
            self.execute_write(sql)
            trid = self.cur.lastrowid
            isnew = True
        for value in lst:
            if isnew:
                sql = "INSERT INTO rangevalues (trid, display_id, value) VALUES ({}, {}, {})"
                sql = sql.format(trid, displayid, value)
            else:
                sql = "UPDATE rangevalues SET value = {} WHERE trid = {} AND display_id = {}"
                sql = sql.format(float(value), trid, displayid)
            # print(sql)
            self.cur.execute(sql)
            displayid += 1
        self.con.commit()
        return rows

    def fill_combo(self, combo, table_name, tbl_col, data_col=None, add_none="") -> QComboBox:
        """
        Will fill combo with the data from table name using column tbl col and data col to add data, these are the column numbers not names

        :param combo:       QComboBox to be populated
        :type combo:        QComboBox
        :param table_name:  Table to get data from
        :type table_name:   str
        :param tbl_col:     Table column to get text from
        :type tbl_col:      int
        :param data_col:    Table column to get data param
        :type data_col:     int
        :param add_none:    Add a default ie. ("Select",-1) will add Select with data as -1
        :type add_none:     str
        :return:            The populated combo box
        :rtype:             QComboBox
        """
        rows2 = self.execute("SELECT * FROM " + table_name)
        if add_none != "":
            if data_col is None:
                combo.addItem(add_none[0])
            else:
                combo.addItem(add_none[0], add_none[1])
        for row2 in rows2:
            if data_col is None:
                combo.addItem(row2[tbl_col])
            else:
                combo.addItem(row2[tbl_col], row2[data_col])
        return combo

    def does_exist(self, table_name, column, value):
        """ Checks the table to see if value is in column """
        sql = 'SELECT ' + column + ' FROM ' + table_name + ' WHERE ' + column + ' = "' + str(value) + '"'
        row = self.execute_single(sql)
        if row is None:
            return False
        return row

    # Returns the number of days a standard pattern takes
    def get_pattern_duration(self, pt_id):
        sql = "SELECT SUM(duration) FROM " + DB_STAGE_PATTERNS + " WHERE pid = " + str(pt_id)
        total = self.execute_single(sql)
        return total

    def get_config(self, title, key, default=None) -> str:
        sql = 'SELECT {} FROM {} WHERE title_c = "{}" AND key_c = "{}"'.format(self.config_col, DB_CONFIG, title, key)
        value = self.execute_single(sql)
        if value is None:
            return default
        return value

    def get_config_alt(self, title, key, default=None) -> str:
        if self.master_mode == MASTER:
            config_col = "value_s"
        else:
            config_col = "value_m"
        sql = 'SELECT {} FROM {} WHERE title_c = "{}" AND key_c = "{}"'.format(config_col, DB_CONFIG, title, key)
        value = self.execute_single(sql)
        if value is None:
            return default
        return value

    def set_config(self, title, key, value):
        sql = "UPDATE {} SET {} = '{}' WHERE title_c = '{}' AND key_c = '{}'".\
            format(DB_CONFIG, self.config_col, value, title, key)
        self.execute_write(sql)

    def set_config_alt(self, title, key, value):
        if self.master_mode == MASTER:
            config_col = "value_s"
        else:
            config_col = "value_m"
        sql = "UPDATE {} SET {} = '{}' WHERE title_c = '{}' AND key_c = '{}'".\
            format(DB_CONFIG, config_col, value, title, key)
        self.execute_write(sql)

    def set_config_both(self, title, key, value):
        self.set_config(title, key, value)
        self.set_config_alt(title, key, value)

    @staticmethod
    def reverse_date(date_):
        d = date_
        if d.find("/") > -1:
            if type(date_) is str:
                d = datetime.strptime(date_, "%d/%m/%Y")
            return datetime.strftime(d, "%Y/%m/%d")
        else:
            if type(date_) is str:
                d = datetime.strptime(date_, "%d-%m-%Y")
            return datetime.strftime(d, "%Y-%m-%d")

    def backup(self, gzip=0, silent=False):
        if not silent:
            msg = QMessageBox(QMessageBox.Question, "Confirm", "Do you wish to back up the database", QMessageBox.Yes | QMessageBox.Cancel)
            if msg.exec_() == QMessageBox.Cancel:
                return
        self.gzip = int(gzip)
        self.silent_backup = silent
        th = threading.Thread(target=self._backup)
        th.start()

    def _backup(self):
        backup_path = os.path.expanduser('~/Documents')
        backup_path += "/EGardiner/Backup"

        file_stamp = datetime.now().strftime('%d-%H%M')
        path_stamp = datetime.now().strftime('%Y%m')
        today_path = backup_path + '/' + path_stamp
        backup_name = self.database + "-" + file_stamp + ".sql"
        try:
            os.stat(today_path)
        except:
            os.makedirs(today_path)

        dump_cmd = "mysqldump -h " + self.host + " -u " + self.user + " -p" + self.password + " " \
                   + self.database + " > " + today_path + "/" + backup_name
        print(os.system(dump_cmd))
        if self.gzip:
            gzip_cmd = "gzip " + pipes.quote(today_path) + "/" + backup_name
            print(os.system(gzip_cmd))
        self.backup_finished.emit(self.silent_backup)

    def notify_finished(self, silent):
        if not silent:
            msg = QMessageBox(QMessageBox.Information, "Complete", "The database backup has finished", QMessageBox.Ok)
            msg.exec_()
        self.main_window.msg_sys.add("Database backup complete", MSG_DATABASE_BACKUP, INFO)

    def __del__(self):
        pass
        # self.con.close()  '192.168.0.138'
