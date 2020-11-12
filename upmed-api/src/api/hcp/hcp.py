from flask import Blueprint, request, jsonify, make_response
from ....src.util.firebase.db import Database
from ....src.util.util import Auth, Twilio
from ....src.models.hcp import HCP
from ....src.models.hours import Hours
from ....src.models.day import Day
from ....src.models.health_event import HealthEvent
from ....src.models.patient import Patient
from ....src.models.enums import Status
from ....src.models.appointment import Appointment



# Setup HCP and Patient Document Collections
db = Database()
hcpdb = db.getHCP()
pat = db.getPatients()
appointmentsdb = db.getAppointments()
auth = Auth()
twilio = Twilio()


hcp_endpoints = Blueprint('hcp', __name__)

@hcp_endpoints.route('/')
def root():
    return "hcp"

@hcp_endpoints.route('/logIn', methods=['POST'])
def login():
    try:
        pid = request.json['id']
        email = request.json['email']
        res = hcpdb.document(str(pid)).get()
        res = res.to_dict()
        print(pid)
        if res['email'] == email:
            utype = "HCP"
            auth_token = auth.encode_auth_token(pid, utype)
            resp = {
                "googleId": pid,
                "token": auth_token.decode()
            }
            # resp = res
            print(resp)
            return jsonify(resp), 200
        else:
            return "False", 404
    except Exception as e:
        return f"An Error Occured: {e}"

@hcp_endpoints.route('/signUp', methods=['POST'])
def signup():
    post_data = request.get_json()

    week = []
    for i in range(0, 7):
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
    try:
        hcp = HCP(
            id=post_data.get('id'),
            firstName=post_data.get('firstName'),
            lastName=post_data.get('lastName'),
            phone=post_data.get('phone'),
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
        except:
            hcp.specialty = ''

        try:
            hcp.title = post_data.get('title')
        except:
            hcp.title = ''

        try:
            hcp.profilePicture = post_data.get('profilePicture')
        except:
            hcp.profilePicture = 'https://www.flaticon.com/svg/static/icons/svg/387/387561.svg'
        # print(f"profile {hcp.profilePicture}")
        if hcp.profilePicture is None:
            # print("Chnaging Profile")
            hcp.profilePicture = 'https://www.flaticon.com/svg/static/icons/svg/387/387561.svg'

        newsched = post_data.get('hours')
        # print(newsched)

        if newsched['sunday']['startTime'] == -1 and newsched['sunday']['endTime'] == -1:
            hcp.hours.sunday.startTime = -1
            hcp.hours.sunday.endTime = -1
        elif 0 <= newsched['sunday']['startTime'] <= newsched['sunday']['endTime'] :
            hcp.hours.sunday.startTime = newsched['sunday']['startTime']
            hcp.hours.sunday.endTime = newsched['sunday']['endTime']

        if newsched['monday']['startTime'] == -1 and newsched['monday']['endTime'] == -1:
            hcp.hours.monday.startTime = -1
            hcp.hours.monday.endTime = -1
        elif 0 <= newsched['monday']['startTime'] <= newsched['monday']['endTime'] :
            hcp.hours.monday.startTime = newsched['monday']['startTime']
            hcp.hours.monday.endTime = newsched['monday']['endTime']
        # print(hcp.hours)

        if newsched['tuesday']['startTime'] == -1 and newsched['tuesday']['endTime'] == -1:
            hcp.hours.tuesday.startTime = -1
            hcp.hours.tuesday.endTime = -1
        elif 0 <= newsched['tuesday']['startTime'] <= newsched['tuesday']['endTime'] :
            hcp.hours.tuesday.startTime = newsched['tuesday']['startTime']
            hcp.hours.tuesday.endTime = newsched['tuesday']['endTime']

        if newsched['wednesday']['startTime'] == -1 and newsched['wednesday']['endTime'] == -1:
            hcp.hours.wednesday.startTime = -1
            hcp.hours.wednesday.endTime = -1
        elif 0 <= newsched['wednesday']['startTime'] <= newsched['wednesday']['endTime'] :
            hcp.hours.wednesday.startTime = newsched['wednesday']['startTime']
            hcp.hours.wednesday.endTime = newsched['wednesday']['endTime']

        if newsched['thursday']['startTime'] == -1 and newsched['thursday']['endTime'] == -1:
            hcp.hours.thursday.startTime = -1
            hcp.hours.thursday.endTime = -1
        elif 0 <= newsched['thursday']['startTime'] <= newsched['thursday']['endTime'] :
            hcp.hours.thursday.startTime = newsched['thursday']['startTime']
            hcp.hours.thursday.endTime = newsched['thursday']['endTime']

        if newsched['friday']['startTime'] == -1 and newsched['friday']['endTime'] == -1:
            hcp.hours.friday.startTime = -1
            hcp.hours.friday.endTime = -1
        elif 0 <= newsched['friday']['startTime'] <= newsched['friday']['endTime'] :
            hcp.hours.friday.startTime = newsched['friday']['startTime']
            hcp.hours.friday.endTime = newsched['friday']['endTime']

        if newsched['saturday']['startTime'] == -1 and newsched['saturday']['endTime'] == -1:
            hcp.hours.sunday.saturday = -1
            hcp.hours.sunday.saturday = -1
        elif 0 <= newsched['saturday']['startTime'] <= newsched['saturday']['endTime'] :
            hcp.hours.saturday.startTime = newsched['saturday']['startTime']
            hcp.hours.saturday.endTime = newsched['saturday']['endTime']

        # print(f"********\n{hcp.hours}")
        # hours = {
        #     "sunday": {
        #         "startTime": hcp.hours.sunday.startTime,
        #         "endTime": 480
        #     },
        #     "monday": {
        #         "startTime": -1,
        #         "endTime": -1
        #     },
        #     "tuesday": {
        #         "startTime": -1,
        #         "endTime": -1
        #     },
        #     "wednesday": {
        #         "startTime": -1,
        #         "endTime": -1
        #     },
        #     "thursday": {
        #         "startTime": -1,
        #         "endTime": -1
        #     },
        #     "friday": {
        #         "startTime": -1,
        #         "endTime": -1
        #     },
        #     "saturday": {
        #         "startTime": -1,
        #         "endTime": -1
        #     }
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
        responseObject = {
            'id': hcp.id,
            'token': auth_token.decode()
        }
        return make_response(jsonify(responseObject)), 201
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': f'Some error, {e} occurred. Please try again.'
        }
        return make_response(jsonify(responseObject)), 401


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
    # get the auth token
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        if utype == "HCP":
            week = []
            for i in range(0, 7):
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
            hcp = hcpdb.document(hid).get().to_dict()
            print(hcp)
            resp = HCP(
                id=hcp['id'],
                firstName=hcp['firstName'],
                lastName=hcp['lastName'],
                phone=hcp['phone'],
                email=hcp['email'],
                specialty=hcp['title'],
                profilePicture=hcp['profilePicture'],
                calendar=[],
                title='',
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

            responseObject = {
                "id": resp.id,
                "firstName": resp.firstName,
                "lastName": resp.lastName,
                "phone": resp.phone,
                "email": resp.email,
                "profilePicture": resp.profilePicture,
                "calendar": resp.calendar,
                "specialty": resp.specialty,
                "title": resp.title,
                "hours": hours,
                "patients": resp.patients
                }
            return make_response(jsonify(responseObject)), 200
        else:
            responseobject = {
                'Success': False,
                'message': 'Not an HCP'
            }
            return make_response(jsonify(responseobject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401


@hcp_endpoints.route('/setRecords', methods=['POST'])
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
                print(resp.health)
                listevents = []
                for i in resp.health:
                    listevents.append(i)
                # healths = ''.join([str(e) for e in listevents])
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
            responseobject = {
                'Success': False,
                'message': 'Not an HCP'
            }
            return make_response(jsonify(responseobject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401


@hcp_endpoints.route('/notify', methods=['POST'])
def notify():
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        post_data = request.get_json()
        if utype == "HCP":
            try:
                appointment_id = post_data.get('id')
                appointment_resp = appointmentsdb.document(str(appointment_id)).get().to_dict()
                appointment = Appointment(
                    id=appointment_resp['id'],
                    startDate=appointment_resp['startDate'],
                    endDate=appointment_resp['endDate'],
                    doctor=appointment_resp['doctor'],
                    patient=appointment_resp['patient'],
                    subject=appointment_resp['subject'],
                    notes=appointment_resp['notes'],
                    videoUrl=appointment_resp['videoUrl']
                )
                patient = pat.document(str(appointment.patient)).get().to_dict()
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
                message = client.messages \
                    .create(
                        body=f"Hi {resp.firstName} you have an appointment at {appointment.startDate} join at "
                             f"{appointment.videoUrl}",
                        from_='+19036182297',
                        to=f'+1{resp.phone}'
                )
                print(message.sid)
                res = {
                    "Success": True
                }

            except Exception as e:
                return f"Unable to find {post_data.get('id')} because {e}", 404

            return make_response(jsonify(res)), 200
        else:
            responseobject = {
                'Success': False,
                'message': 'Not an HCP'
            }
            return make_response(jsonify(responseobject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401
