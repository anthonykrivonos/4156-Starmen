import React from 'react'
import { render, screen } from '@testing-library/react'
import { HoursInputs } from '../../../src/components/form/HoursInputs'
import { Hours } from '../../../src/models'


describe('HoursInputs', () => {

    const HOURS_GOOD = {
        sunday: { startTime: 0, endTime: 1440 },
        monday: { startTime: 0, endTime: 1440 },
        tuesday: { startTime: 0, endTime: 1440 },
        wednesday: { startTime: 0, endTime: 1440 },
        thursday: { startTime: 0, endTime: 1440 },
        friday: { startTime: 0, endTime: 1440 },
        saturday: { startTime: -1, endTime: -1 },
    }

    const hoursInputsProps = {
        label: "hoursInputs label",
        required: true,
        initialHours: HOURS_GOOD,
        onChange: (hours: Hours, isValid: boolean) => {},
        className: "hoursInputs class name",
    }

    test('render.inDocument', () => {
		render(<HoursInputs {...hoursInputsProps}/>)
		const linkElement = screen.getByText(/hoursInputs label/i)
		expect(linkElement).toBeInTheDocument()
	})

})
