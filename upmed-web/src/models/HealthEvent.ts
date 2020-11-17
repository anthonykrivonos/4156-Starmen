import { Status } from './enums'

export interface HealthEvent {
	date: number
	event: string
	remarks?: string
	status: Status
}
