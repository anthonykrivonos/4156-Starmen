import { AppointmentId, DoctorId, PatientId } from './strings'

export interface Appointment {
	id: AppointmentId
	date: number
	duration: number
	doctor: DoctorId
	patient: PatientId
	subject: string
	notes?: string
	videoUrl?: string
}
