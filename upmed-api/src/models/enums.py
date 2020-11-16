import sys, os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))

from enum import Enum

class Status(Enum):
    ACTIVE = 0
    NEVER = 1
    PAST = 2
    REMISSION = 3
    CURED = 4
