from .appointment import appointment_endpoints
from .patient import patient_endpoints
from .hcp import hcp_endpoints
from .logs import logs_endpoints

from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../..'))

from src.util import SuperBlueprint  # noqa


# Blueprint containing all sub-blueprints
api_endpoints = SuperBlueprint('api', __name__, url_prefix='')

# /hcp
api_endpoints.register_blueprint(hcp_endpoints, url_prefix='/hcp')

# /patients
api_endpoints.register_blueprint(patient_endpoints, url_prefix='/patient')

# /logs
api_endpoints.register_blueprint(logs_endpoints, url_prefix='/logs')

# /appointments
api_endpoints.register_blueprint(
    appointment_endpoints, url_prefix='/appointment')
