import URI from 'urijs'

export class URL {
	// Gets a value from query object.
	public static getFromQuery = (fromURL: string, key: string): string | null => {
		const urlObj = URI(fromURL).query(true) as any
		return urlObj.hasOwnProperty(key) ? urlObj[key] : null
	}
}
