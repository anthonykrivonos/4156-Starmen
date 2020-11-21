import datetime
from flask import Blueprint, request, jsonify, make_response

from sys import path
from os.path import join, dirname
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
        res = hcpdb.document(str(pid)).get()
        res = res.to_dict()
        if res['email'] == email:
            utype = "HCP"
            auth_token = auth.encode_auth_token(pid, utype)
            resp = {
                "id": pid,
                "token": auth_token.decode()
            }
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

        utype = "HCP"
        hcpdb.document(hcp.id).set({
            "id": hcp.id,
            "firstName": hcp.firstName,
            "lastName": hcp.lastName,
            "phone": hcp.phone,
            "email": hcp.email,
            "profilePicture": hcp.profilePicture,
            "calendar": hcp.calendar,
            "specialty": hcp.specialty,
            "title": hcp.title,
            "hours": hours,
            "patients": hcp.patients
        })
        auth_token = auth.encode_auth_token(hcp.id, utype)
        response_object = {
            'id': hcp.id,
            'token': auth_token.decode()
        }
        return make_response(jsonify(response_object)), 201
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
        hcpdb.document(pid).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@hcp_endpoints.route('/getByToken', methods=['POST'])
def getbytoken():
    """Get HCP by token

    Returns: Response: JSON
    """
    # Get Auth Token
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        if utype == "HCP":
            schedule = make_week()
            hcp = hcpdb.document(hid).get().to_dict()
            resp = HCP(
                id=hcp['id'],
                firstName=hcp['firstName'],
                lastName=hcp['lastName'],
                phone=hcp['phone'],
                email=hcp['email'],
                specialty=hcp['specialty'],
                profilePicture=hcp['profilePicture'],
                calendar=[],
                title=hcp['title'],
                patients=[],
                hours=schedule
            )

            newsched = hcp['hours']
            res = newsched[0].strip('][').split(', ')

            resp.hours.sunday.startTime = res[0]
            resp.hours.sunday.endTime = res[1]
            res = newsched[1].strip('][').split(', ')
            resp.hours.monday.startTime = res[0]
            resp.hours.monday.endTime = res[1]
            res = newsched[2].strip('][').split(', ')
            resp.hours.tuesday.startTime = res[0]
            resp.hours.tuesday.endTime = res[1]
            res = newsched[3].strip('][').split(', ')
            resp.hours.wednesday.startTime = res[0]
            resp.hours.wednesday.endTime = res[1]
            res = newsched[4].strip('][').split(', ')
            resp.hours.thursday.startTime = res[0]
            resp.hours.thursday.endTime = res[1]
            res = newsched[5].strip('][').split(', ')
            resp.hours.friday.startTime = res[0]
            resp.hours.friday.endTime = res[1]
            res = newsched[6].strip('][').split(', ')
            resp.hours.saturday.startTime = res[0]
            resp.hours.saturday.endTime = res[1]

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
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        post_data = request.get_json()
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
                pat.document(resp.id).set({
                    "id": resp.id,
                    "firstName": resp.firstName,
                    "lastName": resp.lastName,
                    "phone": resp.phone,
                    "email": resp.email,
                    "dateOfBirth": resp.dateOfBirth,
                    "sex": resp.sex,
                    "profilePicture": resp.profilePicture,
                    "height": resp.height,
                    "weight": resp.weight,
                    "drinker": resp.drinker,
                    "smoker": resp.smoker,
                    "calendar": resp.calendar,
                    "health": resp.health,
                    "doctors": resp.doctors
                })
            except Exception as e:
                return f"Unable to find {post_data.get('id')} because {e}", 404

            return make_response(jsonify(jsonevent)), 201
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

    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        post_data = request.get_json()
        # print(f'{hid} and {utype}')
        if utype == "HCP":
            try:
                appointment_id = post_data.get('id')
                appointment_resp = appointmentsdb.document(
                    str(appointment_id)).get().to_dict()
                appointment = Appointment(
                    id=appointment_resp['id'],
                    date=appointment_resp['date'],
                    duration=appointment_resp['duration'],
                    doctor=appointment_resp['doctor'],
                    patient=appointment_resp['patient'],
                    subject=appointment_resp['subject'],
                    notes=appointment_resp['notes'],
                    videoUrl=appointment_resp['videoUrl']
                )
                patient = pat.document(
                    str(appointment.patient)).get().to_dict()
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

                client = twilio.connect()
                message = client.messages.create(
                    body=f"Hi {resp.firstName} you have an appointment at "
                         f"{datetime.datetime.fromtimestamp(appointment.date / 1e3)} join at "
                    f"{appointment.videoUrl}",
                    from_='+19036182297',
                    to=f'+1{str(resp.phone).replace("", "")}')
                print(message)
                print(datetime.datetime.fromtimestamp(appointment.date / 1e3))
                res = {
                    "Success": True
                }

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

    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        post_data = request.get_json()
        # print(f'{hid} and {utype}')
        if utype == "HCP":
            try:
                appointment_id = post_data.get('id')
                appointment_resp = appointmentsdb.document(
                    str(appointment_id)).get().to_dict()
                appointment = Appointment(
                    id=appointment_resp['id'],
                    date=appointment_resp['date'],
                    duration=appointment_resp['duration'],
                    doctor=appointment_resp['doctor'],
                    patient=appointment_resp['patient'],
                    subject=appointment_resp['subject'],
                    notes=appointment_resp['notes'],
                    videoUrl=appointment_resp['videoUrl']
                )
                patient = pat.document(
                    str(appointment.patient)).get().to_dict()
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

                client = twilio.connect()
                message = client.messages.create(
                    body=f"Hi {resp.firstName} you have an appointment at "
                         f"{datetime.datetime.fromtimestamp(appointment.date / 1e3)} join at "
                    f"{appointment.videoUrl}",
                    from_='+19036182297',
                    to=f'+1{str(resp.phone).replace("", "")}')
                print(message)
                print(datetime.datetime.fromtimestamp(appointment.date / 1e3))
                res = {
                    "Success": True
                }

            except Exception as e:
                print(f"Unable to find {post_data.get('id')} because {e}")
                res = {
                    "Success": False
                }
                return make_response(jsonify(res)), 200

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
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        # Get the ids of the HCPs of patient
        if utype == "HCP":
            hcp_resp = hcpdb.document(str(hid)).get().to_dict()
            post_data = request.get_json()
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
                    calendar=hcp_resp['calendar'],
                    title='',
                    patients=hcp_resp['patients'],
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

                if int(newsched['sunday']['startTime']) == \
                        -1 and int(newsched['sunday']['endTime']) == -1:
                    hcp.hours.sunday.startTime = -1
                    hcp.hours.sunday.endTime = -1
                elif 0 <= int(newsched['sunday']['startTime']) \
                        <= int(newsched['sunday']['endTime']):
                    hcp.hours.sunday.startTime = int(
                        newsched['sunday']['startTime'])
                    hcp.hours.sunday.endTime = int(
                        newsched['sunday']['endTime'])

                if int(newsched['monday']['startTime']) == \
                        -1 and int(newsched['monday']['endTime']) == -1:
                    hcp.hours.monday.startTime = -1
                    hcp.hours.monday.endTime = -1
                elif 0 <= int(newsched['monday']['startTime']) \
                        <= int(newsched['monday']['endTime']):
                    hcp.hours.monday.startTime = int(
                        newsched['monday']['startTime'])
                    hcp.hours.monday.endTime = int(
                        newsched['monday']['endTime'])

                if int(newsched['tuesday']['startTime']) == \
                        -1 and int(newsched['tuesday']['endTime']) == -1:
                    hcp.hours.tuesday.startTime = -1
                    hcp.hours.tuesday.endTime = -1
                elif 0 <= int(newsched['tuesday']['startTime']) \
                        <= int(newsched['tuesday']['endTime']):
                    hcp.hours.tuesday.startTime = int(
                        newsched['tuesday']['startTime'])
                    hcp.hours.tuesday.endTime = int(
                        newsched['tuesday']['endTime'])

                if int(newsched['wednesday']['startTime']) == \
                        -1 and int(newsched['wednesday']['endTime']) == -1:
                    hcp.hours.wednesday.startTime = -1
                    hcp.hours.wednesday.endTime = -1
                elif 0 <= int(newsched['wednesday']['startTime']) \
                        <= int(newsched['wednesday']['endTime']):
                    hcp.hours.wednesday.startTime = int(
                        newsched['wednesday']['startTime'])
                    hcp.hours.wednesday.endTime = int(
                        newsched['wednesday']['endTime'])

                if int(newsched['thursday']['startTime']) == \
                        -1 and int(newsched['thursday']['endTime']) == -1:
                    hcp.hours.thursday.startTime = -1
                    hcp.hours.thursday.endTime = -1
                elif 0 <= int(newsched['thursday']['startTime']) \
                        <= int(newsched['thursday']['endTime']):
                    hcp.hours.thursday.startTime = int(
                        newsched['thursday']['startTime'])
                    hcp.hours.thursday.endTime = int(
                        newsched['thursday']['endTime'])

                if int(newsched['friday']['startTime']) == \
                        -1 and int(newsched['friday']['endTime']) == -1:
                    hcp.hours.friday.startTime = -1
                    hcp.hours.friday.endTime = -1
                elif 0 <= int(newsched['friday']['startTime']) \
                        <= int(newsched['friday']['endTime']):
                    hcp.hours.friday.startTime = int(
                        newsched['friday']['startTime'])
                    hcp.hours.friday.endTime = int(
                        newsched['friday']['endTime'])

                if int(newsched['saturday']['startTime']) == \
                        -1 and int(newsched['saturday']['endTime']) == -1:
                    hcp.hours.sunday.saturday = -1
                    hcp.hours.sunday.saturday = -1
                elif 0 <= int(newsched['saturday']['startTime']) \
                        <= int(newsched['saturday']['endTime']):
                    hcp.hours.saturday.startTime = int(
                        newsched['saturday']['startTime'])
                    hcp.hours.saturday.endTime = int(
                        newsched['saturday']['endTime'])

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

                if hid == hcp.id:
                    hcpdb.document(hcp.id).set({
                        "id": hcp.id,
                        "firstName": hcp.firstName,
                        "lastName": hcp.lastName,
                        "phone": hcp.phone,
                        "email": hcp.email,
                        "profilePicture": hcp.profilePicture,
                        "calendar": hcp.calendar,
                        "specialty": hcp.specialty,
                        "title": hcp.title,
                        "hours": hours,
                        "patients": hcp.patients,
                    })
                else:
                    response_object = {
                        'status': 'fail',
                        'message': invalid_token
                    }
                    return make_response(jsonify(response_object)), 401
                response_object = {
                    "Success": True
                }
                return make_response(jsonify(response_object)), 200
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': f'Some error, {e} occurred. Please try again.'
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
            hcp_resp = hcpdb.document(str(hid)).get().to_dict()
            res = {}
            for i in hcp_resp['patients']:
                pats = pat.document(str(i)).get().to_dict()
                entry = {
                    i: pats
                }
                res.update(entry)
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
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        post_data = request.get_json()
        if utype == "HCP":
            try:
                pid = post_data.get('id')
                patient = pat.document(str(pid)).get().to_dict()
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
                    health=[]
                )

                # Get a list of health events
                for ev in post_data.get('health'):
                    event = HealthEvent(
                        date=ev['date'],
                        event=ev['event'],
                        remarks=ev['remarks'] if 'remarks' in ev else '',
                        status=ev['status']
                    )
                    jsonevent = {
                        "date": event.date,
                        "event": event.event,
                        "remarks": event.remarks,
                        "status": event.status
                    }
                    resp.health.append(jsonevent)
                listevents = []
                for i in resp.health:
                    listevents.append(i)
                pat.document(resp.id).set({
                    "id": resp.id,
                    "firstName": resp.firstName,
                    "lastName": resp.lastName,
                    "phone": resp.phone,
                    "email": resp.email,
                    "dateOfBirth": resp.dateOfBirth,
                    "sex": resp.sex,
                    "profilePicture": resp.profilePicture,
                    "height": resp.height,
                    "weight": resp.weight,
                    "drinker": resp.drinker,
                    "smoker": resp.smoker,
                    "calendar": resp.calendar,
                    "health": resp.health,
                    "doctors": resp.doctors
                })
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
        hcps = hcpdb.stream()
        # print(hcps)
        hcps_return = []
        for hcp in hcps:
            h = hcp.to_dict()
            hcp_obj = {
                "id": h['id'],
                "firstName": h['firstName'],
                "lastName": h['lastName'],
                "email": h['email'],
                "phone": h['phone'],
                "profilePicture": h['profilePicture']
            }
            print(f'{hcp.id}=> {hcp_obj}')
            hcps_return.append(hcp_obj)
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
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        pic = request.get_json().get('profilePicture')
        hcpdb.document(str(hid)).update({
            "profilePicture": pic
        })
        response_object = {
            "Success": True,
            "profilePicture": pic
        }
        return make_response(jsonify(response_object)), 200
    else:
        response_object = {
            'status': 'fail',
            'message': "invalid_token"
        }
        return make_response(jsonify(response_object)), 401
