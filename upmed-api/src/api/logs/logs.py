from datetime import datetime
from flask import Blueprint
from sys import path
from os.path import join, dirname

path.append(dirname(__file__))
path.append(join(dirname(__file__), '../../..'))

from . import logs_helper  # noqa


logs_endpoints = Blueprint('logs', __name__)


@logs_endpoints.route('/', methods=['GET'])
def root():
    logs = logs_helper.get_logs()
    res = """
        <div style="font-family:monospace;">
            <h1>Upmed Logs</h1>
            <h4>Last Updated %s</h4>
            <div>
                %s
            </div>
        </div>
    """ % (datetime.today().strftime("%a %b %y @ %H:%M"),
           '<br/>'.join(logs.split('\n')))
    return res
