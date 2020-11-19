// import React from 'react'
// import { render, screen } from '@testing-library/react'
import { AppointmentPopup } from '../../../../../src/pages/profile/subpages/components/AppointmentPopup'

import { Appointment, HCP, Patient } from '../../../../../src/models'


describe('AppointmentPopup', () => {

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

    const AppointmentPopupProps = {
        appointment,
        doctor,
        patient,
        isPatient: true
    }

    test('AppointmentPopup', () => {
        const result = AppointmentPopup(AppointmentPopupProps)

		expect(result).toBeInTheDocument()
	})

})
