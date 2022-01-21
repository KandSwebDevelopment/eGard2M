import copy

# from class_feed import FeedClass
from dbController import *
from datetime import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import collections
# from status_codes import *
from functions import find_it
from status_codes import FC_P_JOURNAL_MISSING, FC_P_TEMPERATURE_SCHEDULE_MISSING


class ProcessClass(QObject):
    alert = pyqtSignal(int, int)

    def __init__(self, pid, parent):
        # QObject.__init__(self)
        super(ProcessClass, self).__init__()
        self.area_controller = parent
        self.id = pid
        self.db = self.area_controller.db
        self.start = None
        self.end = None  # Date due to finish with adjustments
        self.running = False
        self.location = 0
        # self.adjusted = False  # Set if user has adjusted the process
        self.quantity = 0  # The quantity currently in the process. Died or finished removed
        self.quantity_org = 0  # The quantity the process started with
        self.pattern_id = None  # The feed pattern for the process
        self.pattern_name = ""  # The pattern name
        self.change_due = False  # Set true when stage is due to be advanced
        self.running_days = 0  # Total Number of day process has been running
        self.current_lighting = 0  # The current stage lighting schedule
        # self.current_feed_schedule_id = 0  # The current stage feeding schedule
        self.process_offset_total = 0  # The total number of days the process stages are adjusted to current stage
        self.days_total = 0  # Total days in this process
        self.due_date = None  # Date due to finish with no adjustments
        self.cool_warm = UNSET        # Area is is cool = 1, warm = 2, normal = 0
        self.current_stage = 0  # The current stage running
        self.stage_required = 0  # The stage that should be running
        # self.stage_adjustments = []  # Holds the number of days a stage is delayed (+) or advanced (-)
        self.stages_len_default = [0, 0, 0, 0]  # The default number of days for each stage
        self.stages_len_adjustment = [0, 0, 0, 0]  # The number of days each stage is adjusted by. The 1st 0 is for base 0
        # self.stage_offset = 0  # The number of days the current stage is adjusted by
        self.stages_max = 0  # Total number of stages in this process
        self.stage_total_duration = 0  # The current stage total duration
        self.stage_days_elapsed = 0  # Number of days elapsed in current stage
        self.stage_days_remaining = 0  # Number of days remaining in this stage
        self.stage_day_adjust = 0  # Value here will change the current stage day by that amount
        self.stage_start = None  # Date current stage starts
        self.stage_start_day = 0  # Day number of total days current stage starts
        self.stage_end = None  # Date current stage ends
        self.stages = []  # Holds all the info about all the stages in this process  [stage](dur, light, temp, feed, location)
        self.stage_name = ""  # Current stage name
        self.stages_start = []  # List of datetime each stage starts on
        self.stages_end = []
        self.stage_location = None  # The location required for stage 1=Prep, "=Finishing, 3=Drying, 50=None as completed
        self.stage_next_location = None  # The location required for next stage

        self.light_on = None  # The date time when light is due to come on
        self.light_off = None  # Calculated date time light goes off
        self.light_duration = None  # Time duration light is on
        self.light_repeat = 0
        self.light_status = 0  # Light status 1 = on 0 = off
        self.light_status_last = None  # Name of current light schedule
        self.light_name = ""

        self.current_temperature_id = 0  # The current stage temperature schedule id

        # holds default range values for temperature ranges for current stage
        # temperature_ranges_default / adjusted[DAY or NIGHT][item 1 to 4][low, set or high]
        self.temperature_ranges_default = collections.defaultdict(dict)
        self.temperature_ranges_adjusted = collections.defaultdict(dict)    # The default ranges adjusted for this process

        # self.temperature_ranges = collections.defaultdict()  # hold range values for temperature ranges for current stage
        # self.temperature_ranges_active = collections.defaultdict()  # The final in use with any adjustments applied
        # self.temperature_ranges_active_org = collections.defaultdict()  # The original temp range currently active
        # self.temperature_ranges_inactive = collections.defaultdict()  # The final in use with any adjustments applied
        # self.temperature_ranges_inactive_org = collections.defaultdict()  # The original temp range currently active
        self.temperature_name = ""

        self.strains = collections.defaultdict()    # id, shortest, longest, name, plant number -> id: min: max: name
        self.strain_shortest = 0
        self.strain_longest = 0
        self.strain_window = []         # 0 = Not ready, 1 = ready in 7 days, 2 = ready, 3 = beyond window
        self.strain_location = []       # Location of each strain

        # self.water_on = None  # The water heater on time
        # self.water_hrs = 0  # Hours water heater is on for
        self.recipe_id = 0              # Current recipe id
        self.recipe_name = ""           # The name of recipe in use
        self.feed_mode = 1              # 1= Manual, 2 = Semi Auto, 3 = Full auto use feeder
        # self.recipe_original = []       # Array of recipe_item's which makes the complete feed    0=nid, 1=ml, 2=L, 3=rid, 4=freq, 5=adj ml, 6=adj remaining
        # self.recipe_final = []          # Array with changed feed, a manual change to a feed
        # self.recipe_changes = []        # Array of changes to current feed   0=nid, 1=ml, 2=remaining
        # self.recipe_extended = 0        # Indicates the number of days the recipe is extended by due to the stage being delayed
        # self.recipe_next = []           # Next recipe to be used
        # self.recipe_next_id = None      # Next recipe id
        # self.recipe_score = 0           # Used by feeder to determine which area to do first. It is the sum of all the nutrients in the feed, lower score goes first
        # self.recipe_status = 0          # 0 = Same recipe in use, -1 = Recipe will change next feed, 1 = Recipe has changed and next feed will be first
        # self.recipe_is_change = True    # True if recipe has been modified
        # self.recipe_expires_day = 0     # The day number which current recipe expires, used with stage_days_elapsed
        # self.recipe_starts_day = 0      # The day number which current recipe started on
        # self.recipe_next_replaced = False  # True if next recipe does not exist so current will be used
        # self.new_recipe_due = None      # The number of days until a different recipe is used
        # self.feed_schedule = []       # The feed schedule for current stage
        # self.feed_time = ""             # Default feed time, loaded from the db
        # self.feed_litres = 0            # Litres per plant per feed (each)
        # self.feed_litres_next = 0       # Litres per plant per feed (each) for the next recipe
        # self.feed_litres_adj = 0        # Litres to add to feed_liters (total not each), allows manual change
        # self.feed_litres_adj_remaining = 0  # Number of feed to use above adjustment
        # self.feed_schedule_item_num = 0  # The row number currently in use in the feed schedule
        # self.feed_quantity_array = []   # Array with 1 = plant feed, 0 = not feed
        # self.feed_quantity = 0          # The number that feed will be made for which may be different than the quantity
        # self.feed_frequency = 0
        # self.feed_frequency_next = 0
        self.feeds_till_end = []
        self.last_feed_date = None      # Datetime of last feed
        self.cool_time = 0
        self.warm_time = 0

        self.settings = None

        self.startup()

        # Start journal
        self.logging_available = True   # self.area_controller.logger.available
        self.new_line = '\n'
        if self.logging_available:
            self.journal_filename = self.area_controller.main_window.logger.journal_file_template.format(self.id)
            # The following will create the file if it does not exist
            f = open(self.journal_filename, "a")
            f.close()

    def startup(self):
        # Load the process
        sql = "SELECT * FROM " + DB_PROCESS + " WHERE id = {}".format(self.id)
        row = self.db.execute_one_row(sql)
        self.running = row[1]  # Is process running
        self.location = row[2]  # Which area process is in
        self.start = datetime.strptime(row[3].strftime('%Y%m%d'),
                                       '%Y%m%d')  # Date process was started
        self.end = datetime.strptime(row[4].strftime('%Y%m%d'),
                                     '%Y%m%d')  # Date process is due to end
        self.pattern_id = row[5]  # Pattern ID of the process
        self.current_stage = row[6]
        self.quantity_org = row[7]
        sql = "SELECT COUNT(item) FROM {} WHERE process_id = {}".format(DB_AREAS, self.id)
        self.quantity = self.db.execute_single(sql)
        self.feed_mode = row[8]
        self.pattern_name = self.db.execute_single(
            "SELECT name FROM " + DB_PATTERN_NAMES + " WHERE id = " + str(self.pattern_id))

        # Load strains
        self.strains.clear()
        self.strain_location.clear()
        self.strain_longest = 0
        self.strain_shortest = 0
        sql = 'SELECT strain_id, item, location FROM {} WHERE process_id = {} ORDER BY item'.format(DB_PROCESS_STRAINS, self.id)
        rows = self.db.execute(sql)
        if len(rows) > 0:
            for row in rows:
                # if row[2] != 0:     # Location = 0 = plant removed, dead
                self.strain_location.append(row[2])
                s_rows = self.db.execute_one_row('SELECT duration_min, duration_max, name FROM {} WHERE id = {}'.format(DB_STRAINS, row[0]))
                self.strains[row[1]] = {'id': row[0],
                                        'min': s_rows[0],
                                        'max': s_rows[1],
                                        'name': s_rows[2],
                                        'item': row[1]}

            s = ""
            for x in self.strains:
                s += str(self.strains[x]['id']) + ", "
            s = s[:len(s) - 2]      # Remove last comma
            sql = 'SELECT MAX(duration_max) FROM {} WHERE id IN ({})'.format(DB_STRAINS, s)
            row = self.db.execute_single(sql)
            self.strain_longest = row
            sql = 'SELECT MIN(duration_min) FROM {} WHERE id IN ({})'.format(DB_STRAINS, s)
            row = self.db.execute_single(sql)
            # print(row)
            self.strain_shortest = row

        # Get transition times from db. Has to be here as it need location
        self.cool_time = int(self.db.get_config(CFT_AREA, "trans cool {}".format(self.location), 60)) * 60
        self.warm_time = int(self.db.get_config(CFT_AREA, "trans warm {}".format(self.location), 60)) * 60

        self.process_load_stage_info()

        self.load_lighting_schedule()
        self.get_light_status()

    def process_load_stage_info(self):
        # load the the stages for the process
        self.load_process_adjustments()  # Loads any adjustments from the template in use into current_stage_len_adjustments
        self.load_stages()  # Loads the stages form the template in use into stages and applies offset
        self.calculate_stages_start()
        self.is_running()
        self.get_required_stage()
        self.load_stage(self.current_stage)  # Loads the current stage
        self.load_temperature_schedule()

    def load_process_adjustments(self):
        if not self.running:
            return
        self.process_offset_total = 0
        # self.stage_adjustments.clear()
        self.stages_len_adjustment = [0, 0, 0, 0, 0]
        sda = self.db.execute_one_row("SELECT itemid, offset from {} WHERE item = '{}' AND id = {}".
                                      format(DB_PROCESS_ADJUSTMENTS, PA_STAGE_DAY_ADJUST, self.id))
        if sda is None:
            sda = 0
        else:
            if sda[0] == self.current_stage:
                self.stage_day_adjust = int(sda[1])
            else:
                self.stage_day_adjust = 0
        sql = "SELECT * FROM " + DB_PROCESS_ADJUSTMENTS + " WHERE id = {} AND item = '{}' ORDER BY id, item, itemid".format(
            self.id, PA_STAGE_DAY_ADJUST)
        rows = self.db.execute(sql)
        for row in rows:
            #                            stage    offset
            if sda == row[2]:
                v = int(row[3]) - self.stage_day_adjust
            else:
                v = int(row[3])
            # self.stage_adjustments.append([row[2], v])
            self.stages_len_adjustment[row[2]] = v

    def load_stages(self):
        # This loads all the stage info for the process and applies offset
        if not self.running:
            return
        sql = "SELECT * FROM " + DB_STAGE_PATTERNS + " WHERE pid = {} ORDER BY stage".format(self.pattern_id)
        rows = self.db.execute(sql)
        stage = 1
        self.stages.clear()
        self.days_total = 0
        for row in rows:
            stage_len = row[2]
            if stage_len == 0 and row[1] == 3:  # Auto cal flowering
                stage_len = self.strain_longest
            self.stages_len_default[stage - 1] = stage_len
            stage_len += self.stages_len_adjustment[stage]
            #                   stage     dur      light   temp    feed    location
            self.stages.append([row[1], stage_len, row[3], row[4], row[5], row[6]])
            self.days_total += stage_len
            stage += 1
        self.stages_max = stage - 1
        self.due_date = self.start + timedelta(days=self.days_total)

    def load_stage(self, stage):
        if not self.running:
            return
        self.stage_total_duration = self.stages[stage - 1][1]  # includes offset

        if stage == 1:
            diff = datetime.today() - self.start
        elif stage == 2:
            diff = datetime.today() - self.stages_start[stage - 1]
        else:
            diff = datetime.today() - self.stages_start[stage - 1]
        self.stage_days_elapsed = diff.days
        # if self.stage_days_elapsed < 1:
        #     self.stage_days_elapsed = 1

        self.stage_name = self.db.execute_single("SELECT name FROM " + DB_STAGE_NAMES + " WHERE id = " + str(stage))
        self.current_lighting = self.stages[stage - 1][2]
        self.current_temperature_id = self.stages[stage - 1][3]
        # self.current_feed_schedule_id = self.stages[stage - 1][4]
        self.stage_location = self.stages[stage - 1][5]
        self.stage_start = self.stages_start[stage - 1]
        self.stage_end = self.stage_start + timedelta(days=self.stage_total_duration)
        self.stage_days_remaining = self.stage_total_duration - self.stage_days_elapsed

        # self.stage_offset = self.get_stage_adjustment(stage)
        self.stage_day_adjust = self.get_stage_adjustment(stage)
        if stage is self.stages_max:
            self.stage_next_location = 0
        else:
            self.stage_next_location = self.stages[stage][5]

    def load_lighting_schedule(self):
        if not self.running:
            return
        self.light_name = self.db.execute_single(
            "SELECT name FROM " + DB_LIGHT_NAMES + " WHERE id = " + str(self.stages[self.current_stage - 1][2]))

        rows = self.db.execute_one_row(
            "SELECT * FROM " + DB_LIGHT + " WHERE id = " + str(self.stages[self.current_stage - 1][2]))
        if rows is not None:
            ct = datetime.now()
            self.light_on = datetime.combine(date.today(), datetime.min.time()) + rows[
                1]  # datetime(ct.year, ct.month, ct.day, tt.hour, tt.minute)
            self.light_duration = rows[3]
            self.light_off = self.light_on + self.light_duration  # timedelta(hours=self.light_duration.hour, minutes=self.light_duration.minute)
            if ct.hour < self.light_off.hour:
                if self.light_off.date() < ct.date():
                    pass
                else:
                    self.light_on -= timedelta(days=1)
                    self.light_off -= timedelta(days=1)
            # print("light off = ", self.light_off)
            self.light_repeat = rows[4]
        else:
            # No light schedule
            ct = datetime.now()
            self.light_on = datetime(ct.year, ct.month, ct.day, 6, 0)
            self.light_duration = datetime(ct.year, ct.month, ct.day, 0, 0)
            self.light_off = datetime(ct.year, ct.month, ct.day, 6, 0)
            self.light_repeat = 0
            # @ToDo raise error, no light schedule
            # add_info = "For process in area {}<br>Schedule missing is {}".format(self.location, self.light_name)
            # self.area_controller.notifier.add(CRITICAL, "No light schedule could be found", FC_P_LIGHT_SCHEDULE_MISSING,
            #                             add_info)

    def get_required_stage(self):
        if not self.running:
            return
        self.stage_required = None
        # Get active stage
        stage = 1
        start = 0
        ct = datetime.now().date()
        while ct >= self.stages_start[stage].date() and stage < len(self.stages):
            stage += 1
            start += self.stages[stage - 2][1]
        if stage > len(self.stages):
            stage = len(self.stages)
        self.stage_required = stage
        self.stage_start_day = start
        # self.current_duration = self.stages[stage-2][1]
        # print("Stage = " + str(stage))

    def get_stage_name(self, stage):
        # Return the stage name for the given stage
        sql = "SELECT name FROM " + DB_STAGE_NAMES + " WHERE id = {}".format(stage)
        row = self.db.execute(sql)
        return row[0][0]

    def get_stage_adjustment(self, stage):
        return self.stages_len_adjustment[stage]

    def get_stage_adjustment_to_current(self):
        # Return tot total day the process is adjusted up to but not including the current stage
        total = 0
        for x in self.stages_len_adjustment:  # type: list
            if x[0] is PA_STAGE_DAY_ADJUST and x[1] < self.current_stage - 1:
                total += x[2]
        return total

    def get_pattern_name(self):
        row = self.db.execute_one_row("SELECT name FROM " + DB_PATTERN_NAMES + " WHERE id = " + str(self.pattern_id))
        return row[0]

    def get_current_quantity(self):
        return self.db.execute_single(
            "SELECT COUNT(id) AS qty FROM {} WHERE process_id = {} AND location > 0 AND location < 50".
            format(DB_PROCESS_STRAINS, self.id))

    def get_future_feeds(self):
        # if self.get_next_feed_date() is None:
        #     day_offset = 0
        # else:
        #     day_offset = (self.get_next_feed_date().date() - datetime.today().date()).days
        day_offset = 0   # self.area_controller.feed_control.get_days_till_feed(self.location)
        run_day = self.stage_days_elapsed + day_offset
        carry_over = 0  # used to get correct first feed in the next stage
        day_num = day_offset  # used to calculate the actual feed date,
        for stage in range(self.current_stage, self.stages_max):
            if stage != self.current_stage:
                run_day = carry_over
            feed_schedule = self.stages[stage - 1][4]
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
        # pprint(self.feeds_till_end)

    def trans_timeout(self):
        self.cool_warm = NORMAL

    def end_process(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Confirm you wish to End this process")
        msg.setInformativeText("Process Number - " + str(self.id))
        msg.setWindowTitle("Confirm Process End")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Yes:
            # Update event log
            text = "Process Finished\nTotal duration " + str(self.days_total) + " days " + str(
                round(self.days_total / 7, 1)) + " weeks\n"
            text += "Stages\n"
            idx = 0
            if self.stages_start[self.stages_max].date() != datetime.now().date():
                # If end date is not today then adjust last stage length to bring it to today
                self.stages_start[self.stages_max] = datetime.now()
                self.stages_len_adjustment[self.stages_max] -= self.stage_days_remaining
                self.stages[self.stages_max - 1][1] -= self.stage_days_remaining
            for s in self.stages_start:
                if idx > 3:
                    break
                stage_name = self.db.execute_single(
                    "SELECT name FROM " + DB_STAGE_NAMES + " WHERE id = " + str(idx + 1))
                text += "Stage " + str(idx + 1) + " " + stage_name + " from " + s.strftime("%d-%m-%y") + " for " + \
                        str(self.stages[idx][1]) + " days " + str(
                    round(self.stages[idx][1] / 7, 1)) + " weeks ending on " + (
                                    s + timedelta(days=self.stages[idx][1] - 1)).strftime("%d-%m-%y") + "."
                if self.stages_len_adjustment[idx + 1] > 0:
                    text += " This stage was held back by " + str(self.stages_len_adjustment[idx + 1]) + " days."
                elif self.stages_len_adjustment[idx + 1] < 0:
                    text += " This stage was shortened by " + str(abs(self.stages_len_adjustment[idx + 1])) + " days."
                text += "\n"
                idx += 1
            self.journal_write(text)
            ed = datetime.now()
            ed = ed.strftime("%Y-%m-%d")
            # Update process table
            sql = "UPDATE " + DB_PROCESS + ' SET running = "0", location = "50", stage = "0", end = "' + str(
                ed) + '" WHERE id = ' + str(self.id)
            print(sql)
            self.db.execute_write(sql)
            # Clear stage durations
            sql = "DELETE FROM {} WHERE id = {}".format(DB_PROCESS_ADJUSTMENTS, self.id)
            print(sql)
            self.db.execute_write(sql)

            # Reset quantity
            sql = "UPDATE {} SET `offset` = 0 WHERE ITEM = 'quantity' AND id = {}".format(DB_PROCESS_ADJUSTMENTS,
                                                                                          self.location)
            print(sql)
            self.db.execute_write(sql)

            # Reset any stage day advance
            if self.stage_day_adjust != 0:
                self.stages_len_adjustment[self.current_stage] -= self.stage_day_adjust
                sql = "UPDATE {} SET itemid = 0, offset = 0 WHERE item = {} id = {} LIMIT 1".format(
                    DB_PROCESS_ADJUSTMENTS, PA_STAGE_DAY_ADJUST, self.id)
                self.db.execute_write(sql)

            # Clear from drying table
            sql = "DELETE FROM {}".format(DB_PROCESS_ADJUSTMENTS)
            print(sql)
            self.db.execute_write(sql)

            # Remove any feed mixes
            self.db.execute_write('DELETE FROM {} WHERE area = 2'.format(DB_PROCESS_FEED_ADJUSTMENTS))
            self.db.execute_write('DELETE FROM {} WHERE area = 2'.format(DB_PROCESS_MIXES))

            # Feed liters
            # if self.location < 3:
            #     sql = "UPDATE {} SET itemid = 0, offset = 0 WHERE item = {} id = {} LIMIT 1".format(
            #         DB_PROCESS_ADJUSTMENTS, PA_FEED, self.location)
            #     self.db.execute_write(sql)
            # print(sql)
            # self.db.execute_write(sql)

    def is_running(self):
        if self.start < datetime.now():
            diff = datetime.today() - self.start
            self.running_days = diff.days
            if self.running_days == 0:
                self.running_days = 1
            # print("Days running = ", self.running_days)
            # if self.end > datetime.now():
            #     self.running = True
            #     # print("Running")
            # else:
            #     # print("Stopped 1")
            #     self.running = True
        # else:
        #     self.running = False
        return self.running

    def journal_read(self):
        if not self.logging_available:
            return
        try:
            f = open(self.journal_filename)
            text = f.read()
            f.close()
        except FileNotFoundError:
            return "File Missing " + self.journal_filename
        if text == "":
            return "There as no entries in this journal"
        entries = text.split("\n")
        result = "<table>"
        for line in entries:
            if line != "":
                result += "<tr><td>" + line + "</td></tr>"
        result += "</table>"
        return result

    def journal_write(self, entry):
        if not self.logging_available:
            return
        f = open(self.journal_filename, "a")
        text = entry + self.new_line
        # print(text)
        f.write(text)
        f.close()

    def calculate_stages_start(self):
        val = datetime.now()
        running_total = 0
        self.stages_start.clear()
        self.stages_start.append(self.start)
        for stage in range(0, self.stages_max):
            stage_len = self.stages[stage][1]
            running_total += stage_len
            val = self.start + timedelta(days=running_total)
            self.stages_start.append(val)

        self.end = val

    def adjust_stage_days(self, adjustment, other=0):
        """ Advances or delays a stage end by number of days
            It store the adjustment in the processs_adjustments table """
        if not self.running:
            return
        if adjustment != 0:
            self.stage_day_adjust += adjustment
            sql = 'SELECT * FROM ' + DB_PROCESS_ADJUSTMENTS + ' WHERE id = {} AND item = "{}" AND itemid = {}'.format(
                self.id, PA_STAGE_DAY_ADJUST, self.current_stage)
            row = self.db.execute_one_row(sql)
            if row is None:
                sql = 'INSERT INTO ' + DB_PROCESS_ADJUSTMENTS + ' (id, item, itemid, offset, other) VALUES ({}, "{}", {}, {}, {})'.format(
                    self.id, PA_STAGE_DAY_ADJUST, self.current_stage, self.stage_day_adjust, other)
            else:
                co = row[3] + adjustment
                sql = 'UPDATE ' + DB_PROCESS_ADJUSTMENTS + ' SET offset = {} WHERE id = "{}" AND item = "{}" ' \
                                                           'AND itemid = {}'.format(co, self.id, PA_STAGE_DAY_ADJUST, self.current_stage)
            self.db.execute_write(sql)

            # update the end date
            self.end = self.end + timedelta(days=adjustment)
            sql = "UPDATE {} SET end = '{}' WHERE id = {}".format(DB_PROCESS, datetime.strftime(self.end, "%d-%m-%y"),
                                                                  self.id)
            # print(sql)
            self.db.execute_write(sql)

            self.process_load_stage_info()
            # Check if this has caused stage to change, if so load new stage info
            # if self.stage_required is not self.current_stage:
            #     self.change_due = True
            # else:
            #     self.change_due = False

    def load_temperature_schedule(self):
        """
        Loads the temperature schedule in use for the current stage into temperature_ranges, this will contain both
        day and night ranges
        @return: None
        @rtype: None
        """
        if not self.running:
            return
        rows = self.db.execute_one_row(
            "SELECT * FROM " + DB_TEMPERATURE_NAMES + " WHERE id = " + str(self.current_temperature_id))
        self.temperature_name = rows[1]
        rows = self.db.execute(
            "SELECT day_night, item, low, set_point, high FROM " + DB_TEMPERATURES + " WHERE trid = " + str(
                self.current_temperature_id))
        if len(rows) == 0:
            add_info = "For process in area {}<br>Schedule missing is {}".format(self.location, self.temperature_name)
            # self.area_controller.notifier.add(ERROR, "No temperature schedule could be found",
            #                             FC_P_TEMPERATURE_SCHEDULE_MISSING, add_info)

        for row in rows:
            # if row[0] not in self.temperature_ranges.keys():
            #     self.temperature_ranges[row[0]] = {}
            # self.temperature_ranges[row[0]][row[1]] = {'low': row[2], 'set': row[3], 'high': row[4]}
            self.temperature_ranges_default[row[0]][row[1]] = {'low': row[2], 'set': row[3], 'high': row[4]}
        # print(self.temperature_ranges)
        self.load_temperature_adjustments()

    def load_temperature_adjustments(self):
        """ This creates the temperature_ranges_adjusted values which is the current working values
            Call this to update the process of any changes to the temperature ranges"""
        self.temperature_ranges_adjusted = copy.deepcopy(self.temperature_ranges_default)

        sql = "SELECT `day`, item, setting, value FROM {} WHERE `area` = {} AND `day` >= 0 ORDER BY `day`, item".\
            format(DB_PROCESS_TEMPERATURE, self.location)
        rows = self.db.execute(sql)
        for row in rows:
            if row[3] != 0:     # value is not zero
                dn = DAY if row[0] == 1 else NIGHT
                self.temperature_ranges_adjusted[dn][row[1]][row[2]] = row[3]

        sql = 'SELECT value, item, setting FROM {} WHERE `area` = {} and `day` = {}'.\
            format(DB_PROCESS_TEMPERATURE, self.location, self.light_status)
        # rows = self.db.execute(sql)
        # for row in rows:
        #     if row[0] > 0:
        #         if row[1] in self.temperature_ranges_active:
        #             if row[0] == 0:
        #                 # No adjustment so set it to original value
        #                 # temperature_ranges_ [item][setting] = value
        #                 self.temperature_ranges_active[row[1]][row[2]] = row[0]
        #                 # pass
        #             else:
        #                 self.temperature_ranges_active[row[1]][row[2]] = row[0]
        # sql = 'SELECT value, item, setting FROM {} WHERE `area` = {} and `day` = {}'.\
        #     format(DB_PROCESS_TEMPERATURE, self.location, int(not self.light_status))
        # rows = self.db.execute(sql)
        # for row in rows:
        #     if row[0] > 0:
        #         if row[1] in self.temperature_ranges_inactive:
        #             self.temperature_ranges_inactive[row[1]][row[2]] = row[0]

    def get_temperature_ranges(self, current=True):
        """ Returns a dict of the current adjusted temperature ranges
            Set current to False to returns range not currently in use"""
        if current:
            dn = DAY if self.check_light() == 1 else NIGHT
        else:
            dn = DAY if self.check_light() == 0 else NIGHT
        return self.temperature_ranges_adjusted[dn]

    def get_temperature_range_item(self, item, current=True):
        """ Returns a dict of the current adjusted temperature range for item
            Set current to False to returns range not currently in use"""
        if current:
            dn = DAY if self.check_light() == 1 else NIGHT
        else:
            dn = DAY if self.check_light() == 0 else NIGHT
        return self.temperature_ranges_adjusted[dn][item]

    def get_temperature_ranges_default(self, current=True):
        """ Returns a dict of the current default temperature ranges
            Set current to False to returns range not currently in use"""
        if current:
            dn = DAY if self.check_light() == 1 else NIGHT
        else:
            dn = DAY if self.check_light() == 0 else NIGHT
        return self.temperature_ranges_default[dn]

    def get_temperature_range_item_default(self, item, current=True):
        """ Returns a dict of the current default temperature ranges for item
            Set current to False to returns range not currently in use"""
        if current:
            dn = DAY if self.check_light() == 1 else NIGHT
        else:
            dn = DAY if self.check_light() == 0 else NIGHT
        return self.temperature_ranges_default[dn][item]

    # def load_active_temperature_ranges(self):
    #     """
    #     produces two arrays of temperature settings, one for day and one for night,
    #     process.active_temperature_ranges for current light state
    #     process.inactive_temperature_ranges for the alt light state
    #     These will be altered by load_temperature_adjustments to add any user setting
    #     It also creates two arrays of the original default values which can be compared with to detect user changes
    #     DO NOT USE this to get the temp range use the variable process.temperature_ranges_active
    #     @return: Will only have a return list if current is False
    #     @rtype: list
    #     """
    #     if len(self.temperature_ranges) == 0:
    #         return
    #     for dn in self.temperature_ranges:
    #         if dn == self.light_status:
    #             self.temperature_ranges_active_org = self.temperature_ranges[1].copy()
    #             self.temperature_ranges_active = copy.deepcopy(self.temperature_ranges_active_org)
    #             self.temperature_ranges_inactive_org = self.temperature_ranges[2].copy()
    #             self.temperature_ranges_inactive = copy.deepcopy(self.temperature_ranges_inactive_org)
    #         elif dn == 2 and self.light_status == 0:
    #             self.temperature_ranges_active_org = self.temperature_ranges[2].copy()
    #             self.temperature_ranges_active = copy.deepcopy(self.temperature_ranges_active_org)
    #             self.temperature_ranges_inactive_org = self.temperature_ranges[1].copy()
    #             self.temperature_ranges_inactive = copy.deepcopy(self.temperature_ranges_inactive_org)
    #     self.load_temperature_adjustments()
    #
    def info(self, item):
        if not self.running:
            return
        if item is IF_ID:
            return "ID: " + str(self.id)
        elif item is IF_STAGE_NAME:
            return "Stage: " + str(self.current_stage)
        elif item is IF_STAGE_INFO:
            text = "<table>"
            text += "<tr><td>{} - Day {} of {}<br>{} days remaining</td></tr>" \
                .format(self.stage_name, self.stage_days_elapsed, self.stage_total_duration, self.stage_days_remaining)
            if self.stage_day_adjust != 0:
                text += "<tr><td><i>This stage had been adjusted by {} days</i></td></tr>".format(self.stage_day_adjust)
            # text += "<tr><td>Light on at {} for {}hrs</td></tr>".format(datetime.strftime(self.light_on, "%H:%M"),
            #                                                             ':'.join(
            #                                                                 str(self.light_duration).split(':')[:1]))
            text += "<tr><td></td></tr>"
            text += "</table>"
            return text
        elif item == IF_DRYING:
            text = "Drying<br>  Day {}<br>Total days {}".format(self.stage_days_elapsed, self.days_total)
            return text
        return "INFO ERROR"

    def advance_stage(self):
        if self.current_stage == self.stages_max:
            # End of process
            self.end_process()
            return
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Confirm you wish to advance the stage")
        msg.setWindowTitle("Confirm Stage Advance")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        ret_val = msg.exec_()
        if ret_val == QMessageBox.Yes:
            next_stage_name = self.db.execute_single("SELECT name FROM {} WHERE id = {}".
                                                     format(DB_STAGE_NAMES, self.current_stage + 1))
            if next_stage_name is None:
                next_stage_name = "Unknown"
            if self.stage_location is not self.stage_next_location:
                msg.setText("This change requires this process to be moved")
                msg.setWindowTitle("Confirm Location Change")
                msg.setInformativeText("From location " + str(self.stage_location) +
                                       " to " + str(self.stage_next_location) +
                                       "<br><br><b>Has this been done?</b><br>Click Yes if it has been move<br>"
                                       "Click No if it has not been move but you still want to advance the stage")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Cancel)
                ret_val = msg.exec_()
                if ret_val == QMessageBox.Cancel:
                    return
                self.current_stage += 1
                if ret_val == QMessageBox.Yes:  # ############### Advance and move #################
                    # Add journal entry
                    self.journal_write("<b>Stage Change</b> to {} after {} days {}. Moved from area {} to {}"
                                       .format(next_stage_name, self.stage_days_elapsed, self.stage_name,
                                               self.stage_location,  self.stage_next_location))
                    # Update the processes current stage
                    self.db.execute_write(
                        "UPDATE " + DB_PROCESS + " SET stage = " + str(self.current_stage) + ", location = " + str(
                            self.stage_next_location) + " WHERE id = " + str(self.id))
                    # now move the feed date
                    if self.stage_next_location < 3:
                        # Set feed date for new location
                        sql = "UPDATE {} SET dt = {} WHERE item = '{}' and id = {} LIMIT 1".format(
                            DB_PROCESS_ADJUSTMENTS, self.last_feed_date, PA_FEED_DATE, self.stage_next_location)
                        self.db.execute_write(sql)
                        # Remove value from old location
                        sql = "UPDATE {} SET dt = {} WHERE item = '{}' and id = {} LIMIT 1".format(
                            DB_PROCESS_ADJUSTMENTS, None, PA_FEED_DATE, self.stage_location)
                        self.db.execute_write(sql)
                        # Feed liters
                        # if self.location < 3:
                        #     sql = "UPDATE {} SET itemid = 0, offset = 0 WHERE item = {} id = {} LIMIT 1".format(
                        #         DB_PROCESS_ADJUSTMENTS, PA_FEED, self.location)
                        #     self.db.execute_write(sql)
                        # print(sql)
                        # self.db.execute_write(sql)

                else:  # Just advance, not moved
                    self.db.execute_write(
                        "UPDATE " + DB_PROCESS + " SET stage = " + str(self.current_stage) + " WHERE id = " + str(
                            self.id))

            else:   # Advance stage no location change required
                # Add journal entry
                self.journal_write("<b>Stage Change</b> to {} after {} days {}"
                                   .format(next_stage_name, self.stage_days_elapsed, self.stage_name))
                self.current_stage += 1
                # Update the processes current stage
                self.db.execute_write(
                    "UPDATE " + DB_PROCESS + " SET stage = " + str(self.current_stage) + ", location = " + str(
                        self.stage_location) + " WHERE id = " + str(self.id))
            msg.setIcon(QMessageBox.Question)
            msg.setText("Was a feed completed")
            msg.setWindowTitle("Confirm Feeding")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if ret_val == QMessageBox.Yes:
                self.area_controller.main_window.feed_controller.set_last_feed_date(self.stage_location, datetime.now())
            self.process_load_stage_info()

    def change_location(self, from_loc, new_loc):
        self.db.execute_write(
            "UPDATE " + DB_PROCESS + " SET  location = " + str(
                new_loc) + " WHERE id = " + str(self.id))
        # now move the feed date
        if new_loc == 2:  # only necessary if moving into 1 or 2 as 3 doesn't have feeds
            sql = 'UPDATE {} SET dt = "{}" WHERE item = "{}" and id = 2 LIMIT 1'.format(DB_PROCESS_ADJUSTMENTS,
                                                                                        self.last_feed_date,
                                                                                        PA_FEED_DATE)
            self.db.execute_write(sql)
            sql = 'UPDATE {} SET dt = NULL WHERE item = "{}" and id = {} LIMIT 1'.format(DB_PROCESS_ADJUSTMENTS,
                                                                                         PA_FEED_DATE, from_loc)
            self.db.execute_write(sql)

        elif new_loc == 1:
            sql = 'UPDATE {} SET dt = NULL WHERE item = "{}" and id = {} LIMIT 1'.format(DB_PROCESS_ADJUSTMENTS,
                                                                                         PA_FEED_DATE, from_loc)
            self.db.execute_write(sql)
            sql = 'UPDATE {} SET dt = "{}" WHERE item = "{}" and id = 1 LIMIT 1'.format(DB_PROCESS_ADJUSTMENTS,
                                                                                        self.last_feed_date,
                                                                                        PA_FEED_DATE, from_loc)
            self.db.execute_write(sql)

        # Update areas
        sql = 'UPDATE {} SET area = {} WHERE area = {}'.format(DB_AREAS, new_loc, from_loc)
        self.db.execute_write(sql)

        # Update the location in process strains
        sql = 'UPDATE {} SET location = {} WHERE location = {} LIMIT 1'.format(DB_PROCESS_STRAINS, new_loc, from_loc)
        self.db.execute_write(sql)
        dt = datetime.strftime(datetime.now(), '%d/%m/%y %H:%M')
        self.journal_write(dt + "    Moved from area {} to area {} after {} days ".
                           format(from_loc, new_loc, self.stage_days_elapsed))

    def check_trans(self):
        """ This only check for warm up and normal. Cool is detected by check_light as it changes the switching times"""
        ct = datetime.now()
        if self.light_on < ct < (self.light_on + timedelta(seconds=self.warm_time)):
            if self.cool_warm != WARM:
                self.cool_warm = WARM
                self.area_controller.main_panel.update_trans(self.location, WARM)
                self.area_controller.cool_warm[self.location] = WARM
                self.area_controller.max_min_reset_process(DAY)
        elif self.light_off < ct + timedelta(hours=24) < (self.light_off + timedelta(seconds=self.cool_time)):
            if self.cool_warm != COOL:
                self.cool_warm = COOL
                self.area_controller.main_panel.update_trans(self.location, COOL)
                self.area_controller.cool_warm[self.location] = COOL
                self.area_controller.max_min_reset_process(NIGHT)
        else:
            if self.cool_warm != NORMAL:
                self.cool_warm = NORMAL
                self.area_controller.main_panel.update_trans(self.location, NORMAL)
                self.area_controller.cool_warm[self.location] = NORMAL
        return self.cool_warm

    def get_light_status(self) -> int:
        if not self.running:
            return 0
        ct = datetime.now()
        if ct > self.light_on:
            if ct > self.light_off:
                # print("light off")
                self.light_status = 0
            else:
                # print("light on")
                self.light_status = 1
        else:
            if ct > self.light_off:
                self.light_status = 1
                # print("light on")
            else:
                self.light_status = 0
        return self.light_status

    def check_light(self):
        """ Returns 0 for light off or 1 for light on"""
        if not self.running:
            return 0
        self.get_light_status()

        if self.light_status != self.light_status_last:
            self.load_temperature_adjustments()
            # @FixMe above line may have already been done
            if self.light_status == OFF and self.light_status_last == ON:
                print("resetting light times from on at {} off at {}".format(self.light_on, self.light_off))
                self.light_on = self.light_on + timedelta(days=1)
                self.light_off = self.light_off + timedelta(days=1)
                print("to new times on at {} off at {}".format(self.light_on, self.light_off))
                # self.cool_warm = COOL
                # self.area_controller.main_panel.update_trans(self.location, COOL)
                # self.area_controller.cool_warm[self.location] = COOL
                # self.area_controller.max_min_reset_process(NIGHT)

            self.light_status_last = self.light_status
            if self.light_status == 1:
                return 1
            else:
                return 0
                # print("light off")
        return self.light_status

    def day_advance(self):
        # Advances one day
        if not self.running:
            return
        self.running_days += 1
        self.stage_days_elapsed += 1
        self.stage_days_remaining -= 1
        self.days_total += 1

    def check_stage(self):
        """ Checks for stage end. Returns None until 7 days before stage end.
            Then it returns a list with the number of days remaining for each item
            -10 = Removed, 999 = Not in window yet, -100 = In drying"""
        if self.current_stage != 3:
            if not self.running:
                return
            self.stage_days_remaining = self.stage_total_duration - self.stage_days_elapsed
            #                 self.stage_offset = adj
            sd = (self.stages_start[self.current_stage - 1])  #
            ed = sd + timedelta(days=self.stage_total_duration)
            # wd = self.stage_total_duration - self.stage_days_elapsed
            if datetime.now() > ed:
                # Advance stage
                self.change_due = True
            # print(ed.date() - datetime.now().date())
            dd = ed.date() - datetime.now().date()
            # dd +=
            if dd.days - self.stages_len_adjustment[self.current_stage - 1] <= 7:  # Add on the adjustment
                return dd.days
            else:
                return None
        # For stage 3 only as it has flexible end
        if self.stage_days_elapsed < self.strain_shortest - 7:
            return None
        self.strain_window.clear()
        # self.strain_window.append(0)   # Dummy idx 0
        sql = "SELECT ps.item, ps.strain_id, st.duration_min, st.duration_max, ps.location FROM {} ps " \
              "INNER JOIN {} st ON st.id = ps.strain_id AND  ps.process_id = {} ORDER BY ps.item".\
            format(DB_PROCESS_STRAINS, DB_STRAINS, self.id)
        rows = self.db.execute(sql)
        self.strain_window.clear()
        # self.strain_window.append(0)
        for row in rows:
            # 0 = Not ready, 1 = ready in 7 days, 2 = ready, 3 = beyond window
            if row[4] == 0 or row[4] == 50:
                self.strain_window.append(-10)      # removed or finished
                continue
            if row[4] == 3:
                self.strain_window.append(-100)      # in drying
                continue
            if self.stage_days_elapsed > row[3]:
                self.strain_window.append(self.stage_days_elapsed - row[2])
            elif self.stage_days_elapsed >= row[2]:     # ready
                self.strain_window.append(self.stage_days_elapsed - row[2])
            elif self.stage_days_elapsed >= row[2] - 7:     # before
                self.strain_window.append(self.stage_days_elapsed - row[2])
            else:
                self.strain_window.append(999)   # Not in window

        print("Class process, check stage, strain window ", self.strain_window)

    # Helper functions
    @staticmethod
    def hr_from_datetime(the_dt):
        return datetime.strftime(the_dt, '%H')

    @staticmethod
    def time_from_datetime(the_dt):
        return datetime.strftime(the_dt, '%H:%M')

    @staticmethod
    def datetime_to_string(the_dt, format_):
        return datetime.strftime(the_dt, format_)
