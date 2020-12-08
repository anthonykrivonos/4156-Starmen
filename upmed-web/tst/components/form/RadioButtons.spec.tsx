import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { RadioButtons } from '../../../src/components/form/RadioButtons'

describe('RadioButtons', () => {

    const radioButtonsProps = {
        label: "radioButtons label",
        required: true,
        onChange: (option: any, index: number) => {},
        options: ["a", "b"],
        displayOptions: ["c", "d"],
        selectedIdx: 0,
        className: "radioButtons class name",
    }

    const radioButtonsProps2 = {
        required: true,
        onChange: (option: any, index: number) => {},
        options: ["1", "2"],
        displayOptions: ["1", "2", "3", "4"],
        selectedIdx: 1,
        className: "radioButtons class name",
    }

    const radioButtonsProps3 = {
        label: "radioButtons label",
        required: true,
        onChange: (option: any, index: number) => {},
        options: ["1", "2", "3"],
        displayOptions: [],
        selectedIdx: 0,
        className: "radioButtons class name",
    }

    test('render.inDocument', () => {
		render(<RadioButtons {...radioButtonsProps}/>)
        const linkElement = screen.getByText(/radioButtons label/i)
        
        const input = screen.getAllByDisplayValue(/radio.*/i)[0]

        fireEvent.change(input, { target: { value: 10 } })
        fireEvent.click(input)

		expect(linkElement).toBeInTheDocument()
    })
    
    test('render.inDocument diff options', () => {
		render(<RadioButtons {...radioButtonsProps3}/>)
        const linkElement = screen.getByText(1)
		expect(linkElement).toBeInTheDocument()
    })
    
    test('render.inDocument no label', () => {
		render(<RadioButtons {...radioButtonsProps2}/>)
        const linkElement = screen.getByText(1)
		expect(linkElement).toBeInTheDocument()
	})

})
