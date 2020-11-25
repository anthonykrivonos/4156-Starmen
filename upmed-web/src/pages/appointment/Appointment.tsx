import React, { useState, useEffect } from 'react'
import { useHistory, useLocation } from 'react-router-dom'

import { Button, Error as ErrorPage, Loading, Room } from '../../components'
import { TIMEOUT_MS } from '../../constants'
import { Appointment as AppointmentClass, HCP, Patient } from '../../models'
import { Client, Hasher, Users } from '../../utils'

import styles from './Appointment.module.sass'

export const Appointment = () => {
	const location = useLocation()
	const history = useHistory()

	const [loading, setLoading] = useState(true)
	const [error, setError] = useState('')
	const [showError, setShowError] = useState(false)

	const [appointment, setAppointment] = useState(null as AppointmentClass | null)
	const [accessToken, setAccessToken] = useState('')
	const [patient, setPatient] = useState(undefined as Patient | undefined)
	const [doctor, setDoctor] = useState(undefined as HCP | undefined)

	useEffect(() => {
		setLoading(true)

		const timeout = setTimeout(() => setShowError(true), TIMEOUT_MS)

		// setAppointment({
		// 	id: '113163124286821057838,105357507564574717959,1605848400000',
		// 	subject: '12341',
		// 	doctor: '1234',
		// 	patient: '1234'
		// } as AppointmentClass)

		// const path = location.pathname.substring(1)
		// if (path.split('/').length > 2) {
		// 	setAccessToken(HCP_AT)
		// } else {
		// 	setAccessToken(PATIENT_AT)
		// }
		// setLoading(false)

		// Try to unhash the appointment id
		try {
			// Get the appointment hash from the URL
			const path = location.pathname.substring(1)
			if (path.split('/').length < 2) {
				throw new Error('No appointment hash provided')
			}
			const appointmentHash = path.split('/')[1]

			// Decode the appointment ID
			const decodedDetails = Hasher.decode(appointmentHash) as {
				appointmentId?: string
				patient?: Patient
				doctor?: HCP
			}
			setPatient(decodedDetails.patient)
			setDoctor(decodedDetails.doctor)

			const userToken = Users.getUserToken()

			// Get the video information for the given appointment ID
			if (!decodedDetails || (decodedDetails && !decodedDetails.appointmentId)) {
				throw new Error('No appointment ID decoded')
			} else {
				Client.Appointment.video(decodedDetails.appointmentId!, userToken)
					.then((apt) => {
						setLoading(false)
						setAppointment(apt)
						clearTimeout(timeout)
						setAccessToken(apt.accessToken)
					})
					.catch((e) => {
						console.error(e)
						clearTimeout(timeout)
						setLoading(false)
						setError('Unable to Enter Room')
					})
			}
		} catch (e) {
			clearTimeout(timeout)
			setShowError(true)
		}
	}, [location.pathname])

	return error ? (
		<ErrorPage shortMessage={'Oops.'} message={error} />
	) : showError ? (
		<ErrorPage />
	) : loading ? (
		<Loading containerClassName={styles.loading} text={'Loading...'} />
	) : (
		<main>
			{appointment && accessToken && (
				<Room appointment={appointment} accessToken={accessToken} patient={patient} doctor={doctor} />
			)}
			<footer className={styles.room_footer}>
				<Button
					text={'Back to Appointments'}
					onClick={() => history.push('/profile/')}
					className={styles.room_footer_button}
				/>
			</footer>
		</main>
	)
}
