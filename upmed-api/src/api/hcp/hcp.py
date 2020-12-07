from os.path import join, dirname
from sys import path
from flask import Blueprint, request, jsonify, make_response
from .hcp_helper import hcp_signup, hcp_login, hcp_delete, hcp_set_record,\
    hcp_get_by_token, hcp_notify, hcp_get_all, \
    hcp_test_number, hcp_edit_profile, hcp_get_patients, hcp_search, \
    hcp_set_health_events, hcp_set_profile_picture \

path.append(join(dirname(__file__), '../../..'))

from src.util.firebase.db import Database  # noqa
from src.util.util import Auth, Twilio  # noqa
from src.models.hcp import HCP  # noqa
from src.models.hours import Hours  # noqa
from src.models.day import Day  # noqa
from src.models.health_event import HealthEvent  # noqa
from src.models.patient import Patient  # noqa
from src.models.appointment import Appointment  # noqa


# Setup HCP and Patient Document Collections
db = Database()
hcpdb = db.getHCP()
pat = db.getPatients()
appointmentsdb = db.getAppointments()
auth = Auth()
twilio = Twilio()

hcp_endpoints = Blueprint('hcp', __name__)
default_pic = 'https://www.flaticon.com/svg/static/icons/svg/387/387561.svg'
invalid_token = 'Provide a valid auth token'
nonHCP = 'Not an HCP.'


@hcp_endpoints.route('/')
def root():
    return "hcp"


@hcp_endpoints.route('/logIn', methods=['POST'])
def login():
    """HCP Logins

    Returns:
            Response: JSON
    """
    try:
        pid = request.json['id']
        email = request.json['email']
        resp = hcp_login(hcpdb, pid, email)
        if resp != 0:
            return jsonify(resp), 200
        else:
            return "False", 404
    except Exception as e:
        return f"An Error Occured: {e}"


@hcp_endpoints.route('/signUp', methods=['POST'])
def signup():
    """New HCP creates profile

    Returns:
            Response: JSON
    """

    post_data = request.get_json()
    print(post_data)
    schedule = make_week()
    try:
        hcp = HCP(
            id=post_data.get('id'),
            firstName=post_data.get('firstName'),
            lastName=post_data.get('lastName'),
            phone=str(post_data.get('phone')),
            email=post_data.get('email'),
            specialty='',
            profilePicture='',
            calendar=[],
            title='',
            patients=[],
            hours=schedule
        )
        try:
            hcp.specialty = post_data.get('specialty')
        except Exception as e:
            hcp.specialty = ''

        try:
            hcp.title = post_data.get('title')
        except Exception as e:
            hcp.title = ''

        try:
            hcp.profilePicture = post_data.get('profilePicture')
        except Exception as e:
            hcp.profilePicture = default_pic

        if hcp.profilePicture is None:
            hcp.profilePicture = default_pic

        newsched = post_data.get('hours')
        print(newsched)
        if newsched['sunday']['startTime'] == \
                -1 and newsched['sunday']['endTime'] == -1:
            hcp.hours.sunday.startTime = -1
            hcp.hours.sunday.endTime = -1
        elif 0 <= newsched['sunday']['startTime'] \
                <= newsched['sunday']['endTime']:
            hcp.hours.sunday.startTime = newsched['sunday']['startTime']
            hcp.hours.sunday.endTime = newsched['sunday']['endTime']

        if newsched['monday']['startTime'] == \
                -1 and newsched['monday']['endTime'] == -1:
            hcp.hours.monday.startTime = -1
            hcp.hours.monday.endTime = -1
        elif 0 <= newsched['monday']['startTime'] \
                <= newsched['monday']['endTime']:
            hcp.hours.monday.startTime = newsched['monday']['startTime']
            hcp.hours.monday.endTime = newsched['monday']['endTime']

        if newsched['tuesday']['startTime'] == \
                -1 and newsched['tuesday']['endTime'] == -1:
            hcp.hours.tuesday.startTime = -1
            hcp.hours.tuesday.endTime = -1
        elif 0 <= newsched['tuesday']['startTime'] \
                <= newsched['tuesday']['endTime']:
            hcp.hours.tuesday.startTime = newsched['tuesday']['startTime']
            hcp.hours.tuesday.endTime = newsched['tuesday']['endTime']

        if newsched['wednesday']['startTime'] == \
                -1 and newsched['wednesday']['endTime'] == -1:
            hcp.hours.wednesday.startTime = -1
            hcp.hours.wednesday.endTime = -1
        elif 0 <= newsched['wednesday']['startTime'] \
                <= newsched['wednesday']['endTime']:
            hcp.hours.wednesday.startTime = newsched['wednesday']['startTime']
            hcp.hours.wednesday.endTime = newsched['wednesday']['endTime']

        if newsched['thursday']['startTime'] == \
                -1 and newsched['thursday']['endTime'] == -1:
            hcp.hours.thursday.startTime = -1
            hcp.hours.thursday.endTime = -1
        elif 0 <= newsched['thursday']['startTime'] \
                <= newsched['thursday']['endTime']:
            hcp.hours.thursday.startTime = newsched['thursday']['startTime']
            hcp.hours.thursday.endTime = newsched['thursday']['endTime']

        if newsched['friday']['startTime'] == \
                -1 and newsched['friday']['endTime'] == -1:
            hcp.hours.friday.startTime = -1
            hcp.hours.friday.endTime = -1
        elif 0 <= newsched['friday']['startTime'] \
                <= newsched['friday']['endTime']:
            hcp.hours.friday.startTime = newsched['friday']['startTime']
            hcp.hours.friday.endTime = newsched['friday']['endTime']

        if newsched['saturday']['startTime'] == \
                -1 and newsched['saturday']['endTime'] == -1:
            hcp.hours.sunday.saturday = -1
            hcp.hours.sunday.saturday = -1
        elif 0 <= newsched['saturday']['startTime'] \
                <= newsched['saturday']['endTime']:
            hcp.hours.saturday.startTime = newsched['saturday']['startTime']
            hcp.hours.saturday.endTime = newsched['saturday']['endTime']
        hours = []
        time = []
        time.append(hcp.hours.sunday.startTime)
        time.append(hcp.hours.sunday.endTime)
        hours.append(str(time))
        time[0] = hcp.hours.monday.startTime
        time[1] = hcp.hours.monday.endTime
        hours.append(str(time))
        time[0] = hcp.hours.tuesday.startTime
        time[1] = hcp.hours.tuesday.endTime
        hours.append(str(time))
        time[0] = hcp.hours.wednesday.startTime
        time[1] = hcp.hours.wednesday.endTime
        hours.append(str(time))
        time[0] = hcp.hours.thursday.startTime
        time[1] = hcp.hours.thursday.endTime
        hours.append(str(time))
        time[0] = hcp.hours.friday.startTime
        time[1] = hcp.hours.friday.endTime
        hours.append(str(time))
        time[0] = hcp.hours.saturday.startTime
        time[1] = hcp.hours.saturday.endTime
        hours.append(str(time))

        # Helper function
        res = hcp_signup(hcpdb, hcp, hours, post_data.get('npi'))
        if res != 0:
            response_object = {
                'id': hcp.id,
                'token': res
            }
            return make_response(jsonify(response_object)), 201
        else:
            response_object = {
                "message": "Unable to signup."
            }
            return make_response(jsonify(response_object)), 401
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': f'Some error, {e} occurred. Please try again.'
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/delete', methods=['POST'])
def remove():
    """
            delete() : Delete a document from Firestore collection.
    """
    post_data = request.get_json()

    try:
        # Check for ID in URL query
        pid = post_data.get('id')
        res = hcp_delete(hcpdb, pid)
        print(pid, res)
        if res:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 400
    except Exception as e:
        return f"An Error Occured: {e}"


@hcp_endpoints.route('/getByToken', methods=['POST'])
def getbytoken():
    """Get HCP by token

    Returns: Response: JSON
    """
    # Get Auth Token
    auth_token = request.get_json()
    auth_token = auth_token.get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        if utype == "HCP":
            resp = hcp_get_by_token(hcpdb, hid)
            hours = {
                "sunday": {
                    "startTime": resp.hours.sunday.startTime,
                    "endTime": resp.hours.sunday.endTime
                },
                "monday": {
                    "startTime": resp.hours.monday.startTime,
                    "endTime": resp.hours.monday.endTime
                },
                "tuesday": {
                    "startTime": resp.hours.tuesday.startTime,
                    "endTime": resp.hours.tuesday.endTime
                },
                "wednesday": {
                    "startTime": resp.hours.wednesday.startTime,
                    "endTime": resp.hours.wednesday.endTime
                },
                "thursday": {
                    "startTime": resp.hours.thursday.startTime,
                    "endTime": resp.hours.thursday.endTime
                },
                "friday": {
                    "startTime": resp.hours.friday.startTime,
                    "endTime": resp.hours.friday.endTime
                },
                "saturday": {
                    "startTime": resp.hours.saturday.startTime,
                    "endTime": resp.hours.saturday.endTime
                }
            }
            response_object = {
                "id": resp.id,
                "firstName": resp.firstName,
                "lastName": resp.lastName,
                "phone": resp.phone,
                "email": resp.email,
                "profilePicture": resp.profilePicture,
                "calendar": resp.calendar,
                "specialty": resp.specialty,
                "hours": hours,
                "patients": resp.patients,
                "title": resp.title,
            }
            return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'Success': False,
                'message': nonHCP
            }
            return make_response(response_object), 401
    else:
        response_object = {
            'status': 'fail',
            'message': invalid_token
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/setRecord', methods=['POST'])
def set_health_event():
    """
    Creates a health event given an HCP token, a patient ID
    and the criteria of a health event
    :return: HealthEvent
    """
    post_data = request.get_json()
    auth_token = post_data.get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        if utype == "HCP":
            try:
                pid = post_data.get('id')
                patient = pat.document(str(pid)).get().to_dict()
                event = HealthEvent(
                    date=post_data.get('date'),
                    event=post_data.get('event'),
                    remarks=post_data.get('remarks'),
                    status=post_data.get('status')
                )
                jsonevent = {
                    "date": event.date,
                    "event": event.event,
                    "remarks": event.remarks,
                    "status": event.status
                }
                resp = Patient(
                    id=patient['id'],
                    firstName=patient['firstName'],
                    lastName=patient['lastName'],
                    phone=patient['phone'],
                    email=patient['email'],
                    dateOfBirth=patient['dateOfBirth'],
                    sex=patient['sex'],
                    profilePicture=patient['profilePicture'],
                    height=patient['height'],
                    weight=patient['weight'],
                    drinker=patient['drinker'],
                    smoker=patient['smoker'],
                    calendar=patient['calendar'],
                    doctors=patient['doctors'],
                    health=patient['health']
                )
                resp.health.append(jsonevent)
                listevents = []
                for i in resp.health:
                    listevents.append(i)
                res = hcp_set_record(pat, resp)
                if res:
                    return make_response(jsonify(jsonevent)), 201
                else:
                    return make_response(jsonify(jsonevent)), 401
            except Exception as e:
                return f"Unable to find {post_data.get('id')} because {e}", 404
        else:
            response_object = {
                'Success': False,
                'message': nonHCP
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': invalid_token
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/notify', methods=['POST'])
def notify():
    """
    Notify patient of appoint
        Request{
                token: string
                appointment_d: string
        }
    :return: Response
    """
    post_data = request.get_json()
    auth_token = post_data.get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        if utype == "HCP":
            try:
                appointment_id = post_data.get('id')
                res = hcp_notify(appointmentsdb, pat, appointment_id)
            except Exception as e:
                return f"Unable to find {post_data.get('id')} because {e}", 400
            return make_response(jsonify(res)), 200
        else:
            response_object = {
                'Success': False,
                'message': nonHCP
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': invalid_token
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/testNumber', methods=['POST'])
def test_number():
    """
    Notify patient of appoint
        Request{
                token: string
                appointment_id: string
        }
    :return: Response
    """
    post_data = request.get_json()
    auth_token = post_data.get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        if utype == "HCP":
            appointment_id = post_data.get('id')
            res = hcp_test_number(appointmentsdb, pat, appointment_id)
            if res:
                return make_response(jsonify(res)), 200
        else:
            response_object = {
                'Success': False,
                'message': nonHCP
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': invalid_token
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/editProfile', methods=['POST'])
def edit_hcp_profile():
    """
    Edit existing HCP profile

        Returns:
                Response: JSON
        """
    post_data = request.get_json()
    auth_token = post_data.get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        # Get the ids of the HCPs of patient
        if utype == "HCP":
            try:
                response_object = hcp_edit_profile(hcpdb, hid, post_data)
                if response_object['Success']:
                    return make_response(jsonify(response_object)), 200
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': f'Some error, {e} occurred. Please try again.'
                }
                return make_response(jsonify(response_object)), 401
    response_object = {
        'status': 'fail',
        'message': f'Fail to edit HCP profile'
    }
    return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/getPatients', methods=['POST'])
def getpatients():
    """
    Get Patient from token
    :return: Patient
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        # Get the ids of the HCPs of patient
        if utype == "HCP":
            res = hcp_get_patients(hcpdb, pat, hid)
            return make_response(jsonify(res)), 200
        else:
            response_object = {
                'Success': False,
                'message': nonHCP
            }
            return make_response(response_object), 401
    else:
        response_object = {
            'status': 'fail',
            'message': invalid_token
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/setRecords', methods=['POST'])
def set_health_events():
    """
    Creates a health event given an HCP token, a patient ID
    and the criteria of a health event
    :return: HealthEvent
    """
    post_data = request.get_json()
    auth_token = post_data.get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        if utype == "HCP":
            try:
                pid = post_data.get('id')
                resp = hcp_set_health_events(pat, pid, post_data)
            except Exception as e:
                return f"Unable to find {post_data.get('id')} because {e}", 404
            return make_response(jsonify(resp.health)), 200
        else:
            response_object = {
                'Success': False,
                'message': nonHCP
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': invalid_token
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/getAll', methods=['POST'])
def get_all():
    """
        Get all HCPs

        Returns:
                List[HCP]
        :return:
        """

    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        hcps_return = hcp_get_all(hcpdb)
        return jsonify(hcps_return), 200
    else:
        response_object = {
            'status': 'fail',
            'message': invalid_token
        }
        return make_response(jsonify(response_object)), 401


def make_week():
    """
    Makes a blank schedule
    :return: Hours object
    """
    week = []
    for _ in range(0, 7):
        week.append(Day(
            startTime=-1,
            endTime=-1,
        )
        )
    schedule = Hours(
        sunday=week[0],
        monday=week[1],
        tuesday=week[2],
        wednesday=week[3],
        thursday=week[4],
        friday=week[5],
        saturday=week[6]
    )
    return schedule


@hcp_endpoints.route('/setProfilePicture', methods=['POST'])
def set_profile_picture():
    """
    Set HCP Profile Picture

    Returns: Response: JSON
    """
    # Get Auth Token
    post_data = request.get_json()
    auth_token = post_data.get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        pic = post_data.get('profilePicture')
        res = hcp_set_profile_picture(hcpdb, hid, pic)
        if res:
            response_object = {
                "Success": True,
                "profilePicture": pic
            }
            return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': "no response from helper function"
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': "invalid_token"
        }
        return make_response(jsonify(response_object)), 401


@hcp_endpoints.route('/search', methods=['POST'])
def search():
    """
    Searches for a Patient from input

    Returns: Response: JSON
    """
    # Get Auth Token
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        text = request.get_json().get('text')
        if len(text) >= 3:
            res = hcp_search(text)
        else:
            response_object = {
                "Success": False,
                "Not long enough": text
            }
            return make_response(jsonify(response_object)), 400
        if res:
            return make_response(jsonify(res)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Unable to find patient with query'
            }
            return make_response(jsonify(response_object)), 404
    else:
        response_object = {
            'status': 'fail',
            'message': "invalid_token"
        }
        return make_response(jsonify(response_object)), 401
