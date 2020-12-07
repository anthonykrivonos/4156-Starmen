from typing import List, Optional

from .health_event import HealthEvent
from .strings import DoctorId, PatientId, AppointmentId
from .enums import Status

"""
Patient Data Model
"""


class Patient:
    id: PatientId
    firstName: str
    lastName: str
    calendar: List[AppointmentId]
    phone: str
    email: str
    dateOfBirth: str
    sex: str
    profilePicture: Optional[str]
    height: int
    weight: int
    drinker: Status
    smoker: Status
    health: List[HealthEvent]
    doctors: List[DoctorId]

    def __init__(
            self,
            id: PatientId,
            firstName: str,
            lastName: str,
            calendar: List[AppointmentId],
            phone: str,
            email: str,
            dateOfBirth: str,
            sex: str,
            profilePicture: Optional[str],
            height: int,
            weight: int,
            drinker: Status,
            smoker: Status,
            health: List[HealthEvent],
            doctors: List[DoctorId],
    ):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.calendar = calendar
        self.phone = phone
        self.email = email
        self.dateOfBirth = dateOfBirth
        self.sex = sex
        self.profilePicture = profilePicture
        self.height = height
        self.weight = weight
        self.drinker = drinker
        self.smoker = smoker
        self.health = health
        self.doctors = doctors

    def to_dict(self):
        output_dict = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'calendar': self.calendar,
            'phone': self.phone,
            'email': self.email,
            'dateOfBirth': self.dateOfBirth,
            'sex': self.sex,
            'profilePicture': self.profilePicture,
            'height': self.height,
            'weight': self.weight,
            'drinker': self.drinker,
            'smoker': self.smoker,
            'health': self.health,
            'doctors': self.doctors
        }
        return output_dict

    def get(self):
        return self
