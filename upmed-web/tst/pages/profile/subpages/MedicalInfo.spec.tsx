import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { MedicalInfo } from '../../../../src/pages/profile/subpages/MedicalInfo'
import { Appointment, HCP, Patient, HealthEvent, Status } from '../../../../src/models'

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/profile/medical',
    }),
	useHistory: () => ({
		push: jest.fn()
    })
}));

jest.mock('../../../../src/utils/Client')

describe('MedicalInfo', () => {

    const appointment = {
        id: "AppointmentId",
        date: 2020,
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
        health: [{
            date: 23,
            event: "He got cancer",
            remarks: "its sad",
            status: Status.ACTIVE,
        } as HealthEvent, {
            date: 24,
            event: "He got shot in the left ear",
            remarks: "bro how'd that happen",
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

    test('Patient', () => {
        render(<MedicalInfo {...ProfileSubpagePropsPatient}/>)

        const doctorElement = screen.getByTitle("jacky chuen")
        const record = screen.getByText("He got cancer")
        const appointmentElement = screen.getByText("appointment subject")

        fireEvent.click(doctorElement)
        fireEvent.click(record)
        fireEvent.click(appointmentElement)

		const linkElement1 = screen.getByText('My Doctors')
		expect(linkElement1).toBeInTheDocument()
    })
    
    const ProfileSubpagePropsDoctor = {
        user: doctor,
        patients: [patient],
        doctors: [],
        appointments: [appointment],
        healthEvents: [],
        isPatient: false
    }

    test('Doctor Add Record to Patient', () => {
        render(<MedicalInfo {...ProfileSubpagePropsDoctor}/>)
        
        const patientElement = screen.getByTitle("kenneth chuen")

        // Add record to patient
        fireEvent.click(patientElement)

        fireEvent.click(screen.getByText("Close"))


        fireEvent.click(screen.getAllByRole("button", { name: "Delete" })[0])

        fireEvent.click(screen.getByRole("button", { name: "Add Health Record" }))
        fireEvent.click(screen.getByText("Add Health Record"))
        fireEvent.click(screen.getAllByRole("button")[1])


        const subject = screen.getByDisplayValue("He got cancer")
        fireEvent.click(subject)
        fireEvent.change(subject, { target: { value: "He got leg pain" } } )
        let status = screen.getAllByText("ACTIVE")[0]
        fireEvent.click(status)
        status = screen.getAllByText("NEVER")[0]
        fireEvent.click(status)
        const remarks = screen.getByDisplayValue("its sad")
        fireEvent.click(remarks)
        fireEvent.change(remarks, { target: { value: "it'll be ok" } } )

        fireEvent.click(screen.getAllByText("Delete")[0])
        fireEvent.click(screen.getByText("Close"))

        const buttons = screen.getAllByRole("button")
        for (const button of buttons) {
            fireEvent.click(button)
        }

        const linkElement2 = screen.getByText('Editing Health Records')
		expect(linkElement2).toBeInTheDocument()
    })

    test('Doctor Click Appointment', () => {
        render(<MedicalInfo {...ProfileSubpagePropsDoctor}/>)
        
        const appointmentElement = screen.getByText("appointment subject")

        // Click appointment
        fireEvent.click(appointmentElement)

        const linkElement2 = screen.getByText('Appointment Details')
		expect(linkElement2).toBeInTheDocument()
    })

})
