import React, { useState, useEffect } from 'react'
import Autosuggest, {
	RenderSuggestion,
	RenderSuggestionsContainer,
	GetSuggestionValue,
	SuggestionsFetchRequested,
} from 'react-autosuggest'

import { Objects } from '../../utils'

import styles from './SuggestionInput.module.sass'

import 'react-datepicker/dist/react-datepicker.css'

interface SuggestionInputProps {
	label?: string
	value?: string
	required?: boolean
	className?: string
	containerClassName?: string
	suggestionLimit?: number
	onChange?: (value: string) => void
	/** A function to asynchronously provide suggestions to the input. */
	getSuggestions: (value: string) => Promise<any[]>
	/** Function to get the suggestion value from a list of suggestions. */
	getSuggestionValue?: GetSuggestionValue<any>
}

export const SuggestionInput = (props: SuggestionInputProps) => {
	const [value, setValue] = useState('')
	const [suggestions, setSuggestions] = useState([] as any[])

	const getSuggestionValue = (v: any) => {
		if (props.getSuggestionValue) {
			return props.getSuggestionValue(v)
		}
		return v
	}

	const onChange = (nextValue: string) => {
		setValue(nextValue)
		props.onChange && props.onChange(nextValue)
	}

	const renderSuggestion: RenderSuggestion<any> = (suggestion: any, { isHighlighted }) => {
		return (
			<div
				key={getSuggestionValue(suggestion)}
				onClick={() => {
					onChange(getSuggestionValue(suggestion))
					onSuggestionsClearRequested()
				}}
				className={`${styles.suggestion} ${isHighlighted ? styles.highlighted : ''}`}
			>
				{getSuggestionValue(suggestion)}
			</div>
		)
	}

	const renderSuggestionsContainer: RenderSuggestionsContainer = ({ containerProps, children, query }) => {
		containerProps.className = ''
		return (
			<div {...containerProps} className={styles.suggestions}>
				{suggestions.map((s) => renderSuggestion(s, { isHighlighted: false, query }))}
			</div>
		)
	}

	const onSuggestionsFetchRequested: SuggestionsFetchRequested = (res) => {
		props.getSuggestions(res.value).then((s) => setSuggestions(s))
	}

	const onSuggestionsClearRequested = () => {
		setSuggestions([])
	}

	useEffect(() => {
		if (!Objects.isNullish(props.value)) {
			setValue(props.value!)
		}
	}, [props.value])

	return (
		<div className={props.containerClassName}>
			{props.label && (
				<div>
					{props.label}
					{props.required && <span className={'color-quaternary'}> *</span>}
				</div>
			)}
			<Autosuggest
				suggestions={suggestions}
				onSuggestionsFetchRequested={onSuggestionsFetchRequested}
				onSuggestionsClearRequested={onSuggestionsClearRequested}
				renderSuggestionsContainer={renderSuggestionsContainer}
				getSuggestionValue={getSuggestionValue}
				renderSuggestion={renderSuggestion}
				inputProps={{ onChange: (_, res) => onChange(res.newValue), value, className: styles.suggestion_input }}
			/>
		</div>
	)
}
