from sys import path
from os.path import join, dirname
from typing import List

path.append(join(dirname(__file__), '../..'))

from src import Patient, HCP, Appointment, Day, Hours, Status  # noqa
from src import Auth  # noqa


class MockPatient(object):
    patient: Patient
    auth_token: str

    def __init__(self):
        auth = Auth()
        event1 = {
            'date': 2000,
            'event': "schizophrenia",
            'remarks': "Poor compliance",
            'status': Status.ACTIVE
        }
        event2 = {
            'date': 4000,
            'event': "heart attack",
            'remarks': "Poor compliance",
            'status': Status.ACTIVE
        }
        self.patient = Patient(
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
            calendar=['aoc1989,hw2735,1605841671.366644'],
            health=[event1, event2],
            doctors=["hw2735", "fyy1010"]
        )
        self.auth_token = auth.encode_auth_token(self.patient.id, "PATIENT")


class MockHCP(object):
    hcp: HCP
    auth_token: str

    def __init__(self):
        auth = Auth()
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
        self.hcp = HCP(
            id="hw2735",
            firstName="Kevin",
            lastName="Wong",
            phone="+19175587800",
            email="hw2735@columbia.edu",
            specialty="Accident and Emergency",
            profilePicture='',
            calendar=['aoc1989,hw2735,1605841671.366644'],
            title='Resident',
            patients=['aoc1989'],
            hours=schedule)
        self.auth_token = auth.encode_auth_token(self.hcp.id, "HCP")

    def return_time(self):
        hours = []
        time = []
        time.append(self.hcp.hours.sunday.startTime)
        time.append(self.hcp.hours.sunday.endTime)
        hours.append(str(time))
        time[0] = self.hcp.hours.monday.startTime
        time[1] = self.hcp.hours.monday.endTime
        hours.append(str(time))
        time[0] = self.hcp.hours.tuesday.startTime
        time[1] = self.hcp.hours.tuesday.endTime
        hours.append(str(time))
        time[0] = self.hcp.hours.wednesday.startTime
        time[1] = self.hcp.hours.wednesday.endTime
        hours.append(str(time))
        time[0] = self.hcp.hours.thursday.startTime
        time[1] = self.hcp.hours.thursday.endTime
        hours.append(str(time))
        time[0] = self.hcp.hours.friday.startTime
        time[1] = self.hcp.hours.friday.endTime
        hours.append(str(time))
        time[0] = self.hcp.hours.saturday.startTime
        time[1] = self.hcp.hours.saturday.endTime
        hours.append(str(time))
        return hours


class MockAppointment(object):
    appointment: Appointment

    def __init__(self):
        self.appointment = Appointment(
            id='aoc1989,hw2735,1605841671.366644',
            date=1605841671,
            duration=30,
            doctor='hw2735',
            patient='aoc1989',
            subject='psychiatry',
            notes='notes',
            videoUrl='url')


class MockParticipant(object):
    participant: str

    def __init__(self):
        self.participant = 'mock'

    def create(self, identity):
        pass


class MockConversation(object):
    participants: MockParticipant
    chat_service_sid: str

    def __init__(self):
        self.participants = MockParticipant()
        self.chat_service_sid = 'mock sid'


class jwt(object):
    def decode(self):
        return 'mock twilio token'


class MockTwilioToken(object):
    token: jwt

    def add_grant(self, room):
        pass

    def to_jwt(self):
        self.token = jwt()
        return self.token


class MockClientIndex(object):

    def set_settings(self):
        pass

    def search(self):
        hcp1 = MockHCP()
        output = {
            'hits': [hcp1.hcp.to_dict(), hcp1.hcp.to_dict()]
        }
        return output

    def save_object(self, *args):
        pass


class MockSearchClient(object):

    def init_index(self, input):
        tmp = MockClientIndex
        return tmp

    def save_object(self, *args):
        pass


class MockDocument(object):
    stored_value: None

    def __init__(self, stored_value):
        self.stored_value = stored_value

    def get(self):
        return self.stored_value

    def update(self, *args):
        pass


class MockEndpoint(object):
    values: (0, 0)

    def appointment_get_by_token(self):
        return self.values


class MockRequest(object):
    data: dict

    def __init__(self, data):
        self.data = data

    def get_json(self):
        return self.data


class MockHCP2(object):
    id: str
    firstName: str
    lastName: str
    title: str
    specialty: str
    phone: str
    email: str
    calendar: List[str]
    profilePicture: str
    patients: List[str]
    hours: Hours

    def __init__(self):
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
        self.id = 'hw2735'
        self.firstName = "Kevin"
        self.lastName = "Wong"
        self.title = 'Resident'
        self.specialty = "Accident and Emergency"
        self.phone = "+19175587800"
        self.email = "hw2735@columbia.edu"
        self.calendar = ['aoc1989,hw2735,1605841671.366644']
        self.profilePicture = ''
        self.patients = ['aoc1989,hw2735,1605841671.366644']
        self.hours = schedule

    def to_dict(self):
        output_dict = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'title': self.title,
            'specialty': self.specialty,
            'phone': self.phone,
            'email': self.email,
            'calendar': self.calendar,
            'profilePicture': self.profilePicture,
            'patients': self.patients,
            'hours': self.hours.inc(),
        }
        return output_dict

    def get(self):
        return self
