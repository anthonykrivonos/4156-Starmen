# import sys
# sys.path.append('/UpMed/upmed-api/src')
# from src.util.firebase.db import Database


from flask import Blueprint, request, jsonify, make_response
from ....src.util.firebase.db import Database
from ....src.util.util import Auth
from ....src.models.patient import Patient
from ....src.models.health_event import HealthEvent


patient_endpoints = Blueprint('patient', __name__)
pdb = Database()
pat = pdb.getPatients()
auth = Auth()


@patient_endpoints.route('/', methods=['POST'])
def root():
    return "GO TO AN ENDPOINT"


@patient_endpoints.route('/logIn', methods=['POST'])
def login():
    try:
        pid = request.json['id']
        email = request.json['email']
        res = pat.document(str(pid)).get()
        res = res.to_dict()

        if res['email'] == email:
            utype = "PATIENT"
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


@patient_endpoints.route('/signUp', methods=['POST'])
def signup():
    post_data = request.get_json()
    try:
        patient = Patient(
            id= post_data.get('id'),
            firstName = post_data.get('firstName'),
            lastName = post_data.get('lastName'),
            phone = "0000000000",
            email = post_data.get('email'),
            dateOfBirth = post_data.get('dateOfBirth'),
            sex = post_data.get('sex'),
            profilePicture = '',
            height = post_data.get('height'),
            weight = post_data.get('weight'),
            drinker = post_data.get('drinker'),
            smoker = post_data.get('smoker'),
            calendar=[],
            health=[],
            doctors=[]
        )
        try:
            patient.profilePicture = post_data.get('profilePicture')
        except KeyError:
            patient.profilePicture = 'https://www.flaticon.com/svg/static/icons/svg/147/147144.svg'

        # Parse phone number
        phone = str(post_data.get('phone')).replace('-', '')
        patient.phone = phone
        utype = "PATIENT"
        pat.document(patient.id).set({
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
        auth_token = auth.encode_auth_token(patient.id, utype)
        responseObject = {
            'id': patient.id,
            'token': auth_token.decode()
        }
        return make_response(jsonify(responseObject)), 201
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': f'Some error, {e} occurred. Please try again.'
        }
        return make_response(jsonify(responseObject)), 401


@patient_endpoints.route('/delete', methods=['POST'])
def remove():
    """
        delete() : Delete a document from Firestore collection.
        This is for testing purposes and does not have any security
    """
    post_data = request.get_json()
    try:
        # Check for ID in URL query
        pid = post_data.get('id')
        pat.document(pid).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@patient_endpoints.route('/getByToken', methods=['POST'])
def getbytoken():
    # get the auth token
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        patient = pat.document(str(pid)).get().to_dict()
        # print(patient)
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

        responseObject = {
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
            "smoker": resp.smoker
            }
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401


@patient_endpoints.route('/getRecords', methods=['POST'])
def getRecords():
    """
        Based on the supplied patient JWT the health records
        for that patient will be accessed.
    :return: List[HealthEvent]
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
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
            health=patient['health']
        )
        responseObject = []
        for i in resp.health:
            responseObject.append(i)


        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401


@patient_endpoints.route('/editProfile', methods=['POST'])
def editProfile():

    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        patient_resp = pat.document(str(pid)).get().to_dict()
        post_data = request.get_json()
        patient = Patient(
            id=patient_resp['id'],
            firstName=post_data.get('firstName'),
            lastName=post_data.get('lastName'),
            phone=post_data.get('phone'),
            email=post_data.get('email'),
            dateOfBirth=patient_resp['dateOfBirth'],
            sex=patient_resp['sex'],
            profilePicture=post_data.get('profilePicture'),
            height=post_data.get('height'),
            weight=post_data.get('weight'),
            drinker=post_data.get('drinker'),
            smoker=post_data.get('smoker'),
            calendar=patient_resp['calendar'],
            doctors=patient_resp['doctors'],
            health=patient_resp['health']
        )

        pat.document(patient.id).set({
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
        return make_response(jsonify(res)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401