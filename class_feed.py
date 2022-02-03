import collections
import copy
from datetime import timedelta, datetime
from pprint import pprint

from PyQt5.QtCore import QObject

# from class_process import ProcessClass as pClass
from defines import *
from functions import dict2str

START_DAY = 0
END_DAY = 1
LPP = 2
RECIPE = 3
FREQ = 4


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
    try:
        return [int(n) for n in items.split(",")]
    except:
        return []


class FeedClass(QObject):
    def __init__(self, parent):
        """

        @type parent: pClass
        """
        super(FeedClass, self).__init__()
        self.feed_controller = parent
        self.db = parent.db
        self.process_id = 0
        self.process = 0
        self.pattern_id = 0
        self.pattern_name = ""
        self._area = 0
        self.stage = 0
        self.stage_days_max = 0     # Max days in current stage
        self.stages_max = 0
        self.qty_org = 0
        self.qty_current = 0
        self.stage_days_elapsed = 0  # Process stage days elapsed
        self.feed_schedule = None  # Active schedule
        self.feed_schedules_current = None  # Feed schedules for current stage
        self.feed_schedule_current = []  # Current feed schedule
        self.feed_schedules_all = collections.defaultdict(list)  # Feed schedules for all stages
        # feed_schedules_all[stage] = [start day, end day, lpp, rid, frequency]
        #                             [start day, end day, lpp, rid, frequency]
        # defaultdict( < class 'list'>, {1: [[1, 14, 0.25, 100, 4]],
        #                                2: [[1, 11, 1.0, 100, 3],
        #                                   [12, 20, 1.0, 1, 2],
        #                                   [21, 28, 1.0, 3, 2]],
        #                                3: [[1, 7, 1.5, 5, 2],
        #                                   [8, 21, 1.5, 9, 2],
        #                                   [22, 28, 1.5, 11, 2],
        #                                   [29, 35, 1.5, 10, 2],
        #                                   [36, 56, 1.5, 7, 2],
        #                                   [57, 63, 1.0, 100, 2]]})
        # self.feed_schedules_previous = None  # Feed schedules for previous stage
        # self.feed_schedule_item_num = 0  # The idx of the current schedule in feed_schedules_current
        self.feed_time = self.db.get_config(CFT_FEEDER, "feed time", "21:00")
        self.recipe = []  # Original recipe  [nid, ml, L, rid, freq]
        self.recipe_id = 0
        self.recipe_score = 0
        self.recipe_name = ""
        self.recipe_expires_day = 0
        self.recipe_starts_day = 0
        self.recipe_next = []
        self.recipe_next_name = ""
        self.recipe_next_id = 0
        self.new_recipe_due = 0
        self.feed_litres = 0  # Litres per plant
        self.feed_litres_next = 0
        self.nfd = None  # next feed date
        self.lfd = None  # last feed date
        self.r_status = 0  # -1 = last use, 1= Next will be new recipe, 2 = New recipe today 0 = no change
        self.frequency = 0
        self.items = []
        self.items_flushing = []
        self.flush_only = False  # Set True when all items are flushing
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
        self.feeds_till_end = []

    def load(self, area):
        """ This load all the default feed feed schedules for the process in area

        :param area: The area to load data for
        :type area: int
        :rtype: None """
        self.area = area
        self.process = self.feed_controller.main_window.area_controller.get_area_process(area)
        self.qty_current = self.process.get_current_quantity()
        self.qty_org = self.process.quantity_org
        self.pattern_id = self.process.pattern_id
        self.pattern_name = self.db.execute_single(
            'SELECT name FROM {} WHERE id = {}'.format(DB_PATTERN_NAMES, self.pattern_id))
        self.stage = self.process.current_stage
        self.stages_max = self.process.stages_max
        self.stage_days_max = self.process.stage_total_duration
        self.stage_days_elapsed = self.process.stage_days_elapsed
        self.stage_days_elapsed = 1 if self.stage_days_elapsed == 0 else self.stage_days_elapsed
        self.items = self.feed_controller.main_window.area_controller.get_area_items(area)
        sql = "SELECT s.stage, f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = " \
              "s.feeding AND s.pid = {} ORDER BY s.stage, f.start". \
            format(DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id)
        rows_s = self.db.execute(sql)
        for row in rows_s:
            #                        stage          start   end     lpp     rid     freq
            self.feed_schedules_all[row[0]].append([row[1], row[2], row[3], row[4], row[5]])
        # self.feed_schedules_all = self.process.stages

        self.load_feed_schedule_default(self.get_feed_schedule_current())
        self.get_next_feed_schedule()

    def load_feed_schedule_default(self, schedule):
        """ This loads all the data for the default schedule,
            also calls for the recipe to be loaded"""
        self.feed_schedule_current = schedule
        self.recipe_score = 0
        self.feed_schedule = None
        self.new_recipe_due = self.feed_schedule_current[END_DAY] - self.stage_days_elapsed
        self.recipe_id = self.feed_schedule_current[RECIPE]
        self.feed_litres = self.feed_schedule_current[LPP]
        self.recipe_expires_day = self.feed_schedule_current[END_DAY]
        self.recipe_starts_day = self.feed_schedule_current[START_DAY]
        self.frequency = self.feed_schedule_current[FREQ]
        self.load_current_schedule_recipe_default()

    def load_current_schedule_recipe_default(self):
        """ This loads the default recipe for the default schedule, it uses the recipe id to do this and it must be
            set first using load_feed_schedule_default
            Returns a recipe in list format [nid, ml, L"""
        self.recipe.clear()
        if self.recipe_id == WATER_ONLY_IDX:
            self.recipe_name = WATER_ONLY
        else:
            self.recipe_name = self.db.execute_single(
                "SELECT name FROM {} WHERE id = {}".format(DB_RECIPE_NAMES, self.recipe_id))
        if self.feed_schedule_current[RECIPE] is WATER_ONLY_IDX:
            # Water only
            self.recipe.append([WATER_ONLY_IDX, 0, self.feed_schedule_current[LPP], WATER_ONLY_IDX, 1])
            return self.recipe

        sql = "SELECT * FROM {} WHERE rid = {}".format(DB_RECIPES, self.recipe_id)
        r_rows = self.db.execute(sql)
        if r_rows is None:  # Missing
            # @Todo Add call to msg system - recipe missing
            return []
        else:
            for r_row in r_rows:  # loop through items in recipe
                #                     nid        ml              L
                self.recipe.append([r_row[2], r_row[3], self.feed_schedule_current[LPP],
                                    self.feed_schedule_current[RECIPE], r_row[4]])  # rid     freq
                # self.recipe_score += r_row[3] * self.feed_schedule[LPP] * self.quantity
                # print("recipe score ", self.recipe_score)
        return self.recipe

    def get_feed_schedule_current(self) -> list:
        """ This returns the current feed schedule for the current stage and day
            If it over runs last schedule in a stage it will attempt to return the first from the next stage
            It will return empty list if it can't find a schedule"""
        for s in self.feed_schedules_all[self.stage]:
            if s[1] >= self.stage_days_elapsed > s[0]:  # end day >= day > start day
                return s
        return s    # Stage has over run so just return last one
        # if self.stage < self.stages_max:
        #     return self.feed_schedules_all[self.stage + 1]
        # return []

    def get_feed_schedule_for(self, stage, day):
        """ This returns the feed schedule for the given stage and day
            It will return empty list if it can't find a schedule"""
        if stage not in self.feed_schedules_all:
            return []
        for s in self.feed_schedules_all[stage]:
            if s[1] >= day > s[0]:  # end day >= day > start day
                return s
        return []

    def get_next_feed_schedule(self):
        """ Returns the next feed schedule after the current, it will get first in next stage if at end of current
            will return empty list of none found"""
        nfs = []
        max_s = len(self.feed_schedules_all[self.stage])
        for i in range(0, max_s):
            if self.feed_schedules_all[self.stage][i][1] >= self. \
                    stage_days_elapsed > self.feed_schedules_all[self.stage][i][0]:  # end day >= day > start day
                i += 1
                if i < max_s:
                    return self.feed_schedules_all[self.stage][i]
        if self.stage + 1 >= self.stages_max:
            return []
        return self.feed_schedules_all[self.stage + 1][0]

    def get_recipe_next_feed_schedule(self):
        nfs = self.get_next_feed_schedule()
        return self.recipe_from_feed_schedule(nfs)

    def recipe_from_feed_schedule(self, schedule) -> list:
        """ This returns the recipe for any feed schedule given
        :return: Recipe as list
        :rtype: list
        """
        self.recipe_next.clear()
        self.recipe_next_id = schedule[RECIPE]
        self.feed_litres_next = schedule[LPP]

        if schedule[RECIPE] == WATER_ONLY_IDX:
            self.recipe_next_name = WATER_ONLY
        else:
            self.recipe_next_name = self.db.execute_single(
                "SELECT name FROM {} WHERE id = {}".format(DB_RECIPE_NAMES, self.recipe_next_id))
            if self.recipe_next_name is None:
                self.recipe_next_name = ""

        if self.feed_schedule_current[RECIPE] is WATER_ONLY_IDX:
            # Water only
            self.recipe_next.append([WATER_ONLY_IDX, 0, self.feed_schedule_current[LPP], WATER_ONLY_IDX, 1])
            return self.recipe_next

        sql = "SELECT * FROM {} WHERE rid = {}".format(DB_RECIPES, self.recipe_next_id)
        r_rows = self.db.execute(sql)
        if r_rows is None:  # Missing
            return []
        else:
            for r_row in r_rows:
                self.recipe_next.append([r_row[2], r_row[3], self.feed_schedule_current[LPP], self.feed_schedule_current[RECIPE], r_row[4]])
            return self.recipe_next

    # def get_next_feed_recipe(self):
    #     sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding AND" \
    #           " s.pid = {} and s.stage ={}".format(
    #         DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage)
    #     # rows = self.db.execute(sql)
    #     # if self.feed_schedule_item_num < len(rows) - 1:
    #     #     self.recipe_next_from_feed_schedule(rows[self.feed_schedule_item_num + 1])
    #     #     self.next_recipe_id = rows[self.feed_schedule_item_num + 1][3]
    #     #     self.feed_litres_next = rows[self.feed_schedule_item_num + 1][2]
    #     # else:  # No more feeds in this stage so look to next stage
    #     #     if self.stage < self.stages_max:
    #     #         sql = "SELECT f.start, f.dto, f.liters, f.rid, f.frequency FROM {} f INNER JOIN {} s ON f.sid = s.feeding AND s.pid = {} and s.stage ={} ORDER BY f.start".format(
    #     #             DB_FEED_SCHEDULES, DB_STAGE_PATTERNS, self.pattern_id, self.stage + 1)
    #     #         rows = self.db.execute(sql)
    #     #         if len(rows) != 0:
    #     #             # There is a next stage
    #     #             self.recipe_next_from_feed_schedule(rows[0])
    #     #             return
    #     #         else:  # No more stages so continue with use current as next
    #     #             self.recipe_next = self.recipe.copy()
    #     #             self.next_recipe_id = self.recipe_id
    #     #             self.feed_litres_next = self.feed_litres
    #     return self.recipe_next

    def get_has_flush(self):
        return len(self.items_flushing)

    def load_mixes(self):
        """ This loads all the active mixes (different feeds) for the current area.
            If any items are flushing it builds feed 1 as flush """
        self.items_flushing.clear()
        if self.area == 2:
            # Area 2. Check for flushing
            rows = self.db.execute("SELECT item, start FROM {}".format(DB_FLUSHING))
            self.items_flushing.clear()
            for row in rows:
                self.items_flushing.append(row[0])
            # If flushing build mix 1 as flush
            if len(self.items_flushing) > 0:
                self.area_data["mixes"][1] = {}
                self.area_data["mixes"][1]["items"] = self.items_flushing.copy()
                self.area_data["mixes"][1]["lpp"] = self.feed_litres
                self.area_data["mixes"][1]["base id"] = WATER_ONLY_IDX
                self.area_data["mixes"][1]["cycles"] = 10
                # self.area_data["mixes"][0]["recipe"] = {}
                self.area_data["mixes"][1]["water total"] = self.feed_litres * len(
                    self.area_data["mixes"][1]['items'])
                self.area_data["mixes"][1]["recipe"] = WATER_ONLY_IDX

        count = self.db.execute_single('SELECT COUNT(mix_num) as count FROM {} WHERE `area` = {}'.
                                       format(DB_PROCESS_FEED_ADJUSTMENTS, self.area))
        d = self.feed_controller.main_window.area_controller.get_items_drying()
        if len(self.items_flushing) + len(d) < self.qty_current:
            self.flush_only = False
            if count == 0:
                n = 1
                if len(self.items_flushing) > 0:
                    n += 1
                self.load_org_recipe(n)
            else:
                self._load_mixes(self.area)
        else:
            self.flush_only = True
        self._refresh_water_total()
        self.load_feed_date()
        # self.get_future_feeds()

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

    def _load_mixes(self, area):
        """ This loads all the mixes that the user has created, from the process feed adjustment table"""
        rows = self.db.execute(  # ..    0       1    2      3        4        5
            'SELECT mix_num, freq, lpp, `items`, cycles, base_id FROM {} WHERE `area` = {} ORDER BY mix_num'.
            format(DB_PROCESS_FEED_ADJUSTMENTS, area))
        mix_num = 1 if len(self.items_flushing) == 0 else 2
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

    def check_day(self):
        # if self.
        pass

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
                self.update_mix_water_total(mix)
                self.save_adjustments(mix)

    def add_item(self, mix, item):
        """ Add an item to mix's items
            Calls remove_item first to ensure the item is only in one mix"""
        self.remove_item(item)
        if mix > len(self.area_data['mixes']):
            return  # safety
        self.area_data["mixes"][mix]['items'].append(item)
        self.area_data["mixes"][mix]['items'].sort()
        self.update_mix_water_total(mix)
        self.save_adjustments(mix)

    def add_blank_mix(self):
        """ Adds a new mix using next mix number. The mix will be water only with the
            items set to none """
        n = len(self.area_data['mixes']) + 1
        self.area_data["mixes"][n] = {"items": [],  # Plant numbers
                                      "recipe": WATER_ONLY_IDX,
                                      "base id": WATER_ONLY_IDX,
                                      "lpp": self.feed_litres,  # Liters per plant
                                      "water total": 0,  # No items yet
                                      "cycles": 1}  # How many feeds this is used for
        # self.save_all(area, n)

    def add_new_mix(self):
        """ Adds a new mix using next mix number. The mix will be a copy of the original but with the
            items set to none """
        n = len(self.area_data['mixes']) + 1
        self.area_data["mixes"][n] = {"items": [],  # Plant numbers
                                      "recipe": copy.deepcopy(self.recipe),
                                      "base id": self.recipe_id,
                                      "lpp": self.feed_litres,  # Liters per plant
                                      "water total": 0,  # No items yet
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
        """ Calculates the max number of feeds that are left using this recipe

        :return: Number of feeds
        :rtype: int """
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
        """ This changes a recipe item. the change will contain the nid to change and the new mls for that nid
            If the nid does not exist in the recipe it will be added
        :param mix_num: The mix number to change item in
        :type mix_num: int
        :type change: tuple     (nid, mls)
        """
        r = self.area_data['mixes'][mix_num]['recipe']
        #  recipe  nid, ml, L, rid, freq
        if r != WATER_ONLY_IDX:
            if change[1] == 0:
                if not self.nid_in_recipe(change[0], self.recipe):
                    self.remove_nid_from_recipe(change[0], self.area_data['mixes'][mix_num]['recipe'])
                    self.save_mix_adjustment(mix_num)
                    return
            for rl in r:
                if rl[0] == change[0]:
                    rl[1] = change[1]
                    self.save_mix_adjustment(mix_num)
                    return
        else:
            self.area_data['mixes'][mix_num]['recipe'] = []
        # If here it is a new item to the recipe
        self.area_data['mixes'][mix_num]['recipe'].append([change[0], change[1]])
        self.save_mix_adjustment(mix_num)

    def nid_in_recipe(self, nid, recipe):
        """ Returns True if the nid is in the recipe """
        for r in recipe:
            if r[0] == nid:
                return True
        return False

    def remove_nid_from_recipe(self, nid, recipe):
        idx = 0
        for r in recipe:
            if r[0] == nid:
                break
            idx += 1
        recipe.pop(idx)

    def change_items(self, mix_num, items):
        self.area_data['mixes'][mix_num]['items'] = items
        self.update_mix_water_total(mix_num)
        self.save_adjustments(mix_num)

    def update_mix_water_total(self, mix_num):
        self.area_data['mixes'][mix_num]['water total'] = \
            len(self.area_data['mixes'][mix_num]['items']) * self.area_data['mixes'][mix_num]["lpp"]
        self._refresh_water_total()

    # def move_item(self, mix_from, mix_to, item):
    #     self.area_data['mixes'][mix_from]['items'].remove(item)
    #     self.update_mix_water_total(mix_from)
    #     self.area_data['mixes'][mix_to]['items'].append(item)
    #     self.update_mix_water_total(mix_to)

    def change_mix_water(self, mix_num, new_lpp):
        self.area_data['mixes'][mix_num]['lpp'] = new_lpp
        self.area_data['mixes'][mix_num]['water total'] = \
            new_lpp * len(self.area_data['mixes'][mix_num]['items'])
        self._refresh_water_total()
        self.save_adjustments(mix_num)

    def save_adjustments(self, mix_num):
        """ This saves the following for an area mix
            Freq, lpp, cycles, items and base id
            This is either inserted or updated in the process feed adjustments table"""
        if len(self.items_flushing) > 0 and mix_num == 1:
            return  # Flush is not saved to db
        data = self.area_data['mixes'][mix_num]
        if len(self.items_flushing) > 0:  # If flushing mix 1 is the flush which is not stored in db so -1 the mix_num
            mix_num -= 1
        count = self.db.execute_single('SELECT COUNT(area) FROM {} WHERE area = {} AND mix_num = {}'.
                                       format(DB_PROCESS_FEED_ADJUSTMENTS, self.area, mix_num))
        if count > 1:
            print("Only should be 1 entry")
        items = dict2str(data['items'])
        if count == 0:
            # Insert into db
            sql = 'INSERT INTO {} (area, mix_num, freq, lpp, cycles, items, base_id) VALUES ' \
                  '({}, {}, {}, {}, {}, "{}", {})'.format(
                DB_PROCESS_FEED_ADJUSTMENTS, self.area, mix_num, self.frequency, data['lpp'],
                data['cycles'], items, data['base id'])
        else:
            # Update db
            sql = 'UPDATE {} SET freq = {}, lpp = {}, cycles = {}, items = "{}", base_id = {} WHERE area = {} AND mix_num = {} LIMIT 1'. \
                format(DB_PROCESS_FEED_ADJUSTMENTS, self.frequency, data['lpp'],
                       data['cycles'], items, data['base id'], self.area, mix_num)
        self.db.execute_write(sql)

    def save_mix_adjustment(self, mix_num):
        """ This saves the recipe for a mix in the mixes table"""
        if len(self.items_flushing) > 0:  # If flushing mix 1 is the flush which is not stored in db so -1 the mix_num
            mix_num_db = mix_num - 1
        else:
            mix_num_db = mix_num
        # Delete any entries for this. Trust me this is best way
        self.db.execute_write('DELETE FROM {} WHERE area = {} AND mix_num = {}'.
                              format(DB_PROCESS_MIXES, self.area, mix_num_db))
        # Insert into db
        if self.area_data['mixes'][mix_num]['recipe'] == WATER_ONLY_IDX:
            sql = 'INSERT INTO {} (area, mix_num, nid, ml) VALUES ({}, {}, {}, {})'. \
                format(DB_PROCESS_MIXES, self.area, mix_num_db, WATER_ONLY_IDX, 0)
            self.db.execute_write(sql)
            return
        for r in self.area_data['mixes'][mix_num]['recipe']:
            sql = 'INSERT INTO {} (area, mix_num, nid, ml) VALUES ({}, {}, {}, {})'. \
                format(DB_PROCESS_MIXES, self.area, mix_num_db, r[0], r[1])
            self.db.execute_write(sql)

    def get_recipe_status(self):
        """ This checks both areas and sets 'status' in the data structure """
        # -1 = last use, 1= Next will be new recipe, 2 = New recipe today 0 = no change
        if self.lfd is None:
            return 2
        r_change_days = self.recipe_expires_day - self.stage_days_elapsed
        r_start_date = datetime.now().date() - timedelta(days=self.stage_days_elapsed - (self.recipe_starts_day - 1))
        lfd_days = (datetime.now().date() - self.lfd.date()).days

        if r_change_days == 0:
            if lfd_days < self.frequency:
                self.r_status = 1
            else:
                self.r_status = 2
            return self.r_status

        if self.stage_days_elapsed - self.recipe_starts_day - 1 <= self.frequency:
            # After change
            if self.lfd.date() >= r_start_date:
                self.r_status = 0
                return self.r_status
            else:
                self.r_status = 2
                return self.r_status
        if r_change_days + 1 <= self.frequency - 1:
            if lfd_days == 0:
                #  fed today
                self.r_status = 1
                return self.r_status
            else:
                # Not Fed
                self.r_status = -1
                return self.r_status
        if r_change_days <= (self.frequency * 2) - 1:
            if lfd_days == 0:
                # Not fed today
                pass
            else:
                # Fed
                self.r_status = -1
                return self.r_status
        self.r_status = 0
        return self.r_status

    def get_feed_frequency(self):
        return self.frequency

    def get_recipe_days_remaining(self):
        if self.recipe_expires_day > self.stage_days_max:
            return self.stage_days_max - self.stage_days_elapsed
        return self.recipe_expires_day - self.stage_days_elapsed

    def get_feeds_remaining(self, ):
        """ Returns the number of feeds remaining using current recipe """
        if self.recipe_expires_day > self.stage_days_max:
            tot = self.stage_days_max
        else:
            tot = self.recipe_expires_day
        return int((tot - self.stage_days_elapsed)
                   / self.frequency)

    def get_future_feeds(self):
        day_offset = self.get_days_till_feed()
        run_day = self.stage_days_elapsed + day_offset
        carry_over = 0  # used to get correct first feed in the next stage
        day_num = day_offset  # used to calculate the actual feed date,
        for stage in range(self.stage, self.stages_max):
            if stage != self.stage:
                run_day = carry_over
            feed_schedule = self.feed_schedules_all[stage][0]
            if feed_schedule > 0:
                sql = "SELECT start, dto, liters, rid, frequency FROM {} WHERE sid = {}".format(DB_FEED_SCHEDULES,
                                                                                                feed_schedule)
                rows = self.db.execute(sql)
                for row in rows:
                    while run_day <= row[1]:
                        # print(row)                day       rid    liters
                        self.feeds_till_end.append(
                            [run_day, row[3], row[2], stage, (datetime.today() + timedelta(days=day_num)).date()])
                        run_day += row[4]
                        day_num += row[4]
                        if run_day == row[1]:
                            carry_over = row[4]
                            break
                        if run_day > row[1]:
                            carry_over = run_day - row[1]
                            break
        pprint(self.feeds_till_end)

    def set_last_feed_date(self, f_date):
        """ Sets the last feed date and the next feed date and the also updates the db
        :type f_date: datetime
        """
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

        if len(self.items_flushing) > 0:  # If flushing mix 1 is the flush which is not stored in db so -1 the mix_num
            mix_num -= 1
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
        self.stage_days_elapsed += 1
        self.load_feed_schedule_default(self.get_feed_schedule_current())
        self.get_next_feed_schedule()
        self.load_mixes()
        self.get_recipe_status()
        self._refresh_water_total()

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, a):
        self._area = a
