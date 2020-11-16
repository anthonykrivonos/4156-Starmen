/* istanbul ignore file */

import { Status, Patient, HCP, Hours, AppointmentId, PatientId, Appointment, HealthEvent, DoctorId } from '../models'
import { DateTime } from './DateTime'
import { Objects } from './Objects'

class PatientClient {
	public static logIn = (id: string, email: string): Promise<{ id: string; token: string }> => {
		return client('/patient/logIn', { id, email })
	}

	public static signUp = (
		id: string,
		firstName: string,
		lastName: string,
		phone: string,
		email: string,
		dateOfBirth: string,
		sex: string,
		height: number,
		weight: number,
		drinker: Status,
		smoker: Status,
		profilePicture?: string,
	): Promise<{ id: string; token: string }> => {
		return client('/patient/signUp', {
			id,
			firstName,
			lastName,
			phone,
			email,
			dateOfBirth,
			sex,
			profilePicture,
			height,
			weight,
			drinker,
			smoker,
		})
	}

	public static delete = (id: string): Promise<{ success: boolean }> => {
		return client('/patient/delete', { id })
	}

	public static getByToken = (token: string): Promise<Patient> => {
		return client('/patient/getByToken', { token })
	}

	public static getHCPs = async (token: string): Promise<HCP[]> => {
		const hcpMap = (await client('/patient/getHCPs', { token })) as any
		const hcps = Objects.objToArray(hcpMap) as HCP[]
		for (const hcp of hcps) {
			hcp.hours = DateTime.safeParseHours(hcp.hours)
		}
		return Objects.objToArray(hcpMap) as HCP[]
	}

	public static editProfile = (
		id: PatientId,
		token: string,
		firstName: string,
		lastName: string,
		phone: string,
		email: string,
		height: number,
		weight: number,
		drinker: Status,
		smoker: Status,
		profilePicture?: string,
	): Promise<{ success: boolean }> => {
		return client('/patient/editProfile', {
			id,
			token,
			firstName,
			lastName,
			phone,
			email,
			profilePicture,
			height,
			weight,
			drinker,
			smoker,
		})
	}

	public static getRecords = async (token: string): Promise<HealthEvent[]> => {
		const healthMap = (await client('/patient/getRecords', { token })) as any
		return Objects.objToArray(healthMap) as HealthEvent[]
	}

	public static getAll = (token: string): Promise<Patient[]> => {
		return client('/patient/getAll', { token })
	}
}

class HCPClient {
	public static logIn = (id: string, email: string): Promise<{ id: string; token: string }> => {
		return client('/hcp/logIn', { id, email })
	}

	public static signUp = (
		id: string,
		hours: Hours,
		firstName: string,
		lastName: string,
		phone: string,
		email: string,
		specialty?: string,
		title?: string,
		profilePicture?: string,
	): Promise<{ id: string; token: string }> => {
		return client('/hcp/signUp', {
			id,
			hours,
			firstName,
			lastName,
			phone,
			email,
			specialty,
			title,
			profilePicture,
		})
	}

	public static getByToken = async (token: string): Promise<HCP> => {
		const hcp = await client('/hcp/getByToken', { token })
		hcp.hours = DateTime.safeParseHours(hcp.hours)
		return hcp
	}

	public static editProfile = (
		id: DoctorId,
		token: string,
		hours: Hours,
		firstName: string,
		lastName: string,
		phone: string,
		email: string,
		specialty?: string,
		title?: string,
		profilePicture?: string,
	): Promise<{ id: string; token: string }> => {
		return client('/hcp/editProfile', {
			id,
			token,
			hours,
			firstName,
			lastName,
			phone,
			email,
			specialty,
			title,
			profilePicture,
		})
	}

	public static getPatients = async (token: string): Promise<Patient[]> => {
		const patientMap = (await client('/hcp/getPatients', { token })) as any
		return Objects.objToArray(patientMap) as Patient[]
	}

	public static setRecords = (token: string, id: PatientId, health: HealthEvent[]): Promise<HealthEvent[]> => {
		return client('/hcp/setRecords', { token, id, health }) as any
	}

	public static notify = (token: string, id: AppointmentId): Promise<{ success: boolean }> => {
		return client('/hcp/notify', { token, id }) as any
	}

	public static getAll = (token: string): Promise<HCP[]> => {
		return client('/hcp/getAll', { token })
	}
}

class AppointmentClient {
	public static createAppointment = async (
		token: string,
		date: number,
		duration: number,
		subject: string,
		patient?: PatientId,
		hcpid?: DoctorId,
		notes?: string,
		videoUrl?: string,
	): Promise<{ id: AppointmentId }> => {
		return client('/appointment/createAppointment', {
			token,
			date,
			duration,
			patient,
			hcpid,
			subject,
			notes,
			videoUrl,
		})
	}

	public static deleteAppointment = (id: AppointmentId): Promise<{ success: boolean }> => {
		return client('/appointment/deleteAppointment', { id })
	}

	public static getCalendar = async (token: string): Promise<Appointment[]> => {
		return client('/appointment/getCalendar', { token })
	}
}

export class Client {
	public static Patient = PatientClient
	public static HCP = HCPClient
	public static Appointment = AppointmentClient
}

const API_URL = 'https://upmed-api.herokuapp.com'
// const API_URL = 'http://localhost:8080'

/**
 * Creates a URI from the endpoint and API URL.
 * @param endpoint The endpoint to append.
 * @returns A string URI to the given endpoint.
 */
const getUri = (endpoint: string): string => {
	let uri = API_URL
	if (uri.lastIndexOf('/') === uri.length - 1) {
		uri = uri.substring(0, uri.length - 1)
	}
	uri += endpoint
	return uri
}

const parseResponse = async (res: Response) => {
	const resText = await res.text()
	if (!res.ok) {
		throw new Error(resText)
	}
	// Return null if the response is null
	if (!resText || resText === 'null') {
		return null
	}
	// Return JSON if the response is JSON
	try {
		const resJson = JSON.parse(resText)
		if (Objects.isObject(resJson)) {
			return resJson
		}
	} catch {}
	// Return text if the response is text
	return resText
}

/**
 * Calls a upmed-api endpoint and returns the result as JSON or text (or null), depending on what it is.
 * @param endpoint The endpoint to call, starting with a /.
 * @param body The body of the request, usually an object.
 * @returns Asynchronously returns a response.
 * @throws An error coming from upmed-api.
 */
export const client = async (endpoint: string, body: any): Promise<any> => {
	if (endpoint.indexOf('/') !== 0) {
		throw new Error('client Error: endpoint must start with a forward slash')
	}
	const uri = getUri(endpoint)
	console.log(body)
	try {
		const res = await fetch(uri, {
			method: 'POST',
			body: Objects.isObject(body) ? JSON.stringify(body) : body,
			headers: {
				'Content-Type': Objects.isObject(body) ? 'application/json' : 'text/plain',
			},
		})
		return parseResponse(res)
	} catch (e) {
		console.log(e)
		throw new Error(`upmed-api Error: ${e.toString()}`)
	}
}
