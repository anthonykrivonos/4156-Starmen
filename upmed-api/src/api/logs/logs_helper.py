import os
import atexit
import threading
import heroku3

from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../../..'))

from src.util.env import Env  # noqa

logs_path = join(
    os.path.dirname(
        os.path.realpath(__file__)),
    'logs')

"""
Create empty file for logs to go into
"""
with open(logs_path, "w") as fp:
    pass

"""
Helper function to output logs
"""


def get_logs():
    logs = ""
    with open(logs_path, "r") as f:
        logs = f.read()
    return logs


"""
Begin tailing logs on run
"""
app = None


def get_heroku_app():
    heroku_conn = heroku3.from_key(Env.HEROKU_API_KEY())
    super.app = heroku_conn.apps()['upmed-api']


def watch_logs():
    if app is not None:
        for line in app.stream_log(lines=1):
            with open(logs_path, "a") as f:
                f.write(line.decode("utf-8") + "\n")


th = threading.Thread(target=watch_logs)
th.start()

"""
Delete logs before server closes
"""


def delete_logs_on_exit():
    os.remove(logs_path)
    th.join()


atexit.register(delete_logs_on_exit)
