# import unittest
#
# import requests
# from ....src.util.firebase.db import Database
# from ....src.models.patient import Patient
# from ....src.models.hcp import HCP
# from ....src.models.appointment import Appointment
# from ....src.models.day import Day
# from ....src.models.hours import Hours
# from ....src.models.enums import Status
# from ....src.util.util import Auth
#
#
# """
# Patient Endpoint Tests
# ----------Heroku Imports--------------
# from util.firebase.db import Database
# from models.patient import Patient
# from models.hcp import HCP
# from models.appointment import Appointment
# from models.day import Day
# from models.hours import Hours
# from models.enums import Status
# from util.util import Auth
#
#
# ---Relative Imports---
# from ....src.util.firebase.db import Database
# from ....src.models.patient import Patient
# from ....src.models.hcp import HCP
# from ....src.models.appointment import Appointment
# from ....src.models.day import Day
# from ....src.models.hours import Hours
# from ....src.models.enums import Status
# from ....src.util.util import Auth
# """
#
#
# def create_dummy_data():
#     # Add some dummy patient and hcp
#     week = []
#     for i in range(0, 7):
#         week.append(Day(startTime=540, endTime=1020, ))
#     schedule = Hours(
#         sunday=week[0],
#         monday=week[1],
#         tuesday=week[2],
#         wednesday=week[3],
#         thursday=week[4],
#         friday=week[5],
#         saturday=week[6])
#     dummy_hcp = HCP(
#         id="hw2735",
#         firstName="Kevin",
#         lastName="Wong",
#         phone="+19175587800",
#         email="hw2735@columbia.edu",
#         specialty="Accident and Emergency",
#         profilePicture='',
#         calendar=[],
#         title='Resident',
#         patients=[],
#         hours=schedule)
#
#     dummy_patient = Patient(
#         id="aoc1989",
#         firstName="Alexandria",
#         lastName="Ocasio-Cortez",
#         phone="0000000000",
#         email="aoc@democrat.com",
#         dateOfBirth="1989-10-13",
#         sex='F',
#         profilePicture='',
#         height=150,
#         weight=60,
#         drinker=Status.NEVER,
#         smoker=Status.NEVER,
#         calendar=[],
#         health=[],
#         doctors=["hw2735"]
#     )
#
#     dummy_appointment = Appointment(
#         id='aoc1989,hw2735,1605505365',
#         date=1605505365,
#         duration=30,
#         doctor='hw2735',
#         patient='aoc1989',
#         subject='follow up',
#         notes='need to check if she is compliant to prescriptions',
#         videoUrl='https://www.youtube.com/watch?v=EsKZHGtSoVA'
#     )
#     return dummy_hcp, dummy_patient, dummy_appointment
#
#
# class PatientTestCase(unittest.TestCase):
#     auth = Auth()
#     pdb = Database()
#     hcp_db = pdb.getHCP()
#     patient_db = pdb.getPatients()
#     appointmentsdb = pdb.getAppointments()
#     dummy_hcp, dummy_patient, dummy_appointment = create_dummy_data()
#     hcp_db.document(dummy_hcp.id).set({
#         "id": dummy_hcp.id,
#         "firstName": dummy_hcp.firstName,
#         "lastName": dummy_hcp.lastName,
#         "phone": dummy_hcp.phone,
#         "email": dummy_hcp.email,
#         "profilePicture": dummy_hcp.profilePicture,
#         "calendar": dummy_hcp.calendar,
#         "specialty": dummy_hcp.specialty,
#         "title": dummy_hcp.title,
#         "hours": dummy_hcp,
#         "patients": dummy_hcp.patients
#     })
#     patient_db.document(dummy_patient.id).set({
#         "id": dummy_patient.id,
#         "firstName": dummy_patient.firstName,
#         "lastName": dummy_patient.lastName,
#         "phone": dummy_patient.phone,
#         "email": dummy_patient.email,
#         "dateOfBirth": dummy_patient.dateOfBirth,
#         "sex": dummy_patient.sex,
#         "profilePicture": dummy_patient.profilePicture,
#         "height": dummy_patient.height,
#         "weight": dummy_patient.weight,
#         "drinker": dummy_patient.drinker,
#         "smoker": dummy_patient.smoker,
#         "calendar": dummy_patient.calendar,
#         "health": dummy_patient.health,
#         "doctors": dummy_patient.doctors
#     })
#     appointmentsdb.document(dummy_appointment.id).set({
#         'id': dummy_appointment.id,
#         'date': dummy_appointment.date,
#         'duration': dummy_appointment.duration,
#         'doctor': dummy_appointment.doctor,
#         'patient': dummy_appointment.patient,
#         'subject': dummy_appointment.subject,
#         'notes': dummy_appointment.notes,
#         'videoUrl': dummy_appointment.videoUrl
#     })
#
#     auth_token = auth.encode_auth_token(dummy_hcp.id, "HCP")
#     hcp_token = auth_token.decode()
#
#     auth_token = auth.encode_auth_token(dummy_patient.id, "PATIENT")
#     patient_token = auth_token.decode()
#
#     def signup_test(self):
#         payload = {'id': "jb0000",
#                    'firstName': "Joe",
#                    'lastName': "Biden",
#                    'phone': '"9175587000"',
#                    'email': "joebiden@democrat.edu",
#                    'dateOfBirth': "1942-11-20",
#                    'sex': 'M',
#                    'height': 183,
#                    'weight': 60,
#                    'drinker': 0,
#                    'smoker': 0}
#
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/signUp',
#             params=payload)
#         self.assertEqual(201, response.status_code)
#         self.assertEqual({'id': 'jb0000'}, response.id)
#
#     def login_test(self):
#         payload = {'id': "jb0000",
#                    'email': "joebiden@democrat.edu"}
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/logIn',
#             params=payload)
#         self.assertEqual(200, response.status_code)
#         self.assertEqual({'id': 'jb0000'}, response.id)
#
#     def getbytoken_test(self):
#         payload = {'token': PatientTestCase.patient_token}
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/getbytoken',
#             params=payload)
#         self.assertEqual(201, response.status_code)
#
#     def getRecords_test(self):
#         payload = {'token': PatientTestCase.patient_token}
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/notify',
#             params=payload)
#         self.assertEqual(200, response.status_code)
#
#     def remove_test(self):
#         payload = {'id': 'jb0000'}
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/delete',
#             params=payload)
#         self.assertEqual(200, response.status_code)
#
#     def editProfile_test(self):
#         payload = {'token': PatientTestCase.patient_token,
#                    'firstName': "Nansi",
#                    'lastName': "Pelosi",
#                    'phone': "0000000000",
#                    'email': "np@democrat.com",
#                    'dateOfBirth': "1989-10-13",
#                    'sex': 'F',
#                    'profilePicture': '',
#                    'height': 150,
#                    'weight': 60,
#                    'drinker': Status.NEVER,
#                    'smoker': Status.NEVER,
#                    'calendar': [],
#                    'health': [],
#                    'doctors': ["hw2735"]
#                    }
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/editProfile',
#             params=payload)
#         self.assertEqual(200, response.status_code)
#
#     def gethcps_test(self):
#         payload = {'token': PatientTestCase.patient_token}
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/getHCPs',
#             params=payload)
#         self.assertEqual(200, response.status_code)
#
#     def get_all_test(self):
#         payload = {'token': PatientTestCase.patient_token}
#         response = requests.get(
#             'http://127.0.0.1:8080/patient/getAll',
#             params=payload)
#         self.assertEqual(200, response.status_code)
#
#
# if __name__ == '__main__':
#     unittest.main()
