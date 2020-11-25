import React, { useState } from 'react'
import { useHistory } from 'react-router-dom'
import { VIDEO } from '../../../../assets'

import { Button, Loading, Popup, PopupProps } from '../../../../components'
import { Appointment, HCP, Patient } from '../../../../models'
import { Client, DateTime, Hasher, Users } from '../../../../utils'
import styles from './AppointmentPopup.module.sass'

interface AppointmentPopupProps extends PopupProps {
	appointment?: Appointment
	doctor?: HCP
	patient?: Patient
	isPatient?: boolean
}

export const AppointmentPopup = (props: AppointmentPopupProps) => {
	const [notifyLoading, setNotifyLoading] = useState(false)
	const [notifyMessage, setNotifyMessage] = useState('')

	const history = useHistory()

	const endDate = props.appointment ? props.appointment.date + props.appointment.duration * 60 * 1000 : 0

	const notify = async () => {
		setNotifyLoading(true)
		try {
			const test = await Client.HCP.testNumber(Users.getUserToken(), props.appointment!.id)
			if (!test.success) {
				setNotifyMessage(
					`Looks like ${
						props.patient ? props.patient.firstName : 'your patient'
					} does not have texting enabled.`,
				)
			} else {
				await Client.HCP.notify(Users.getUserToken(), props.appointment!.id)
				setNotifyMessage('Sent!')
			}
		} catch {
			setNotifyMessage('An error occurred. Please try again later.')
		}
		setNotifyLoading(false)
	}

	const goToVideo = () => {
		const appointmentHash = Hasher.encode({
			appointmentId: props.appointment?.id,
			doctor: props.doctor,
			patient: props.patient,
		})
		const appointmentURL = `/appointment/${appointmentHash}`
		history.push(appointmentURL)
	}

	return (
		<Popup
			{...props}
			onClose={() => {
				setNotifyMessage('')
				props.onClose && props.onClose()
			}}
		>
			{props.appointment && (
				<div className={styles.appointment_popup_container}>
					<h2 className={`font-title mb-1`}>Appointment Details</h2>
					<div className={'color-medium mb-4'}>
						{DateTime.prettyDate(new Date(props.appointment.date))} @{' '}
						{new Date(props.appointment.date).toLocaleTimeString().toLowerCase()} (
						{props.appointment.duration} min)
					</div>
					<div>
						<b>Subject: </b>
						{props.appointment.subject}
					</div>
					{props.doctor && (
						<div>
							<b>Doctor: </b>
							{props.doctor.firstName} {props.doctor.lastName}
						</div>
					)}
					{props.patient && (
						<div>
							<b>Patient: </b>
							{props.patient.firstName} {props.patient.lastName}
						</div>
					)}
					{props.appointment.notes && (
						<div className={'mt-3'}>
							<b>Notes:</b>
							<br />
							{props.appointment.notes}
						</div>
					)}
					<div className={'d-flex flex-row align-items-center justify-content-start mt-4'}>
						{!props.isPatient && props.patient && (
							<div className={'d-flex flex-row align-items-center mr-2'}>
								<Button
									text={'Notify Patient'}
									onClick={notify}
									disabled={notifyLoading || (notifyMessage !== '' && notifyMessage !== 'Sent!')}
									className={styles.notify_button}
								/>
								{notifyLoading && <Loading size={'50px'} className={'w-25 ml-4'} />}
								{notifyMessage && (
									<div className={`ml-4 ${notifyMessage !== 'Sent!' ? 'color-quaternary' : ''}`}>
										{notifyMessage}
									</div>
								)}
							</div>
						)}
						{props.appointment && Date.now() < endDate && (
							<Button
								text={'Enter Room'}
								iconName={VIDEO}
								onClick={goToVideo}
								disabled={notifyLoading || (notifyMessage !== '' && notifyMessage !== 'Sent!')}
								className={styles.video_button}
							/>
						)}
					</div>
				</div>
			)}
		</Popup>
	)
}
