
import React from 'react'
import { render, screen } from '@testing-library/react'

// import Video, { Room as RoomClass, Participant as ParticipantClass } from 'twilio-video'
import { Appointment, HCP, Patient,  } from '../../../src/models'
import { Users, } from '../../../src/utils'
import { Room } from '../../../src/components/video'

const appointment = {
    id: "102635040599824430135,109828603357133107692,1607422607470",
    date: 1607422607470,
    duration: 45,
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
    id: "109828603357133107692",
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
    id: "102635040599824430135",
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

const RoomProps = {
	appointment,
	doctor,
	patient,
	accessToken: "accessToken"
}

describe('Room', () => {

    test('Room render.inDocument null user', () => {
        Users.getCurrentUser = jest.fn().mockResolvedValue(null)

		render(<Room {...RoomProps}/>)
        const linkElement = screen.getByText(/appointment subject/i)
		expect(linkElement).toBeInTheDocument()
    })

      
    test('Room render.inDocument patient', () => {
        Users.getCurrentUser = jest.fn().mockResolvedValue(patient)

		render(<Room {...RoomProps}/>)
        const linkElement = screen.getByText(/appointment subject/i)
		expect(linkElement).toBeInTheDocument()
    })

    test('Room render.inDocument doctor', () => {
        Users.getCurrentUser = jest.fn().mockResolvedValue(doctor)

		render(<Room {...RoomProps}/>)
        const linkElement = screen.getByText(/appointment subject/i)
		expect(linkElement).toBeInTheDocument()
    })
    
})
