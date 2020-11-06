from typing import List, Optional

from .enums import Status
from .strings import DoctorId, PatientId, AppointmentId
from .health_event import HealthEvent

class Patient:
    id: PatientId
    firstName: str
    lastName: str
    calendar: List[AppointmentId]
    phone: str
    email: str
    dateOfBirth: int
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
        dateOfBirth: int,
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