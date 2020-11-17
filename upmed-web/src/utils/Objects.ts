export class Objects {
	/**
	 * Checks if val is null or undefined (nullish).
	 * @param val The value to test.
	 * @returns True if val is null, false otherwise.
	 */
	public static isNullish = (val: any): boolean => val === undefined || val === null

	/**
	 * Checks if val is an array.
	 * @param obj The value to test.
	 * @returns True if val is an array, false otherwise.
	 */
	public static isArray = (val: any): boolean => !Objects.isNullish(val) && val.constructor === Array

	/**
	 * Checks if val is an object.
	 * @param obj The value to test.
	 * @returns True if val is an object, false otherwise.
	 */
	public static isObject = (val: any): boolean => !Objects.isNullish(val) && typeof val === 'object'

	/**
	 * Checks if val is a string.
	 * @param obj The value to test.
	 * @returns True if val is a string, false otherwise.
	 */
	public static isString = (val: any): boolean => typeof val === 'string' || val instanceof String

	/**
	 * Checks if val is a number.
	 * @param obj The value to test.
	 * @returns True if val is a number, false otherwise.
	 */
	public static isNumber = (val: any): boolean => typeof val === 'number' && isFinite(val)

	/**
	 * Flattens an object into an array (keys are removed).
	 * @param obj The object to flatten.
	 * @return An array of values.
	 */
	public static objToArray = (obj: any): any[] => {
		const arr: any[] = []
		for (const key in obj) {
			arr.push(obj[key])
		}
		return arr
	}

	/**
	 * Copies the object.
	 * @param obj The object to copy or deep-copy.
	 * @param withoutProperties The properties to omit.
	 * @param shallow Make a shallow copy of the object? Doesn't use copy() recursively if true.
	 * @returns The copied object.
	 */
	public static copy = (obj: any, withoutProperties: string[] = [], shallow: boolean = false): any => {
		if (Objects.isNullish(obj) || !Objects.isObject(obj)) {
			return obj
		}
		const c = obj.constructor()
		for (const attr in obj) {
			if (obj.hasOwnProperty(attr) && !withoutProperties.includes(attr)) {
				if (shallow) {
					c[attr] = obj[attr]
				} else {
					c[attr] = Objects.copy(obj[attr], [])
				}
			}
		}
		return c
	}
}
