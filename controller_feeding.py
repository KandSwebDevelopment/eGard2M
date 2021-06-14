import collections
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal
from class_feed import FeedClass
from defines import *


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

    def new_day(self):
        for a in range(1, 3):
            self.feeds[a].new_day()
