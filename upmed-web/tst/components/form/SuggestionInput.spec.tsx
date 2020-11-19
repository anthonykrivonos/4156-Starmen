import React from 'react'
import { render, screen } from '@testing-library/react'
import { SuggestionInput } from '../../../src/components/form/SuggestionInput'


describe('SuggestionInput', () => {

    const SuggestionInputProps = {
        label: "SuggestionInput label",
        value: "SuggestionInput value",
        required: true,
        className: "SuggestionInput className",
        containerClassName: "SuggestionInput containerClassName",
        suggestionLimit: 5,
        onChange: (value: string) => {},
        
        /** A function to asynchronously provide suggestions to the input. */
        getSuggestions: async (value: string): Promise<any[]> => {
            return []
        } 

        /** Function to get the suggestion value from a list of suggestions. */
        // getSuggestionValue: GetSuggestionValue<any>
    }

    test('render.inDocument', () => {
		render(<SuggestionInput {...SuggestionInputProps}/>)
		const linkElement = screen.getByText(/SuggestionInput label/i)
		expect(linkElement).toBeInTheDocument()
	})

})
