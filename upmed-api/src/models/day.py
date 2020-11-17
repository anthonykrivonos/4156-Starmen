import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))


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
        return res
