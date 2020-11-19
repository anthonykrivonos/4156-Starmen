import React, { useState } from 'react'

import { ProfileSubpageProps } from '../Profile'

import { Avatar, Button, Dropdown, Popup, TextInput } from '../../../components'
import { STATUS, DAYS_LOWER, DAYS } from '../../../constants'
import { Formatter, DateTime, Validator, Objects, Client, Users } from '../../../utils'
import { HCP, DoctorId, Appointment, Day, PatientId, Patient, HealthEvent, Status } from '../../../models'

import styles from './MedicalInfo.module.sass'
import { AppointmentPopup } from './components'

export const MedicalInfo = (props: ProfileSubpageProps) => {
	const [currentAppointment, setCurrentAppointment] = useState(null as Appointment | null)
	const [currentDoctor, setCurrentDoctor] = useState(null as HCP | null)
	const [allPatients, setAllPatients] = useState(props.patients || ([] as Patient[]))
	const [currentPatient, setCurrentPatient] = useState(null as Patient | null)
	const [currentHealthEvent, setCurrentHealthEvent] = useState(null as HealthEvent | null)
	const [isCurrentlyEditingHealthEvents, setIsCurrentlyEditingHealthEvent] = useState(false)
	const [healthEvents, setHealthEvents] = useState(props.healthEvents.sort((a, b) => b.date - a.date))
	const [areHealthEventsValid, setAreHealthEventsValid] = useState(true)

	const getDoctorById = (id: DoctorId): HCP | null => {
		for (const d of props.doctors) {
			if (d.id === id) {
				return d
			}
		}
		return null
	}
	const getPatientById = (id: PatientId): Patient | null => {
		for (const p of props.patients) {
			if (p.id === id) {
				return p
			}
		}
		return null
	}

	let toggleAppointmentPopup = null as any
	const openAppointment = (apt: Appointment, patient: Patient | null, doctor: HCP | null = null) => {
		if (toggleAppointmentPopup) {
			setCurrentAppointment(apt)
			setCurrentPatient(patient)
			patient && setHealthEvents(patient.health)
			setCurrentDoctor(doctor)
			toggleAppointmentPopup(true)
		}
	}

	let toggleInfoPopup = null as any
	const openDoctor = (doctor: HCP | null) => {
		if (toggleInfoPopup) {
			setCurrentDoctor(doctor)
			toggleInfoPopup(true)
		}
	}

	let toggleHealthEventPopup = null as any
	const openHealthEvent = (healthEvent: HealthEvent | null) => {
		if (toggleHealthEventPopup) {
			setCurrentHealthEvent(healthEvent)
			toggleHealthEventPopup(true)
		}
	}

	const editPatientHealthEvents = (patient: Patient) => {
		setCurrentPatient(patient)
		patient && setHealthEvents(patient.health)
		setIsCurrentlyEditingHealthEvent(true)
	}

	const updateHealthEvents = (
		index: number,
		event: string | null = null,
		remarks: string | null = null,
		status: Status | null = null,
	) => {
		const newHealthEvents = Objects.copy(healthEvents) as HealthEvent[]
		if (event !== null) {
			newHealthEvents[index].event = event!
		}
		if (remarks !== null) {
			newHealthEvents[index].remarks = remarks!
		}
		if (status !== null) {
			newHealthEvents[index].status = status!
		}
		if (event !== null || remarks !== null || status !== null) {
			if (!newHealthEvents[index].remarks) {
				newHealthEvents[index].remarks = undefined
			}
			setHealthEvents(newHealthEvents)

			let areValid = true
			for (const healthEvent of newHealthEvents) {
				if (healthEvent.event === '') {
					areValid = false
					break
				}
			}
			setAreHealthEventsValid(areValid)

			if (areValid && currentPatient) {
				const newPatients = Objects.copy(allPatients)
				for (let i = 0; i < newPatients.length; i++) {
					if (currentPatient && newPatients[i].id === currentPatient.id) {
						newPatients[i].health = newHealthEvents
						break
					}
				}
				setAllPatients(newPatients)
				try {
					Client.HCP.setRecords(Users.getUserToken(), currentPatient.id, newHealthEvents)
				} catch (e) {
					console.error(e)
				}
			}
		}
	}

	const addHealthEvent = () => {
		const hE = {
			date: Date.now(),
			status: Status.ACTIVE,
			event: '',
		} as HealthEvent
		const newHealthEvents = Objects.copy(healthEvents) as HealthEvent[]
		newHealthEvents.unshift(hE)
		setHealthEvents(newHealthEvents)
		const newPatients = Objects.copy(allPatients)
		for (let i = 0; i < newPatients.length; i++) {
			if (currentPatient && newPatients[i].id === currentPatient.id) {
				newPatients[i].health = newHealthEvents
				break
			}
		}
		setAllPatients(newPatients)
		setAreHealthEventsValid(false)
	}

	const removeHealthEvent = (index: number) => {
		const newHealthEvents = Objects.copy(healthEvents) as HealthEvent[]
		newHealthEvents.splice(index, 1)
		setAreHealthEventsValid(true)

		for (let i = newHealthEvents.length - 1; i >= 0; i--) {
			if (newHealthEvents[i].event === '') {
				newHealthEvents.splice(i, 1)
			}
		}
		setHealthEvents(newHealthEvents)

		const newPatients = Objects.copy(allPatients)
		for (let i = 0; i < newPatients.length; i++) {
			if (currentPatient && newPatients[i].id === currentPatient.id) {
				newPatients[i].health = newHealthEvents
				break
			}
		}
		setAllPatients(newPatients)

		if (currentPatient) {
			try {
				Client.HCP.setRecords(Users.getUserToken(), currentPatient.id, newHealthEvents)
			} catch (e) {
				console.error(e)
			}
		}
	}

	return isCurrentlyEditingHealthEvents && currentPatient ? (
		<main id="editingHealthEvent">
			<div className={styles.editing_health_event}>
				<div className={styles.editing_health_event_inner}>
					<div className={'d-flex flex-row justify-content-between align-items-center'}>
						<div>
							<h2 className="font-title mb-1">Editing Health Records</h2>
							<div className="h5">
								{currentPatient.firstName} {currentPatient.lastName}
							</div>
						</div>
						<Button text={'Close'} onClick={() => setIsCurrentlyEditingHealthEvent(false)} />
					</div>
					<div className={'mt-3'}>
						<Avatar user={currentPatient} size={'6rem'} />
						<h4 className={`font-title mt-2 mb-3`}>Patient Details</h4>
						<div className={'row p-0 m-0'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>DOB</div>
							<div className={'col-9 m-0 p-0'}>{currentPatient.dateOfBirth}</div>
						</div>
						<div className={'row p-0 m-0'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>Sex</div>
							<div className={'col-9 m-0 p-0'}>{currentPatient.sex}</div>
						</div>
						<div className={'row p-0 m-0'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>Height</div>
							<div className={'col-9 m-0 p-0'}>{currentPatient.height} cm</div>
						</div>
						<div className={'row p-0 m-0'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>Weight</div>
							<div className={'col-9 m-0 p-0'}>{currentPatient.weight} kg</div>
						</div>
						<div className={'row p-0 m-0'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>Drinker</div>
							<div className={'col-9 m-0 p-0'}>{STATUS[currentPatient.drinker]}</div>
						</div>
						<div className={'row p-0 m-0'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>Smoker</div>
							<div className={'col-9 m-0 p-0'}>{STATUS[currentPatient.smoker]}</div>
						</div>
						<div className={'row p-0 m-0 mt-3'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>Email</div>
							<div className={'col-9 m-0 p-0'}>{currentPatient.email}</div>
						</div>
						<div className={'row p-0 m-0'}>
							<div className={'col-3 m-0 p-0 font-weight-bolder'}>Phone</div>
							<div className={'col-9 m-0 p-0'}>{currentPatient.phone}</div>
						</div>
						<h4 className={`font-title mt-4 mb-3`}>Health Records</h4>
						<div className={styles.edit_health_events}>
							<Button
								text={'Add Health Record'}
								onClick={addHealthEvent}
								disabled={!areHealthEventsValid}
								className={styles.add_health_event}
							/>
							{healthEvents.map((hE, idx) => (
								<div key={`edit-he-${hE.date}`} className={'row p-0 m-0 mb-2 pr-4 align-items-start'}>
									<div className={'col-3 m-0 p-0 pr-2 align-items-center'}>
										<TextInput
											value={hE.event}
											label={'Subject'}
											validator={Validator.text}
											onChange={(value) => updateHealthEvents(idx, value, null, null)}
										/>
									</div>
									<div className={'col-2 pr-2 align-items-center'}>
										<Dropdown
											options={[
												Status.ACTIVE,
												Status.NEVER,
												Status.PAST,
												Status.REMISSION,
												Status.CURED,
											]}
											displayOptions={['ACTIVE', 'NEVER', 'PAST', 'REMISSION', 'CURED']}
											label={'Status'}
											className={styles.input_short}
											selectedIdx={[
												Status.ACTIVE,
												Status.NEVER,
												Status.PAST,
												Status.REMISSION,
												Status.CURED,
											].indexOf(hE.status)}
											onChange={(option) => updateHealthEvents(idx, null, null, option)}
											required
										/>
									</div>
									<div className={'col-6 m-0 p-0 pr-2 align-items-center'}>
										<TextInput
											value={hE.remarks}
											label={'Remarks'}
											validator={Validator.text}
											onChange={(value) => updateHealthEvents(idx, null, value, null)}
										/>
									</div>
									<div className={'col-1 m-0 p-0 align-items-center'}>
										<Button
											text={'Delete'}
											onClick={() => removeHealthEvent(idx)}
											className={'mb-2 mt-4 color-quaternary p-2 pl-4 pr-4 align-self-end'}
										/>
									</div>
								</div>
							))}
						</div>
					</div>
				</div>
			</div>
		</main>
	) : (
		<main id="medicalInfo">
			<section className={styles.medical_info}>
				{!props.isPatient && (
					<div className={styles.my_container}>
						<h2 className="font-title mb-4">My Patients</h2>
						{allPatients.length === 0 ? (
							<div className={styles.empty}>You have no patients yet.</div>
						) : (
							<div className={`${styles.doctors} d-flex flex-direction-row justify-content-start`}>
								{allPatients.map((p, idx) => (
									<div
										key={`allPatients-${idx}`}
										className={styles.container}
										onClick={() => editPatientHealthEvents(p)}
									>
										<Avatar user={p} size={'80px'} />
										<div className={'h5 mt-3 font-weight-bolder'}>
											{p.firstName} {p.lastName}
										</div>
										<div className={'h7'}>{p.phone}</div>
										<a className={'h7 word-wrap'} href={`mailto:${p.email}`}>
											{p.email}
										</a>
									</div>
								))}
							</div>
						)}
					</div>
				)}
				{props.isPatient && (
					<>
						<div className={styles.my_container}>
							<h2 className="font-title mb-4">My Doctors</h2>
							{props.doctors.length === 0 ? (
								<div className={styles.empty}>You have no doctors yet.</div>
							) : (
								<div className={`${styles.doctors} d-flex flex-direction-row justify-content-start`}>
									{props.doctors.map((d, idx) => (
										<div
											key={`allDoctors-${idx}`}
											className={styles.container}
											onClick={() => openDoctor(d)}
										>
											<Avatar user={d} size={'80px'} />
											<div className={'h5 mt-3 font-weight-bolder'}>
												{d.firstName} {d.lastName}
											</div>
											<div className={'h7'}>{d.phone}</div>
											<a className={'h7'} href={`mailto:${d.email}`}>
												{d.email}
											</a>
										</div>
									))}
								</div>
							)}
						</div>
						<div className={styles.health_events}>
							<h2 className="font-title mb-4">Health Records</h2>
							{props.healthEvents.length === 0 ? (
								<div className={styles.empty}>You have no health records yet.</div>
							) : (
								<div className={styles.health_events_inner}>
									{props.healthEvents
										.sort((a, b) => Number(a.date < b.date))
										.map((healthEvent, idx) => {
											return (
												<div
													key={`${healthEvent.event}-${idx}`}
													className={styles.health_event_row}
												>
													<div>{Formatter.stringDate(new Date(healthEvent.date))}</div>
													{/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
													<a
														className={`${styles.subject} unselectable`}
														onClick={() => openHealthEvent(healthEvent)}
													>
														{healthEvent.event}
													</a>
													<div
														className={`${
															healthEvent.status === Status.ACTIVE
																? 'color-quaternary font-weight-bold'
																: healthEvent.status === Status.CURED
																? 'color-good font-weight-bold'
																: 'color-medium'
														}`}
													>
														{STATUS[healthEvent.status]}
													</div>
												</div>
											)
										})}
								</div>
							)}
						</div>
					</>
				)}
				<div className={styles.apts}>
					<h2 className="font-title mb-4">Recent Appointments</h2>
					{props.appointments.length === 0 ? (
						<div className={styles.empty}>You have no appointments to display.</div>
					) : (
						<div className={styles.apts_inner}>
							{props.appointments
								.sort((a, b) => b.date - a.date)
								.map((apt, idx) => {
									const doctor = getDoctorById(apt.doctor)
									const patient = getPatientById(apt.patient)
									return (
										<div key={`apt-${idx}`} className={styles.appt_row}>
											<div>{Formatter.stringDate(new Date(apt.date))}</div>
											{/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
											<a
												className={`${styles.subject} unselectable`}
												onClick={() => openAppointment(apt, patient, doctor)}
											>
												{apt.subject}
											</a>
											{props.isPatient && doctor && (
												<div>
													{doctor.firstName} {doctor.lastName}
												</div>
											)}
											{!props.isPatient && patient && (
												<div>
													{patient.firstName} {patient.lastName}
												</div>
											)}
										</div>
									)
								})}
						</div>
					)}
				</div>
				<AppointmentPopup
					open={false}
					toggleRef={(t) => (toggleAppointmentPopup = t)}
					patient={currentPatient || undefined}
					doctor={currentDoctor || undefined}
					appointment={currentAppointment || undefined}
				/>
				<Popup open={false} toggleRef={(t) => (toggleInfoPopup = t)}>
					{currentDoctor && (
						<div className={styles.popup_container}>
							<div className={styles.doctor_details}>
								<Avatar user={currentDoctor} size={'80px'} />
								<div className={'d-flex flex-column ml-3 flex-1'}>
									<div className={'h5 font-weight-bolder'}>
										{currentDoctor.firstName} {currentDoctor.lastName}
									</div>
									<div className={'h6'}>{currentDoctor.phone}</div>
									<a className={'h6'} href={`mailto:${currentDoctor.email}`}>
										{currentDoctor.email}
									</a>
									<div className={styles.doctor_hours}>
										{DAYS_LOWER.map((day) => (currentDoctor.hours as any)[day] as Day).map(
											(day, idx) => (
												<div key={`day-${idx}`} className={styles.hours}>
													<div>{DAYS[idx]}</div>
													{day.startTime !== -1 ? (
														<div>
															{DateTime.minutesToHHMMAA(day.startTime)} to{' '}
															{DateTime.minutesToHHMMAA(day.endTime)}
														</div>
													) : (
														<div>Closed</div>
													)}
												</div>
											),
										)}
									</div>
								</div>
							</div>
						</div>
					)}
				</Popup>
				<Popup open={false} toggleRef={(t) => (toggleHealthEventPopup = t)}>
					{currentHealthEvent && (
						<div className={styles.popup_container}>
							<h2 className={`font-title mb-1`}>Health Record</h2>
							<div className={'color-medium mb-4'}>
								{DateTime.prettyDate(new Date(currentHealthEvent.date))}
							</div>
							<div>
								<b>Event: </b>
								{currentHealthEvent.event}
							</div>
							<div>
								<b>Status: </b>
								<span
									className={`${
										currentHealthEvent.status === Status.ACTIVE
											? 'color-quaternary font-weight-bold'
											: currentHealthEvent.status === Status.CURED
											? 'color-good font-weight-bold'
											: 'color-medium'
									}`}
								>
									{STATUS[currentHealthEvent.status]}
								</span>
							</div>
							{currentHealthEvent.remarks && (
								<div className={'mt-3'}>
									<b>Remarks:</b>
									<br />
									{currentHealthEvent.remarks}
								</div>
							)}
						</div>
					)}
				</Popup>
			</section>
		</main>
	)
}
