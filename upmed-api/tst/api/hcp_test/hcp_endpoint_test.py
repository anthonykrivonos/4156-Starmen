import unittest
from src import Patient, HCP, Day, Hours, Status, Appointment, Auth  # noqa
from src.api.hcp.hcp import *
from tst.mock_helpers import *
from unittest.mock import patch

appointment_token = 'aoc1989,hw2735,1605841671.366644'
mockpatient = MockPatient()
mockhcp = MockHCP()
mockappointment = MockAppointment()
mockconversation = MockConversation()
mocktwiliotoken = MockTwilioToken()


class HCPEndpoints(unittest.TestCase):
    @patch("src.hcp.request")
    @patch("src.hcp.hcp_login", return_value=1)
    @patch("src.hcp.jsonify")
    def test_login(self, mock1, mock2, mock3):
        login()
        self.assertTrue(mock1.called, "jsonify not being called")
        self.assertTrue(mock2.called, "hcp_login not being called")

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.hcp_signup", return_value=1)
    @patch("src.hcp.jsonify")
    def test_signup(self, mock1, mock2, mock3, mock4):
        payload = mockhcp.hcp.to_dict()
        mock3.get_json.return_value = payload
        signup()
        self.assertTrue(mock1.called, "mock1 not being called")
        self.assertTrue(mock2.called, "mock2 not being called")

    @patch("src.hcp.request")
    @patch("src.hcp.hcp_delete", return_value=1)
    @patch("src.hcp.jsonify")
    def test_remove(self, mock1, mock2, mock3):
        remove()
        self.assertTrue(mock1.called, "mock1 not being called")
        self.assertTrue(mock2.called, "mock2 not being called")

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_get_by_token", return_value=mockhcp.hcp)
    def test_getbytoken(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token
        }
        mock3.get_json.return_value = payload
        response, status_code = getbytoken()
        self.assertEqual(status_code, 200)

        payload = {
            'token': auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        }
        mock3.get_json.return_value = payload
        response, status_code = getbytoken()
        self.assertEqual(status_code, 401)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = getbytoken()
        self.assertEqual(status_code, 401)

    @patch("src.hcp.pat.document", return_value=mockpatient.patient)
    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_set_record", return_value=mockhcp.hcp)
    def test_set_health_event(self, mock1, mock2, mock3, mock4, mock5):
        payload = {
            'token': mockhcp.auth_token,
            'id': mockpatient.patient.id,

        }
        mock3.get_json.return_value = payload
        response, status_code = set_health_event()
        self.assertEqual(status_code, 201)

        payload = {
            'token': auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        }
        mock3.get_json.return_value = payload
        response, status_code = set_health_event()
        self.assertEqual(status_code, 401)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = set_health_event()
        self.assertEqual(status_code, 401)

    @patch("src.hcp.pat.document", return_value=mockpatient.patient)
    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_notify", return_value=mockhcp.hcp)
    def test_notify(self, mock1, mock2, mock3, mock4, mock5):
        payload = {
            'token': mockhcp.auth_token,
            'id': mockpatient.patient.id,
        }
        mock3.get_json.return_value = payload
        response, status_code = notify()
        self.assertEqual(status_code, 200)

        payload = {
            'token': auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        }
        mock3.get_json.return_value = payload
        response, status_code = notify()
        self.assertEqual(status_code, 401)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = notify()
        self.assertEqual(status_code, 401)

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_test_number", return_value=mockhcp.hcp)
    def test_test_number(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token,
            'id': mockpatient.patient.id,
        }
        mock3.get_json.return_value = payload
        response, status_code = test_number()
        self.assertEqual(status_code, 200)

        payload = {
            'token': auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        }
        mock3.get_json.return_value = payload
        response, status_code = test_number()
        self.assertEqual(status_code, 401)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = test_number()
        self.assertEqual(status_code, 401)

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_get_patients", return_value={'Success': True})
    def test_edit_hcp_profile(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token,
        }
        mock3.get_json.return_value = payload
        response, status_code = getpatients()
        self.assertEqual(status_code, 200)

        payload = {
            'token': auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        }
        mock3.get_json.return_value = payload
        response, status_code = getpatients()
        self.assertEqual(status_code, 401)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = getpatients()
        self.assertEqual(status_code, 401)

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_edit_profile", return_value={'Success': True})
    def test_getpatients(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token,
            'id': mockpatient.patient.id,
        }
        mock3.get_json.return_value = payload
        response, status_code = edit_hcp_profile()
        self.assertEqual(status_code, 200)

        payload = {
            'token': auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        }
        mock3.get_json.return_value = payload
        response, status_code = edit_hcp_profile()
        self.assertEqual(status_code, 401)

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_set_health_events", return_value=mockpatient.patient)
    def test_set_health_events(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token,
            'id': mockpatient.patient.id,
        }
        mock3.get_json.return_value = payload
        response, status_code = set_health_events()
        self.assertEqual(status_code, 200)
        payload = {
            'token': auth.encode_auth_token(mockpatient.patient.id, "LAWYER")
        }
        mock3.get_json.return_value = payload
        response, status_code = set_health_events()
        self.assertEqual(status_code, 401)

        payload = {
            'token': None
        }
        mock3.get_json.return_value = payload
        response, status_code = set_health_events()
        self.assertEqual(status_code, 401)

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_get_all", return_value=mockpatient.patient)
    def test_get_all(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token,
            'id': mockpatient.patient.id,
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

    def test_make_week(self):
        self.assertIsNotNone(make_week())

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_set_profile_picture", return_value=mockpatient.patient)
    def test_set_profile_picture(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token
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

    @patch("src.hcp.make_response")
    @patch("src.hcp.request")
    @patch("src.hcp.jsonify")
    @patch("src.hcp.hcp_search", return_value=mockpatient.patient)
    def test_search(self, mock1, mock2, mock3, mock4):
        payload = {
            'token': mockhcp.auth_token,
            'text': 'hihihi',
        }
        mock3.get_json.return_value = payload
        response, status_code = search()
        self.assertEqual(status_code, 200)

        payload = {
            'token': mockhcp.auth_token,
            'text': 'hi',
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
