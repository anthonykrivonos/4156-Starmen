import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { HoursInputs } from '../../../src/components/form/HoursInputs'
import { Hours } from '../../../src/models'
import { Hasher } from '../../../src/utils'

describe('HoursInputs', () => {

    const HOURS_GOOD = {
        sunday: { startTime: 0, endTime: 1440 },
        monday: { startTime: 0, endTime: 1440 },
        tuesday: { startTime: 0, endTime: 1440 },
        wednesday: { startTime: 0, endTime: 1440 },
        thursday: { startTime: 0, endTime: 1440 },
        friday: { startTime: 0, endTime: 1440 },
        saturday: { startTime: -1, endTime: 1440 },
    }

    const HOURS_BAD = {
        sunday: { startTime: 1440, endTime: 0 },
        monday: { startTime: 0, endTime: 1440 },
        tuesday: { startTime: 0, endTime: 1440 },
        wednesday: { startTime: 0, endTime: 1440 },
        thursday: { startTime: 0, endTime: 1440 },
        friday: { startTime: 0, endTime: 1440 },
        saturday: { startTime: -1, endTime: 1440 },
    }

    const hoursInputsProps = {
        label: "hoursInputs label",
        required: true,
        initialHours: HOURS_GOOD,
        onChange: (hours: Hours, isValid: boolean) => {},
        className: "hoursInputs class name",
    }

    const hoursInputsPropsBad = {
        label: "hoursInputs label",
        required: true,
        initialHours: HOURS_BAD,
        onChange: (hours: Hours, isValid: boolean) => {},
        className: "hoursInputs class name",
    }

    const hoursInputsProps2 = {
        required: true,
        onChange: (hours: Hours, isValid: boolean) => {},
        className: "hoursInputs class name",
    }

    test('HoursInput render.inDocument good', () => {
		render(<HoursInputs {...hoursInputsProps}/>)
        const linkElement = screen.getByText(/hoursInputs label/i)
        
        const day = screen.getByDisplayValue('Sunday')
        const day2 = screen.getByDisplayValue('Saturday')

        const hour = screen.getAllByDisplayValue('12:00 AM')[0]
        const hour2 = screen.getAllByDisplayValue('12:00 AM')[1]

        fireEvent.change(hour, { target: { value: '12:30 PM' } })
        fireEvent.click(hour)
        fireEvent.change(hour2, { target: { value: '12:00 AM' } })
        fireEvent.click(hour2)
        fireEvent.click(day)
        fireEvent.click(day2)
        fireEvent.click(day)
        fireEvent.click(day2)

		expect(linkElement).toBeInTheDocument()
    })

    test('HoursInput render.inDocument bad', () => {
		render(<HoursInputs {...hoursInputsPropsBad}/>)
        const linkElement = screen.getByText(/hoursInputs label/i)
        
        const day = screen.getByDisplayValue('Sunday')
        const day2 = screen.getByDisplayValue('Saturday')

        const hour = screen.getAllByDisplayValue('12:00 AM')[0]
        const hour2 = screen.getAllByDisplayValue('12:00 AM')[1]

        fireEvent.change(hour, { target: { value: '12:30 AM' } })
        fireEvent.click(hour)
        fireEvent.change(hour2, { target: { value: '12:30 AM' } })
        fireEvent.click(hour2)
        fireEvent.click(day)
        fireEvent.click(day2)
        fireEvent.click(day)
        fireEvent.click(day2)

		expect(linkElement).toBeInTheDocument()
    })

    
    test('HoursInput render.inDocument no label/hours', () => {
        Hasher.encode = jest.fn().mockResolvedValue('encoded')

		render(<HoursInputs {...hoursInputsProps2}/>)
        const linkElement = screen.getByText("Sunday")
		expect(linkElement).toBeInTheDocument()
	})


})
