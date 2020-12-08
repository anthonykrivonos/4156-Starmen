/* istanbul ignore file */
import React, { useState, useEffect } from 'react'
import Video, { Room as RoomClass, Participant as ParticipantClass } from 'twilio-video'

import { Appointment, HCP, Patient } from '../../models'
import { DateTime, Users } from '../../utils'
import { Participant } from './Participant'

import styles from './Room.module.sass'

interface RoomProps {
	appointment: Appointment
	doctor?: HCP
	patient?: Patient
	accessToken: string
}

export const Room = (props: RoomProps) => {
	const [currentUser, setCurrentUser] = useState(undefined as (Patient | HCP) | undefined)
	const [otherUser, setOtherUser] = useState(undefined as (Patient | HCP) | undefined)
	const [room, setRoom] = useState(null as RoomClass | null)
	const [participants, setParticipants] = useState([] as ParticipantClass[])

	useEffect(() => {
		Users.getCurrentUser()
			.then((u) => {
				u ? setCurrentUser(u) : ''
				if (!u) {
					return
				}
				if (props.doctor && props.doctor.id === u.id) {
					setOtherUser(props.patient)
				} else {
					setOtherUser(props.doctor)
				}
			})
			.catch()

		const participantConnected = (participant: ParticipantClass) => {
			setParticipants((prevParticipants) => [...prevParticipants, participant])
		}

		const participantDisconnected = (participant: ParticipantClass) => {
			setParticipants((prevParticipants) => prevParticipants.filter((p) => p !== participant))
		}

		Video.connect(props.accessToken, { name: props.appointment.id }).then((r: RoomClass) => {
			setRoom(r)
			r.on('participantConnected', participantConnected)
			r.on('participantDisconnected', participantDisconnected)
			r.participants.forEach(participantConnected)
		})

		return () => {
			setRoom((currentRoom) => {
				if (currentRoom && currentRoom.localParticipant.state === 'connected') {
					currentRoom.localParticipant.tracks.forEach((trackPublication: any) => {
						trackPublication.track.stop()
					})
					currentRoom.disconnect()
					return null
				} else {
					return currentRoom
				}
			})
		}
	}, [props.appointment, props.accessToken])

	return (
		<div className={styles.room}>
			<div className={styles.room_name}>{props.appointment.subject}</div>
			<div className={styles.appointment_date}>{DateTime.prettyDate(new Date(props.appointment.date))}</div>
			{participants.length > 0 && (
				<Participant
					key={participants[0].sid}
					participant={participants[0]}
					user={otherUser}
					className={styles.other_user}
					isMe={false}
				/>
			)}
			{room ? (
				<Participant
					key={room.localParticipant.sid}
					participant={room.localParticipant}
					user={currentUser}
					className={styles.current_user}
					isMe={true}
				/>
			) : (
				''
			)}
		</div>
	)
}
