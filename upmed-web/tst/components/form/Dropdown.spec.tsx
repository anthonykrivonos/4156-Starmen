import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Dropdown } from '../../../src/components/form/Dropdown'

describe('Dropdown', () => {

    const dropdownProps = {
        label: "dropdown label",
        required: true,
        onChange: jest.fn(),
        options: [],
        displayOptions: [],
        selectedIdx: 1,
        className: "dropdown class name",
        containerClassName: "dropdown container name"
    }

    const dropdownPropsOptions = {
        label: "dropdown label",
        required: true,
        onChange: jest.fn(),
        options: ["1", "2", "3"],
        displayOptions: [],
        selectedIdx: 1,
        className: "dropdown class name",
        containerClassName: "dropdown container name"
    }

    const dropdownPropsOptions2 = {
        label: "dropdown label",
        required: true,
        onChange: jest.fn(),
        options: ["1", "2"],
        displayOptions: ["1", "2", "3", "4"],
        selectedIdx: 1,
        className: "dropdown class name",
        containerClassName: "dropdown container name"
    }

    test('Dropdown render.inDocument no options', () => {
		render(<Dropdown {...dropdownProps}/>)
        const linkElement = screen.getByText(/dropdown label/i)

        const dropdownList = screen.getByRole('combobox')
        
        fireEvent.change(dropdownList, { target: { value: '23' } })

		expect(linkElement).toBeInTheDocument()
    })
    
    test('Dropdown render.inDocument with options', () => {
		render(<Dropdown {...dropdownPropsOptions}/>)
        const linkElement = screen.getByText(/dropdown label/i)

        const dropdownList = screen.getByRole('combobox')
        
        fireEvent.change(dropdownList, { target: { value: '23' } })

		expect(linkElement).toBeInTheDocument()
    })
    
    test('Dropdown render.inDocument with options2', () => {
		render(<Dropdown {...dropdownPropsOptions2}/>)
        const linkElement = screen.getByText(/dropdown label/i)

        const dropdownList = screen.getByRole('combobox')
        
        fireEvent.change(dropdownList, { target: { value: '23' } })

		expect(linkElement).toBeInTheDocument()
	})


})
