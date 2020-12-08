import React from 'react'
import { render, screen } from '@testing-library/react'
import { Profile } from '../../../src/pages/profile'
import { Appointment, HCP, Patient } from '../../../src/models'
import { Client, Users } from '../../../src/utils'

const appointment = {
	id: "AppointmentId",
	date: 2020,
	duration: 1000,
	doctor: "DoctorId",
	patient: "PatientId",
	subject: "appointment subject",
	notes: "appointment notes",
	videoUrl: "appointment url",
} as Appointment

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
	doctors: []
} as Patient

// const ProfileSubpagePropsPatient = {
// 	user: patient,
// 	patients: [],
// 	doctors: [doctor],
// 	appointments: [appointment],
// 	healthEvents: [],
// 	isPatient: true
// } as ProfileSubpageProps

// const ProfileSubpagePropsDoctor = {
// 	user: doctor,
// 	patients: [patient],
// 	doctors: [],
// 	appointments: [appointment],
// 	healthEvents: [],
// 	isPatient: false
// } as ProfileSubpageProps

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/profile/edit',
	}),
	useHistory: () => ({
		push: jest.fn()
	}),
}));

jest.mock('../../../src/utils/Client')
jest.mock('../../../src/utils/Users')

Users.getUserToken = jest.fn().mockReturnValue("token")
Client.Patient.getHCPs = jest.fn().mockResolvedValue([doctor])
Client.HCP.getPatients = jest.fn().mockResolvedValue([patient])
Client.Appointment.getCalendar = jest.fn().mockResolvedValue([appointment])
  
describe('Profile', () => {

    test('Profile render.inDocument Patient', () => {
		Users.getIsPatient = jest.fn().mockReturnValueOnce(true)
		Users.getCurrentUser = jest.fn().mockResolvedValueOnce(patient)

		render(<Profile />)
		const linkElement = screen.getByText('Loading...')
		expect(linkElement).toBeInTheDocument()
	})

	test('Profile render.inDocument Doctor', () => {
		Users.getIsPatient = jest.fn().mockReturnValueOnce(false)
		Users.getCurrentUser = jest.fn().mockResolvedValueOnce(doctor)

		render(<Profile />)
		const linkElement = screen.getByText('Loading...')

		screen.debug()

		expect(linkElement).toBeInTheDocument()
	})
})
