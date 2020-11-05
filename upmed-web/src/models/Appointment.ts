import { AppointmentId, DoctorId } from './strings'

export interface Appointment {
    id: AppointmentId
    startDate: number
    endDate: number
    doctor: DoctorId
    subject: string
    notes?: string
    videoUrl?: string
}
