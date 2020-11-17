/* istanbul ignore file */
import { decode } from 'jsonwebtoken'
import { Storage } from './Storage'
import { STORAGE_KEYS } from '../constants'
import { Patient, HCP } from '../models'
import { Client } from './Client'

export class Users {
	public static getCurrentUser = async (): Promise<(Patient | HCP) | null> => {
		const userToken = Storage.get(STORAGE_KEYS.USER_TOKEN)
		if (userToken === null) {
			return null
		}
		let user = null as (Patient | HCP) | null
		try {
			const decoded = decode(userToken) as any
			const isPatient = decoded.userType !== 'HCP'
			if (isPatient) {
				user = await Client.Patient.getByToken(userToken)
			} else {
				user = await Client.HCP.getByToken(userToken)
			}
		} catch (e) {}
		return user
	}

	public static getIsPatient = (): boolean => {
		const userToken = Storage.get(STORAGE_KEYS.USER_TOKEN)
		if (userToken === null) {
			return true
		}
		const decoded = decode(userToken) as any
		return decoded.userType !== 'HCP'
	}

	public static logOut = () => Users.clearUserToken()

	public static getUserToken = () => Storage.get(STORAGE_KEYS.USER_TOKEN)
	public static hasUserToken = () => Storage.has(STORAGE_KEYS.USER_TOKEN)
	public static setUserToken = (userToken: string) => Storage.set(STORAGE_KEYS.USER_TOKEN, userToken)
	public static clearUserToken = () => Storage.remove(STORAGE_KEYS.USER_TOKEN)
}
