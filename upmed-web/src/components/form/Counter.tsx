import React, { useState, useEffect } from 'react'

import { Objects } from '../../utils'

import { Button } from '../button'
import styles from './Counter.module.sass'

interface CounterProps {
	label?: string
	errorLabel?: string
	value?: number
	onChange?: (val: number) => void
	onFocus?: (val: number) => void
	onBlur?: (val: number) => void
	min?: number
	max?: number
	containerClassName?: string
	required: boolean
}

export const Counter = (props: CounterProps) => {
	const initialValue = !Objects.isNullish(props.value)
		? props.value!
		: !Objects.isNullish(props.min)
		? props.min!
		: !Objects.isNullish(props.max)
		? props.max!
		: 0
	const [value, setValue] = useState(initialValue)
	const [didSetValue, setDidSetValue] = useState(false)

	const increase = () => onChange((value + 1).toString())
	const decrease = () => onChange((value - 1).toString())

	const onChange = (val: string) => {
		let num = Number(val)
		if (!isNaN(num)) {
			if (!Objects.isNullish(props.max)) {
				num = Math.min(num, props.max!)
			}
			if (!Objects.isNullish(props.min)) {
				num = Math.max(num, props.min!)
			}
		} else {
			num = initialValue
		}
		setValue(num)
		props.onChange && props.onChange(num)
	}

	const onFocus = () => {
		if (props.onFocus) {
			props.onFocus(value)
		}
	}

	const onBlur = () => {
		if (props.onBlur) {
			props.onBlur(value)
		}
	}

	useEffect(() => {
		if (!didSetValue && !Objects.isNullish(props.value)) {
			setValue(props.value!)
			setDidSetValue(true)
		}
	}, [didSetValue, props.value])

	return (
		<div className={props.containerClassName}>
			{props.label && (
				<div>
					{props.label}
					{props.required && <span className={'color-quaternary'}> *</span>}
				</div>
			)}
			<div className={styles.counter_inner}>
				<Button text={'–'} className={styles.counter_button} onClick={decrease} />
				<input
					className={styles.input_inner}
					onChange={(e) => onChange(e.target.value)}
					onFocus={onFocus}
					onBlur={onBlur}
					value={value}
				/>
				<Button text={'+'} className={styles.counter_button} onClick={increase} />
			</div>
		</div>
	)
}
