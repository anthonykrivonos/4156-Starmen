import React, { Component } from 'react'

import { Objects } from '../../utils'

import styles from './TextInput.module.sass'

interface TextInputProps {
	label?: string
	errorLabel?: string
	value?: string
	placeholder?: string
	onChange?: (val: string) => void
	onFocus?: (val: string) => void
	onBlur?: (val: string) => void
	validator?: (val: string) => boolean
	formatter?: (val: string) => string
	limit: number
	containerClassName?: string
	className?: string
	required: boolean
	rows: number
}

export class TextInput extends Component<TextInputProps> {
	public static defaultProps = {
		className: '',
		containerClassName: '',
		placeholder: '',
		limit: 100,
		required: false,
		rows: 1,
	}

	public state = {
		/** Keep track of text value privately. */
		value: '',
		/** Keep track of validity */
		isValid: true,
	}

	private didReceiveInitialValue: boolean = false

	public componentDidMount() {
		let value = (this.props as any).value
		if (!Objects.isNullish(value)) {
			let isValid = value.length <= this.props.limit
			if (this.props.formatter) {
				value = this.props.formatter(value)
			}
			if (this.props.validator) {
				isValid = isValid && this.props.validator(value)
			}
			this.setState({ value, isValid })
		}
	}

	public componentDidUpdate() {
		let value = (this.props as any).value
		if (!this.didReceiveInitialValue && !Objects.isNullish(value)) {
			let isValid = value.length <= this.props.limit
			if (this.props.formatter) {
				value = this.props.formatter(value)
			}
			if (this.props.validator) {
				isValid = isValid && this.props.validator(value)
			}
			this.didReceiveInitialValue = true
			this.setState({ value, isValid })
		}
	}

	/** Publically return the text value. */
	public getValue = () => {
		return this.state.value
	}

	/** Publically set the text value. */
	public setValue = (value: string) => {
		if (this.props.formatter) {
			value = this.props.formatter(value)
		}
		return this.setState({ value })
	}

	public render() {
		const {
			label,
			errorLabel,
			containerClassName,
			placeholder,
			onFocus,
			onBlur,
			className,
			required,
			rows,
		} = this.props

		const { isValid } = this.state

		return (
			<div className={`${styles.text_outer} ${containerClassName}`}>
				<label>
					{label && (
						<div>
							{label}
							{required && <span className={'color-quaternary'}> *</span>}
						</div>
					)}
					{rows === 1 ? (
						<input
							className={`${styles.text_input} ${isValid ? '' : styles.text_input_error} ${className}`}
							onChange={(e) => this.onChangeText(e.target.value)}
							onFocus={(_) => onFocus && onFocus(this.state.value)}
							onBlur={() => onBlur && onBlur(this.state.value)}
							placeholder={placeholder}
							value={this.state.value}
						/>
					) : (
						<textarea
							className={`${styles.text_input} ${isValid ? '' : styles.text_input_error} ${className}`}
							onChange={(e) => this.onChangeText(e.target.value)}
							onFocus={(_) => onFocus && onFocus(this.state.value)}
							onBlur={() => onBlur && onBlur(this.state.value)}
							placeholder={placeholder}
							rows={rows}
							value={this.state.value}
						/>
					)}
					{!isValid && errorLabel && <div className={styles.error_label}>{errorLabel}</div>}
				</label>
			</div>
		)
	}

	/** Handle text changes here. */
	private onChangeText = (unsanitizedValue: string) => {
		const { onChange, limit, onBlur, rows } = this.props
		// Shorten text to limit
		let value = unsanitizedValue.substring(0, limit)
		if (this.props.formatter) {
			value = this.props.formatter(value)
		}
		if (rows === 1) {
			value = value.replace('\n', '')
		}
		let isValid = value.length <= this.props.limit

		if (this.props.validator) {
			isValid = isValid && this.props.validator(value)
		}

		if (rows === 1 && unsanitizedValue.includes('\n')) {
			onBlur && onBlur(value)
			return
		}

		this.setState({ value, isValid }, () => {
			if (!Objects.isNullish(onChange)) {
				onChange && onChange(value)
			}
		})
	}
}
