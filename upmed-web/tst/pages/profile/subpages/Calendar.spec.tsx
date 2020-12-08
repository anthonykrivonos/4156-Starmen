/* istanbul ignore file */
import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { Calendar } from '../../../../src/pages/profile/subpages/Calendar'
import { Appointment, HCP, Patient, HealthEvent, Status } from '../../../../src/models'
import { Client, } from '../../../../src/utils'

const appointment = {
    id: "AppointmentId",
    date: 1607304649950,
    duration: 45,
    doctor: "DoctorId fake",
    patient: "100",
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
    phone: "293-829-3824",
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
    email: "kc3334@columbia",
    dateOfBirth: "1998/02/05",
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
    doctors: [],
    appointments: [appointment],
    healthEvents: [],
    isPatient: false
}

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/profile/appointments',
    }),
	useHistory: () => ({
		push: jest.fn()
    })
    // useState: jest.fn()
    //     .mockReturnValueOnce("subject")
    //     .mockReturnValueOnce("subject")
    //     .mockReturnValueOnce(30)
    //     .mockReturnValueOnce(new Date())
    //     .mockReturnValueOnce(false)
    //     .mockReturnValueOnce(patient)
    //     .mockReturnValueOnce(doctor)
    //     .mockReturnValueOnce('')
    //     .mockReturnValueOnce(false),

}));

jest.mock('../../../../src/utils/Client')

Client.Patient.getAll = jest.fn().mockResolvedValue([patient])
Client.HCP.getAll = jest.fn().mockResolvedValue([doctor])

describe('Calendar', () => {
    
    test('Calendar Patient', () => {

        render(<Calendar {...ProfileSubpagePropsPatient}/>)
        
        const buttons = screen.getAllByRole("button")
        for (const button of buttons) {
            fireEvent.click(button)
        }
        for (const button of buttons) {
            fireEvent.click(button)
        }
        

        // const headings = screen.getAllByRole("heading")
        // for (const heading of headings) {
        //     fireEvent.click(heading)
        // }

        // const tables = screen.getAllByRole("table")
        // for (const table of tables) {
        //     fireEvent.click(table)
        // }

        // const rowgroups = screen.getAllByRole("rowgroup")
        // for (const rowgroup of rowgroups) {
        //     fireEvent.click(rowgroup)
        // }

        // const rows = screen.getAllByRole("row")
        // for (const row of rows) {
        //     fireEvent.click(row)
        // }

        // const cells = screen.getAllByRole("cell")
        // for (const cell of cells) {
        //     fireEvent.click(cell)
        // }

        // const columnheaders = screen.getAllByRole("columnheader")
        // for (const columnheader of columnheaders) {
        //     fireEvent.click(columnheader)
        // }

        const schedule = screen.getByText("Schedule Appointment")
        fireEvent.click(schedule)

        expect(schedule).toBeInTheDocument()
    })
    
    test('Calendar Doctor', () => {
        render(<Calendar {...ProfileSubpagePropsDoctor}/>)

        const buttons = screen.getAllByRole("button")
        for (const button of buttons) {
            fireEvent.click(button)
        }
        for (const button of buttons) {
            fireEvent.click(button)
        }

        const schedule = screen.getByText("Schedule Appointment")
        fireEvent.click(schedule)

        expect(schedule).toBeInTheDocument()
	})

})
