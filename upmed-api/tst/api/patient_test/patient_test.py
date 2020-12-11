import unittest
from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), '../../..'))  # noqa
from unittest.mock import MagicMock, Mock, patch
from src import Patient, HCP, Day, Hours, Status, Appointment, Auth  # noqa
from src import pat_delete, pat_edit_profile, pat_login, pat_get_by_token, pat_set_profile_picture, pat_signup, \
    pat_get_all, pat_get_hcps, pat_get_records, pat_search, add_pat  # noqa
from tst.mock_helpers import MockHCP, MockPatient, MockAppointment, MockSearchClient, MockHCP2  # noqa

auth = Auth()

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

"""
Patient Endpoint Tests
"""


class PatientTestCase(unittest.TestCase):

    @patch("src.patient_helper.add_pat")
    def test_signup_test(self, mock1):
        mock1.return_value = 'Mocked add_pat'
        db = Mock()
        set_func = Mock()

        set_func.set = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)
        res = pat_signup(db, mockpatient.patient, True)
        self.assertNotEqual(res, 0)

        set_func.set = MagicMock(return_value=None)
        res = pat_signup(db, mockpatient.patient, True)
        self.assertEqual(res, 0)

        # Reset the mock return values
        set_func.set = MagicMock(return_value=1)

    def test_login(self):
        func = Mock()
        func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        func.get = MagicMock(return_value=mockpatient.patient)
        db_2 = Mock()
        db_2.document = MagicMock(return_value=func)

        res = pat_login(db_2, mockpatient.patient.id, "fake email address")
        self.assertEqual(res, 0)

        res = pat_login(db_2, mockpatient.patient.id, mockpatient.patient.email)
        self.assertEqual(res['id'], mockpatient.patient.id)

    def test_getByToken(self):
        set_func = Mock()
        db = Mock()
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)
        res, bool_result = pat_get_by_token(db, mockpatient.patient.id)
        self.assertTrue(bool_result)

    def test_delete(self):
        db = Mock()
        set_func = Mock()
        set_func.delete = MagicMock(return_value=default_value_3)
        db.document = MagicMock(return_value=set_func)

        res = pat_delete(db, mockpatient.patient)
        self.assertEqual(res, default_value_3)

    def test_edit_profile(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
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
            'smoker': 0
        }
        res = pat_edit_profile(db, mockpatient.patient.id, payload)
        self.assertIsNotNone(res)

        # Invalid patient details
        res = pat_edit_profile(db, mockpatient.patient.id, None)
        self.assertFalse(res['Success'])

    def test_pat_get_records(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)
        res = pat_get_records(db, mockpatient.patient.id)
        self.assertIsNotNone(res)

        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=None)
        set_func.get = MagicMock(return_value=None)
        db.document = MagicMock(return_value=None)
        res = pat_get_records(db, None)
        self.assertIsNone(res)

    def test_get_hcps(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)

        db2 = Mock()
        set_func2 = Mock()
        mockhcp2 = MockHCP2()
        set_func2.to_dict = MagicMock(return_value=mockhcp2.to_dict())
        set_func2.set = MagicMock(return_value=default_value_1)
        set_func2.get = MagicMock(return_value=mockhcp2)
        db2.document = MagicMock(return_value=set_func2)
        res = pat_get_hcps(db, db2, mockpatient.patient.id)
        self.assertIsNotNone(res)

        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=default_value_1)
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)

        db2 = Mock()
        set_func2 = Mock()
        mockhcp2 = MockHCP2()
        set_func2.to_dict = MagicMock(return_value=default_value_1)
        set_func2.set = MagicMock(return_value=default_value_1)
        set_func2.get = MagicMock(return_value=default_value_1)
        db2.document = MagicMock(return_value=set_func2)
        res = pat_get_hcps(db, db2, mockpatient.patient.id)
        self.assertEqual(res, 0)

    def test_get_all(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.stream = MagicMock(return_value=[mockpatient.patient, mockpatient.patient])
        db.document = MagicMock(return_value=set_func)
        res = pat_get_all(db)
        self.assertEqual(len(res), 2)

    def test_set_profile_picture(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)
        res = pat_set_profile_picture(
            db, mockpatient.patient.id, "URL for new profile pic")
        self.assertEqual(res, "URL for new profile pic")

    @patch("src.patient_helper.SearchClient.create", return_value=searchclient)
    def test_pat_search(self, mock):
        res = pat_search('mock')
        self.assertEqual(len(res), 2)
        self.assertTrue(mock.called, "mock searchclient not being called")

    @patch("src.patient_helper.SearchClient.create", return_value=searchclient)
    def test_add_pat(self, mock):
        res = add_pat(mockpatient.patient)
        self.assertEqual(res, 0)
        self.assertTrue(mock.called, "mock searchclient not being called")


if __name__ == '__main__':
    unittest.main()
