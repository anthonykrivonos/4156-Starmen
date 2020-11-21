from typing import Optional

from .strings import AppointmentId, DoctorId, PatientId

"""
Appointments Model
"""


class Appointment:
    id: AppointmentId
    date: int
    duration: int
    doctor: DoctorId
    patient: PatientId
    subject: str
    notes: Optional[str]
    videoUrl: Optional[str]

    def __init__(
        self,
        id: AppointmentId,
        date: int,
        duration: int,
        doctor: DoctorId,
        patient: PatientId,
        subject: str,
        notes: Optional[str],
        videoUrl: Optional[str],
    ):
        self.id = id
        self.date = date
        self.duration = duration
        self.doctor = doctor
        self.patient = patient
        self.subject = subject
        self.notes = notes
        self.videoUrl = videoUrl
