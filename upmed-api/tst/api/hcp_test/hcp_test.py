import unittest
from unittest.mock import MagicMock, Mock, patch
from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../../..'))
from src.api.patient.patient_helper import *  # noqa
from src.api.hcp.hcp_helper import *  # noqa
from src.models import Patient, Appointment, HCP, Day, Hours, Status  # noqa
from src.api.hcp.hcp_helper import hcp_signup, hcp_login, hcp_delete, hcp_set_record, hcp_get_by_token, hcp_notify, hcp_get_all, hcp_test_number, hcp_edit_profile, hcp_get_patients, hcp_search, hcp_set_health_events, hcp_set_profile_picture, add_hcp, hcp_set_health_events  # noqa

from tst.mock_helpers import MockHCP, MockAppointment, MockPatient, MockSearchClient, MockHCP2  # noqa

"""
HCP Endpoint Tests
"""


# Set up dummy database and dummy objects
default_value_1 = 1
default_value_2 = 2
default_value_3 = 3

appointment_token = 'aoc1989,hw2735,1605841671.366644'
mockpatient = MockPatient()
mockhcp = MockHCP()
mockappointment = MockAppointment()
searchclient = MockSearchClient()

unittest.TestLoader.sortTestMethodsUsing = None
hcp_token = ''

twilio_set_func = Mock()
twilio_set_func.connect.messages.create = MagicMock(return_value=default_value_1)


class HCPTestCase(unittest.TestCase):

    @patch("src.hcp_helper.requests.get")
    def test_signup_test(self, mock_request):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=default_value_1)
        set_func.set = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)
        res = hcp_signup(db, mockhcp.hcp, mockhcp.hcp.hours, 'JON')
        self.assertNotEqual(res, 0)

    def test_login_test(self):
        func = Mock()
        func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        func.get = MagicMock(return_value=mockhcp.hcp)
        db_2 = Mock()
        db_2.document = MagicMock(return_value=func)

        res = hcp_login(db_2, mockhcp.hcp.id, mockhcp.hcp.email)
        self.assertNotEqual(res, 0)

    def test_set_record(self):
        db = Mock()
        set_func = Mock()
        set_func.set = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)

        res = hcp_set_record(db, mockpatient.patient)
        self.assertEqual(res, default_value_1)

    @patch("src.hcp_helper.Twilio.connect", return_value=twilio_set_func)
    def test_notify_test(self, mock):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)

        adb = Mock()
        set_func2 = Mock()
        set_func2.to_dict = MagicMock(return_value=mockappointment.appointment.to_dict())
        set_func2.get = MagicMock(return_value=mockappointment.appointment)
        adb.document = MagicMock(return_value=set_func2)

        res = hcp_notify(adb, db, mockappointment.appointment.id)
        self.assertTrue(mock.called, "twilio not being called")
        self.assertTrue(res['Success'], 0)

    def test_remove_test(self):
        db = Mock()
        set_func = Mock()
        set_func.delete = MagicMock(return_value=default_value_3)
        db.document = MagicMock(return_value=set_func)
        res = hcp_delete(db, mockhcp.hcp.id)
        self.assertEqual(res, 3)

    def test_getByToken(self):
        set_func = Mock()
        db = Mock()
        mockhcp2 = MockHCP2()
        set_func.get = MagicMock(return_value=mockhcp2)
        db.document = MagicMock(return_value=set_func)

        res = hcp_get_by_token(db, mockhcp.hcp.id)
        self.assertTrue(isinstance(res, HCP))

    @patch("src.hcp_helper.Twilio.connect", return_value=twilio_set_func)
    def test_test_number(self, mock):
        adb = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockappointment.appointment.to_dict())
        set_func.get = MagicMock(return_value=mockappointment.appointment)
        adb.document = MagicMock(return_value=set_func)

        pdb = Mock()
        set_func2 = Mock()
        set_func2.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func2.get = MagicMock(return_value=mockpatient.patient)
        pdb.document = MagicMock(return_value=set_func2)

        res = hcp_test_number(adb, pdb, mockappointment.appointment.id)
        self.assertTrue(mock.called, "twilio not being called")
        self.assertTrue(res['Success'], 0)

    def test_edit_profile(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=mockhcp.hcp)
        db.document = MagicMock(return_value=set_func)
        payload = {
            'id': 'hw2735',
            'firstName': 'athena',
            'lastName': 'pang',
            'phone': '9175587880',
            'email': 'fake email address',
            'specialty': 'family medicine',
            'title': 'consultant',
            'profilePicture': 'dummy profile pic',
            'hours': mockhcp.hcp.hours.to_dict()
        }
        res = hcp_edit_profile(db, mockhcp.hcp.id, payload)

        self.assertTrue(res['Success'])
        payload = {
            'id': 'pyy1010',
            'firstName': 'athena',
            'lastName': 'pang',
            'phone': '9175587880',
            'email': 'fake email address',
            'specialty': 'family medicine',
            'title': 'consultant',
            'profilePicture': 'dummy profile pic',
            'hours': mockhcp.hcp.hours.to_dict()
        }
        res = hcp_edit_profile(db, mockhcp.hcp.id, payload)
        self.assertFalse(res['Success'])

    def test_health_event(self):
        db = Mock()
        set_func = Mock()
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)
        payload = {
            'firstName': 'athena',
            'lastName': 'pang',
            'phone': '9175587880',
            'email': 'fake email address',
            'height': '156',
            'weight': '50',
            'drinker': 0,
            'smoker': 0,
            'calendar': ['aoc1989,hw2735,1605841671.366644'],
            'doctors': ["hw2735", "fyy1010"],
            'health': mockpatient.patient.health
        }
        res = hcp_set_health_events(db, mockpatient.patient.id, payload)
        self.assertIsInstance(res, Patient)

    def test_get_all(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        db.stream = MagicMock(return_value=[mockhcp.hcp, mockhcp.hcp])

        res = hcp_get_all(db)
        self.assertEqual(res[0]["id"], mockhcp.hcp.id)
        self.assertEqual(res[1]["id"], mockhcp.hcp.id)

    def test_get_patients(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        set_func.get = MagicMock(return_value=mockhcp.hcp)
        db.document = MagicMock(return_value=set_func)

        pdb = Mock()
        set_func2 = Mock()
        set_func2.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func2.get = MagicMock(return_value=mockpatient.patient)
        pdb.document = MagicMock(return_value=set_func2)

        res = hcp_get_patients(db, pdb, mockhcp.hcp.id)
        self.assertEqual(res['aoc1989']['id'], 'aoc1989')

    def test_set_profile_picture(self):
        db = Mock()
        set_func = Mock()
        set_func.update = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)

        res = hcp_set_profile_picture(
            db, mockhcp.hcp.id, mockhcp.hcp.profilePicture)
        self.assertEqual(res, mockhcp.hcp.profilePicture)

    @patch("src.hcp_helper.SearchClient.create", return_value=searchclient)
    def test_hcp_search(self, mock):
        res = hcp_search('mock')
        self.assertEqual(len(res), 2)
        self.assertTrue(mock.called, "mock searchclient not being called")

    @patch("src.hcp_helper.SearchClient.create", return_value=searchclient)
    def test_add_hcp(self, mock):
        res = add_hcp(mockhcp.hcp)
        self.assertEqual(res, 0)
        self.assertTrue(mock.called, "mock searchclient not being called")


if __name__ == '__main__':
    unittest.main()
