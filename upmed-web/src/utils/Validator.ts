import Filter from 'bad-words'
import { Day, Hours } from '../models'

export class Validator {
	// Returns true if there are no bad words.
	public static badWords(value: string): boolean {
		const filter = new Filter()
		return value === '' || filter.clean(value) === value
	}

	// Returns true if the name is valid, false otherwise.
	public static realName(value: string): boolean {
		return (
			value === '' ||
			(value.trim() !== '' && Validator.badWords(value) && /^[a-zA-Z ]+(?:-[a-zA-Z]+)*$/.test(value))
		)
	}

	// Returns true if the short text is valid, false otherwise.
	public static text(value: string): boolean {
		return Validator.badWords(value)
	}

	// Returns true if the phone number is valid.
	public static phone(value: string): boolean {
		return value === '' || /^(()?\d{3}())?(-|\s)?\d{3}(-|\s)?\d{4}$/i.test(value)
	}

	// Returns true if the NPI is valid.
	public static npi(value: string): boolean {
		return value === '' || (value.length === 10 && /^\d+$/.test(value))
	}

	// Returns true if the YYYY-MM-DD date is valid.
	public static stringDate(value: string): boolean {
		return value === '' || /^(\d{4}-\d{2}-\d{2})$/i.test(value)
	}

	// Returns true if the email is valid, false otherwise.
	public static email(value: string): boolean {
		return (
			value === '' ||
			/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
				value.toLowerCase(),
			)
		)
	}

	// Returns true if the hours object is valid.
	public static hours(value: Hours): boolean {
		for (const day in value as any) {
			const dayObj = (value as any)[day] as Day
			if (
				(value.hasOwnProperty(day) &&
					((dayObj.startTime === -1 && dayObj.endTime !== -1) ||
						(dayObj.startTime !== -1 && dayObj.endTime === -1))) ||
				(dayObj.startTime < 0 && dayObj.startTime !== -1) ||
				dayObj.startTime > 1440 ||
				dayObj.startTime > dayObj.endTime ||
				dayObj.endTime > 1440
			) {
				return false
			}
		}
		return true
	}
}
