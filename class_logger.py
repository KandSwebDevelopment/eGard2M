import os
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject
from defines import *


class Logger(QObject):

    def __init__(self, parent):
        super(Logger, self).__init__()
        # super().__init__()
        self.my_parent = parent
        self.db = parent.db
        self.today_name = datetime.strftime(datetime.now(), "%Y%m%d")
        self.data_filename = self.today_name + ".cvs"
        self.output_filename = self.today_name + ".opd"
        self.new_line = '\n'    # os.linesep
        self.fan_file = ""
        self.available = True       # Set False if unable to connect to file system
        doc_folder = self.db.get_config(CFT_LOGGER, "doc path")
        try:
            self.doc_folder = doc_folder
            if not os.path.exists(self.doc_folder):
                os.makedirs(self.doc_folder)
            self.log_path = self.doc_folder + "\\Logs"
            self.events_path = self.doc_folder + "\\Events"
            self.journal_path = self.doc_folder + "\\Journals"
            self.system_path = self.doc_folder + "\\System"
            self.feeding_path = self.doc_folder + "\\Feeding"
            self.dispatch_path = self.doc_folder + "\\Dispatch"

            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)
            if not os.path.exists(self.events_path):
                os.makedirs(self.events_path)
            if not os.path.exists(self.journal_path):
                os.makedirs(self.journal_path)
            if not os.path.exists(self.feeding_path):
                os.makedirs(self.feeding_path)
            if not os.path.exists(self.dispatch_path):
                os.makedirs(self.dispatch_path)
            if not os.path.exists(self.system_path):
                os.makedirs(self.system_path)
            # self.my_parent.msg_sys.remove(MSG_1 * -1)
        except Exception as e:  # OSError
            self.available = False
            self.my_parent.msg_sys.add("Logging unavailable", MSG_1, WARNING, persistent=1)
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            if self.my_parent.master_mode == MASTER:
                msg.setText("Unable to connect to the file system. <br><b>All logging will be disabled</b>"
                            "Check the logging settings")
                msg.setInformativeText("Check the logging settings")
            else:
                msg.setText("Unable to connect to the file system. <br><b>All logging will be disabled</b>")
                msg.setInformativeText("Check the Master is running and the logging settings")
            msg.setWindowTitle("File System Error")
            # msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        self.log_file = self.log_path + "\\" + self.data_filename
        self.events_file_template = self.events_path + "\\events_{}.event"  # Process id inserted
        self.journal_file_template = self.journal_path + "\\Journal_{}.jrn"  # Process id inserted
        self.system_file_template = self.system_path + "\\system.log"
        self.feeding_file_template = self.feeding_path + "\\Feeding{}.fed"  # Process id inserted
        self.dispatch_counter_file_template = self.dispatch_path + "\\Counter file {}.dsp"  # year-month inserted

    def save(self):
        pass

    def save_fan_log(self, data):
        if not self.available:
            return
        self.fan_file = self.log_path + "\\{}.fan".format(self.today_name)
        f = open(self.fan_file, "a")
        text = datetime.strftime(datetime.now(), "%H:%M, ") + data + self.new_line
        f.write(text)
        f.close()

    def save_fan_tune_log(self, data):
        if not self.available:
            return
        f = open(self.log_path + "\\{}.ftl".format(self.today_name), "a")
        text = datetime.strftime(datetime.now(), "%H:%M, ") + data + self.new_line
        f.write(text)
        f.close()

    def save_power_log(self, data):
        if not self.available:
            return
        f = open(self.log_path + "\\{}.pwr".format(self.today_name), "a")
        text = datetime.strftime(datetime.now(), "%H:%M, ") + data + self.new_line
        f.write(text)
        f.close()

    def get_fan_log(self, fan):
        """
        Open and read a fan log file into a list
        @param fan: Can be 1 or 2 and it will attempt to open today's log for that fan
                    Can be a full file path and file name and it will open that log
        @type fan:
        @return: A list where each entry will be a string of comma separated data
        @rtype:
        """
        if not self.available:
            return
        if type(fan) == int:
            log = self.system_path + "\\fan_{}_{}.txt".format(fan, self.today_name)
        else:
            log = fan
        try:
            f = open(log)
            text = f.read()
            f.close()
        except FileNotFoundError:
            return ""
        entries = text.split("\n")
        data = []
        for line in entries:
            if line != "":
                data.append(line)
        return data

    def save_log(self, data):
        """Log file  contains all sensor readings etc for graphs"""
        if not self.available:
            return
        f = open(self.log_file, "a")
        s = ""
        # for d in data:
        #     s += d + ", "
        # s = s[0: len(s) - 2]
        text = datetime.strftime(datetime.now(), "%H:%M, ") + data + self.new_line
        # print(text)
        f.write(text)
        f.close()

    def save_output_log(self, data):
        """Log file  contains all output positions for graphs"""
        if not self.available:
            return
        f = open(self.log_path + "\\" + self.output_filename, "a")
        text = datetime.strftime(datetime.now(), "%H:%M, ") + data + self.new_line
        # print(text)
        f.write(text)
        f.close()

    def save_system(self, data):  # Log file  contains all system events
        if not self.available:
            return
        f = open(self.system_file_template, "a")
        text = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S ") + data + self.new_line
        # print(text)
        f.write(text)
        f.close()

    def save_feed(self, process_id, log):  # Log file  contains all feeds for a process
        if not self.available:
            return
        f = open(self.feeding_file_template.format(process_id), "a")
        # print(text)
        f.write(log)
        f.close()

    def save_event(self, pid, data, stage):  # Event file contains, stage changes, process adjustments etc
        if not self.available:
            return
        name = self.events_file_template.format(pid)
        f = open(name, "a")
        text = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S ") + " Stage:" + str(
            stage) + " - " + data + self.new_line
        print("Event log :- ", text)
        f.write(text)
        f.close()

    def new_day(self):
        if not self.available:
            return
        self.today_name = datetime.strftime(datetime.now(), "%Y%m%d")
        self.data_filename = self.today_name + ".cvs"
        self.output_filename = self.today_name + ".opd"
        self.log_file = self.log_path + "\\" + self.data_filename

    def save_dispatch_counter(self, client, amount, jar, strain_name, strain_id, weight_r, weight_a):
        """
        Log dispatcher counter event
        :param strain_id: Strain ID
        :type strain_id: int
        :param strain_name: Strain Name
        :type strain_name: str
        :param weight_a: Actual weight
        :type weight_a: float
        :param client: Client receiving
        :type client: str
        :param amount: Amount in pounds
        :type amount: str
        :param jar: From Jar
        :type jar: str
        :param weight_r: Required weight
        :type weight_r: float
        """
        if not self.available:
            return
        log = self.dispatch_counter_file_template.format(datetime.strftime(datetime.now(), "%Y-%m"))
        f = open(log, "a")
        text = datetime.strftime(datetime.now(), "%a %d/%m/%y  %H:%M, ") \
            + client + ", " + amount + ", " + jar + ", " + strain_name + ", " + str(strain_id) + ", " \
            + str(weight_r) + ", " + str(weight_a) + ", " + str(round(weight_a - weight_r, 1)) + self.new_line
        f.write(text)
        f.close()

    def get_log_list(self, log) -> list:
        if not self.available:
            return []
        p = ""
        if log == LOG_DATA:
            p = self.log_path
        elif log == LOG_EVENTS:
            p = self.events_path
        elif log == LOG_JOURNAL:
            p = self.journal_path
        elif log == LOG_SYSTEM:
            p = self.system_path
        elif log == LOG_FEED:
            p = self.feeding_path
        elif log == LOG_DISPATCH:
            p = self.dispatch_path
        elif log == LOG_ACCESS:
            p = ""
        if p == "":
            return []
        files = os.listdir(p)
        return files

    def get_log(self, log_type, log_file) -> str:
        if not self.available:
            return ""
        p = ""
        if log_type == LOG_DATA:
            p = self.log_path
        elif log_type == LOG_EVENTS:
            p = self.events_path
        elif log_type == LOG_JOURNAL:
            p = self.journal_path
        elif log_type == LOG_SYSTEM:
            p = self.system_path
        elif log_type == LOG_FEED:
            p = self.feeding_path
        elif log_type == LOG_DISPATCH:
            p = self.dispatch_path
        elif log_type == LOG_ACCESS:
            p = ""
        if p == "" or log_file is None or log_file == 0:
            return ""
        log = p + "\\" + log_file
        try:
            f = open(log)
            text = f.read()
            f.close()
        except FileNotFoundError:
            return "File Missing " + log
        if text == "":
            return "There as no entries in this journal"
        entries = text.split("\n")
        return entries

    def get_log_contents(self, log_type, log_file) -> str:
        if not self.available:
            return ""
        p = ""
        if log_type == LOG_DATA:
            p = self.log_path
        elif log_type == LOG_EVENTS:
            p = self.events_path
        elif log_type == LOG_JOURNAL:
            p = self.journal_path
        elif log_type == LOG_SYSTEM:
            p = self.system_path
        elif log_type == LOG_FEED:
            p = self.feeding_path
        elif log_type == LOG_DISPATCH:
            p = self.dispatch_path
        elif log_type == LOG_ACCESS:
            p = ""
        if p == "" or log_file is None or log_file == 0:
            return ""
        log = p + "\\" + log_file
        try:
            f = open(log)
            text = f.read()
            f.close()
        except FileNotFoundError:
            return "File Missing " + log
        if text == "":
            return "There as no entries in this journal"
        entries = text.split("\n")
        result = ''    # '<table  cellpadding = "5"  border = "1" cellspacing = "0">'
        for line in entries:
            result += line + '<br>'
            # if line != "":
            #     parts = line.split(",")
            #     cols = len(parts)
            #     result += "<tr>"
            #     for x in range(0, cols):
            #         result += "<td>" + parts[x] + "</td>"
            #     result += "</tr>"
        # result += "</table>"
        return result
