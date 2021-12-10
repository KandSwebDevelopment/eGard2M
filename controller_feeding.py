import collections
from datetime import datetime, timedelta

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
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
        self.main_window = parent
        self.db = self.main_window.db
        self.feeds = collections.defaultdict(FeedClass)
        self.nutrients = collections.defaultdict()
        self.feed_mode = int(self.db.get_config(CFT_FEEDER, "mode", 1))  # 1=Manual, 2=Semi auto, 3=Full auto
        self.feed_time = self.db.get_config(CFT_FEEDER, "feed time", "21:00")
        self.feed_time_tolerance = int(self.db.get_config(CFT_PROCESS, "feed time tolerance", 4))
        self.log_txt = ""
        self.mute = False

        self.timer_mute = QTimer(self)
        self.timer_mute.timeout.connect(self.mute_timeout)

        rows = self.db.execute("SELECT id, name FROM " + DB_NUTRIENTS_NAMES)
        for row in rows:
            self.nutrients[row[0]] = row[1]

        self.start_up()

    def start_up(self):
        for area in range(1, 3):
            p = self.main_window.area_controller.get_area_process(area)
            if p != 0:
                self.feeds[area] = FeedClass(self)
                self.feeds[area].load(area, p.pattern_id, p.current_stage, p.stage_days_elapsed, p.stages_max,
                                      self.main_window.area_controller.get_area_items(area))
                self.feeds[area].qty_org = p.quantity_org
                self.feeds[area].load_mixes()

    def reload_area(self, area):
        """ Reloads the feed data for the area. """
        p = self.main_window.area_controller.get_area_process(area)
        if p != 0:
            self.feeds[area].load(area, p.pattern_id, p.current_stage, p.stage_days_elapsed, p.stages_max,
                                  self.main_window.area_controller.get_area_items(area))
            self.feeds[area].qty_org = p.quantity_org
            self.feeds[area].load_mixes()

    def mute_timeout(self):
        self.mute = False
        self.timer_mute.stop()

    def mute_start(self, minutes):
        self.mute = True
        self.timer_mute.start(minutes * 60000)

    def set_feed_time(self, feed_time):
        """

        :type feed_time: str
        """
        if feed_time == self.feed_time:
            return
        self.feed_time = feed_time
        self.db.set_config_both(CFT_FEEDER, "feed time", feed_time)

    def days_till_feed(self, area):
        if area in self.feeds:
            return self.feeds[area].get_days_till_feed()
        else:
            return 101

    def feed_due_today(self):
        """ Returns true if either area is due today"""
        if self.days_till_feed(1) > 0:
            return False
        if self.days_till_feed(2) > 0:
            return False
        return True

    def check_item_included(self, area, item) -> int:
        """ Check to ensure the item is included in some feed and only once in all the feeds
        @return: 0 = Not included anywhere, 1 included once, > 1 the number of times included
        @rtype: int
        """
        mixes = self.feeds[area].get_mixes()
        flag = 0
        for m in mixes:
            if item in mixes[m]['items']:
                flag += 1
        return flag

    def get_recipe_status(self, area):
        return self.feeds[area].r_status

    def get_feed_mode(self, area):
        return 1

    def get_recipe_days_remaining(self, area):
        return self.feeds[area].get_recipe_days_remaining()

    def get_feeds_remaining(self, area):
        return self.feeds[area].get_feeds_remaining()

    def get_recipe_name(self, area):
        return self.feeds[area].recipe_name

    def get_days_till_feed(self):
        a = b = 99
        if self.main_window.area_controller.area_has_process(1):
            a = self.feeds[1].get_days_till_feed()
        if self.main_window.area_controller.area_has_process(2):
            b = self.feeds[2].get_days_till_feed()
        return min(a, b)

    def get_feed_frequency(self, area):
        return self.feeds[area].get_feed_frequency()

    def get_items(self, area, mix_num=1):
        return self.feeds[area].get_items(mix_num)

    def get_all_items(self, area):
        return self.feeds[area].items

    def get_next_feed_date(self, area):
        return self.feeds[area].nfd

    def get_last_feed_date(self, area):
        return self.feeds[area].lfd

    def get_next_recipe(self, area):
        # return self.feeds[area].get_next_feed_recipe()
        return self.feeds[area].recipe_next

    def get_recipe_item(self, area, mix_num, nid):
        return self.feeds[area].get_recipe_item(mix_num, nid)

    def get_next_lpp(self, area):
        return self.feeds[area].feed_litres_next

    def get_mix_count(self, area):
        return self.feeds[area].get_mix_count()

    def get_recipe(self, area, mix_num=1):
        return self.feeds[area].area_data['mixes'][mix_num]['recipe']

    def get_lpp(self, area, mix_num=1):
        return self.feeds[area].area_data['mixes'][mix_num]['lpp']

    def get_lpp_org(self, area):
        return self.feeds[area].feed_litres

    def get_water_total(self, area, mix_num=1):
        """ Get the water require for a specific mix in an area"""
        return self.feeds[area].area_data['mixes'][mix_num]['water total']

    def get_next_water_required(self):
        """ Get the total water required for next feed date"""
        a1 = self.days_till_feed(1)
        a2 = self.days_till_feed(2)
        if a1 == a2:
            return self.get_area_water_total(1) + self.get_area_water_total(2)
        if a1 < a2:
            return self.get_area_water_total(1)
        return self.get_area_water_total(2)

    def get_area_water_total(self, area):
        """ Calculates the total amount of water required for the area for all mixes for said area """
        t = 0.0
        mixes = self.feeds[area].area_data['mixes']
        for m in mixes:
            t += mixes[m]['water total']
        # self.feeds[area].area_data['water total'] = t
        return t

    def set_last_feed_date(self, area, feed_date):
        self.feeds[area].set_last_feed_date(feed_date)

    def recipe_item_status(self, area, mix_num, item):
        """ Checks the item (nid, mls) against the original recipe
        @return: 0 = Unchanged, 1 = Existing item changed, 2 = New item
                 The mls differance. Note only 1 will return a value for this, 0 & 2 this will be 0
        @rtype: int, float
        @type mix_num: int
        @type area: int
        @param item: The recipe item to look for (nid, mls)
        @type item: tuple
        """
        r_org = self.feeds[area].recipe
        for nid in r_org:
            if item[0] == nid[0]:
                # nid found
                if item[1] == nid[1]:
                    return 0, 0.0   # Unchanged
                return 1, float(item[1] - nid[1])   # changed)
        return 2, 0.0                # New

    def change_items(self, area, mix_num, items):
        self.feeds[area].change_items(mix_num, items)

    # def move_item(self, area, mix_from, mix_to, item):
    #     """ Move an item from one mix to another """
    #     self.feeds[area].move_item(mix_from, mix_to, item)

    def add_item(self, area, mix_num, item):
        """ This adds an item to mix num. It removes the item from any other mixes"""
        self.feeds[area].add_item(mix_num, item)

    def remove_item(self, area, item):
        """ This removes an item from all mixes"""
        self.feeds[area].remove_item(item)

    def new_day(self):
        for a in range(1, 3):
            if a in self.feeds:
                self.feeds[a].new_day()

    def feed(self, area, f_date=None):
        if not self.main_window.area_controller.area_has_process(area):
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
                    date_done = dt
                elif ret_val == QMessageBox.No:
                    date_done = datetime.now()
                else:
                    return
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

        # save feed details to the log
        self.log_txt = "{}      Feed    \r\n{} Mix{}  Area: {}   Mode: {}\r\n".\
            format(datetime.now().strftime('%d %b %y %H:%M'), len(mixes), "" if len(mixes) == 1 else "es",
                   area, self.get_feed_mode(area))
        if self.get_feed_mode(area) == 1:  # Manual
            self.deduct_fed_feed(area)  # This adds to the log_text
        else:  # Semi auto and auto
            if self.main_window.master_mode == MASTER:
                pass
        self.log_txt += "\r\n"
        self.main_window.logger.save_feed(self.main_window.area_controller.get_area_pid(area), self.log_txt)
        self.feeds[area].cycles_reduce()
        self.feeds[area].get_recipe_status()
        # self._check_feed_due_today()
        self.main_window.main_panel.lbl_water_required.setText(str(self.get_next_water_required()))
        self.main_window.main_panel.update_next_feeds()

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
                    # self.main_window.feeder.deduct_nutrient(item, mls)
                    if item[0] == WATER_ONLY_IDX:
                        nut = WATER_ONLY
                    else:
                        nut = self.db.execute_single('SELECT name FROM {} WHERE id = {}'.
                                                     format(DB_NUTRIENTS_NAMES, item[0]))
                    self.log_txt += "{}: Mix total {}mls   {}mls per plant.\r".format(nut, mls, item[1])
                else:
                    self.log_txt += "Water only\r"
        # self.main_window.feeder.check_pot_levels()
        # self.main_window.feeder.check_nutrient_levels()

