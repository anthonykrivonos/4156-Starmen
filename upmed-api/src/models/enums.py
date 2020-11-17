from enum import Enum
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))

"""Enums Data Model
    """


class Status(Enum):
    ACTIVE = 0
    NEVER = 1
    PAST = 2
    REMISSION = 3
    CURED = 4
