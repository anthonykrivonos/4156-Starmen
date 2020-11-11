import os

from util.env import Env
from flask import Flask

from api import api_endpoints

"""
Create app and register blueprints
"""
app = Flask(__name__)
api_endpoints.bind_to_app(app)

@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)

if __name__ == "__main__":
    app.run(port=Env.PORT())
