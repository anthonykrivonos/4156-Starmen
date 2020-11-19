import React from 'react'
import { render, screen } from '@testing-library/react'
import { TextInput } from '../../../src/components/form/TextInput'


describe('TextInput', () => {

    const TextInputProps = {
        label: "TextInput label",
        errorLabel: "TextInput error label",
        value: "TextInput value",
        placeholder: "TextInput placeholder",
        onChange: (val: string) => {},
        onFocus: (val: string) => {},
        onBlur: (val: string) => {},
        validator: (val: string) => {return true},
        formatter: (val: string) => {return "hello"},
        limit: 10,
        containerClassName: "TextInput containerClassName",
        className: "TextInput className",
        required: true,
        rows: 4,
    }

    test('render.inDocument', () => {
		render(<TextInput {...TextInputProps}/>)
		const linkElement = screen.getByText(/TextInput label/i)
		expect(linkElement).toBeInTheDocument()
	})

})
