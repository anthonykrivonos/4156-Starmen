from .enums import Status
from typing import Optional

"""
HealthEvent Data Model
"""


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
