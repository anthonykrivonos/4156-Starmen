from .strings import AppointmentId, DoctorId, PatientId
from typing import Optional
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))
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
