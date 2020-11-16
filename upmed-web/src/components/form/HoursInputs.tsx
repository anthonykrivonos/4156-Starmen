import React, { useState } from 'react'
import { capitalize } from 'lodash'

import { INITIAL_HOURS, DAYS } from '../../constants'
import { Hasher, DateTime, Objects } from '../../utils'
import { Hours, Day } from '../../models'
import { Dropdown } from './Dropdown'

import styles from './HoursInputs.module.sass'

interface HoursInputsProps {
	label?: string
	required?: boolean
	initialHours?: Hours
	onChange?: (hours: Hours, isValid: boolean) => void
	className?: string
}

// Values set in the Day object for a given day if the office is closed
const TIME_ABSENT = -1

export const HoursInputs = (props: HoursInputsProps) => {
	// const offset = DateTime.hoursOffset() * 60
	const name = `radio-${new Date().getTime()}-${Hasher.encode(props.label || Math.random().toString())}`

	const [hours, setHours] = useState(DateTime.safeParseHours(props.initialHours || (INITIAL_HOURS as Hours)))
	const [invalids, setInvalids] = useState(new Set<string>())

	const getHours = (day: string) => {
		return (hours as any)[day.toLowerCase()] as Day
	}

	const availableTimes: number[] = []
	const displayAvailableTimes: string[] = []
	for (let i = 0; i < 1440; i += 30) {
		availableTimes.push(i)
		displayAvailableTimes.push(DateTime.minutesToHHMMAA(i))
	}

	const updateHours = (day: string, startTime?: number, endTime?: number) => {
		day = day.toLowerCase()
		const hrs = Objects.copy(hours)
		if (startTime !== undefined) {
			;(hrs[day] as Day).startTime = startTime
		}
		if (endTime !== undefined) {
			;(hrs[day] as Day).endTime = endTime
		}
		const isValid = (hrs[day] as Day).startTime <= (hrs[day] as Day).endTime
		const newInvalids = new Set(invalids)
		!isValid ? newInvalids.add(day) : newInvalids.delete(day)
		setInvalids(newInvalids)
		setHours(hrs)
		onChange(hrs, isValid)
	}

	const onDaySelect = (day: string) => {
		if (getHours(day) && getHours(day).startTime === TIME_ABSENT) {
			updateHours(day, 0, 1440)
		} else {
			updateHours(day, TIME_ABSENT, TIME_ABSENT)
		}
	}

	const onChange = (h: Hours, isValid: boolean) => {
		const hrs = Objects.copy(h)
		// Normalize the hours to UTC
		for (let day of DAYS) {
			day = day.toLowerCase()
			;(hrs[day] as Day).startTime = (hrs[day] as Day).startTime % 1440
			;(hrs[day] as Day).endTime = (hrs[day] as Day).endTime % 1440
		}
		props.onChange && props.onChange(hrs, isValid)
	}

	return (
		<div className={`${styles.hours_outter} ${props.className ? props.className : ''}`}>
			{props.label && (
				<div>
					{props.label}
					{props.required && <span className={'color-quaternary'}> *</span>}
				</div>
			)}
			{DAYS.map((day, idx) => (
				<div
					key={`hours-day-${idx}`}
					className={`${styles.hours_row} ${invalids.has(day) ? styles.hours_row_invalid : ''} clickable`}
					onClick={() => onDaySelect(day)}
				>
					<div className={'col-1 d-flex flex-direction-row justify-content-start p-0 unselectable clickable'}>
						<input
							type="checkbox"
							name={`${name}-${day}`}
							value={day}
							onChange={() => onDaySelect(day)}
							checked={getHours(day).startTime !== TIME_ABSENT}
						/>
					</div>
					<div
						className={`col-3 p-0 ${
							getHours(day).startTime !== TIME_ABSENT ? 'font-weight-bold' : ''
						} unselectable clickable`}
					>
						<label htmlFor={`${name}-${day}`} className={'clickable'}>
							{capitalize(day)}
						</label>
					</div>
					<div className={'col-4'} onClickCapture={(e) => e.stopPropagation()}>
						{hours && getHours(day).startTime !== TIME_ABSENT ? (
							<Dropdown
								rerender={hours}
								options={availableTimes}
								displayOptions={displayAvailableTimes}
								selectedIdx={availableTimes.indexOf(getHours(day).startTime)}
								onChange={(t) => updateHours(day, t, undefined)}
							/>
						) : (
							<div className={styles.closed}>Closed</div>
						)}
					</div>
					<div className={'col-4'} onClickCapture={(e) => e.stopPropagation()}>
						{hours && getHours(day).endTime !== TIME_ABSENT && (
							<Dropdown
								rerender={hours}
								options={availableTimes}
								displayOptions={displayAvailableTimes}
								selectedIdx={availableTimes.indexOf(getHours(day).endTime)}
								onChange={(t) => updateHours(day, undefined, t)}
							/>
						)}
					</div>
				</div>
			))}
		</div>
	)
}
