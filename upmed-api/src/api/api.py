from util import SuperBlueprint

from .hcp import hcp_endpoints
from .patient import patient_endpoints

"""
Register api blueprints
"""
api_endpoints = SuperBlueprint('api', __name__, url_prefix='/api')

# /api/hcp
api_endpoints.register_blueprint(hcp_endpoints, url_prefix='/hcp')

# /api/patients
api_endpoints.register_blueprint(patient_endpoints, url_prefix='/patient')
