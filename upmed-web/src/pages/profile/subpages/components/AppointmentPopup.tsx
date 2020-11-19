import React, { useState } from 'react'

import { Button, Loading, Popup, PopupProps } from '../../../../components'
import { Appointment, HCP, Patient } from '../../../../models'
import { Client, DateTime, Users } from '../../../../utils'
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
					{props.isPatient && props.doctor && (
						<div>
							<b>Doctor: </b>
							{props.doctor.firstName} {props.doctor.lastName}
						</div>
					)}
					{!props.isPatient && props.patient && (
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
					{!props.isPatient && props.patient && (
						<div className={'mt-4 d-flex flex-row align-items-center'}>
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
				</div>
			)}
		</Popup>
	)
}
