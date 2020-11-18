import React, { useState, useEffect } from 'react'

import { ProfileSubpageProps } from '../Profile'

import FullCalendar, { EventInput } from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'

import { Button, Popup, TextInput, DateInput, RadioButtons, Dropdown, Loading } from '../../../components'
import { Appointment, HCP, Patient } from '../../../models'
import { Client, DateTime, Objects, Users, Validator } from '../../../utils'

import styles from './Calendar.module.sass'
import { useLocation } from 'react-router-dom'
import { AppointmentPopup } from './components'

const appointmentToFullCalendarEvent = (appointment: Appointment): EventInput => {
	return {
		id: appointment.id,
		start: appointment.date,
		end: appointment.date + appointment.duration * 60 * 1000,
		title: appointment.subject,
		editable: false,
	}
}

export const Calendar = (props: ProfileSubpageProps) => {
	const location = useLocation()

	let togglePopup = null as any

	const [subject, setSubject] = useState('')
	const [duration, setDuration] = useState(30)
	const [date, setDate] = useState(new Date())
	const [isValid, setIsValid] = useState(false)
	const [patient, setPatient] = useState(
		props.patients.length > 0 ? props.patients[0] : (undefined as Patient | undefined),
	)
	const [doctor, setDoctor] = useState(props.doctors.length > 0 ? props.doctors[0] : (undefined as HCP | undefined))
	const [scheduleError, setScheduleError] = useState('')
	const [scheduleLoading, setScheduleLoading] = useState(false)

	const [currentAppointment, setCurrentAppointment] = useState(null as Appointment | null)
	const [currentDoctor, setCurrentDoctor] = useState(null as HCP | null)
	const [currentPatient, setCurrentPatient] = useState(null as Patient | null)

	// Search for new doctors or patients
	const [newDoctors, setNewDoctors] = useState([] as HCP[])
	const [newPatients, setNewPatients] = useState([] as Patient[])
	const [newLoaded, setNewLoaded] = useState(false)

	useEffect(() => {
		if (!newLoaded) {
			setNewLoaded(true)
			const token = Users.getUserToken()
			if (props.isPatient) {
				Client.HCP.getAll(token)
					.then((doctors) => {
						setNewDoctors(doctors.sort((a, b) => Number(a.lastName < b.lastName)))
						if (newDoctors.length > 0) {
							setDoctor(newDoctors[0])
						}
					})
					.catch(() => {
						setScheduleError('Could not load doctors.')
					})
			} else {
				Client.Patient.getAll(token)
					.then((patients) => {
						setNewPatients(patients.sort((a, b) => Number(a.lastName < b.lastName)))
						if (newPatients.length > 0) {
							setPatient(newPatients[0])
						}
					})
					.catch(() => {
						setScheduleError('Could not load patients.')
					})
			}
		}
	}, [location.pathname, newDoctors, newLoaded, newPatients, props.isPatient])

	useEffect(() => {
		// Perform one-line validation on all the inputs
		setScheduleError('')
		setIsValid(
			subject.length > 0 &&
				Validator.text(subject) &&
				date.getTime() > Date.now() &&
				duration >= 30 &&
				// Patient validation
				(props.isPatient ? !Objects.isNullish(doctor) : true) &&
				// Doctor validation
				(!props.isPatient ? patient !== null : true),
		)
		console.log(subject, date, duration, doctor, patient, isValid)
	}, [duration, date, patient, doctor, subject, props.isPatient, isValid])

	const scheduleAppointment = async () => {
		setScheduleLoading(true)
		try {
			await Client.Appointment.createAppointment(
				Users.getUserToken(),
				date.getTime(),
				duration,
				subject,
				props.isPatient ? props.user.id : patient!.id,
				!props.isPatient ? props.user.id : doctor!.id,
				'',
				'',
			)
			if (!props.isPatient && patient && currentAppointment) {
				// Feature: notification
				try {
					const test = await Client.HCP.testNumber(Users.getUserToken(), currentAppointment.id)
					if (test.success) {
						Client.HCP.notify(Users.getUserToken(), patient.id)
					}
				} catch {}
			}
			window.location.reload()
		} catch {
			setScheduleError(
				`Looks like ${props.isPatient ? doctor!.firstName : patient!.firstName} is busy during this time.`,
			)
		}
		setScheduleLoading(false)
	}

	let toggleAppointmentPopup = null as any
	const openAppointment = (appointment: Appointment | null) => {
		if (appointment && toggleAppointmentPopup) {
			let doc
			let pat
			if (props.isPatient) {
				for (const d of props.doctors) {
					if (d.id === appointment.doctor) {
						doc = d
						break
					}
				}
				pat = props.user as Patient
			} else {
				for (const p of props.patients) {
					if (p.id === appointment.patient) {
						pat = p
						break
					}
				}
				doc = props.user as HCP
			}

			if (doc && pat) {
				setCurrentDoctor(doc)
				setCurrentPatient(pat)
				setCurrentAppointment(appointment)
				toggleAppointmentPopup(true)
			}
		}
	}

	const appointmentAtId = (id: string): Appointment | null => {
		for (const appointment of props.appointments) {
			if (appointment.id === id) {
				return appointment
			}
		}
		return null
	}

	const clearAppointment = () => {
		setSubject('')
		setDate(new Date())
		setIsValid(false)
		setDuration(30)
		setScheduleError('')
		props.isPatient && setDoctor(undefined)
		!props.isPatient && setPatient(undefined)
	}

	return (
		<div className={styles.calendar_outter}>
			<div className={styles.calendar_top}>
				<div className={styles.calendar_bar}>
					<div>
						<b>Today: </b>
						{DateTime.prettyDate(new Date())}
					</div>
					<Button
						text={'Schedule Appointment'}
						className={styles.appointment_btn}
						onClick={() => togglePopup(true)}
						disabled={scheduleError !== ''}
					/>
				</div>
			</div>
			<div className={styles.calendar_inner}>
				<div className={styles.calendar}>
					<FullCalendar
						plugins={[dayGridPlugin]}
						initialView="dayGridMonth"
						height={'70vh'}
						selectable={true}
						initialEvents={props.appointments.map((apt) => appointmentToFullCalendarEvent(apt))}
						eventClick={(arg) => {
							openAppointment(appointmentAtId(arg.event.id))
						}}
					/>
				</div>
			</div>
			<Popup open={false} toggleRef={(t) => (togglePopup = t)} onClose={clearAppointment}>
				<div className={styles.popup_container}>
					<h2 className={`font-title mb-4`}>Schedule an Appointment</h2>
					<TextInput
						value={subject}
						label={'Appointment Subject'}
						errorLabel={'Invalid subject.'}
						validator={Validator.text}
						onChange={(t) => setSubject(t)}
						required
					/>
					<div className={`${styles.popup_mid_inputs} d-flex flex-direction-row mt-3 mb-4`}>
						<div className={styles.input_short}>
							<DateInput
								label={'Appointment Time'}
								containerClassName={styles.input_short}
								onDateChange={(d) => setDate(d)}
								minDate={DateTime.getModifiedDate(new Date(), undefined, undefined, 1)}
								timeSelect
								required
							/>
							{props.isPatient && newDoctors.length > 0 && (
								<Dropdown
									displayOptions={newDoctors.map((d) => `${d.lastName}, ${d.firstName} <${d.email}>`)}
									onChange={(d) => setDoctor(d)}
									options={newDoctors}
									label={'Doctor/Provider'}
									containerClassName={'mt-3 w-75'}
									required
								/>
							)}
							{!props.isPatient && newPatients.length > 0 && (
								<Dropdown
									displayOptions={newPatients.map(
										(p) => `${p.lastName}, ${p.firstName} <${p.email}>`,
									)}
									onChange={(p) => setPatient(p)}
									options={newPatients}
									label={'Patient'}
									containerClassName={'mt-3 w-75'}
									required
								/>
							)}
							{scheduleError && <div className={'mt-4 h6 color-quaternary'}>{scheduleError}</div>}
						</div>
						<RadioButtons
							options={[30, 45, 60]}
							displayOptions={['30min', '45min', '1hr']}
							label={'Duration'}
							className={styles.duration}
							onChange={(millis) => setDuration(millis)}
							required
						/>
					</div>
					<div className={'d-flex flex-row-reverse align-items-center'}>
						<Button
							text={'Create Appointment'}
							className={`${styles.schedule_btn} ml-4`}
							onClick={scheduleAppointment}
							disabled={!isValid || scheduleError !== '' || scheduleLoading}
						/>
						{scheduleLoading && <Loading size={'40px'} />}
					</div>
				</div>
			</Popup>
			<AppointmentPopup
				open={false}
				toggleRef={(t) => (toggleAppointmentPopup = t)}
				patient={currentPatient || undefined}
				doctor={currentDoctor || undefined}
				appointment={currentAppointment || undefined}
			/>
		</div>
	)
}
