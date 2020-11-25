/* istanbul ignore file */
import { decode } from 'jsonwebtoken'
import { Storage } from './Storage'
import { STORAGE_KEYS } from '../constants'
import { Patient, HCP } from '../models'
import { Client } from './Client'
import { DateTime } from './DateTime'
import { Hasher } from './Hasher'

export class Users {
	public static getCurrentUser = async (): Promise<(Patient | HCP) | null> => {
		const hashedUserData = Storage.get(STORAGE_KEYS.USER_DATA) as string | null
		let userData = hashedUserData ? Hasher.decode(hashedUserData) : null
		if (userData && userData.expDate > Date.now() && !userData.expired) {
			return userData
		}

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
			userData = user as any
			// Expire in one minute
			userData.expDate = DateTime.getModifiedDate(new Date(), 0, 0, 0, 0, 1).getTime()
			userData.expired = false

			Storage.set(STORAGE_KEYS.USER_DATA, Hasher.encode(userData))
		} catch (e) {}

		return user
	}

	public static expireCurrentUser = (): void => {
		const hashedUserData = Storage.get(STORAGE_KEYS.USER_DATA) as string | null
		const userData = hashedUserData ? Hasher.decode(hashedUserData) : null

		if (!userData) {
			return
		}

		userData.expired = true
		Storage.set(STORAGE_KEYS.USER_DATA, Hasher.encode(userData))
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
