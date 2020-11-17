import React, { useState } from 'react'
import { Hasher } from '../../utils'

import styles from './RadioButtons.module.sass'

interface RadioButtonsProps {
	label?: string
	required?: boolean
	onChange?: (option: any, index: number) => void
	options: any[]
	displayOptions?: string[]
	selectedIdx?: number
	className?: string
}

export const RadioButtons = (props: RadioButtonsProps) => {
	const name = `radio-${new Date().getTime()}-${Hasher.encode(props.options.join(','))}-${Hasher.encode(
		props.label || Math.random().toString(),
	)}`
	const [selectedIdx, setSelectedIdx] = useState(props.selectedIdx || 0)

	const onChange = (option: any, index: number) => {
		setSelectedIdx(index)
		props.onChange && props.onChange(option, index)
	}

	return (
		<div className={`${styles.radio_outter} ${props.className || ''}`}>
			{props.label && (
				<div>
					{props.label}
					{props.required && <span className={'color-quaternary'}> *</span>}
				</div>
			)}
			{props.options.map((option, idx) => (
				<div
					key={`radio-${idx}`}
					className={`${styles.radio_inner} unselectable`}
					onClick={() => onChange(option, idx)}
				>
					<label htmlFor={`${name}-${option}`}>
						{props.displayOptions && props.displayOptions.length > idx ? props.displayOptions[idx] : option}
					</label>
					<input
						type="radio"
						name={name}
						value={`${name}-${option}`}
						checked={selectedIdx === idx}
						onChange={() => onChange(option, idx)}
					/>
				</div>
			))}
		</div>
	)
}
