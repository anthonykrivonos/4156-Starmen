import unittest
from src import Patient, HCP, Day, Hours, Status, Appointment, Auth  # noqa
from src.api.appointment.appointment import *
from tst.mock_helpers import *
from unittest.mock import MagicMock, Mock, patch


class AppointmentEndpoints(unittest.TestCase):
    @patch("src.appointment.request")
    @patch("src.appointment.appointment_helper.create_appointment", return_value=(0, 0))
    @patch("src.appointment.make_response")
    @patch("src.appointment.jsonify")
    def test_createAppointment(self, mock1, mock2, mock3, mock4):
        create_appointment()
        self.assertTrue(mock1.called, "make_response not being called")
        self.assertTrue(mock2.called, "create_appointment not being called")
        self.assertTrue(mock3.called, "request not being called")

    @patch("src.appointment.request")
    @patch("src.appointment.appointment_helper.appointment_get_by_token", return_value=(0, 0))
    @patch("src.appointment.make_response")
    @patch("src.appointment.jsonify")
    def test_get_by_token(self, mock1, mock2, mock3, mock4):
        get_by_token()
        self.assertTrue(mock1.called, "make_response not being called")
        self.assertTrue(mock2.called, "create_appointment not being called")
        self.assertTrue(mock3.called, "request not being called")

    @patch("src.appointment.request")
    @patch("src.appointment.appointment_helper.appointment_get_calendar", return_value=(0, 0))
    @patch("src.appointment.make_response")
    @patch("src.appointment.jsonify")
    def test_get_calendar(self, mock1, mock2, mock3, mock4):
        get_calendar()
        self.assertTrue(mock1.called, "make_response not being called")
        self.assertTrue(mock2.called, "create_appointment not being called")
        self.assertTrue(mock3.called, "request not being called")

    @patch("src.appointment.request")
    @patch("src.appointment.appointment_helper.delete_appointment", return_value=(0, 0))
    @patch("src.appointment.make_response")
    @patch("src.appointment.jsonify")
    def test_delete_appointment(self, mock1, mock2, mock3, mock4):
        delete_appointment()
        self.assertTrue(mock1.called, "make_response not being called")
        self.assertTrue(mock2.called, "create_appointment not being called")
        self.assertTrue(mock3.called, "request not being called")


if __name__ == '__main__':
    unittest.main()
