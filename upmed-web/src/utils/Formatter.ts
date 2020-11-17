export class Formatter {
	public static phone(value: string): string {
		const m = value.match(/^(\d{3})(\d{3})(\d{4})$/)
		return m ? m[1] + '-' + m[2] + '-' + m[3] : value
	}

	public static stringDate(date: Date): string {
		let month = '' + (date.getMonth() + 1)
		let day = '' + date.getDate()
		const year = date.getFullYear()

		if (month.length < 2) {
			month = '0' + month
		}
		if (day.length < 2) {
			day = '0' + day
		}

		return [year, month, day].join('-')
	}
}
