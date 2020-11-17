import { AppointmentId, DoctorId, PatientId } from './strings'
import { Status } from './enums'
import { HealthEvent } from './HealthEvent'

export interface Patient {
	id: PatientId
	firstName: string
	lastName: string
	calendar: AppointmentId[]
	phone: string
	email: string
	dateOfBirth: string
	sex: string
	profilePicture?: string
	height: number
	weight: number
	drinker: Status
	smoker: Status
	health: HealthEvent[]
	doctors: DoctorId[]
}
