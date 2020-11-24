import unittest
import requests
import time
from unittest.mock import MagicMock, Mock


from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))


from src import Database, Patient, Appointment, HCP, Day, Hours, Status, Auth, hcp, Twilio, hcp_signup, hcp_get_all, hcp_login, hcp_delete, hcp_set_record, hcp_get_by_token, hcp_notify, hcp_test_number, hcp_edit_profile, hcp_get_patients, hcp_set_health_events, hcp_set_profile_picture, hcp_set_health_events  # noqa
from tst.constants import dummy_hcp, dummy_appointment, dummy_patient  # noqa
"""
HCP Endpoint Tests
"""
db = Database()
set_func = Mock()
set_func.to_dict = MagicMock(return_value=1)
set_func.set = MagicMock(return_value=1)
set_func.get = MagicMock(return_value=1)
set_func.stream = MagicMock(return_value=2)
set_func.delete = MagicMock(return_value=3)
db.document = MagicMock(return_value=set_func)
db.stream = MagicMock(return_value=2)

hcpdb = db.getHCP()
pat = db.getPatients()
appointmentsdb = db.getAppointments()
auth = Auth()
twilio = Twilio()


unittest.TestLoader.sortTestMethodsUsing = None
hcp_token = ''


class HCPTestCase(unittest.TestCase):
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
                   }
                  }
        res = hcp_signup(db, dummy_hcp, dummy_hcp.hours)
        self.assertNotEqual(res, 0)
        # self.assertEqual(res, 1)

    def test_login_test(self):
        res = hcp_login(db, dummy_hcp.id, dummy_hcp.id)
        self.assertNotEqual(res, 0)

    def test_set_record(self):
        res = hcp_set_record(db, dummy_patient)
        self.assertNotEqual(res, 0)

    def test_notify_test(self):
        res = hcp_notify(db, db, dummy_appointment.id)
        self.assertEqual(res, 0)

    def test_remove_test(self):
        res = hcp_delete(db, dummy_hcp.id)
        self.assertEqual(res, 3)

    def test_getByToken(self):
        res = hcp_get_by_token(db, dummy_hcp.id)
        self.assertEqual(res, 0)

    def test_test_number(self):
        res = hcp_test_number(db, db, dummy_appointment.id)
        self.assertEqual(res, 0)

    def test_edit_profile(self):
        res = hcp_set_profile_picture(db, dummy_hcp.id, {"stuff": "stuff"})
        self.assertIsNotNone(res)

    def test_health_event(self):
        res = hcp_set_health_events(db, dummy_patient.id, {"stuff": "stuff"})
        self.assertEqual(res, 0)

    def test_get_all(self):
        res = hcp_get_all(db)
        self.assertEqual(res, 2)

    def test_get_patients(self):
        res = hcp_get_patients(db, db, dummy_hcp.id)
        self.assertEqual(res, 0)

    def test_set_profile_picture(self):
        res = hcp_set_profile_picture(
            db, dummy_hcp.id, dummy_hcp.profilePicture)
        print(res)
        self.assertEqual(res, dummy_patient.profilePicture)



if __name__ == '__main__':
    unittest.main()
