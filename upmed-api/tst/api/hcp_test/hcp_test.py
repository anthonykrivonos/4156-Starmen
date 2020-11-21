import unittest
import requests
import time

from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))

from src import Database, Patient, Appointment, HCP, Day, Hours, Status, Auth  # noqa

"""
HCP Endpoint Tests
"""


unittest.TestLoader.sortTestMethodsUsing = None
hcp_token = ''


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


class HCPTestCase(unittest.TestCase):
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
        week = []
        for i in range(0, 7):
            week.append(Day(startTime=540, endTime=1020))
        schedule = Hours(
            sunday=week[0],
            monday=week[1],
            tuesday=week[2],
            wednesday=week[3],
            thursday=week[4],
            friday=week[5],
            saturday=week[6])

        payload = {'id': "ap0000",
                   'firstName': "Athena",
                   'lastName': "Pang",
                   'phone': '"9175587800"',
                   'email': "ap0000@columbia.edu",
                   'specialty': "Accident and Emergency",
                   'hours': {
                       "sunday": {
                           "startTime": schedule.sunday.startTime,
                           "endTime": schedule.sunday.endTime
                       },
                       "monday": {
                           "startTime": schedule.monday.startTime,
                           "endTime": schedule.monday.endTime
                       },
                       "tuesday": {
                           "startTime": schedule.tuesday.startTime,
                           "endTime": schedule.tuesday.endTime
                       },
                       "wednesday": {
                           "startTime": schedule.wednesday.startTime,
                           "endTime": schedule.wednesday.endTime
                       },
                       "thursday": {
                           "startTime": schedule.thursday.startTime,
                           "endTime": schedule.thursday.endTime
                       },
                       "friday": {
                           "startTime": schedule.friday.startTime,
                           "endTime": schedule.friday.endTime
                       },
                       "saturday": {
                           "startTime": schedule.saturday.startTime,
                           "endTime": schedule.saturday.endTime
                       }
                   },
                   'videoUrl': 'https://www.youtube.com/watch?v=dMTQKFS1tpA'
                   }

        response = requests.post('https://upmed-api.herokuapp.com/hcp/signUp',
                                 json=payload)
        hcp_id_r = response.json()
        hcp_id = hcp_id_r['id']
        self.assertEqual(201, response.status_code)
        self.assertEqual('ap0000', hcp_id)

    def test_login_test(self):
        payload = {'id': "hw2735",
                   'email': "hw2735@columbia.edu"}
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/logIn',
            json=payload)
        hcp = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual('hw2735', hcp['id'])

    def test_setRecords(self):
        payload = {'token': HCPTestCase.hcp_token,
                   'id': 'aoc1989',
                   'health': [
                       {
                           'date': time.time(),
                           'event': 'schizophrenia',
                           'remarks': 'Strong violent tendency',
                           'status': 0
                       }
                   ]
                   }
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/setRecords',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_notify_test(self):
        payload = {'token': HCPTestCase.hcp_token,
                   'id': 'aoc1989,hw2735,1605505365'}
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/notify',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_remove_test(self):
        payload = {
            'id': 'ap0000',
            'token': HCPTestCase.hcp_token
        }
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/delete',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_getByToken(self):
        payload = {'token': HCPTestCase.hcp_token}
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/getByToken',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_setRecord(self):
        payload = {'token': HCPTestCase.hcp_token,
                   'id': 'aoc1989',
                   'health': [
                       {
                           'date': time.time(),
                           'event': 'schizophrenia',
                           'remarks': 'Strong violent tendency',
                           'status': 0
                       }
                   ]
                   }
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/setRecord',
            json=payload)
        self.assertEqual(201, response.status_code)

    def test_editProfile(self):
        week = []
        for i in range(0, 7):
            week.append(Day(startTime=540, endTime=1020))
        schedule = Hours(
            sunday=week[0],
            monday=week[1],
            tuesday=week[2],
            wednesday=week[3],
            thursday=week[4],
            friday=week[5],
            saturday=week[6])
        print(HCPTestCase.hcp_token)
        payload = {
                   'id': "hw2735",
                   'token': HCPTestCase.hcp_token,
                   'firstName': "Athena",
                   'lastName': "Pang",
                   'phone': '"9175587800"',
                   'email': "hw2735@columbia.edu",
                   'specialty': "Accident and Emergency",
                   'hours': {
                       "sunday": {
                           "startTime": schedule.sunday.startTime,
                           "endTime": schedule.sunday.endTime
                       },
                       "monday": {
                           "startTime": schedule.monday.startTime,
                           "endTime": schedule.monday.endTime
                       },
                       "tuesday": {
                           "startTime": schedule.tuesday.startTime,
                           "endTime": schedule.tuesday.endTime
                       },
                       "wednesday": {
                           "startTime": schedule.wednesday.startTime,
                           "endTime": schedule.wednesday.endTime
                       },
                       "thursday": {
                           "startTime": schedule.thursday.startTime,
                           "endTime": schedule.thursday.endTime
                       },
                       "friday": {
                           "startTime": schedule.friday.startTime,
                           "endTime": schedule.friday.endTime
                       },
                       "saturday": {
                           "startTime": schedule.saturday.startTime,
                           "endTime": schedule.saturday.endTime
                       }
                   },
                   'videoUrl': 'https://www.youtube.com/watch?v=dMTQKFS1tpA'
                   }
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/editProfile',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_getpatients(self):
        payload = {'token': HCPTestCase.hcp_token}
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/getPatients',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_getAll(self):
        payload = {'token': HCPTestCase.hcp_token}
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/getAll',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_set_profile_picture(self):
        payload = {'token': HCPTestCase.hcp_token,
                   'profilePicture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed'
                                     '/Elon_Musk_Royal_Society.jpg/440px-Elon_Musk_Royal_Society.jpg'}
        response = requests.post(
            'https://upmed-api.herokuapp.com/hcp/setProfilePicture',
            json=payload)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
