import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
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
        }, 

        /** Function to get the suggestion value from a list of suggestions. */
        getSuggestionValue: () => {return "lol u thought"},
    }

    test('SuggestionInput render.inDocument', async () => {
		render(<SuggestionInput {...SuggestionInputProps}/>)

        const combobox = screen.getByRole("combobox")
        const listbox = screen.getByRole("listbox")
        const input = screen.getByRole("textbox")

        fireEvent.click(combobox)
        // fireEvent.change(combobox, { target: { value: "surgeon" } })
        fireEvent.click(listbox)
        // fireEvent.change(listbox, { target: { value: "surgeon" } })
        fireEvent.click(input)
        fireEvent.change(input, { target: { value: "dentist" } })

        await new Promise((r) => setTimeout(r, 2000));

        screen.debug()

        fireEvent.change(input, { target: { value: "" } })


        const linkElement = screen.getByText(/SuggestionInput label/i)

		expect(linkElement).toBeInTheDocument()
	})

})
