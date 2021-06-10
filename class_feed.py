import collections

from PyQt5.QtCore import QObject

# from class_process import ProcessClass as pClass
from defines import *


class FeedClass(QObject):
    def __init__(self, parent):
        """

        @type parent: pClass
        """
        super(FeedClass, self).__init__()
        self.my_parent = parent
        self.db = parent.db
        self.process_id = parent.id
        self.pattern_id = parent.pattern_id
        self.pattern_name = parent.pattern_name
        self.stage = parent.current_stage
        self.stage_day = parent.stage_days_elapsed
        self.qty_total = parent.quantity_org
        self.qty_current = parent.quantity

        self.plants = collections.defaultdict()
        for i in range(1, self.qty_current + 1):
            self.plants[i] = {'recipe': 0}

        sql = "SELECT s.stage, f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding " \
              "AND s.pid = {} ORDER BY s.stage, f.start".\
            format(DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id)
        rows_s = self.db.execute(sql)
        self.feed_schedules_all = rows_s.copy()
        sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding " \
              "AND s.pid = {} and s.stage ={} ORDER BY f.start".\
            format(DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage)
        rows_s = self.db.execute(sql)
        self.feed_schedule_current = rows_s.copy()
        if self.stage > 1:
            sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding " \
                  "AND s.pid = {} and s.stage ={} ORDER BY f.start". \
                format(DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage - 1)
            rows_s = self.db.execute(sql)
            self.feed_schedule_previous = rows_s.copy()
        print(rows_s)
