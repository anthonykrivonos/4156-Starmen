import os
from flask import Flask
from flask_cors import CORS

from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '..'))

from src.util.env import Env  # noqa
from src.api import api_endpoints  # noqa


"""
Create app and register blueprints
"""
app = Flask(__name__)
if Env.USE_CORS():
    CORS(app)
api_endpoints.bind_to_app(app)


@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)


if __name__ == "__main__":
    app.run(port=Env.PORT())
