import os
import atexit
import threading
import heroku3

from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../../..'))

from src.util.env import Env  # noqa
from src.util.util import is_unit_test  # noqa

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
th = None


def get_heroku_app():
    global app
    heroku_conn = heroku3.from_key(Env.HEROKU_API_KEY())
    app = heroku_conn.apps()['upmed-api']


def watch_logs():
    global app
    if app is not None:
        # Get initial logs
        with open(logs_path, "a") as f:
            f.write(app.get_log())

        # Continue watching logs
        for line in app.stream_log(lines=1):
            with open(logs_path, "a") as f:
                f.write(line.decode("utf-8") + "\n")


def delete_logs_on_exit():
    global th
    os.remove(logs_path)
    if th is not None:
        th.join()


if not is_unit_test():
    get_heroku_app()
    th = threading.Thread(target=watch_logs)
    th.start()
    atexit.register(delete_logs_on_exit)
