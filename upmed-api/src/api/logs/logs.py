import heroku3
from datetime import datetime

from flask import Blueprint

from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))

from src.util.env import Env


logs_endpoints = Blueprint('logs', __name__)

heroku_conn = heroku3.from_key(Env.HEROKU_API_KEY())
app = heroku_conn.apps()['upmed-api']


@logs_endpoints.route('/', methods=['GET'])
def root():
    logs = app.get_log()
    res = """
        <h1>Upmed Logs</h1>
        <h4>Last Updated %s</h4>
        <div>
            %s
        </div>
    """ % (datetime.today().strftime("%a %b %y @ %H:%M"), '<br/>'.join(logs.split('\n')))
    return res
