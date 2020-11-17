import React, { useState } from 'react'
import { Hasher } from '../../utils'

import styles from './Dropdown.module.sass'

interface DropdownProps {
	label?: string
	required?: boolean
	onChange?: (option: any, index: number) => void
	options: any[]
	displayOptions?: string[]
	selectedIdx?: number
	className?: string
	containerClassName?: string
	rerender?: any
}

const name = `dropdown-${new Date().getTime()}-${Hasher.encode(Math.random().toString())}`

export const Dropdown = (props: DropdownProps) => {
	const [selectedIdx, setSelectedIdx] = useState(props.selectedIdx || 0)

	const onChange = (option: any, index: number) => {
		props.onChange && props.onChange(option, index)
		setSelectedIdx(index)
	}

	return (
		<div className={props.containerClassName}>
			{props.label && (
				<div>
					{props.label}
					{props.required && <span className={'color-quaternary'}> *</span>}
				</div>
			)}
			<select
				className={`${styles.dropdown} ${props.className} mt-1 w-100`}
				name={name}
				onChange={(e) => onChange(props.options[e.target.selectedIndex], e.target.selectedIndex)}
				value={
					props.displayOptions && props.displayOptions.length > selectedIdx
						? props.displayOptions[selectedIdx]
						: props.options[selectedIdx]
				}
			>
				{props.options.map((option, idx) => (
					<option
						key={`${name}-${idx}`}
						value={
							props.displayOptions && props.displayOptions.length > idx
								? props.displayOptions[idx]
								: option
						}
					>
						{props.displayOptions && props.displayOptions.length > idx ? props.displayOptions[idx] : option}
					</option>
				))}
			</select>
		</div>
	)
}
