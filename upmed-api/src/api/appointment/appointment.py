from flask import Blueprint, request, jsonify, make_response
from util.firebase.db import Database
from util.util import Auth
from models.appointment import Appointment

import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '../..'))

"""
Appointment API

----Heroku Imports----
from flask import Blueprint, request, jsonify, make_response
from util.firebase.db import Database
from util.util import Auth
from models.appointment import Appointment

---Relative Imports----
from flask import Blueprint, request, jsonify, make_response, json
from ....src.util.firebase.db import Database
from ....src.util.util import Auth
from ....src.models.patient import Patient
from ....src.models.hcp import HCP
from ....src.models.health_event import HealthEvent
from ....src.models.hours import Hours
from ....src.models.day import Day
from ....src.util.util import Twilio
from ....src.models.appointment import Appointment

"""

pdb = Database()
hcp_db = pdb.getHCP()
patient_db = pdb.getPatients()
appointmentsdb = pdb.getAppointments()
auth = Auth()

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
    """
        Get the appointment details given appointment ID, request
        must be from concerned patient or healthcare professional.
        Request:
        {
            token: string
            appointmentId: string
        }
        Response:
        200 OK
        (Appointment object in JSON format)
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        try:
            pid, utype = Auth.decode_auth_token(auth_token)
            post_data = request.get_json()
            appointmentId = post_data.get('appointmentId')
            elements = appointmentId.split(',')

            if (utype == "HCP") and (str(pid) == str(elements[1])) or (
                    utype == "PATIENT") and (str(pid) == str(elements[0])):
                appointmentId = post_data.get('appointmentId')
                appointments_output = appointmentsdb.document(
                    str(appointmentId)).get().to_dict()

                response_object = {
                    "id": appointments_output['id'],
                    "date": appointments_output['date'],
                    "duration": appointments_output['duration'],
                    "doctor": appointments_output['doctor'],
                    "patient": appointments_output['patient'],
                    "subject": appointments_output['subject'],
                    "notes": appointments_output['notes'],
                    "videoUrl": appointments_output['videoUrl']
                }

                return make_response(jsonify(response_object)), 200

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Delete request not '
                               'originated from concerned patient or '
                               'healthcare professional.'
                }
                return make_response(jsonify(response_object)), 401
        except Exception as e:
            return f"An Error Occurred: {e}"
    else:
        response_object = {
            'status': 'fail',
            'message': 'Error in token authentication'
        }
        return make_response(jsonify(response_object)), 401


@appointment_endpoints.route('/getCalendar', methods=['POST'])
def get_calendar():
    """
        Get a list of Appointment IDs specific to the
        user from within the token.
        Request:
        {
            token: string
        }
        Response:
        200 OK
        ( List[AppointmentId] )
    """
    auth_token = request.get_json().get('token')

    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        output = []
        print(f'{utype} and {pid}')
        if utype == "PATIENT":
            docs = patient_db.document(str(pid)).get().to_dict()
            print(docs)
            output = docs['calendar']
        elif utype == "HCP":
            docs = hcp_db.document(str(pid)).get().to_dict()
            output = docs['calendar']
        else:
            response_object = {
                'Success': False,
                'message': 'Failed to verify role'
            }
            return make_response(jsonify(response_object)), 401
        calendar = []
        for event in output:
            appointments_output = appointmentsdb.document(
                str(event)).get().to_dict()
            calendar.append(appointments_output)
        return make_response(jsonify(calendar)), 200
    response_object = {
        'status': 'fail',
        'message': 'Error, in token authentication'
    }
    return make_response(jsonify(response_object)), 401


@appointment_endpoints.route('/createAppointment', methods=['POST'])
def create_appointment():
    """
    Create a new appointment given the appointment details,
    returns an unique appointment id
    Request:
            token: string
            date: int (UNIX Time)
            duration: int (0-1440 minutes)
            hcpid: str    (if patient initiate an appointment need
                to specify which hcp)
            patient: str  (if HCP initiate an appointment
                need to specify which patient)
            subject: str
            notes: Optional[str]
            videoUrl: Optional[str]
    Response:
    200 OK
    {
        appointmentId: string
    }
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        doctor_id = pid
        patient_id = pid
        post_data = request.get_json()

        # Check whether user is HCP or Patient
        if utype == "HCP":
            # Get the existing appointments:
            patient_id = post_data.get('patient')
        elif utype == "PATIENT":
            doctor_id = post_data.get('hcpid')
        else:
            response_object = {
                'Success': False,
                'message': 'Failed to verify role'
            }
            return make_response(jsonify(response_object)), 401

        appointment_id = str(patient_id) + "," + \
            str(doctor_id) + "," + str(post_data.get('date'))
        try:
            new_appointment = Appointment(
                id=appointment_id,
                date=post_data.get('date'),
                duration=post_data.get('duration'),
                doctor=str(doctor_id),
                patient=str(patient_id),
                subject=post_data.get('subject'),
                notes=post_data.get('notes'),
                videoUrl=post_data.get('videoUrl')
            )
            appointmentsdb.document(new_appointment.id).set({
                "id": new_appointment.id,
                "date": new_appointment.date,
                "duration": new_appointment.duration,
                "doctor": str(doctor_id),
                "patient": str(patient_id),
                "subject": new_appointment.subject,
                "notes": new_appointment.notes,
                "videoUrl": new_appointment.videoUrl
            })

            # Add the appointment id to both respective patient and HCP
            # database
            patient_ref = patient_db.document(str(patient_id))
            hcp_ref = hcp_db.document(str(doctor_id))

            # Get the existing list of appointments and append it
            patient_calendar = patient_ref.get().to_dict()['calendar']
            patient_calendar.append(appointment_id)
            patient_ref.update({u'calendar': patient_calendar})

            patient_doctors = patient_ref.get().to_dict()['doctors']
            if str(doctor_id) not in patient_doctors:
                patient_doctors.append(doctor_id)
                print('Updating docs')
                patient_ref.update({u'doctors': patient_doctors})

            hcp_patients = hcp_ref.get().to_dict()['patients']
            if str(patient_id) not in hcp_patients:
                hcp_patients.append(patient_id)
                print('Updating pats')
                hcp_ref.update({u'patients': hcp_patients})

            hcp_calendar = hcp_ref.get().to_dict()['calendar']
            hcp_calendar.append(appointment_id)
            hcp_ref.update({u'calendar': hcp_calendar})

            response_object = {
                "appointmentId": new_appointment.id
            }
            return make_response(jsonify(response_object)), 200
        except Exception as e:
            return f"Failure due to {e}", 404
    else:
        response_object = {
            'status': 'fail',
            'message': 'Error: Error in token authentication'
        }
        return make_response(jsonify(response_object)), 401


@appointment_endpoints.route('/delete_appointment', methods=['POST'])
def delete_appointment():
    """
        Remove appointment with the given appointment id,
        the request must originate from either the concerned patient
        or healthcare professional
        Request:
        {
            id: string
        }
        Response:
        200 OK
        {
            success: boolean
        }
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        try:
            pid, utype = Auth.decode_auth_token(auth_token)
            post_data = request.get_json()
            appointment_id = post_data.get('id')
            elements = appointment_id.split(',')
            doctor_id = str(elements[1])
            patient_id = str(elements[0])

            user_id_verified = False
            if (utype == "HCP") and (str(pid) == doctor_id) or (
                    utype == "PATIENT") and (str(pid) == patient_id):
                user_id_verified = True

            if user_id_verified:
                # Access both respective patient and HCP document
                patient_ref = patient_db.document(patient_id)
                hcp_ref = hcp_db.document(doctor_id)

                # Remove the appointment and update
                patient_calendar = patient_ref.get().to_dict()['calendar']
                patient_calendar.remove(appointment_id)
                patient_ref.update({u'calendar': patient_calendar})

                hcp_calendar = hcp_ref.get().to_dict()['calendar']
                hcp_calendar.remove(appointment_id)
                hcp_ref.update({u'calendar': hcp_calendar})

                appointmentsdb.document(appointment_id).delete()
                return jsonify({"success": True}), 200

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Delete request not originated from '
                               'concerned patient or healthcare professional.'
                }
                return make_response(jsonify(response_object)), 401
        except Exception as e:
            return f"An Error Occurred: {e}"
    else:
        response_object = {
            'status': 'fail',
            'message': 'Error in token authentication'
        }
        return make_response(jsonify(response_object)), 401
