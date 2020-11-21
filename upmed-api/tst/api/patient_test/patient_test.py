import unittest
import requests

from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))

from src import Database, Patient, HCP,  Appointment, Day, Hours, Status, Auth  # noqa

"""
Patient Endpoint Tests
"""


def create_dummy_data():
    # Add some dummy patient and hcp
    week = []
    for i in range(0, 7):
        week.append(Day(startTime=540, endTime=1020, ))
    schedule = Hours(
        sunday=week[0],
        monday=week[1],
        tuesday=week[2],
        wednesday=week[3],
        thursday=week[4],
        friday=week[5],
        saturday=week[6])

    dummy_hcp = HCP(
        id="hw2735",
        firstName="Kevin",
        lastName="Wong",
        phone="610-844-1360",
        email="hw2735@columbia.edu",
        specialty="Accident and Emergency",
        profilePicture='',
        calendar=[],
        title='Resident',
        patients=['aoc1989'],
        hours=schedule)

    dummy_patient = Patient(
        id="aoc1989",
        firstName="Alexandria",
        lastName="Ocasio-Cortez",
        phone="6108441360",
        email="aoc@democrat.com",
        dateOfBirth="1989-10-13",
        sex='F',
        profilePicture='',
        height=150,
        weight=60,
        drinker=Status.NEVER,
        smoker=Status.NEVER,
        calendar=[],
        health=[],
        doctors=["hw2735"]
    )

    dummy_appointment = Appointment(
        id='aoc1989,hw2735,1605505365',
        date=1605505365,
        duration=30,
        doctor='hw2735',
        patient='aoc1989',
        subject='follow up',
        notes='need to check if she is compliant to prescriptions',
        videoUrl='https://www.youtube.com/watch?v=EsKZHGtSoVA'
    )
    return dummy_hcp, dummy_patient, dummy_appointment


class PatientTestCase(unittest.TestCase):
    auth = Auth()
    pdb = Database()
    hcp_db = pdb.getHCP()
    patient_db = pdb.getPatients()
    appointmentsdb = pdb.getAppointments()
    dummy_hcp, dummy_patient, dummy_appointment = create_dummy_data()
    hours = []
    time = []
    time.append(dummy_hcp.hours.sunday.startTime)
    time.append(dummy_hcp.hours.sunday.endTime)
    hours.append(str(time))
    time[0] = dummy_hcp.hours.monday.startTime
    time[1] = dummy_hcp.hours.monday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.tuesday.startTime
    time[1] = dummy_hcp.hours.tuesday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.wednesday.startTime
    time[1] = dummy_hcp.hours.wednesday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.thursday.startTime
    time[1] = dummy_hcp.hours.thursday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.friday.startTime
    time[1] = dummy_hcp.hours.friday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.saturday.startTime
    time[1] = dummy_hcp.hours.saturday.endTime
    hours.append(str(time))

    hcp_db.document(dummy_hcp.id).set({
        "id": dummy_hcp.id,
        "firstName": dummy_hcp.firstName,
        "lastName": dummy_hcp.lastName,
        "phone": dummy_hcp.phone,
        "email": dummy_hcp.email,
        "profilePicture": dummy_hcp.profilePicture,
        "calendar": dummy_hcp.calendar,
        "specialty": dummy_hcp.specialty,
        "title": dummy_hcp.title,
        "hours": hours,
        "patients": dummy_hcp.patients
    })
    patient_db.document(dummy_patient.id).set({
        "id": dummy_patient.id,
        "firstName": dummy_patient.firstName,
        "lastName": dummy_patient.lastName,
        "phone": dummy_patient.phone,
        "email": dummy_patient.email,
        "dateOfBirth": dummy_patient.dateOfBirth,
        "sex": dummy_patient.sex,
        "profilePicture": dummy_patient.profilePicture,
        "height": dummy_patient.height,
        "weight": dummy_patient.weight,
        "drinker": dummy_patient.drinker.value,
        "smoker": dummy_patient.smoker.value,
        "calendar": dummy_patient.calendar,
        "health": dummy_patient.health,
        "doctors": dummy_patient.doctors
    })
    appointmentsdb.document(dummy_appointment.id).set({
        'id': dummy_appointment.id,
        'date': dummy_appointment.date,
        'duration': dummy_appointment.duration,
        'doctor': dummy_appointment.doctor,
        'patient': dummy_appointment.patient,
        'subject': dummy_appointment.subject,
        'notes': dummy_appointment.notes,
        'videoUrl': dummy_appointment.videoUrl
    })

    auth_token = auth.encode_auth_token(dummy_hcp.id, "HCP")
    hcp_token = auth_token.decode()

    auth_token = auth.encode_auth_token(dummy_patient.id, "PATIENT")
    patient_token = auth_token.decode()

    def test_signup_test(self):
        payload = {'id': "jb0000",
                   'firstName': "Joe",
                   'lastName': "Biden",
                   'phone': '"9175587000"',
                   'email': "joebiden@democrat.edu",
                   'dateOfBirth': "1942-11-20",
                   'sex': 'M',
                   'height': 183,
                   'weight': 60,
                   'drinker': 0,
                   'smoker': 0}

        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/signUp',
            json=payload)

        patient_resp = response.json()
        self.assertEqual(201, response.status_code)
        self.assertEqual('jb0000', patient_resp['id'])

    def test_login_test(self):
        payload = {'id': "jb0000",
                   'email': "joebiden@democrat.edu"}
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/logIn',
            json=payload)
        patient_resp = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual('jb0000', patient_resp['id'])

    def test_getbytoken_test(self):
        payload = {'token': PatientTestCase.patient_token}
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/getByToken',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_getRecords_test(self):
        payload = {'token': PatientTestCase.patient_token}
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/getRecords',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_remove_test(self):
        payload = {'id': 'jb0000'}
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/delete',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_editProfile_test(self):
        payload = {'token': PatientTestCase.patient_token,
                   'firstName': "Nansi",
                   'lastName': "Pelosi",
                   'phone': "0000000000",
                   'email': "np@democrat.com",
                   'dateOfBirth': "1989-10-13",
                   'sex': 'F',
                   'profilePicture': '',
                   'height': 150,
                   'weight': 60,
                   'drinker': Status.NEVER.value,
                   'smoker': Status.NEVER.value,
                   'calendar': [],
                   'health': [],
                   'doctors': ["hw2735"]
                   }
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/editProfile',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_gethcps_test(self):
        payload = {'token': PatientTestCase.patient_token}
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/getHCPs',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_get_all_test(self):
        payload = {'token': PatientTestCase.patient_token}
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/getAll',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_set_profile_picture(self):
        payload = {'token': PatientTestCase.patient_token,
                   'profilePicture': 'https://upload.wikimedia.org/wikipedia/commons/b/b5'
                                     '/191125_Taylor_Swift_at_the_2019_American_Music_Awards_%28cropped%29.png'}
        response = requests.post(
            'https://upmed-api.herokuapp.com/patient/getRecords',
            json=payload)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
