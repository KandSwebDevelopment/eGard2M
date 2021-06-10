import collections

from PyQt5.QtCore import QObject
from defines import *
from class_process import ProcessClass


class AreaController(QObject):
    def __init__(self, parent):
        super(AreaController, self).__init__()
        self.my_parent = parent
        self.db = self.my_parent.db
        self.areas_pid = collections.defaultdict(int)                         # The PID in the area
        self.areas_items = collections.defaultdict(list)     # The items in the area
        self.areas_processes = collections.defaultdict(ProcessClass)

        self.load_areas()
        self.load_processes()

    def load_areas(self):
        """ Load the PID's and items for all the areas"""
        for area in range(1, 4):  # Areas 1 to 3, the only ones that can have a process
            sql = "SELECT process_id, item FROM {} WHERE area = {}".format(DB_AREAS, area)
            rows = self.db.execute(sql)
            if len(rows) > 0:
                self.areas_pid[area] = rows[0][0]
                items = []
                for row in rows:
                    items.append(row[1])
                self.areas_items[area] = items
            else:
                self.areas_pid[area] = 0
                self.areas_items[area] = []

    def load_processes(self):
        for p in self.areas_pid:
            if self.areas_pid[p] > 0:
                self.areas_processes[p] = ProcessClass(self.areas_pid[p], self.my_parent)

    def get_area_pid(self, area):
        """ Returns the PID in the area"""
        return self.areas_pid[area]

    def get_area_items(self, area):
        """ Returns a list of the items in the area"""
        return self.areas_items[area]

    def get_area_process(self, area):
        """
        Returns the process in the area
        :type area: int
        :rtype : ProcessClass
        """
        return self.areas_processes[area]
