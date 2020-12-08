import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { DateInput } from '../../../src/components/form/DateInput'

describe('DateInput', () => {

    const dateInputProps = {
        label: "date label",
        value: new Date(500),
        required: true,
        className: "date class label",
        containerClassName: "container name",
        onDateChange: (date: Date) => {},
        timeSelect: true,
        maxDate: new Date(0),
        minDate: new Date(2000000),
    }

    test('render.inDocument', () => {

		render(<DateInput {...dateInputProps}/>)
        const linkElement = screen.getByText(/date label/i)
        
        const datepicker = screen.getByDisplayValue('1969/12/31 07:00 PM')

        fireEvent.change(datepicker, { target: { value: '1969/12/31 08:00 PM' } })

		expect(linkElement).toBeInTheDocument()
	})

})
