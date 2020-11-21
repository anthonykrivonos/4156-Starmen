from enum import Enum

"""
Enums Model
"""


class Status(Enum):
    ACTIVE = 0
    NEVER = 1
    PAST = 2
    REMISSION = 3
    CURED = 4
