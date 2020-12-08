// import React from 'react'
// import { fireEvent, render, screen } from '@testing-library/react'

// import { Track, Participant as ParticipantClass } from 'twilio-video'
// import { MUTE, UNMUTE } from '../../../src/assets'
import { HCP, Patient,  } from '../../../src/models'
// import { Users, DateTime } from '../../../src/utils'
// import { Button } from '../../../src/components/button'

// import { Participant } from '../../../src/components/video'

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

// cannot mock participant
// const ParticipantPropsPatient = {
// 	participant: new ParticipantClass(),
// 	user: patient,
// 	isMe: true,
// }

// const ParticipantPropsDoctor = {
// 	participant: new ParticipantClass(),
// 	user: doctor,
// 	isMe: false,
// }

describe('Participant', () => {

    test('stop jest from being mad', () => {
        console.log(patient)
        console.log(doctor)
    })

    // test.skip('Participant render.inDocument patient', () => {
	// 	render(<Participant {...ParticipantPropsPatient}/>)
    //     const linkElement = screen.getByRole('button')
	// 	expect(linkElement).toBeInTheDocument()
    // })

})
