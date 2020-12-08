import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
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

    const TextInputProps2 = {
        label: "TextInput label",
        errorLabel: "TextInput error label",
        value: "TextInput value\naaa",
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
        rows: 1,
    }

    test('render.inDocument', () => {
		render(<TextInput {...TextInputProps}/>)
        const linkElement = screen.getByText(/TextInput label/i)
        
        const input = screen.getByText('hello')
        
        fireEvent.change(input, { target: { value: 10 } })
        fireEvent.change(input, { target: { value: 'hm' } })
        fireEvent.change(input, { target: { value: 'not a num\n' } })
        fireEvent.blur(input)
        fireEvent.focus(input)
        input.blur()
        input.focus()

		expect(linkElement).toBeInTheDocument()
    })
    
    test('render.inDocument with row=1', () => {
		render(<TextInput {...TextInputProps2}/>)
        const input = screen.getByPlaceholderText(/TextInput placeholder/i)

        fireEvent.change(input, { target: { value: 10 } })
        fireEvent.change(input, { target: { value: 'not a num\nasdsd' } })
        fireEvent.focus(input)
        fireEvent.blur(input)
        input.blur()
        input.focus()
        
		expect(input).toBeInTheDocument()
	})

})
