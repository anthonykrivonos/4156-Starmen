import { DAYS, DAYS_LOWER, MONTHS, INITIAL_HOURS } from '../constants'
import { Hours, Day } from '../models'
import { Objects } from './Objects'

export class DateTime {
	/**
	 * Parses hours in case minutes come back as strings from the backend.
	 * @param hours The hours object to parse.
	 * @returns A parsed hours object.
	 */
	public static safeParseHours = (hours: Hours) => {
		const safeHours = Objects.copy(INITIAL_HOURS)
		for (const day of DAYS_LOWER) {
			;((safeHours as any)[day] as Day).startTime = parseInt(((hours as any)[day] as Day).startTime as any)
			;((safeHours as any)[day] as Day).endTime = parseInt(((hours as any)[day] as Day).endTime as any)
		}
		return safeHours
	}

	/**
	 * Gets the current timezone offset, in hours.
	 * @param date An optional date to test. Defaults to the current Date.
	 * @returns The timezone offset from UTC, in hours.
	 */
	public static hoursOffset = (date?: Date) => {
		if (!date) {
			date = new Date()
		}
		return -date.getTimezoneOffset() / 60
	}

	/**
	 * Gets the minutes in the given date, in locale time.
	 * @param date The date to get the minutes.
	 * @returns The date in minutes.
	 */
	public static getMinutes = (date: Date): number => {
		return date.getHours() * 60 + date.getMinutes()
	}

	/**
	 * Converts a number of minutes to HH:MM string time.
	 * @param minutes A number of minutes.
	 * @returns A time in hh:mm AA format.
	 */
	public static minutesToHHMMAA = (minutes: number): string => {
		const mins = minutes % 60
		const realHours = Math.floor(minutes / 60)
		const amPm = realHours > 11 && realHours < 24 ? 'PM' : 'AM'
		let hours = realHours
		hours = hours === 0 ? 12 : hours % 12 === 0 ? 12 : hours % 12
		return `${hours < 10 ? '0' : ''}${hours}:${mins < 10 ? '0' : ''}${mins} ${amPm}`
	}

	/**
	 * Converts an hh:mm AA time string to minutes.
	 * @param hhMM A time in hh:mm format.
	 * @returns The number of minutes.
	 */
	public static hhmmAAToMinutes = (hhMM: string): number => {
		const isPM = hhMM.substring(6, 8).toLowerCase().includes('pm')
		const mins = parseInt(hhMM.substring(3))
		let hours = parseInt(hhMM.substring(0, 2))
		hours = hours === 12 ? (isPM ? 12 : 0) : isPM ? hours + 12 : hours
		return hours * 60 + mins
	}

	/**
	 * Converts a number of minutes to hh:mm string time.
	 * @param minutes A number of minutes.
	 * @returns A time in hh:nn format.
	 */
	public static minutesToHHMM = (minutes: number): string => {
		const mins = minutes % 60
		const hours = Math.floor(minutes / 60)
		return `${hours < 10 ? '0' : ''}${hours}:${mins < 10 ? '0' : ''}${mins}`
	}

	/**
	 * Converts an hh:mm time string to minutes.
	 * @param hhMM A time in hh:mm format.
	 * @returns The number of minutes.
	 */
	public static hhmmToMinutes = (hhMM: string): number => {
		const mins = parseInt(hhMM.substring(3))
		const hours = parseInt(hhMM.substring(0, 2))
		return hours * 60 + mins
	}

	/**
	 * Converts a yyyy-MM-dd string to a date.
	 * @param hhMM A time in hh:mm format.
	 * @returns The number of minutes.
	 */
	public static dateFromStringDate = (yyyyMMDD: string): Date => {
		const years = parseInt(yyyyMMDD.substring(0, 4))
		const months = parseInt(yyyyMMDD.substring(5, 7))
		const date = parseInt(yyyyMMDD.substring(8, 10))
		const dt = new Date()
		dt.setFullYear(years, months - 1, date)
		return dt
	}

	/**
	 * Modifies the provided date by the inputted offsets.
	 * @param date The date to modify.
	 * @param dYears The offset in years.
	 * @param dMonths The offset in months.
	 * @param dDays The offset in days.
	 * @param dHours The offset in hours.
	 * @param dMinutes The offset in minutes.
	 * @param dSeconds The offset in seconds.
	 * @returns The offsetted date.
	 */
	public static getModifiedDate = (
		date: Date,
		dYears: number = 0,
		dMonths: number = 0,
		dDays: number = 0,
		dHours: number = 0,
		dMinutes: number = 0,
		dSeconds: number = 0,
	): Date => {
		date.setFullYear(date.getFullYear() + dYears)
		date.setMonth((date.getMonth() + dMonths) % 12)
		date.setDate(date.getDate() + dDays)
		date.setHours(date.getHours() + dHours, date.getMinutes() + dMinutes, date.getSeconds() + dSeconds)
		return date
	}

	/**
	 * Creates a pretty date for the given date.
	 * @param date The date to make pretty.
	 * @returns A stringified pretty date.
	 */
	public static prettyDate = (date: Date) => {
		return `${DAYS[date.getDay()]}, ${MONTHS[date.getMonth()]} ${date.getDate()} ${date.getFullYear()}`
	}
}
