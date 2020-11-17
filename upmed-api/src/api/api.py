import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))

from util import SuperBlueprint
from .appointment import appointment_endpoints
from .patient import patient_endpoints
from .hcp import hcp_endpoints

"""
Register appointment blueprints
---Heroku Imports----
from .appointment import appointment_endpoints
from .patient import patient_endpoints
from .hcp import hcp_endpoints
from util import SuperBlueprint
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))

---Relative Imports-----
from ..util import SuperBlueprint

from .hcp import hcp_endpoints
from .patient import patient_endpoints
from .appointment import appointment_endpoints

"""
api_endpoints = SuperBlueprint('appointment', __name__, url_prefix='')

# /hcp
api_endpoints.register_blueprint(hcp_endpoints, url_prefix='/hcp')

# /patients
api_endpoints.register_blueprint(patient_endpoints, url_prefix='/patient')

# /appointments
api_endpoints.register_blueprint(
    appointment_endpoints, url_prefix='/appointment')
