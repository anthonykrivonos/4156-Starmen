from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../..'))

from .db import Database  # noqa
