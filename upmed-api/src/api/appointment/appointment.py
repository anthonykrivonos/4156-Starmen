from flask import Blueprint, request, jsonify, make_response


from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))

from src.util.firebase.db import Database  # noqa
from src.util import Auth  # noqa
from src.models.appointment import Appointment  # noqa
from src.api.appointment import appointment_helper  # noqa

pdb = Database()
hcp_db = pdb.getHCP()
patient_db = pdb.getPatients()
appointmentsdb = pdb.getAppointments()
auth = Auth()


path.append(join(dirname(__file__), '../../..'))
appointment_endpoints = Blueprint('appointment', __name__)


@appointment_endpoints.route('/')
def root():
    """
    Deafault Route

    Returns:
        reponse: string
    """
    return "appointment root"


@appointment_endpoints.route('/getByToken', methods=['POST'])
def get_by_token():
    post_data = request.get_json()
    response, status_code = appointment_helper.appointment_get_by_token(
        post_data)
    return make_response(jsonify(response), status_code)


@appointment_endpoints.route('/getCalendar', methods=['POST'])
def get_calendar():
    post_data = request.get_json()
    response, status_code = appointment_helper.appointment_get_calendar(
        post_data)
    return make_response(jsonify(response), status_code)


@appointment_endpoints.route('/createAppointment', methods=['POST'])
def create_appointment():
    post_data = request.get_json()
    response, status_code = appointment_helper.create_appointment(post_data)
    return make_response(jsonify(response), status_code)


@appointment_endpoints.route('/delete_appointment', methods=['POST'])
def delete_appointment():
    post_data = request.get_json()
    response, status_code = appointment_helper.delete_appointment(post_data)
    return make_response(jsonify(response), status_code)


@appointment_endpoints.route('/video', methods=['POST'])
def create_room():
    post_data = request.get_json()
    response, status_code = appointment_helper.video(post_data)
    return make_response(jsonify(response), status_code)
