import unittest
import time
from src import Database, Patient, HCP, Day, Hours, Status, Auth  # noqa
from src.api.appointment import appointment_helper
from unittest.mock import MagicMock, Mock
from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../../..'))

"""
Patient Endpoint Tests
Note: run as python3 -m upmed-api.tst.api.appointment_test.appointment_test
"""
appointment_token = ''

pdb = Database()
set_func = Mock()
set_func.set = MagicMock(return_value=None)
pdb.document = MagicMock(return_value=set_func)
hcp_db = pdb.getHCP()
patient_db = pdb.getPatients()
appointmentsdb = pdb.getAppointments()


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
        phone="+19175587800",
        email="hw2735@columbia.edu",
        specialty="Accident and Emergency",
        profilePicture='',
        calendar=[],
        title='Resident',
        patients=[''],
        hours=schedule)

    dummy_patient = Patient(
        id="aoc1989",
        firstName="Alexandria",
        lastName="Ocasio-Cortez",
        phone="0000000000",
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
    return dummy_hcp, dummy_patient


class AppointmentApiTestCase(unittest.TestCase):
    auth = Auth()
    dummy_hcp, dummy_patient = create_dummy_data()
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

    # hcp_db.document(dummy_hcp.id).set({
    #     "id": dummy_hcp.id,
    #     "firstName": dummy_hcp.firstName,
    #     "lastName": dummy_hcp.lastName,
    #     "phone": dummy_hcp.phone,
    #     "email": dummy_hcp.email,
    #     "profilePicture": dummy_hcp.profilePicture,
    #     "calendar": dummy_hcp.calendar,
    #     "specialty": dummy_hcp.specialty,
    #     "title": dummy_hcp.title,
    #     "hours": hours,
    #     "patients": dummy_hcp.patients
    # })
    # patient_db.document(dummy_patient.id).set({
    #     "id": dummy_patient.id,
    #     "firstName": dummy_patient.firstName,
    #     "lastName": dummy_patient.lastName,
    #     "phone": dummy_patient.phone,
    #     "email": dummy_patient.email,
    #     "dateOfBirth": dummy_patient.dateOfBirth,
    #     "sex": dummy_patient.sex,
    #     "profilePicture": dummy_patient.profilePicture,
    #     "height": dummy_patient.height,
    #     "weight": dummy_patient.weight,
    #     "drinker": dummy_patient.drinker.value,
    #     "smoker": dummy_patient.smoker.value,
    #     "calendar": dummy_patient.calendar,
    #     "health": dummy_patient.health,
    #     "doctors": dummy_patient.doctors
    # })

    auth_token = auth.encode_auth_token(dummy_hcp.id, "HCP")
    hcp_token = auth_token.decode()

    auth_token = auth.encode_auth_token(dummy_patient.id, "PATIENT")
    patient_token = auth_token.decode()
    appointment_token = 'aoc1989,hw2735,1605841671.366644'

    def test_createAppointment_test(self, hcp_token=hcp_token):
        timpstamp = time.time()
        payload = {
            'token': hcp_token,
            'date': timpstamp,
            'duration': 45,
            'hcpid': 'hw2735',
            'patient': 'aoc1989',
            'subject': 'Follow Up',
            'notes': 'Follow up for her schizophrenia',
            'videoUrl': 'https://www.youtube.com/watch?v=dMTQKFS1tpA'}
        response, status_code = appointment_helper.create_appointment(payload)
        self.assertEqual(200, status_code)

    def test_getCalendar_test(self, hcp_token=hcp_token):
        payload = {'token': hcp_token}
        response, status_code = appointment_helper.appointment_get_calendar(payload)
        self.assertEqual(200, status_code)

    def test_getByToken_test(self, hcp_token=hcp_token):
        payload = {'token': hcp_token,
                   'id': 'aoc1989,hw2735,1605841671.366644'}
        response, status_code = appointment_helper.appointment_get_by_token(payload)
        self.assertEqual(401, status_code)

    def test_delete_appointment_test(self, hcp_token=hcp_token):
        payload = {
            'token': hcp_token,
            'id': 'aoc1989,hw2735,1605841671.366644'
        }
        response, status_code = appointment_helper.delete_appointment(payload)
        self.assertEqual(200, status_code)


if __name__ == '__main__':
    unittest.main()
