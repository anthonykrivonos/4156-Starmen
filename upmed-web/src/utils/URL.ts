import URI from 'urijs'

export class URL {
	// Gets a value from query object.
	public static getFromQuery = (fromURL: string, key: string) => {
		return (URI(fromURL).query(true) as any)[key]
	}
}
