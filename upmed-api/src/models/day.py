"""
Day Model
"""


class Day:
    startTime: int
    endTime: int

    def __init__(
        self,
        startTime: int,
        endTime: int,
    ):
        self.startTime = startTime
        self.endTime = endTime

    def list(self):
        res = []
        res.append(self.startTime)
        res.append(self.endTime)
        return str(res)
