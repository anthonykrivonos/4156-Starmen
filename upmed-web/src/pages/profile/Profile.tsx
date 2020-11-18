import React, { useState, useEffect } from 'react'
import { useHistory, useLocation } from 'react-router-dom'

import { Error, Loading, Sidebar } from '../../components'
import { Patient, HCP, Appointment, HealthEvent } from '../../models'
import { Client, Users } from '../../utils'

import { Calendar, MedicalInfo, EditProfile } from './subpages'

import styles from './Profile.module.sass'
import { TIMEOUT_MS } from '../../constants'

const PROFILE_SUBPAGES = [
	{
		name: 'Appointments',
		component: Calendar,
		path: '/profile/appointments',
	},
	{
		name: 'Medical Info',
		component: MedicalInfo,
		path: '/profile/medical',
	},
	{
		name: 'Edit Profile',
		component: EditProfile,
		path: '/profile/edit',
	},
]

export interface ProfileSubpageProps {
	user: Patient | HCP
	patients: Patient[]
	doctors: HCP[]
	appointments: Appointment[]
	healthEvents: HealthEvent[]
	isPatient: boolean
}

const getSubpageProps = async () => {
	const isPatient = Users.getIsPatient()

	const user = await Users.getCurrentUser()
	const token = Users.getUserToken()

	let doctors = [] as HCP[]
	let healthEvents = [] as HealthEvent[]
	let patients = [] as Patient[]
	let appointments = [] as Appointment[]

	if (isPatient) {
		doctors = await Client.Patient.getHCPs(token)
		healthEvents = (user as Patient).health
	} else {
		patients = await Client.HCP.getPatients(token)
	}

	// Band-aid for empty calendar bug
	appointments = await Client.Appointment.getCalendar(token)

	return {
		user,
		appointments,
		patients,
		doctors,
		isPatient,
		healthEvents,
	} as ProfileSubpageProps
}

export const Profile = () => {
	const history = useHistory()
	const location = useLocation()

	const [loading, setLoading] = useState(true)
	const [showError, setShowError] = useState(false)
	const [subpage, setSubpage] = useState(null as any)
	const [didSetSubpageProps, setDidSetSubpageProps] = useState(false)
	const [subpageProps, setSubpageProps] = useState(null as ProfileSubpageProps | null)

	useEffect(() => {
		setLoading(true)
		let didSetPath = false
		for (const sp of PROFILE_SUBPAGES) {
			if (sp.path === location.pathname) {
				setSubpage(sp)
				didSetPath = true
				break
			}
		}
		if (!didSetPath) {
			history.push(PROFILE_SUBPAGES[0].path)
		}

		if (!didSetSubpageProps) {
			setDidSetSubpageProps(true)
			const timeout = setTimeout(() => setShowError(true), TIMEOUT_MS)
			getSubpageProps()
				.then((p) => {
					setSubpageProps(p)
					clearTimeout(timeout)
					setLoading(false)
				})
				.catch(() => {
					setShowError(true)
					clearTimeout(timeout)
					setLoading(false)
				})
		} else {
			setLoading(false)
		}
	}, [didSetSubpageProps, history, location.pathname])

	return showError ? (
		<Error />
	) : loading || !subpage || !subpageProps ? (
		<Loading containerClassName={styles.loading} text={'Loading...'} />
	) : (
		<main className={styles.profile_outter}>
			<div className={styles.sideBar}>
				<Sidebar
					className={styles.sideBar_inner}
					user={subpageProps.user}
					isPatient={subpageProps.isPatient}
					onAvatarClick={() => history.push('/profile/')}
					buttons={PROFILE_SUBPAGES.map((sp) => ({
						text: sp.name,
						onClick: () => history.push(sp.path),
						active: location.pathname === sp.path,
					})).concat([
						{
							text: 'Log Out',
							isBottom: true,
							onClick: () => {
								Users.logOut()
								window.open(window.location.origin, '_self')
							},
						},
					] as any[])}
				/>
			</div>
			<div className={styles.subpage}>{<subpage.component {...subpageProps} />}</div>
		</main>
	)
}
