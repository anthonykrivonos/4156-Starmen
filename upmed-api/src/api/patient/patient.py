from flask import Blueprint, request, jsonify, make_response

from .patient_helper import pat_delete, pat_edit_profile, pat_login, \
    pat_get_by_token, pat_set_profile_picture, \
    pat_signup, pat_get_all, pat_get_hcps, pat_get_records, pat_search  # noqa

from sys import path
from os.path import join, dirname

path.append(dirname(__file__))
path.append(join(dirname(__file__), '../../..'))

from src.util.firebase.db import Database  # noqa
from src.util.util import Auth  # noqa
from src.models.patient import Patient  # noqa

patient_endpoints = Blueprint('patient', __name__)

pdb = Database()
pat = pdb.getPatients()
auth = Auth()
hcpdb = pdb.getHCP()


@patient_endpoints.route('/', methods=['POST'])
def root():
    """Default api route

    Returns:
        Response: string
    """
    return "GO TO AN ENDPOINT", 404


@patient_endpoints.route('/logIn', methods=['POST'])
def login():
    """Login existing patient

    Returns:
        Response: JSON
    """
    try:
        post_data = request.get_json()
        pid = post_data.get('id')
        email = post_data.get('email')
        resp = pat_login(pat, pid, email)
        if resp:
            return jsonify(resp), 200
        else:
            return "False", 404
    except Exception as e:
        return f"An Error Occured: {e}", 500


@patient_endpoints.route('/signUp', methods=['POST'])
def signup():
    """Create new Patient object and record

    Returns:
        Response: JSON
    """
    post_data = request.get_json()
    try:
        patient = Patient(
            id=post_data.get('id'),
            firstName=post_data.get('firstName'),
            lastName=post_data.get('lastName'),
            phone="0000000000",
            email=post_data.get('email'),
            dateOfBirth=post_data.get('dateOfBirth'),
            sex=post_data.get('sex'),
            profilePicture='',
            height=post_data.get('height'),
            weight=post_data.get('weight'),
            drinker=post_data.get('drinker'),
            smoker=post_data.get('smoker'),
            calendar=[],
            health=[],
            doctors=[]
        )
        try:
            patient.profilePicture = post_data.get('profilePicture')
        except KeyError:
            patient.profilePicture = 'https://www.flaticon.com/svg/static/' \
                                     'icons/svg/147/147144.svg'

        # Parse phone number
        # phone = str(post_data.get('phone')).replace('-', '')
        patient.phone = str(post_data.get('phone'))
        res = pat_signup(pat, patient, False)
        if res != 0:
            response_object = {
                'id': patient.id,
                'token': res
            }
            return make_response(jsonify(response_object)), 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': f'Some error, {e} occurred. Please try again.'
        }
        return make_response(jsonify(response_object)), 401


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
        res = pat_delete(pat, pid)
        if res:
            return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@patient_endpoints.route('/getByToken', methods=['POST'])
def getbytoken():
    """Get Patients by token

    Returns:
        Response: JSON
    """
    # get the auth token
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        resp, success = pat_get_by_token(pat, pid)
        if not success:
            return make_response(resp), 404
        response_object = {
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
            "health": resp.health
        }
        return make_response(jsonify(response_object)), 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Invalid token. Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401


@patient_endpoints.route('/getRecords', methods=['POST'])
def get_records():
    """
        Based on the supplied patient JWT the health records
        for that patient will be accessed.
    :return: List[HealthEvent]
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        response_object = pat_get_records(pat, pid)
        return make_response(jsonify(response_object)), 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Invalid. Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401


@patient_endpoints.route('/editProfile', methods=['POST'])
def edit_profile():
    """edit Patient Profile

    Returns:
        Response: JSON
    """
    post_data = request.get_json()
    auth_token = post_data.get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        res = pat_edit_profile(pat, pid, post_data)
        return make_response(jsonify(res)), 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401


@patient_endpoints.route('/getHCPs', methods=['POST'])
def gethcps():
    """Get Patients's HCPs

    Returns:
        Response: JSON
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        # Get the ids of the HCPs of patient
        results = pat_get_hcps(pat, hcpdb, pid)
        return make_response(jsonify(results)), 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Token Invalid. Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401


@patient_endpoints.route('/getAll', methods=['POST'])
def get_all():
    """Get Patients

    Returns:
        Response: JSON
    """
    auth_token = request.get_json().get('token')
    if auth_token:
        hid, utype = Auth.decode_auth_token(auth_token)
        pats_return = pat_get_all(pat)
        return jsonify(pats_return), 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401


@patient_endpoints.route('/setProfilePicture', methods=['POST'])
def set_profile_picture():
    """
    Set Patient Profile Picture

    Returns: Response: JSON
    """
    # Get Auth Token
    auth_token = request.get_json().get('token')
    if auth_token:
        pid, utype = Auth.decode_auth_token(auth_token)
        pic = request.get_json().get('profilePicture')
        res = pat_set_profile_picture(pat, pid, pic)
        if res:
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


@patient_endpoints.route('/search', methods=['POST'])
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
            res = pat_search(text)

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
