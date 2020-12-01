from flask import Blueprint, request, jsonify, make_response, json
from algoliasearch.search_client import SearchClient  # noqa

from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../../..'))

from src.util.firebase.db import Database  # noqa
from src.util.util import Auth  # noqa
from src.util.env import Env  # noqa
from src.models.patient import Patient  # noqa
from src.models.appointment import Appointment  # noqa
from src.models.hcp import HCP  # noqa
from src.models.hours import Hours  # noqa
from src.models.day import Day  # noqa

auth = Auth()


def pat_login(db, pid, email):
    """HCP Logins

    Returns:
            Response: JSON
    """
    try:
        res = db.document(str(pid)).get()
        res = res.to_dict()
        if res['email'] == email:
            utype = "PATIENT"
            auth_token = auth.encode_auth_token(pid, utype)
            resp = {
                "id": pid,
                "token": auth_token.decode()
            }
            return resp
        else:
            return 0
    except Exception as e:
        return f"An Error Occurred: {e}"


def pat_signup(pat, patient):
    """New HCP creates profile

    Returns:
            Response: JSON
    """
    utype = "PATIENT"
    res = pat.document(patient.id).set({
        "id": patient.id,
        "firstName": patient.firstName,
        "lastName": patient.lastName,
        "phone": patient.phone,
        "email": patient.email,
        "dateOfBirth": patient.dateOfBirth,
        "sex": patient.sex,
        "profilePicture": patient.profilePicture,
        "height": patient.height,
        "weight": patient.weight,
        "drinker": patient.drinker,
        "smoker": patient.smoker,
        "calendar": patient.calendar,
        "health": patient.health,
        "doctors": patient.doctors

    })
    # print("HERE")
    add_pat(patient)
    # print("HERE2")
    if (res):
        auth_token = auth.encode_auth_token(patient.id, utype)
    else:
        return 0
    if (len(auth_token) > 0):
        return auth_token.decode()
    else:
        return 0


def pat_get_records(pat, pid):
    patient = pat.document(str(pid)).get()
    if patient == 1:
        return 0
    patient = patient.to_dict()
    print(patient)
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
    response_object = []
    for i in resp.health:
        response_object.append(i)

    return response_object


def pat_delete(db, pid):
    return db.document(pid).delete()


def pat_get_by_token(db, pid):
    try:
        patient = db.document(str(pid)).get()
        if (patient == 1):
            return 0
        patient = patient.to_dict()
        resp = Patient(
            id=pid,
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
        return resp, True
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Unable to find patient.'
        }
        return jsonify(response_object), False


def pat_edit_profile(db, pid, post_data):
    patient_resp = db.document(str(pid)).get()
    if patient_resp == 1:
        return 0
    patient_resp = patient_resp.to_dict()
    print(patient_resp)
    patient = Patient(
        id=patient_resp['id'],
        firstName=post_data.get('firstName'),
        lastName=post_data.get('lastName'),
        phone=post_data.get('phone'),
        email=post_data.get('email'),
        dateOfBirth=patient_resp['dateOfBirth'],
        sex=patient_resp['sex'],
        profilePicture=patient_resp['profilePicture'],
        height=post_data.get('height'),
        weight=post_data.get('weight'),
        drinker=post_data.get('drinker'),
        smoker=post_data.get('smoker'),
        calendar=patient_resp['calendar'],
        doctors=patient_resp['doctors'],
        health=patient_resp['health']
    )

    try:
        patient.profilePicture = post_data.get('profilePicture')
    except KeyError:
        patient.profilePicture = patient_resp['profilePicture']

    db.document(patient.id).set({
        "id": patient.id,
        "firstName": patient.firstName,
        "lastName": patient.lastName,
        "phone": patient.phone,
        "email": patient.email,
        "dateOfBirth": patient.dateOfBirth,
        "sex": patient.sex,
        "profilePicture": patient.profilePicture,
        "height": patient.height,
        "weight": patient.weight,
        "drinker": patient.drinker,
        "smoker": patient.smoker,
        "calendar": patient.calendar,
        "health": patient.health,
        "doctors": patient.doctors

    })
    res = {
        "Success": True
    }
    print(res)
    return res


def pat_get_hcps(pat, hcpdb, pid):
    patient_resp = pat.document(str(pid)).get()
    if patient_resp == 1:
        return 0
    patient_resp = patient_resp.to_dict()
    print(patient_resp)
    print(patient_resp['doctors'])
    results = {}
    for i in patient_resp['doctors']:
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
        hcp = hcpdb.document(i).get().to_dict()
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

        response_object = {
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

        entry = {
            i: response_object
        }
        # print(i)
        results.update(entry)
    return results


def pat_get_all(pat):
    pats = pat.stream()
    if pats == 2:
        return 2
    pats_return = []
    for patient in pats:
        h = patient.to_dict()
        print(f'{patient.id}=> {h["firstName"]}')
        pat_obj = {
            "id": h['id'],
            "firstName": h['firstName'],
            "lastName": h['lastName'],
            "email": h['email'],
            "phone": h['phone'],
            "profilePicture": h['profilePicture']
        }

        pats_return.append(pat_obj)
    return pats_return


def pat_set_profile_picture(db, pid, pic):
    db.document(str(pid)).update({
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


def pat_search(text):
    print(text)
    api = Env.ALGOLIA()
    admin = Env.ALGOLIA_ADMIN()
    # print(api)
    # add_pat(pat)
    client = SearchClient.create(api, admin)
    index = client.init_index('patients')
    index.set_settings({"customRanking": ["desc(followers)"]})
    index.set_settings({"searchableAttributes": ["firstName", "lastName", "phone",
                                                 "email", "id"]})
    res = index.search(text)

    # Res is all hits of Patients with matching
    hits = res['hits']

    pats_return = []
    # patient = pat.document(str(pid)).get()
    for h in hits:
        pat_obj = {
            "id": h['id'],
            "firstName": h['firstName'],
            "lastName": h['lastName'],
            "email": h['email'],
            "phone": h['phone'],
            "profilePicture": h['profilePicture']
        }
        pats_return.append(pat_obj)

    return pats_return

def add_pat(patient):
    api = Env.ALGOLIA()
    admin = Env.ALGOLIA_ADMIN()
    client = SearchClient.create(api, admin)
    index = client.init_index('patients')
    res = {
        "id": patient.id,
        "firstName": patient.firstName,
        "lastName": patient.lastName,
        "phone": patient.phone,
        "email": patient.email,
        "profilePicture": patient.profilePicture
    }
    with open('js.json', 'w') as fp:
        json.dump(res, fp)

    batch = json.load(open('js.json'))
    fp.close()
    try:
        index.save_object(batch, {'autoGenerateObjectIDIfNotExist': True})
    except Exception as e:
        print(f'Error: {e}')
    return 0
