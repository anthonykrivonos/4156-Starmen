import datetime
from flask import Blueprint, request, jsonify, make_response
import requests
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

auth = Auth()
twilio = Twilio()
default_pic = 'https://www.flaticon.com/svg/static/icons/svg/387/387561.svg'
invalid_token = 'Provide a valid auth token'
nonHCP = 'Not an HCP.'


def hcp_login(db, pid, email):
    """HCP Logins

    Returns:
            Response: JSON
    """
    try:
        res = db.document(str(pid)).get()
        res = res.to_dict()
        if res['email'] == email:
            utype = "HCP"
            auth_token = auth.encode_auth_token(pid, utype)
            resp = {
                "id": pid,
                "token": auth_token.decode()
            }
            return resp
        else:
            return 0
    except Exception as e:
        return f"An Error Occured: {e}"


def hcp_signup(db, hcp, hours, npi):
    """New HCP creates profile

    Returns:
            Response: JSON
    """
    utype = "HCP"
    # Check NPI
    response = requests.get("https://clinicaltables.nlm.nih.gov/api/npi_org/v3/search", params={"terms": str(npi),
                                                                                                "sf": "NPI"})
    if response.json()[0] != 1:
        return 0

    res = db.document(hcp.id).set({
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
    if (res):
        auth_token = auth.encode_auth_token(hcp.id, utype)
    else:
        return 0
    if (len(auth_token) > 0):
        return auth_token.decode()
    else:
        return 0


def hcp_delete(db, hcp):
    return db.document(hcp).delete()


def hcp_set_record(db, resp):
    return db.document(resp.id).set({
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


def hcp_get_by_token(db, hid):
    schedule = make_week()
    hcp = db.document(hid).get()
    if (hcp == 1):
        return 0
    hcp = hcp.to_dict()
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
    return resp


def hcp_notify(adb, pdb, appointment_id):
    try:
        appointment_resp = adb.document(
            str(appointment_id)).get()
        if appointment_resp == 1:
            return 0
        appointment_resp = appointment_resp.to_dict()
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
        patient = pdb.document(
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
            f"{datetime.datetime.fromtimestamp(appointment.date / 1e3)}"
            f" join at "
            f"{appointment.videoUrl}",
            from_='+19036182297',
            to=f'+1{str(resp.phone).replace("", "")}')
        print(message)
        print(datetime.datetime.fromtimestamp(appointment.date / 1e3))
        res = {
            "Success": True
        }
        return res
    except Exception as e:
        return 0


def hcp_test_number(adb, pdb, appointment_id):
    try:
        appointment_resp = adb.document(
            str(appointment_id)).get()
        if appointment_resp == 1:
            return 0
        appointment_resp = appointment_resp.to_dict()
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
        patient = pdb.document(
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
            f"{datetime.datetime.fromtimestamp(appointment.date / 1e3)}"
            f" join at "
            f"{appointment.videoUrl}",
            from_='+19036182297',
            to=f'+1{str(resp.phone).replace("", "")}')
        print(message)
        print(datetime.datetime.fromtimestamp(appointment.date / 1e3))
        res = {
            "Success": True
        }
    except Exception as e:
        print(f"Unable to find {appointment_id} because {e}")
        res = {
            "Success": False
        }
    return res


def hcp_edit_profile(db, hid, post_data):
    hcp_resp = db.document(str(hid)).get().to_dict()
    if hcp_resp == 1:
        return 0
    schedule = make_week()
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
        db.document(hcp.id).set({
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
            'Success': False,
            'message': "Ivalid Token"
        }
        return response_object
    response_object = {
        "Success": True
    }
    return response_object


def hcp_get_patients(hdb, pdb, hid):
    hcp_resp = hdb.document(str(hid)).get()
    if hcp_resp == 1:
        return 0
    hcp_resp = hcp_resp.to_dict()
    res = {}
    print(hcp_resp)
    for i in hcp_resp['patients']:
        pats = pdb.document(str(i)).get().to_dict()
        print(pats)
        entry = {
            i: pats
        }
        res.update(entry)
    return res


def hcp_set_health_events(pat, pid, post_data):
    patient = pat.document(str(pid)).get()
    if patient == 1:
        return 0
    patient = patient.to_dict()
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
    return resp


def hcp_get_all(hcpdb):
    hcps = hcpdb.stream()
    if hcps == 2:
        return 2
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
    return hcps_return


def hcp_set_profile_picture(db, hid, pic):
    db.document(str(hid)).update({
        "profilePicture": pic
    })
    return pic


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
