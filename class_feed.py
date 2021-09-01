import collections
import copy
from datetime import timedelta, datetime

from PyQt5.QtCore import QObject

# from class_process import ProcessClass as pClass
from defines import *
from functions import dict2str


def str2dict(items_str):
    d = collections.defaultdict()
    if items_str == "":
        return d
    i = items_str.split(",")
    for v in i:
        d[int(v)] = 1
    return d


def list_to_str(items) -> str:
    i = ""
    for p in range(1, len(items) + 1):
        i += str(p) + ","
    return i[:len(i) - 1]  # Remove last comma


def str_to_list(items) -> list:
    return [int(n) for n in items.split(",")]


class FeedClass(QObject):
    def __init__(self, parent):
        """

        @type parent: pClass
        """
        super(FeedClass, self).__init__()
        self.feed_controller = parent
        self.db = parent.db
        self.process_id = 0
        self.pattern_id = 0
        self.pattern_name = ""
        self._area = 0
        self.stage = 0
        self.stages_max = 0
        self.qty_org = 0
        self.qty_current = 0
        self.stage_days_elapsed = 0  # Process stage days elapsed
        self.feed_schedule = None  # Active schedule
        self.feed_schedules_current = None  # Feed schedules for current stage
        self.feed_schedules_all = None  # Feed schedules for all stages
        self.feed_schedules_previous = None  # Feed schedules for previous stage
        self.feed_schedule_item_num = 0  # The idx of the current schedule in feed_schedules_current
        self.feed_time = self.db.get_config(CFT_FEEDER, "feed time", "21:00")
        self.recipe = []  # Original recipe  nid, ml, L, rid, freq
        self.recipe_score = 0
        self.recipe_name = ""
        self.new_recipe_due = 0
        self.recipe_id = 0
        self.feed_litres = 0  # Litres per plant
        self.nfd = None  # next feed date
        self.lfd = None  # last feed date
        self.recipe_expires_day = 0
        self.recipe_starts_day = 0
        self.r_status = 0  # -1 = last use, 1= Next will be new recipe, 2 = New recipe today 0 = no change
        self.next_recipe_id = 0
        self.next_feed_litres = 0
        self.feed_litres_next = 0
        self.frequency = 0
        self.next_recipe_name = ""
        self.recipe_next = []
        self.items = []
        self.items_flushing = []
        self.flush_mix = 0  # The mix number that is the flush mix
        self.water_total = 0  # Total water required for all mixes
        self.area_data = {"mixes": {1: {"items": [],  # Plant numbers
                                        "recipe": {},  # Dict of ingredients {nid, ml}
                                        "base id": 0,  # Recipe ID this is based off
                                        "lpp": 0,  # Liters per plant
                                        "water total": 0,  # nid changed from org, ml change
                                        "cycles": 0},  # How many feeds this is used for
                                    },
                          }

    def load(self, area, pattern_id, stage, current_day, max_stages, items):
        """
        This load all the feed data for a process in area
        :param items: A list of the items actually in the area
        :type items: list
        :param area:
        :type area: int
        :param pattern_id:
        :type pattern_id: int
        :param stage:
        :type stage: int
        :param current_day:
        :type current_day: int
        :param max_stages:
        :type max_stages: int
        :return:
        :rtype: None
        """
        self.area = area
        self.pattern_id = pattern_id
        self.stage = stage
        self.stages_max = max_stages
        self.stage_days_elapsed = current_day
        self.items = items
        sql = "SELECT s.stage, f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding " \
              "AND s.pid = {} ORDER BY s.stage, f.start". \
            format(DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id)
        rows_s = self.db.execute(sql)
        self.feed_schedules_all = rows_s.copy()
        sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding " \
              "AND s.pid = {} and s.stage ={} ORDER BY f.start". \
            format(DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage)
        rows_s = self.db.execute(sql)
        self.feed_schedules_current = rows_s.copy()
        if self.stage > 1:
            sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding " \
                  "AND s.pid = {} and s.stage ={} ORDER BY f.start". \
                format(DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage - 1)
            rows_s = self.db.execute(sql)
            self.feed_schedules_previous = rows_s.copy()
        self.recipe_current_from_feed_schedule()
        self.get_next_feed_recipe()
        # print(self.recipe)
        # print(self.recipe_next)

    def recipe_current_from_feed_schedule(self):
        """
        This loads the default recipe using the feed schedule for current day of current stage
        :return: None
        :rtype: None
        """
        self.recipe_score = 0
        self.feed_schedule = None
        stage_days_elapsed = 1 if self.stage_days_elapsed == 0 else self.stage_days_elapsed
        x = schedule = 0
        for schedule in self.feed_schedules_current:
            if schedule[1] >= stage_days_elapsed >= schedule[0]:
                self.feed_schedule = schedule
                self.feed_schedule_item_num = x
                break
            x += 1
        if self.feed_schedule is None:
            # The process has over run the last day of feed schedule, so use the last one in use
            self.feed_schedule = schedule
            self.feed_schedule_item_num = x
            # @Todo Add call to msg system - feed schedule missing

        self.new_recipe_due = self.feed_schedule[1] - stage_days_elapsed
        self.recipe_id = self.feed_schedule[3]
        self.feed_litres = self.feed_schedule[2]
        self.recipe_expires_day = self.feed_schedule[1]
        self.recipe_starts_day = self.feed_schedule[0]
        self.frequency = self.feed_schedule[4]
        if self.recipe_id == WATER_ONLY_IDX:
            self.recipe_name = WATER_ONLY
        else:
            self.recipe_name = self.db.execute_single(
                "SELECT name FROM {} WHERE id = {}".format(DB_RECIPE_NAMES, self.recipe_id))
        if self.feed_schedule[3] is WATER_ONLY_IDX:
            # Water only
            self.recipe_score = 0
            self.recipe.append([WATER_ONLY_IDX, 0, self.feed_schedule[2], WATER_ONLY_IDX, 1])
            return
        sql = "SELECT * FROM {} WHERE rid = {}".format(DB_RECIPES, self.feed_schedule[3])
        r_rows = self.db.execute(sql)
        if r_rows is None:  # Missing
            pass
            # @Todo Add call to msg system - recipe missing
        else:
            for r_row in r_rows:  # current feed
                #                nid    ml              L                               rid                     freq   adj_ml  remain
                self.recipe.append([r_row[2], r_row[3], self.feed_schedule[2], self.feed_schedule[3], r_row[4]])
                # self.recipe_score += r_row[3] * self.feed_schedule[2] * self.quantity
                # print("recipe score ", self.recipe_score)
        return

    def recipe_next_from_feed_schedule(self, schedule):
        """
        This loads the a recipe for the next feed schedule
        :return: None
        :rtype: None
        """
        self.recipe_next = []
        self.next_recipe_id = schedule[3]
        self.next_feed_litres = schedule[2]
        if self.recipe_id == WATER_ONLY_IDX:
            self.next_recipe_name = WATER_ONLY
        else:
            self.next_recipe_name = self.db.execute_single(
                "SELECT name FROM {} WHERE id = {}".format(DB_RECIPE_NAMES, self.next_recipe_id))
        if schedule[3] is WATER_ONLY_IDX:
            # Water only
            self.recipe_next.append([WATER_ONLY_IDX, 0, schedule[2], WATER_ONLY_IDX, 1])
            return
        sql = "SELECT * FROM {} WHERE rid = {}".format(DB_RECIPES, schedule[3])
        r_rows = self.db.execute(sql)
        if r_rows is None:  # Missing
            pass
            # @Todo Add call to msg system - recipe missing
        else:
            for r_row in r_rows:  # current feed
                #                           nid         ml       L       rid             freq
                self.recipe_next.append([r_row[2], r_row[3], schedule[2], schedule[3], r_row[4]])
        return

    def get_next_feed_recipe(self):
        sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding AND" \
              " s.pid = {} and s.stage ={}".format(
                DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage)
        rows = self.db.execute(sql)
        if self.feed_schedule_item_num < len(rows) - 1:
            self.recipe_next_from_feed_schedule(rows[self.feed_schedule_item_num + 1])
            self.next_recipe_id = rows[self.feed_schedule_item_num + 1][3]
            self.feed_litres_next = rows[self.feed_schedule_item_num + 1][2]
        else:  # No more feeds in this stage so look to next stage
            if self.stage < self.stages_max:
                sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding AND s.pid = {} and s.stage ={} ORDER BY f.start".format(
                    DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage + 1)
                rows = self.db.execute(sql)
                if len(rows) != 0:
                    # There is a next stage
                    self.recipe_next_from_feed_schedule(rows[0])
                    return
                else:  # No more stages so continue with use current as next
                    self.recipe_next = self.recipe.copy()
                    self.next_recipe_id = self.recipe_id
                    self.feed_litres_next = self.feed_litres
        return self.recipe_next

    def load_mixes(self):
        """
        This loads all mixes (different feeds) for the current area
        :return: None
        :rtype: None
        """
        rows = self.db.execute("SELECT item, start FROM {}".format(DB_FLUSHING))
        self.items_flushing.clear()
        for row in rows:
            self.items_flushing.append(row)

        count = self.db.execute_single('SELECT COUNT(mix_num) as count FROM {} WHERE `area` = {}'.
                                       format(DB_PROCESS_FEED_ADJUSTMENTS, self.area))
        if count == 0:
            self.load_org_recipe(1)
        else:
            self._load_mixes(self.area)
        self._refresh_water_total()
        self.load_feed_date()

    def load_org_recipe(self, mix_num):
        """Load original recipe/mix into mix number"""
        self.area_data["mixes"][mix_num]['items'] = self.items
        self.area_data["mixes"][mix_num]["recipe"] = copy.deepcopy(self.recipe)
        self.area_data["mixes"][mix_num]["lpp"] = self.feed_litres
        self.area_data["mixes"][mix_num]["base id"] = self.recipe_id
        self.area_data["mixes"][mix_num]["cycles"] = self.max_feeds_till_change()
        self.area_data["mixes"][mix_num]["water total"] = \
            self.feed_litres * \
            len(self.area_data["mixes"][mix_num]['items'])

    def _load_mixes(self, area):  # ..    0       1    2      3        4        5
        rows = self.db.execute(
            'SELECT mix_num, freq, lpp, `items`, cycles, base_id FROM {} WHERE `area` = {} ORDER BY mix_num'.
            format(DB_PROCESS_FEED_ADJUSTMENTS, area))
        mix_num = 1
        for row in rows:
            if mix_num not in self.area_data['mixes']:
                self.area_data["mixes"][mix_num] = {}
            self.area_data["mixes"][mix_num]["items"] = str_to_list(row[3])
            self.area_data["mixes"][mix_num]["lpp"] = row[2]
            self.area_data["mixes"][mix_num]["base id"] = row[5]
            self.area_data["mixes"][mix_num]["cycles"] = row[4]
            self.area_data["mixes"][mix_num]["recipe"] = {}
            self.area_data["mixes"][mix_num]["water total"] = row[2] * len(
                self.area_data["mixes"][mix_num]['items'])
            self.area_data["mixes"][mix_num]["recipe"] = self.load_mix_recipe(mix_num)
            mix_num += 1

    def create_flush_mix(self):
        if len(self.items_flushing) == 0:
            return
        self.flush_mix = len(self.area_data['mixes'])
        self.area_data["mixes"][self.flush_mix]['items'] = self.items_flushing
        self.area_data["mixes"][self.flush_mix]["recipe"] = [WATER_ONLY_IDX, 0, self.feed_litres, WATER_ONLY_IDX, 1]
        self.area_data["mixes"][self.flush_mix]["lpp"] = self.feed_litres
        self.area_data["mixes"][self.flush_mix]["base id"] = WATER_ONLY_IDX
        self.area_data["mixes"][self.flush_mix]["cycles"] = 7
        self.area_data["mixes"][self.flush_mix]["water total"] = \
            self.feed_litres * \
            len(self.flush_mix['items'])

    def remove_item(self, item):
        """ Remove the item from all mixed"""
        for mix in self.area_data['mixes']:
            if item in self.area_data['mixes'][mix]['items']:
                self.area_data['mixes'][mix]['items'].remove(item)

    def add_item(self, mix, item):
        """ Add an item to mix's items
            Calls remove_item first to ensure the item is only in one mix"""
        self.remove_item(item)
        if mix > len(self.area_data['mixes']):
            return  # safety
        self.area_data["mixes"][mix]['items'].append(item)
        self.area_data["mixes"][mix]['items'].sort()

    def add_blank_mix(self):
        """ Adds a new mix using next mix number. The mix will be water only with the
            items set to none """
        n = len(self.area_data['mixes']) + 1
        self.area_data["mixes"][n] = {"items": {},  # Plant numbers
                                      "recipe": WATER_ONLY_IDX,
                                      "base id": WATER_ONLY_IDX,
                                      "lpp": self.feed_litres,  # Liters per plant
                                      "water total": 0,   # No items yet
                                      "cycles": 1}  # How many feeds this is used for
        # self.save_all(area, n)

    def add_new_mix(self):
        """ Adds a new mix using next mix number. The mix will be a copy of the original but with the
            items set to none """
        n = len(self.area_data['mixes']) + 1
        self.area_data["mixes"][n] = {"items": {},  # Plant numbers
                                      "recipe": copy.deepcopy(self.recipe),
                                      "base id": self.recipe_id,
                                      "lpp": self.feed_litres,  # Liters per plant
                                      "water total": 0,   # No items yet
                                      "cycles": 1}  # How many feeds this is used for
        # self.save_all(area, n)

    def load_mix_recipe(self, mix_num) -> list:
        """Load the recipe for the mix number
           If none is found it returns the original"""
        ingredients = self.db.execute('SELECT nid, ml FROM {} WHERE `area` = {} AND mix_num = {}'.
                                      format(DB_PROCESS_MIXES, self.area, mix_num))
        if len(ingredients) == 0:
            if self.area_data['mixes'][mix_num]['base id'] == WATER_ONLY_IDX:
                self.area_data["mixes"][mix_num]["recipe"] = WATER_ONLY_IDX
                return WATER_ONLY_IDX
            else:
                # self.area_data[area]["mixes"][mix_num] = {}
                self.area_data["mixes"][mix_num]["recipe"].clear()
                self.area_data["mixes"][mix_num]["base id"] = self.recipe_id
                return copy.deepcopy(self.recipe)
        i = []
        for ingredient in ingredients:
            i.append([ingredient[0], ingredient[1]])
        return i

    def _refresh_water_total(self):
        """ Calculates the total amount of water required for the area for all mixes for said area """
        t = 0.0
        mixes = self.area_data['mixes']
        for m in mixes:
            t += mixes[m]['water total']
        self.water_total = t

    def max_feeds_till_change(self) -> int:
        """
        Calculates the max number of feeds are left using this recipe
        :return:
        :rtype: int
        """
        return int((self.recipe_expires_day - self.stage_days_elapsed) /
                   self.frequency)

    def load_feed_date(self):
        sql = "SELECT dt FROM {} WHERE item = 'feed date' and id = {}".format(DB_PROCESS_ADJUSTMENTS, self.area)
        f_date = self.db.execute_single(sql)
        if f_date is None:
            self.nfd = datetime.now().date()
            self.lfd = self.nfd - timedelta(days=self.frequency)
            # @Todo add to msg sys  no feed date
            return
        self.lfd = f_date
        self.nfd = f_date + timedelta(days=self.frequency)
        # self.get_future_feeds()

    def get_days_till_feed(self):
        if self.nfd is None:
            return 101
        return (self.nfd.date() - datetime.now().date()).days

    def get_mix_count(self):
        """ Return the number of mixes for the area"""
        return len(self.area_data['mixes'])

    def get_mixes(self):
        """ Return the mixes for the area"""
        return self.area_data['mixes']

    def get_items(self, mix_num=1):
        return self.area_data['mixes'][mix_num]['items']

    def get_recipe_item(self, mix_num, nid):
        for i in self.area_data['mixes'][mix_num]['recipe']:
            if i[0] == nid:
                return i
        return [0, 0, 0, 0, 0, 0]

    def change_cycles(self, mix_num, cycles):
        self.area_data['mixes'][mix_num]['cycles'] = cycles
        self.save_adjustments(mix_num)

    def change_recipe_item(self, mix_num, change):
        """

        :param mix_num: The mix number to change item in
        :type mix_num: int
        :type change: tuple     (nid, mls)
        """
        r = self.area_data['mixes'][mix_num]['recipe']
        #  recipe  nid, ml, L, rid, freq
        if r == WATER_ONLY_IDX:
            return
        for rl in r:
            if rl[0] == change[0]:
                rl[1] = change[1]
                self.save_mix_adjustment(mix_num)
                return
        # If here it is a new item to the recipe
        r.append([change[0], change[1]])

    def change_items(self, mix_num, items):
        self.area_data['mixes'][mix_num]['items'] = items
        self.area_data['mixes'][mix_num]['water total'] = \
            len(items) * self.area_data['mixes'][mix_num]["lpp"]
        self.save_adjustments(mix_num)
        self._refresh_water_total()

    def change_mix_water(self, mix_num, new_lpp):
        self.area_data['mixes'][mix_num]['lpp'] = new_lpp
        self.area_data['mixes'][mix_num]['water total'] = \
            new_lpp * len(self.area_data['mixes'][mix_num]['items'])
        self._refresh_water_total()
        self.save_adjustments(mix_num)

    def save_adjustments(self, mix_num):
        data = self.area_data['mixes'][mix_num]
        count = self.db.execute_single('SELECT COUNT(area) FROM {} WHERE area = {} AND mix_num = {}'.
                                       format(DB_PROCESS_FEED_ADJUSTMENTS, self.area, mix_num))
        if count > 1:
            print("Only should be 1 entry")
        items = dict2str(data['items'])
        if count == 0:
            # Insert into db
            sql = 'INSERT INTO {} (area, mix_num, freq, lpp, cycles, items, base_id) VALUES ({}, {}, {}, {}, {}, "{}", {})'.\
                format(DB_PROCESS_FEED_ADJUSTMENTS, self.area, mix_num, self.frequency, data['lpp'],
                       data['cycles'], items, data['base id'])
        else:
            # Update db
            sql = 'UPDATE {} SET freq = {}, lpp = {}, cycles = {}, items = "{}", base_id = {} WHERE area = {} AND mix_num = {} LIMIT 1'.\
                format(DB_PROCESS_FEED_ADJUSTMENTS, self.frequency, data['lpp'],
                       data['cycles'], items, data['base id'], self.area, mix_num)
        self.db.execute_write(sql)

    def save_mix_adjustment(self, mix_num):
        """ This save any adjustments to a mix"""
        # Delete any entries for this. Trust me this is best way
        self.db.execute_write('DELETE FROM {} WHERE area = {} AND mix_num = {}'.
                              format(DB_PROCESS_MIXES, self.area, mix_num))
        # Insert into db
        if self.area_data['mixes'][mix_num]['recipe'] == WATER_ONLY_IDX:
            sql = 'INSERT INTO {} (area, mix_num, nid, ml) VALUES ({}, {}, {}, {})'. \
                format(DB_PROCESS_MIXES, self.area, mix_num, WATER_ONLY_IDX, 0)
            self.db.execute_write(sql)
            return
        for r in self.area_data['mixes'][mix_num]['recipe']:
            sql = 'INSERT INTO {} (area, mix_num, nid, ml) VALUES ({}, {}, {}, {})'. \
                format(DB_PROCESS_MIXES, self.area, mix_num, r[0], r[1])
            self.db.execute_write(sql)

    def get_recipe_status(self):
        """ This checks both areas and sets 'status' in the data structure """
        # -1 = last use, 1= Next will be new recipe, 2 = New recipe today 0 = no change
        if self.lfd is None:
            return 0
        r_change_days = self.recipe_expires_day - self.stage_days_elapsed
        r_start_date = datetime.now().date() - timedelta(days=self.stage_days_elapsed - (self.recipe_starts_day - 1))
        lfd_days = (datetime.now().date() - self.lfd.date()).days

        if r_change_days == 0:
            if lfd_days == 0:
                self.r_status = 2
            else:
                self.r_status = 1
            return

        if self.stage_days_elapsed - self.recipe_starts_day - 1 <= self.frequency:
            # After change
            if self.lfd.date() >= r_start_date:
                self.r_status = 0
                return
            else:
                self.r_status = 2
                return
        if r_change_days + 1 <= self.frequency - 1:
            if lfd_days == 0:
                #  fed today
                self.r_status = 1
                return
            else:
                # Not Fed
                self.r_status = -1
                return
        if r_change_days <= (self.frequency * 2) - 1:
            if lfd_days == 0:
                # Not fed today
                pass
            else:
                # Fed
                self.r_status = -1
                return
        self.r_status = 0

    def get_feed_frequency(self):
        return self.frequency

    def get_recipe_days_remaining(self):
        return self.recipe_expires_day - self.stage_days_elapsed

    def get_feeds_remaining(self, ):
        """ Returns the number of feeds remaining using current recipe """
        return int((self.recipe_expires_day - self.stage_days_elapsed)
                   / self.frequency)

    def set_last_feed_date(self, f_date):
        """ Sets the last feed date and next and the also updates the db"""
        t = self.feed_time.split(":")
        f_date = datetime(f_date.year, f_date.month, f_date.day, int(t[0]), int(t[1]))
        self.lfd = f_date
        self.nfd = f_date + timedelta(days=self.frequency)
        sql = "UPDATE {} SET dt = '{}' WHERE item = '{}' and id = {} LIMIT 1". \
            format(DB_PROCESS_ADJUSTMENTS, f_date, PA_FEED_DATE, self.area)
        self.db.execute_write(sql)
        # self._check_feed_due_today()
        self.feed_controller.main_window.area_controller.output_controller.water_heater_update_info()

    def cycles_reduce(self):
        """ Reduces the number of cycles in each mix in the area by 1 and remove any mixes
            with 0 cycles except mix 1 """
        mixes = self.area_data['mixes']
        for m in mixes:
            mixes[m]['cycles'] -= 1
            if mixes[m]['cycles'] < 1:
                if m == 1:
                    # default mix was over ride but now returning to original for rest of recipe
                    self.load_org_recipe(1)
                    # if mixes[m]['cycles'] == 0:
                    #     print("Shouldn't be here as 0 cycles for mix 1 means recipe change ")
                else:
                    mixes[1]['items'] = mixes[m]['items']  # Copies items from mix to be deleted to mix 1
                    self.delete_mix(m)
                    return
            # self.save_all(m)

    def delete_mix(self, mix_num):
        if mix_num == 1:
            return
        mixes = self.area_data['mixes']
        mixes.pop(mix_num)
        if len(mixes) == 1:
            # Only 1 mix left so make sure all items are selected
            self.area_data["mixes"][1]['items'] = self.get_items(1)
        # if mix_num < self.get_mix_count():
        #     # Its not the last one so move rest up
        #     for mix_n in mixes.copy():
        #         if mix_n == mix_num:
        #             self.copy_mix_to_mix(mix_n + 1 if mix_n + 1 <= self.get_mix_count() else self.get_mix_count(),
        #                                  mix_n)
        #     mixes.pop(self.get_mix_count())
        self.db.execute_write('DELETE FROM {} WHERE area = {} AND mix_num ={}'.
                              format(DB_PROCESS_MIXES, self.area, mix_num))
        self.db.execute_write('DELETE FROM {} WHERE area = {} AND mix_num ={}'.
                              format(DB_PROCESS_FEED_ADJUSTMENTS, self.area, mix_num))
        self.db.execute_write('UPDATE {} SET mix_num = mix_num - 1 WHERE area = {} AND mix_num > {} '.
                              format(DB_PROCESS_FEED_ADJUSTMENTS, self.area, mix_num))
        # else:
        #     self.db.execute_write('DELETE FROM {} WHERE area = {} AND mix_num ={}'.
        #                           format(DB_PROCESS_MIXES, self.area, mix_num))
        #     self.db.execute_write('DELETE FROM {} WHERE area = {} AND mix_num ={}'.
        #                           format(DB_PROCESS_FEED_ADJUSTMENTS, self.area, mix_num))
        #     mixes.pop(mix_num)
        print(mixes)

    def copy_mix_to_mix(self, from_mix, to_mix):
        mixes = self.area_data['mixes']
        mixes[to_mix] = mixes[from_mix]
        self.save_mix_adjustment(to_mix)

    def swap_mix_to_mix(self, from_mix, to_mix):
        mixes = self.area_data['mixes']
        t = mixes[to_mix].copy()
        mixes[to_mix] = mixes[from_mix]
        self.save_mix_adjustment(to_mix)
        mixes[from_mix] = t
        self.save_mix_adjustment(from_mix)

    def reset_water(self, mix_num):
        self.area_data["mixes"][mix_num]["lpp"] = self.feed_litres
        self.area_data["mixes"][mix_num]["water total"] = \
            self.area_data["mixes"][mix_num]["lpp"] * \
            len(self.area_data["mixes"][mix_num]['items'])
        self.save_adjustments(mix_num)
        self._refresh_water_total()

    def reset_nutrients(self, mix_num):
        """ Resets nutrients back to original recipe values, also sets cycles to remaining number and saves"""
        self.area_data["mixes"][mix_num]["recipe"] = copy.deepcopy(self.recipe)
        self.area_data["mixes"][mix_num]["base id"] = self.recipe_id
        self.area_data["mixes"][mix_num]["cycles"] = self.max_feeds_till_change()
        self.save_mix_adjustment(mix_num)

    def new_day(self):
        self.get_recipe_status()
        self._refresh_water_total()

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, a):
        self._area = a
