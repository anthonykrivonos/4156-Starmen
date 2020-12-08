import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Counter } from '../../../src/components/form/Counter'

describe('Counter', () => {

    const counterProps = {
        label: "label",
        errorLabel: "errorLabel",
        value: 5,
        onChange: (val: number) => {},
        onFocus: (val: number) => {},
        onBlur: (val: number) => {},
        min: 0,
        max: 100,
        containerClassName: "containerClassName",
        required: true
    }

    const counterProps2 = {
        label: "label",
        errorLabel: "errorLabel",
        containerClassName: "containerClassName",
        required: true
    }

    const counterProps3 = {
        label: "label",
        errorLabel: "errorLabel",
        onChange: (val: number) => {},
        onFocus: (val: number) => {},
        onBlur: (val: number) => {},
        min: 0,
        containerClassName: "containerClassName",
        required: true
    }

    const counterProps4 = {
        label: "label",
        errorLabel: "errorLabel",
        onChange: (val: number) => {},
        onFocus: (val: number) => {},
        onBlur: (val: number) => {},
        max: 100,
        containerClassName: "containerClassName",
        required: true
    }

    test('Counter render.inDocument with min/max', () => {
		render(<Counter {...counterProps}/>)
        const add = screen.getByText('+')
        const sub = screen.getByText('–')

        const input = screen.getByDisplayValue('5')
        
        fireEvent.change(input, { target: { value: 10 } })
        fireEvent.change(input, { target: { value: 'not a num' } })

        fireEvent.focus(input)
        fireEvent.blur(input)
        input.focus()
        input.blur()

        fireEvent.click(add)
        fireEvent.click(sub)

		expect(input).toBeInTheDocument()
    })
    
    test('Counter render.inDocument with nothing', () => {
		render(<Counter {...counterProps2}/>)

        const input = screen.getByDisplayValue('0')
        
        fireEvent.change(input, { target: { value: 10 } })
        fireEvent.change(input, { target: { value: 'not a num' } })

        fireEvent.focus(input)
        fireEvent.blur(input)
        input.focus()
        input.blur()
    
		expect(input).toBeInTheDocument()
    })
    
    test('Counter render.inDocument only min', () => {
		render(<Counter {...counterProps3}/>)

        const input = screen.getByDisplayValue('0')
        
        fireEvent.change(input, { target: { value: 10 } })
        fireEvent.change(input, { target: { value: 'not a num' } })
    
		expect(input).toBeInTheDocument()
    })
    
    test('Counter render.inDocument only max', () => {
		render(<Counter {...counterProps4}/>)

        const input = screen.getByDisplayValue('100')
        
        fireEvent.change(input, { target: { value: 10 } })
        fireEvent.change(input, { target: { value: 'not a num' } })
    
		expect(input).toBeInTheDocument()
	})



})
