import sys, os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))

from typing import Optional

from .enums import Status

class HealthEvent:
    date: int
    event: str
    remarks: Optional[str]
    status: Status

    def __init__(
        self,
        date: int,
        event: str,
        remarks: Optional[str],
        status: Status,
    ):
        self.date = date
        self.event = event
        self.remarks = remarks
        self.status = status
