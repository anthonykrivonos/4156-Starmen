from typing import Optional

from .strings import AppointmentId, DoctorId, PatientId

class Appointment:
    id: AppointmentId
    startDate: int
    endDate: int
    doctor: DoctorId
    subject: str
    notes: Optional[str]
    videoUrl: Optional[str]

    def __init__(
        self,
        id: AppointmentId,
        startDate: int,
        endDate: int,
        doctor: DoctorId,
        subject: str,
        notes: Optional[str],
        videoUrl: Optional[str],
    ):
        self.id = id
        self.startDate = startDate
        self.endDate = endDate
        self.doctor = doctor
        self.subject = subject
        self.notes = notes
        self.videoUrl = videoUrl
