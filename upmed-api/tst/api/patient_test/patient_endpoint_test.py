import unittest
from src import Patient, HCP, Day, Hours, Status, Appointment, Auth  # noqa
from src.api.patient.patient import *
from tst.mock_helpers import *
from unittest.mock import patch

appointment_token = 'aoc1989,hw2735,1605841671.366644'
mockpatient = MockPatient()
mockhcp = MockHCP()
mockappointment = MockAppointment()
mockconversation = MockConversation()
mocktwiliotoken = MockTwilioToken()


class PatientEndpoints(unittest.TestCase):
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_login", return_value=1)
    @patch("src.patient.request")
    def test_login(self, mock1, mock2, mock3):
        payload = {
            'id': mockpatient.patient.id,
            'email': mockpatient.patient.email
        }
        mock1.get_json.return_value = payload
        response, status_code = login()
        self.assertEqual(status_code, 200)

        payload = None
        mock1.get_json.return_value = payload
        response, status_code = login()
        self.assertEqual(status_code, 500)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_signup", return_value=mockpatient.patient)
    def test_signup(self, mock1, mock2, mock3, mock4):
        # Normal case
        payload = mockpatient.patient.to_dict()
        mock3.get_json.return_value = payload
        response, status_code = signup()
        self.assertEqual(status_code, 201)

        # No signup data
        payload = None
        mock3.get_json.return_value = payload
        response, status_code = signup()
        self.assertEqual(status_code, 401)

    @patch("src.patient.request")
    @patch("src.patient.pat_delete", return_value=1)
    @patch("src.patient.jsonify")
    def test_remove(self, mock1, mock2, mock3):
        response, status_code = remove()
        self.assertEqual(status_code, 200)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_get_by_token", return_value=(mockpatient.patient, True))
    def test_getbytoken(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockpatient.auth_token
        }
        mock3.get_json.return_value = payload
        response, status_code = getbytoken()
        self.assertEqual(status_code, 200)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = getbytoken()
        self.assertEqual(status_code, 401)

        payload = {
            'hihihi': 'hihihi'
        }
        mock3.get_json.return_value = payload
        response, status_code = getbytoken()
        self.assertEqual(status_code, 401)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_get_records", return_value=mockpatient.patient)
    def test_get_records(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockpatient.auth_token
        }
        mock3.get_json.return_value = payload
        response, status_code = get_records()
        self.assertEqual(status_code, 200)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = get_records()
        self.assertEqual(status_code, 401)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_edit_profile", return_value=mockpatient.patient)
    def test_edit_profile(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockpatient.auth_token
        }
        mock3.get_json.return_value = payload
        response, status_code = edit_profile()
        self.assertEqual(status_code, 200)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = edit_profile()
        self.assertEqual(status_code, 401)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_get_hcps", return_value=mockhcp.hcp)
    def test_gethcps(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockpatient.auth_token
        }
        mock3.get_json.return_value = payload
        response, status_code = gethcps()
        self.assertEqual(status_code, 200)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = gethcps()
        self.assertEqual(status_code, 401)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_get_all", return_value=mockpatient.patient)
    def test_get_all(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockpatient.auth_token
        }
        mock3.get_json.return_value = payload
        response, status_code = get_all()
        self.assertEqual(status_code, 200)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = get_all()
        self.assertEqual(status_code, 401)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_set_profile_picture", return_value=mockpatient.patient)
    def test_set_profile_picture(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockpatient.auth_token
        }
        mock3.get_json.return_value = payload
        response, status_code = set_profile_picture()
        self.assertEqual(status_code, 200)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = set_profile_picture()
        self.assertEqual(status_code, 401)

    @patch("src.patient.make_response")
    @patch("src.patient.request")
    @patch("src.patient.jsonify")
    @patch("src.patient.pat_search", return_value=mockpatient.patient)
    def test_search(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockpatient.auth_token,
            'text': 'hihihi'
        }
        mock3.get_json.return_value = payload
        response, status_code = search()
        self.assertEqual(status_code, 200)

        # Search text at exactly 3
        payload = {
            'token': mockpatient.auth_token,
            'text': 'hii'
        }
        mock3.get_json.return_value = payload
        response, status_code = search()
        self.assertEqual(status_code, 200)

        # Too short search text
        payload = {
            'token': mockpatient.auth_token,
            'text': 'hi'
        }
        mock3.get_json.return_value = payload
        response, status_code = search()
        self.assertEqual(status_code, 400)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = search()
        self.assertEqual(status_code, 401)


if __name__ == '__main__':
    unittest.main()
