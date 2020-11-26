from src.util.firebase.db import Database  # noqa
from src.util.util import Auth, Twilio #noqa
from src.models.appointment import Appointment  # noqa
from sys import path
from os.path import join, dirname


from twilio.jwt.access_token.grants import VideoGrant, ChatGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

path.append(join(dirname(__file__), '../../..'))

# Setup HCP and Patient Document Collections
auth = Auth()
pdb = Database()
hcp_db = pdb.getHCP()
patient_db = pdb.getPatients()
appointmentsdb = pdb.getAppointments()
twilio = Twilio()


def appointment_get_by_token(post_data):
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
    auth_token = post_data.get('token')
    if auth_token:
        try:
            pid, utype = Auth.decode_auth_token(auth_token)
            appointmentid = post_data.get('id')
            elements = appointmentid.split(',')
            if (utype == "HCP") and (str(pid) == str(elements[1])) or (
                    utype == "PATIENT") and (str(pid) == str(elements[0])):
                appointmentid = post_data.get('appointmentId')
                appointments_output = appointmentsdb.document(
                    str(appointmentid)).get().to_dict()
                try:
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
                    return response_object, 200
                except Exception as e:
                    response_object = {
                        'status': 'fail to extract appointment details',
                        'message': e
                    }
                    return response_object, 401

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Delete request not '
                               'originated from concerned patient or '
                               'healthcare professional.'
                }
                return response_object, 401
        except Exception as e:
            return f"An Error Occurred: {e}", 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Error in token authentication'
        }
        return response_object, 401


def appointment_get_calendar(post_data):
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
    auth_token = post_data.get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        if utype == "PATIENT":
            docs = patient_db.document(str(pid)).get().to_dict()
            output = docs['calendar']
        elif utype == "HCP":
            docs = hcp_db.document(str(pid)).get().to_dict()
            output = docs['calendar']
        else:
            response_object = {
                'Success': False,
                'message': 'Failed to verify role'
            }
            return response_object, 401
        calendar = []
        for event in output:
            appointments_output = appointmentsdb.document(
                str(event)).get().to_dict()
            calendar.append(appointments_output)
        return calendar, 200
    response_object = {
        'status': 'fail',
        'message': 'Error, in token authentication'
    }
    return response_object, 401


def delete_appointment(post_data):
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
    auth_token = post_data.get('token')
    if auth_token:
        try:
            pid, utype = Auth.decode_auth_token(auth_token)
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
                try:
                    patient_calendar.remove(appointment_id)
                except Exception:
                    pass
                patient_ref.update({u'calendar': patient_calendar})
                hcp_calendar = hcp_ref.get().to_dict()['calendar']
                try:
                    hcp_calendar.remove(appointment_id)
                except Exception:
                    pass
                hcp_ref.update({u'calendar': hcp_calendar})
                appointmentsdb.document(appointment_id).delete()
                response_object = {
                    'success': 'True'
                }
                return response_object, 200

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Delete request not originated from '
                               'concerned patient or health care professional.'
                }
                return response_object, 401
        except Exception as e:
            return f"An Error Occurred: {e}", 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Error in token authentication'
        }
        return response_object, 401


def create_appointment(post_data):
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
    auth_token = post_data.get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        doctor_id = pid
        patient_id = pid

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
            return response_object, 401

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
            return response_object, 200
        except Exception as e:
            return f"Failure due to {e}", 404
    else:
        response_object = {
            'status': 'fail',
            'message': 'Error: Error in token authentication'
        }
        return response_object, 401


def video(post_data):
    """
    Creates JWT Twlio Room token
    Request:
        appointmentId: string
        hcpToken: string?
        patientToken: string?
    Response:
        token: videoId
        id: AppointmentId
        date: number
        duration: number
        doctor: DoctorId
        patient: PatientId
        subject: string
    """
    auth_token = post_data.get('token')
    if auth_token:
        pid, _ = Auth.decode_auth_token(auth_token)

        appointment_id = post_data.get('appointmentId')
        appointments_output = appointmentsdb.document(
            str(appointment_id)).get().to_dict()
        print(appointments_output)
        if not (pid == appointments_output['patient'] or pid == appointments_output['doctor']):
            response_object ={
                "Success": False,
                "message": "Id not in appointment, unable to access room"
            }
            return response_object, 401

        conversation = get_chatroom(str(appointment_id))

        try:
            conversation.participants.create(identity=pid)
        except TwilioRestException as exc:
            # do not error if the user is already in the conversation
            if exc.status != 409:
                raise

        token = twilio.access_token(pid)
        token.add_grant(VideoGrant(room=str(appointment_id)))
        token.add_grant(ChatGrant(service_sid=conversation.chat_service_sid))

        response_object = {
            "accessToken": token.to_jwt().decode(),
            "id": appointments_output['id'],
            "date": appointments_output['date'],
            "duration": appointments_output['duration'],
            "doctor": appointments_output['doctor'],
            "patient": appointments_output['patient'],
            "subject": appointments_output['subject'],
            "notes": appointments_output['notes']
        }
        return response_object, 200
    else:
        response_object = {
            'Success': False,
            'message': 'Failed to verify role'
        }
        return response_object, 401


def get_chatroom(name):
    client = twilio.connect()
    for conversation in client.conversations.conversations.list():
        if conversation.friendly_name == name:
            return conversation

    # a conversation with the given name does not exist ==> create a new one
    return client.conversations.conversations.create(
        friendly_name=name)
