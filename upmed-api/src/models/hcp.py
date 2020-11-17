from .strings import DoctorId, PatientId, AppointmentId
from .hours import Hours
from typing import List, Optional
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))

"""
HCP Data Model

---Heroku Imports----
from .strings import DoctorId, PatientId, AppointmentId
from .hours import Hours
from typing import List, Optional
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))


---Relative Imports----
from .strings import DoctorId, PatientId, AppointmentId
from .hours import Hours
from typing import List, Optional
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
