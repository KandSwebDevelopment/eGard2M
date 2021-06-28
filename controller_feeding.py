import collections
from datetime import datetime, timedelta

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

from class_feed import FeedClass
from defines import *


def list_to_str(items) -> str:
    i = ""
    for p in range(1, len(items) + 1):
        i += str(p) + ","
    return i[:len(i) - 1]      # Remove last comma


class FeedControl(QThread):
    area_days = ...  # type: list[int]
    update_status_feeder = pyqtSignal(int)
    update_status_nutrients = pyqtSignal(int)
    sig1 = pyqtSignal(str)
    fault = pyqtSignal(int, int, int)  # Fault source code, Fault code, tank number

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.my_parent = parent
        self.db = self.my_parent.db
        self.feeds = collections.defaultdict(FeedClass)
        self.feed_mode = int(self.db.get_config(CFT_FEEDER, "mode", 1))  # 1=Manual, 2=Semi auto, 3=Full auto
        self.feed_time = self.db.get_config(CFT_FEEDER, "feed time", "21:00")
        self.feed_time_tolerance = int(self.db.get_config(CFT_PROCESS, "feed time tolerance", 4))
        self.log_txt = ""
        self.start_up()

    def start_up(self):
        for area in range(1, 3):
            p = self.my_parent.area_controller.get_area_process(area)
            if p != 0:
                self.feeds[area] = FeedClass(self)
                self.feeds[area].load(area, p.pattern_id, p.current_stage, p.stage_days_elapsed, p.stages_max,
                                      self.my_parent.area_controller.get_area_items(area))
                self.feeds[area].load_mixes()

    def days_till_feed(self, area):
        return self.feeds[area].get_days_till_feed()

    def feed_due_today(self):
        """ Returns true if either area is due today"""
        for f in self.feeds:
            if f.nfd is not None and f.nfd.date() == datetime.now().date():
                return True
        return False

    def get_recipe_status(self, area):
        return self.feeds[area].r_status

    def get_feed_mode(self, area):
        return 1

    def get_recipe_days_remaining(self, area):
        return self.feeds[area].get_recipe_days_remaining()

    def get_feeds_remaining(self, area):
        return self.feeds[area].get_feeds_remaining()

    def get_feed_frequency(self, area):
        return self.feeds[area].get_feed_frequency()

    def get_next_feed_date(self, area):
        return self.feeds[area].nfd

    def get_mix_count(self, area):
        return self.feeds[area].get_mix_count()

    def new_day(self):
        for a in range(1, 3):
            self.feeds[a].new_day()

    def feed(self, area, f_date=None):
        if not self.my_parent.area_controller.area_has_process(area):
            return
        mixes = self.feeds[area].get_mixes()
        date_done = datetime.now()
        if self.get_feed_mode(area) == 1:  # Manual
            # Only display question if manual feed
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Confirm Feed")
            if f_date is None:
                dtt = self.get_next_feed_date(area)
                ft = self.feed_time.split(":")
                dt = dtt.replace(hour=int(ft[0]), minute=int(ft[1]))
            else:
                dt = f_date
            if datetime.now() > (dt + timedelta(hours=self.feed_time_tolerance)):
                action_flag = 1  # 0= On time , 2 = Early, 1 = Late
            elif datetime.now() < (dt - timedelta(hours=self.feed_time_tolerance)):
                action_flag = 2
            else:
                action_flag = 0
            mixes_txt = ""
            if len(mixes) > 1:
                mixes_txt = "<br><b>This feed has {} mixes.<br>DO NOT proceed unless all have been done</b>".\
                    format(len(mixes))
            if action_flag == 0:
                msg.setWindowTitle("Confirm Feed Completed")
                msg.setText("Confirm this feed has been completed" + mixes_txt)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setDefaultButton(QMessageBox.No)
                ret_val = msg.exec_()
                if ret_val == QMessageBox.No:
                    return
            elif action_flag == 1:
                msg.setWindowTitle("Confirm LATE Feed Completed")
                msg.setText("Confirm when feed was completed")
                msg.setInformativeText("This feed was due on " +
                                       datetime.strftime(dt, "%d-%m-%y") +
                                       ". If it was done then click Yes<br>If it was only done today click No " + mixes_txt)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Cancel)
                ret_val = msg.exec_()
                if ret_val == QMessageBox.Yes:
                    # print("Update with original date")
                    date_done = dt
                elif ret_val == QMessageBox.No:
                    date_done = datetime.now()
            elif action_flag == 2:
                msg.setWindowTitle("Confirm EARLY Feed Completed")
                msg.setText("Confirm this feed has been completed")
                msg.setInformativeText(
                    "This feed is Not due until " + datetime.strftime(dt, "%d-%m-%y") +
                    ". <br>Has it been done " + mixes_txt)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setDefaultButton(QMessageBox.No)
                ret_val = msg.exec_()
                if ret_val == QMessageBox.No:
                    return

        # Do for all modes
        self.feeds[area].set_last_feed_date(date_done)
        self.log_txt = "{}      Feed    {} Mix{}  Area: {}   Mode: {}\r".\
            format(datetime.now().strftime('%d %b %y %H:%M'), len(mixes), "" if len(mixes) == 1 else "es", area,
                   self.get_feed_mode(area))

        if self.get_feed_mode(area) == 1:  # Manual
            self.deduct_fed_feed(area)
        else:  # Semi auto and auto
            if self.my_parent.mode == MASTER:
                pass
        # save feed details to the log
        self.log_txt += "\r\n"
        # self.my_parent.logger.save_feed(self.my_parent.area_controller.get_area_pid(), self.log_txt)
        self.feeds[area].cycles_reduce()
        self.feeds[area].get_recipe_status()
        # self._check_feed_due_today()
        # self.my_parent.lbl_water_required.setText(str(self.get_next_water_required()))

        # self.my_parent.process_from_location(area).load_feed_date()

    def deduct_fed_feed(self, area):
        """ Deducts the nutrients used by all the mixes in this feed from stock levels, also builds
            part of the feed log"""
        mixes = self.feeds[area].get_mixes()
        for mix in mixes:
            items_str = list_to_str(mixes[mix]['items'])
            self.log_txt += "Mix Number {} for {} plants ({}) at {}L each. Mix total {}L\r".\
                format(mix, len(mixes[mix]['items']), items_str, mixes[mix]['lpp'], mixes[mix]['water total'])
            if mixes[mix]['recipe'] == WATER_ONLY_IDX:
                return
            for item in mixes[mix]['recipe']:
                if item != WATER_ONLY_IDX:
                    mls = item[1] * mixes[mix]['lpp'] * len(mixes[mix]['items'])
                    # self.my_parent.feeder.deduct_nutrient(item, mls)
                    if item[0] == WATER_ONLY_IDX:
                        nut = WATER_ONLY
                    else:
                        nut = self.db.execute_single('SELECT name FROM {} WHERE id = {}'.
                                                     format(DB_NUTRIENTS_NAMES, item[0]))
                    self.log_txt += "{}: Mix total {}mls   {}mls per plant.\r".format(nut, mls, item[1])
                else:
                    self.log_txt += "Water only\r"
        # self.my_parent.feeder.check_pot_levels()
        # self.my_parent.feeder.check_nutrient_levels()

