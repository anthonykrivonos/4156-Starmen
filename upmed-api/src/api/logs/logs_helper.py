import os
import atexit
import heroku3
import threading

from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))

from src.util.env import Env  # noqa

heroku_conn = heroku3.from_key(Env.HEROKU_API_KEY())
app = heroku_conn.apps()['upmed-api']


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
Begin tailing logs on run
"""
def watch_logs():
    for line in app.stream_log(lines=1):
        with open(logs_path, "a") as f:
            f.write(line.decode("utf-8") + "\n")
th = threading.Thread(target=watch_logs)
th.start()

"""
Helper function to output logs
"""
def get_logs():
    logs = ""
    with open(logs_path, "r") as f:
        logs = f.read()
    return logs

"""
Delete logs before server closes
"""
def delete_logs_on_exit():
    os.remove(logs_path)
    th.join()
atexit.register(delete_logs_on_exit)
