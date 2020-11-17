from .day import Day
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))
"""
    Hours Object Model
"""


class Hours:
    sunday: Day
    monday: Day
    tuesday: Day
    wednesday: Day
    thursday: Day
    friday: Day
    saturday: Day

    def __init__(
        self,
        sunday: Day,
        monday: Day,
        tuesday: Day,
        wednesday: Day,
        thursday: Day,
        friday: Day,
        saturday: Day,
    ):
        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday

    def inc(self):
        res = []
        res.append(list(self.sunday))
        res.append(list(self.monday))
        res.append(list(self.tuesday))
        res.append(list(self.wednesday))
        res.append(list(self.thursday))
        res.append(list(self.friday))
        res.append(list(self.saturday))
