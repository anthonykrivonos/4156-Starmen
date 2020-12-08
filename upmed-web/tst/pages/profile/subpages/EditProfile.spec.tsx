import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { EditProfile } from '../../../../src/pages/profile/subpages/EditProfile'
import { Appointment, HCP, Patient, HealthEvent, Status } from '../../../../src/models'

const appointment = {
    id: "AppointmentId",
    date: 2020,
    duration: 30,
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
    email: "jchuen@nyu.edu",
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
    email: "kc3334@columbia.edu",
    dateOfBirth: "1998-02-05",
    sex: "M",
    height: 179,
    weight: 154,
    drinker: 0,
    smoker: 0,
    health: [{
        date: 23,
        event: "He got cancer",
        remarks: "its sad",
        status: Status.ACTIVE,
    } as HealthEvent],
    doctors: ["DoctorId fake"]
} as Patient

const ProfileSubpagePropsPatient = {
    user: patient,
    patients: [],
    doctors: [doctor],
    appointments: [appointment],
    healthEvents: [{
        date: 23,
        event: "He got cancer",
        remarks: "its sad",
        status: Status.ACTIVE,
    } as HealthEvent],
    isPatient: true
}
const ProfileSubpagePropsDoctor = {
    user: doctor,
    patients: [patient],
    doctors: [doctor],
    appointments: [appointment],
    healthEvents: [{
        date: 23,
        event: "He got cancer",
        remarks: "its sad",
        status: Status.ACTIVE,
    } as HealthEvent],
    isPatient: false
}

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/profile/edit',
    }),
}));

jest.mock('../../../../src/utils/Client')

describe('EditProfile', () => {

    test('EditProfile Patient', () => {
        render(<EditProfile {...ProfileSubpagePropsPatient}/>)

        const firstName = screen.getByDisplayValue('kenneth')
        const lastName = screen.getByDisplayValue('chuen')
        const email = screen.getByDisplayValue('kc3334@columbia.edu')
        const phone = screen.getByDisplayValue('347-681-6990')
        const dob = screen.getByDisplayValue('1998/02/05')
        const height = screen.getByDisplayValue('179')
        const weight = screen.getByDisplayValue('154')
        const drinkerYes = screen.getAllByDisplayValue(/radio.*/i)[0]
        const drinkerPast = screen.getAllByDisplayValue(/radio.*/i)[1]
        const drinkerNever = screen.getAllByDisplayValue(/radio.*/i)[2]
        const smokerYes = screen.getAllByDisplayValue(/radio.*/i)[3]
        const smokerPast = screen.getAllByDisplayValue(/radio.*/i)[4]
        const smokerNever = screen.getAllByDisplayValue(/radio.*/i)[5]

        fireEvent.change(firstName, { target: { value: 'Kenneth' } })
        fireEvent.change(lastName, { target: { value: 'Chuen' } })
        fireEvent.change(email, { target: { value: 'kc@gmail.com' } })
        fireEvent.change(phone, { target: { value: '347-619-4852' } })
        fireEvent.change(dob, { target: { value: '1995/02/05' } })
        fireEvent.change(height, { target: { value: 165 } })
        fireEvent.change(weight, { target: { value: 60 } })
        fireEvent.click(drinkerYes)
        fireEvent.click(drinkerPast)
        fireEvent.click(drinkerNever)
        fireEvent.click(smokerYes)
        fireEvent.click(smokerPast)
        fireEvent.click(smokerNever)

        const linkElement = screen.getByText('Update Account')
        fireEvent.click(linkElement)

		expect(linkElement).toBeInTheDocument()
    })
    
    test('EditProfile Doctor', () => {
        render(<EditProfile {...ProfileSubpagePropsDoctor}/>)

        const business = screen.getByDisplayValue('MD')
        const specialty = screen.getByDisplayValue('cancer')
        
        fireEvent.change(business, { target: { value: "NYU presby" } })
        fireEvent.change(specialty, { target: { value: "dentist" } })

        const day = screen.getByDisplayValue('Sunday')
        const day2 = screen.getByDisplayValue('Saturday')
        const hour = screen.getAllByDisplayValue('12:00 AM')[0]
        const hour2 = screen.getAllByDisplayValue('12:00 AM')[1]
        fireEvent.click(day)
        fireEvent.click(day2)
        fireEvent.change(hour, { target: { value: '12:30 AM' } })
        fireEvent.click(hour)
        fireEvent.change(hour2, { target: { value: '12:00 PM' } })
        fireEvent.click(hour2)
        
        const linkElement = screen.getByText('Update Account')
        fireEvent.click(linkElement)
		expect(linkElement).toBeInTheDocument()
    })

    test('EditProfile debug', () => {
        render(<EditProfile {...ProfileSubpagePropsPatient}/>)

        const update = screen.getByRole('button', { name: 'Update Account' } )
        fireEvent.click(update)

        screen.debug()

        const firstName = screen.getByDisplayValue('kenneth')
        fireEvent.change(firstName, { target: { value: 'mike' } })

        screen.debug()

        const linkElement = screen.getByRole('button', { name: 'Update Account' } )
        fireEvent.click(linkElement)

        screen.debug()

		expect(update).toBeInTheDocument()
    })
    
})
