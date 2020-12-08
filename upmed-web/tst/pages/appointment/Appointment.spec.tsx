import React from 'react'
import { render, screen } from '@testing-library/react'
import { Appointment } from '../../../src/pages/appointment'
import { Appointment as AppointmentClass, HCP, Patient,  } from '../../../src/models'
import { Hasher, Client, Users } from '../../../src/utils'

const appointmentWithAccessToken = {
    id: "AppointmentId",
    date: 1605970800000,
    duration: 45,
    doctor: "DoctorId",
    patient: "PatientId",
    subject: "appointment subject",
    notes: "appointment notes",
    videoUrl: "appointment url",
    accessToken: 'asdfasdf',
} as AppointmentClass & { accessToken: string }

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
    calendar: ["AppointmentId"],
    profilePicture: "profile Pic link",
    patients: ["100"],
    hours: HOURS_GOOD,
} as HCP

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
    doctors: ["DoctorId fake"]
} as Patient

jest.mock('../../../src/utils/Client')

Client.Appointment.video = jest.fn().mockResolvedValue(appointmentWithAccessToken)

Users.getUserToken = jest.fn().mockResolvedValue('token')

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/appointments/hash',
    }),
	useHistory: () => ({
		push: jest.fn()
    })
}));

Hasher.decode = jest.fn().mockReturnValue({
    appointmentId: "AppointmentId",
    patient,
    doctor,
})

describe('Appointment', () => {
      
    test('Appointment render.inDocument loading', () => {
		render(<Appointment />)
        const linkElement = screen.getByText(/Loading.../i)
		expect(linkElement).toBeInTheDocument()
    })

    test('Appointment fail promise', () => {
        Client.Appointment.video = jest.fn().mockRejectedValueOnce('reject')

		render(<Appointment />)
        const linkElement = screen.getByText(/Loading.../i) // Failed to enter room
		expect(linkElement).toBeInTheDocument()
    })

    test('Appointment no hash', () => {
        jest.mock('react-router-dom', () => ({
            useLocation: jest.fn().mockReturnValueOnce({
              pathname: '/sdasdjkasdjlkasdj',
            })
        }))
        Hasher.decode = jest.fn().mockReturnValueOnce({})
        
		render(<Appointment />)
        const linkElement = screen.getByRole('button', { name: 'Try Again' } ) 
		expect(linkElement).toBeInTheDocument()
    })

    test('Appointment no id decoded', () => {
        jest.mock('react-router-dom', () => ({
            useLocation: jest.fn().mockReturnValueOnce({
              pathname: '/asdasdjkasdjlkasdj',
            })
        }))
		render(<Appointment />)
        const linkElement = screen.getByRole('button', { name: 'Try Again' } ) // No id decoded
		expect(linkElement).toBeInTheDocument()
    })
    
})
