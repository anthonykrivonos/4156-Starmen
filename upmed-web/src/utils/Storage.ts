/* istanbul ignore file */
import { Objects } from './Objects'

export class Storage {
	// Set an object, string, or number is localStorage
	public static set(key: string, value: object | string | number | boolean) {
		if (Objects.isObject(value)) {
			// Item is an object
			const item = JSON.stringify(value)
			localStorage.setItem(key, item)
		} else if (Objects.isNumber(value)) {
			// Item is a number
			const item = `${value}`
			localStorage.setItem(key, item)
		} else {
			// Item is a string
			const item = value as string
			localStorage.setItem(key, item)
		}
	}

	// Get an object, string, or number from localStorage
	public static get(key: string) {
		const item = localStorage.getItem(key)
		if (!Objects.isNullish(item)) {
			try {
				// Try to parse the JSON object
				return JSON.parse(item!)
			} catch (e) {
				// Could not parse the item, that means its a string
				if (!isNaN(item as any)) {
					// Item is a number, return it parsed
					return +item!
				} else if (item === Boolean(item).toString()) {
					// Item is a boolean, return it as a boolean
					return Boolean(item)
				}
				// Item is not an object nor a string
				return item
			}
		}
		return null
	}

	// Check if an object exists in the storage
	public static has(key: string) {
		return !Objects.isNullish(Storage.get(key))
	}

	// Remove an item from localstorage
	public static remove(key: string) {
		localStorage.removeItem(key)
	}

	// Clear localStorage
	public static clear() {
		localStorage.clear()
	}
}
