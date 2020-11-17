import React, { useState, useEffect } from 'react'
import DatePicker from 'react-datepicker'
import { Objects } from '../../utils'
import styles from './DateInput.module.sass'

import 'react-datepicker/dist/react-datepicker.css'

interface DateInputProps {
	label?: string
	value?: Date
	required?: boolean
	className?: string
	containerClassName?: string
	onDateChange?: (date: Date) => void
	timeSelect?: boolean
	maxDate?: Date
	minDate?: Date
}

export const DateInput = (props: DateInputProps) => {
	const [date, setDate] = useState(null as Date | null)
	const [didSetDate, setDidSetDate] = useState(false)

	const onDateChange = (nextDate: Date) => {
		setDate(nextDate)
		setDidSetDate(true)
		props.onDateChange && props.onDateChange(nextDate)
	}

	useEffect(() => {
		if (!didSetDate && !Objects.isNullish(props.value) && props.value !== date) {
			setDate(props.value!)
		}
	}, [date, didSetDate, props.value])

	return (
		<div className={props.containerClassName}>
			{props.label && (
				<div>
					{props.label}
					{props.required && <span className={'color-quaternary'}> *</span>}
				</div>
			)}
			<DatePicker
				showMonthDropdown={true}
				showYearDropdown={true}
				className={`${styles.date_picker} ${props.className}`}
				selected={date}
				maxDate={props.maxDate}
				minDate={props.minDate}
				showTimeSelect={props.timeSelect === true}
				dateFormat={`yyyy/MM/dd${props.timeSelect === true ? ' hh:mm aa' : ''}`}
				onChange={(d) => onDateChange(d as Date)}
			/>
		</div>
	)
}
