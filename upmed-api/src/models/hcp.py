from .strings import DoctorId, PatientId, AppointmentId
from .hours import Hours
from typing import List, Optional

"""
HCP Data Model
"""


class HCP:
    id: DoctorId
    firstName: str
    lastName: str
    title: Optional[str]
    specialty: Optional[str]
    phone: str
    email: str
    calendar: List[AppointmentId]
    profilePicture: Optional[str]
    patients: List[PatientId]
    hours: Hours

    def __init__(
            self,
            id: DoctorId,
            firstName: str,
            lastName: str,
            title: Optional[str],
            specialty: Optional[str],
            phone: str,
            email: str,
            calendar: List[AppointmentId],
            profilePicture: Optional[str],
            patients: List[PatientId],
            hours: Hours,
    ):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.title = title
        self.specialty = specialty
        self.phone = phone
        self.email = email
        self.calendar = calendar
        self.profilePicture = profilePicture
        self.patients = patients
        self.hours = hours

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
            'hours': self.hours.to_dict(),
        }
        return output_dict

    def to_inc(self):
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
