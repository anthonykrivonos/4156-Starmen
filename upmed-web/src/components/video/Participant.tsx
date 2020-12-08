/* istanbul ignore file */
import React, { useState, useEffect, useRef, RefObject } from 'react'
import { Track, Participant as ParticipantClass } from 'twilio-video'

import { MUTE, UNMUTE } from '../../assets'
import { HCP, Patient } from '../../models'
import { Button } from '../button'

import styles from './Participant.module.sass'

interface ParticipantProps {
	participant: ParticipantClass
	user?: Patient | HCP
	isMe?: boolean
	className?: string
	containerClassName?: string
}

export const Participant = (props: ParticipantProps) => {
	const [videoTracks, setVideoTracks] = useState([] as Track[])
	const [audioTracks, setAudioTracks] = useState([] as Track[])

	const [isMuted, setMuted] = useState(false)
	const [showOverlay, setShowOverlay] = useState(false)

	const videoRef = useRef() as RefObject<HTMLVideoElement>
	const audioRef = useRef() as RefObject<HTMLAudioElement>

	const trackpubsToTracks = (trackMap: any) =>
		Array.from(trackMap.values())
			.map((pub: any) => pub.track)
			.filter((track) => track !== null)

	useEffect(() => {
		setVideoTracks(trackpubsToTracks(props.participant.videoTracks))
		setAudioTracks(trackpubsToTracks(props.participant.audioTracks))

		const trackSubscribed = (track: Track) => {
			if (track.kind === 'video') {
				setVideoTracks((vT) => [...vT, track])
			} else if (track.kind === 'audio') {
				setAudioTracks((aT) => [...aT, track])
			}
		}

		const trackUnsubscribed = (track: Track) => {
			if (track.kind === 'video') {
				setVideoTracks((vT) => vT.filter((v) => v !== track))
			} else if (track.kind === 'audio') {
				setAudioTracks((aT) => aT.filter((a) => a !== track))
			}
		}

		props.participant.on('trackSubscribed', trackSubscribed)
		props.participant.on('trackUnsubscribed', trackUnsubscribed)

		return () => {
			setVideoTracks([])
			setAudioTracks([])
			props.participant.removeAllListeners()
		}
	}, [props.participant])

	useEffect(() => {
		const videoTrack = videoTracks[0] as any
		if (videoTrack) {
			videoTrack.attach(videoRef.current)
			return () => {
				videoTrack.detach()
			}
		}
	}, [videoTracks])

	useEffect(() => {
		const audioTrack = audioTracks[0] as any
		if (audioTrack) {
			audioTrack.attach(audioRef.current)
			return () => {
				audioTrack.detach()
			}
		}
	}, [audioTracks])

	return (
		<div className={`${styles.participant} ${props.containerClassName || ''}`}>
			<div
				className={`${styles.participant_inner} ${props.className || ''}`}
				onMouseOver={() => setShowOverlay(true)}
				onMouseOut={() => setShowOverlay(false)}
			>
				<div className={styles.overlay} style={{ opacity: showOverlay ? 0.8 : 0 }}>
					<Button
						iconName={isMuted ? UNMUTE : MUTE}
						text={isMuted ? 'Unmute' : 'Mute'}
						className={`${styles.mute_button} ${isMuted ? styles.unmute : styles.mute}`}
						onClick={() => setMuted(!isMuted)}
					/>
				</div>
				<video ref={videoRef} autoPlay={true} />
			</div>
			<audio ref={audioRef} autoPlay={true} muted={props.isMe ? true : isMuted} />
			<div
				className={`${styles.identity} ${props.isMe ? styles.me : ''} ${
					isMuted && !props.isMe ? styles.muted : ''
				}`}
			>
				{props.isMe ? 'Me' : props.user ? props.user.firstName : ''}
				{isMuted && !props.isMe ? ' (Muted)' : ''}
			</div>
		</div>
	)
}
