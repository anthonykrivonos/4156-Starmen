import unittest
import requests
from unittest.mock import MagicMock, Mock


from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))


from src import Database, Patient, HCP,  Appointment, Day, Hours, Status, Auth, pat_signup, pat_get_all, pat_login, pat_delete, pat_get_by_token, pat_edit_profile, pat_get_hcps, pat_set_profile_picture, pat_get_records  # noqa
from tst.constants import dummy_hcp, dummy_appointment, dummy_patient  # noqa


"""
Patient Endpoint Tests
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


unittest.TestLoader.sortTestMethodsUsing = None
hcp_token = ''


class PatientTestCase(unittest.TestCase):
    def test_signup_test(self):
        res = pat_signup(db, dummy_patient)
        self.assertNotEqual(res, 0)

    def test_login(self):
        res = pat_login(db, dummy_patient.id, dummy_patient.email)
        self.assertNotEqual(res, 0)

    def test_getByToken(self):
        res = pat_get_by_token(db, dummy_patient.id)
        self.assertEqual(res, 0)

    def test_delete(self):
        res = pat_delete(db, dummy_patient)
        self.assertEqual(res, 3)

    def test_edit_profile(self):
        res = pat_edit_profile(db, dummy_patient.id, {"stuff": "stuff"})
        self.assertIsNotNone(res)

    def pat_get_records(self):
        res = pat_get_records(db, dummy_patient.id)
        self.assertEqual(res, 0)

    def test_get_hcps(self):
        res = pat_get_hcps(db, db, dummy_patient.id)
        self.assertIsNotNone(res)

    def test_get_all(self):
        res = pat_get_all(db)
        self.assertEqual(res, 2)

    def test_set_profile_picture(self):
        res = pat_set_profile_picture(
            db, dummy_patient.id, dummy_patient.profilePicture)
        self.assertEqual(res, dummy_patient.profilePicture)
        
        
if __name__ == '__main__':
    unittest.main()
