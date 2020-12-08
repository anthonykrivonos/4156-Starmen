import React from 'react'
import { render, screen } from '@testing-library/react'
import { Sidebar } from '../../../src/components/bars/Sidebar'

describe('Sidebar', () => {

    const buttonA = {
        text: "string",
        icon: <span>Element</span>,
        isBottom: false,
        centered: false,
        active: false,
	    onClick: () => {},
    }

    const buttonB = {
        text: "butt",
        icon: <span>Element</span>,
        isBottom: true,
        centered: true,
        active: true,
	    onClick: () => {},
    }

    const buttonC = {
        text: "butt",
        // icon: <span>Element</span>,
        isBottom: true,
        centered: false,
        active: true,
	    onClick: () => {},
    }

    const buttonD = {
        text: "string",
        // icon: <span>Element</span>,
        isBottom: false,
        centered: true,
        active: true,
	    onClick: () => {},
    }

    const patient = {
        id: "100",
        firstName: "kenneth",
        lastName: "chuen",
        calendar: [],
        phone: "347-681-6990",
        email: "kc3334@columbia",
        dateOfBirth: "02/05/1997",
        sex: "M",
        height: 179,
        weight: 154,
        drinker: 0,
        smoker: 0,
        health: [],
        doctors: []
    }

    const HOURS_GOOD = {
        sunday: { startTime: 0, endTime: 1440 },
        monday: { startTime: 0, endTime: 1440 },
        tuesday: { startTime: 0, endTime: 1440 },
        wednesday: { startTime: 0, endTime: 1440 },
        thursday: { startTime: 0, endTime: 1440 },
        friday: { startTime: 0, endTime: 1440 },
        saturday: { startTime: -1, endTime: -1 },
    }

    const doctor = {
        id: "DoctorId fake",
        firstName: "jacky",
        lastName: "chuen",
        title: "MD",
        specialty: "cancer",
        phone: "2938293824",
        email: "jchuen@nyu",
        calendar: [],
        profilePicture: "profile Pic link",
        patients: [],
        hours: HOURS_GOOD,
    }

    it('Sidebar render.inDocument Patient', () => {
		render(<Sidebar buttons={[buttonA, buttonB, buttonC, buttonD]} user={patient} isPatient={true}/>)
		const linkElement = screen.getByText(/upmed/i)
		expect(linkElement).toBeInTheDocument()
    })
    
    it('Sidebar render.inDocument Doctor', () => {
		render(<Sidebar buttons={[buttonA, buttonB, buttonC, buttonD]} user={doctor} isPatient={false}/>)
		const linkElement = screen.getByText(/upmed/i)
		expect(linkElement).toBeInTheDocument()
	})

})


