from .day import Day

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
        res = [self.sunday.list(), self.monday.list(),
               self.tuesday.list(), self.wednesday.list(),
               self.thursday.list(), self.friday.list(), self.saturday.list()]
        return res

    def to_dict(self):
        res = {
            'sunday': self.sunday.__dict__,
            'monday': self.monday.__dict__,
            'tuesday': self.tuesday.__dict__,
            'wednesday': self.wednesday.__dict__,
            'thursday': self.thursday.__dict__,
            'friday': self.friday.__dict__,
            'saturday': self.saturday.__dict__,
        }
        return res
