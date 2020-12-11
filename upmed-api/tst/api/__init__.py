from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../..'))

from .appointment_test import *
from .hcp_test import *
from .patient_test import *
