from .day import Day

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
