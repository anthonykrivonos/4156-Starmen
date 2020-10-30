import os

from flask import Flask

from api.api import api_endpoints

"""
Create app and register blueprints
"""
app = Flask(__name__)
api_endpoints.bind_to_app(app)

@app.route('/api')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
