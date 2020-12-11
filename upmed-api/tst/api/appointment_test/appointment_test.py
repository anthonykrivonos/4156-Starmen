import unittest
import time, datetime
from src import Patient, HCP, Day, Hours, Status, Appointment, Auth  # noqa
from tst.mock_helpers import *
from unittest.mock import MagicMock, Mock, patch
from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../../..'))
auth = Auth()

"""
Patient Endpoint Tests
Note: run as python3 -m upmed-api.tst.api.appointment_test.appointment_test
"""
appointment_token = 'aoc1989,hw2735,1605841671.366644'
mockpatient = MockPatient()
mockhcp = MockHCP()
mockhcp2 = MockHCP2()
mockappointment = MockAppointment()
mockconversation = MockConversation()
mocktwiliotoken = MockTwilioToken()
path.append(join(dirname(__file__), '../../..'))

"""
Patient Endpoint Tests
Note: run as python3 -m upmed-api.tst.api.appointment_test.appointment_test
"""


class AppointmentTestCase(unittest.TestCase):
    @patch("src.appointment.appointment_helper.appointmentsdb.document")
    @patch("src.appointment.appointment_helper.patient_db.document")
    @patch("src.appointment.appointment_helper.hcp_db.document")
    def test_createAppointment_test(self, mock1, mock2, mock3):
        from src.api.appointment import appointment_helper
        # Define initial payload
        # Test normal case
        timpstamp = datetime.datetime(2020, 12, 9, 12, 30)
        timpstamp = datetime.datetime.timestamp(timpstamp)
        mock1.return_value = MockDocument(mockhcp2)
        payload = {
            'token': mockhcp.auth_token,
            'date': timpstamp,
            'duration': 45,
            'hcpid': 'hw2735',
            'patient': 'aoc1989',
            'subject': 'Follow Up',
            'notes': 'Follow up for her schizophrenia',
            'videoUrl': 'https://www.youtube.com/watch?v=dMTQKFS1tpA'}
        response, status_code = appointment_helper.create_appointment(payload)
        self.assertTrue(mock1.called, "hcp_db.document not being called")
        self.assertTrue(mock2.called, "patient_db.document not being called")
        self.assertTrue(mock3.called, "appointmentsdb.document not being called")
        self.assertEqual(200, status_code)

        # Test using patient token
        payload = {
            'token': mockpatient.auth_token,
            'date': timpstamp,
            'duration': 45,
            'hcpid': 'aoc1989',
            'patient': 'hw2735',
            'subject': 'Follow Up',
            'notes': 'Follow up for schizophrenia',
            'videoUrl': 'https://www.youtube.com/watch?v=dMTQKFS1tpA'}
        response, status_code = appointment_helper.create_appointment(payload)
        self.assertEqual(200, status_code)

        # Test using wrong token
        payload['token'] = None
        response, status_code = appointment_helper.create_appointment(payload)
        self.assertEqual(401, status_code)

        # Test using another identify
        payload['token'] = auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        response, status_code = appointment_helper.create_appointment(payload)
        self.assertEqual(401, status_code)

        # Appointment time out of office hours
        timpstamp = datetime.datetime(2020, 12, 9, 22, 30)
        timpstamp = datetime.datetime.timestamp(timpstamp)
        mock1.return_value = MockDocument(mockhcp2)
        payload = {
            'token': mockhcp.auth_token,
            'date': timpstamp,
            'duration': 45,
            'hcpid': 'hw2735',
            'patient': 'aoc1989',
            'subject': 'Follow Up',
            'notes': 'Follow up for her schizophrenia',
            'videoUrl': 'https://www.youtube.com/watch?v=dMTQKFS1tpA'}
        response, status_code = appointment_helper.create_appointment(payload)
        self.assertEqual(401, status_code)


    @patch("src.appointment.appointment_helper.appointmentsdb.document")
    @patch("src.appointment.appointment_helper.patient_db.document")
    @patch("src.appointment.appointment_helper.hcp_db.document")
    def test_getCalendar_test(self, mock1, mock2, mock3):
        from src.api.appointment import appointment_helper
        mock1.return_value = MockDocument(mockhcp.hcp)
        mock2.return_value = MockDocument(mockpatient.patient)

        # HCP case
        payload = {'token': mockhcp.auth_token}
        response, status_code = appointment_helper.appointment_get_calendar(payload)
        self.assertEqual(200, status_code)

        # Patient case
        payload = {'token': mockpatient.auth_token}
        response, status_code = appointment_helper.appointment_get_calendar(payload)
        self.assertEqual(200, status_code)

        # Invalid token case
        payload = {'token': None}
        response, status_code = appointment_helper.appointment_get_calendar(payload)
        self.assertEqual(401, status_code)

        # No token case
        payload = {'empty': mockpatient.auth_token}
        response, status_code = appointment_helper.appointment_get_calendar(payload)
        self.assertEqual(401, status_code)

        # Invalid token case
        payload = {'token': auth.encode_auth_token('pyy2020', "NURSE")}
        response, status_code = appointment_helper.appointment_get_calendar(payload)
        self.assertEqual(401, status_code)

    @patch("src.appointment.appointment_helper.appointmentsdb.document")
    def test_getByToken_test(self, mock1):
        from src.api.appointment import appointment_helper
        from src.util.util import Auth
        auth = Auth()

        # Normal Case
        payload = {'token': mockhcp.auth_token,
                   'appointmentId': appointment_token}
        mock1.return_value = mockappointment.appointment
        response, status_code = appointment_helper.appointment_get_by_token(payload)
        self.assertEqual(200, status_code)

        # Empty token
        payload = {'token': None,
                   'appointmentId': appointment_token}
        response, status_code = appointment_helper.appointment_get_by_token(payload)
        self.assertEqual(401, status_code)

        # Wrong token
        payload = {'token': auth.encode_auth_token('pyy2020', "NURSE"),
                   'appointmentId': appointment_token}
        response, status_code = appointment_helper.appointment_get_by_token(payload)
        self.assertEqual(401, status_code)

        # Missing token
        payload = {'appointmentId': appointment_token}
        response, status_code = appointment_helper.appointment_get_by_token(payload)
        self.assertEqual(401, status_code)

        # No appointment id
        payload = {'token': mockhcp.auth_token,
                   'appointmentId': None}
        response, status_code = appointment_helper.appointment_get_by_token(payload)
        self.assertEqual(401, status_code)

    @patch("src.appointment.appointment_helper.appointmentsdb.document")
    @patch("src.appointment.appointment_helper.patient_db.document")
    @patch("src.appointment.appointment_helper.hcp_db.document")
    def test_delete_appointment_test(self, mock1, mock2, mock3):
        from src.api.appointment import appointment_helper

        payload = {
            'token': mockhcp.auth_token,
            'id': appointment_token
        }
        response, status_code = appointment_helper.delete_appointment(payload)
        self.assertEqual(200, status_code)

        payload = {
            'token': None,
            'id': None
        }
        response, status_code = appointment_helper.delete_appointment(payload)
        self.assertEqual(401, status_code)

        # Invalid token case
        payload = {'token': auth.encode_auth_token('pyy2020', "NURSE"),
                   'id': appointment_token}
        response, status_code = appointment_helper.appointment_get_calendar(payload)
        self.assertEqual(401, status_code)

        # Test using another identify
        payload = {'token': auth.encode_auth_token(mockhcp.hcp.id, "LAWYER"),
                   'id': appointment_token}
        response, status_code = appointment_helper.delete_appointment(payload)
        self.assertEqual(401, status_code)

    @patch("src.appointment_helper.twilio.access_token", return_value=mocktwiliotoken)
    @patch("src.appointment_helper.appointmentsdb.document", return_value=mockappointment.appointment)
    @patch("src.appointment_helper.get_chatroom", return_value=mockconversation)
    def test_video(self, mock_get_chatroom, mock_document, mock_twilio_token):
        from src.api.appointment import appointment_helper
        payload = {
            'token': mockhcp.auth_token,
            'appointmentId': appointment_token,
        }
        response, status_code = appointment_helper.video(payload)
        self.assertEqual(200, status_code)
        self.assertTrue(mock_get_chatroom.called, "mock_get_chatroom not being called")
        self.assertTrue(mock_document.called, "mock_document not being called")
        self.assertTrue(mock_twilio_token.called, "mock_twilio_token not being called")

        payload = {
            'abc': None,
            'appointmentId': appointment_token,
        }
        response, status_code = appointment_helper.video(payload)
        self.assertEqual(401, status_code)

        payload = {
            'token': auth.encode_auth_token("abc0000", "LAWYER"),
            'appointmentId': appointment_token,
        }
        response, status_code = appointment_helper.video(payload)
        self.assertEqual(401, status_code)


if __name__ == '__main__':
    unittest.main()
