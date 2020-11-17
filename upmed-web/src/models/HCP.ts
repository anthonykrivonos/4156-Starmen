import { AppointmentId, DoctorId, PatientId } from './strings'
import { Hours } from './Hours'

export interface HCP {
	id: DoctorId
	firstName: string
	lastName: string
	title: string
	specialty?: string
	phone: string
	email: string
	calendar: AppointmentId[]
	profilePicture?: string
	patients: PatientId[]
	hours: Hours
}
