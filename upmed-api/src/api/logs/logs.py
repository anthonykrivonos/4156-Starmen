import heroku3
from datetime import datetime

from flask import Blueprint

from .logs_helper import get_logs


logs_endpoints = Blueprint('logs', __name__)

@logs_endpoints.route('/', methods=['GET'])
def root():
    logs = get_logs()
    res = """
        <h1>Upmed Logs</h1>
        <h4>Last Updated %s</h4>
        <div>
            %s
        </div>
    """ % (datetime.today().strftime("%a %b %y @ %H:%M"), '<br/>'.join(logs.split('\n')))
    return res
