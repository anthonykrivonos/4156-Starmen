import React, { useState, useEffect } from 'react'

import { ERROR1, ERROR2, ERROR3 } from '../../assets'
import { Button } from '../button'
import styles from './Error.module.sass'

interface ErrorProps {
	containerClassName?: string
	className?: string
	shortMessage?: string
	message?: string
}

const ERRORS = [
	{
		image: ERROR1,
		shortMessage: 'Breathe!',
		message: "Something went wrong, but we can still feel the server's heartbeat.",
	},
	{
		image: ERROR2,
		shortMessage: 'Hmmmm...',
		message: "We couldn't answer in time, but our doctors are getting to the bottom of it.",
	},
	{
		image: ERROR3,
		shortMessage: 'Oops.',
		message: 'Our server might be dealing with somebody else at the moment, so please be patient!',
	},
]

export const Error = (props: ErrorProps) => {
	const [error, setError] = useState(ERRORS[0])

	useEffect(() => {
		const errorIdx = Math.floor(Math.random() * ERRORS.length)
		setError(ERRORS[errorIdx])
	})

	const reload = () => window.location.reload()

	return (
		<div className={`${styles.error_outter} ${props.containerClassName || ''}`}>
			<div className={`${styles.error_inner} ${props.className || ''}`}>
				<img className={styles.error_image} src={error.image} alt={error.shortMessage} />
				<div className={styles.error_short}>{props.shortMessage || error.shortMessage}</div>
				<div className={styles.error_message}>{props.message || error.message}</div>
				<div className={styles.retry}>Click the button below to try again.</div>
				<div className={styles.button_container}>
					<Button text={'Try Again'} className={styles.button} onClick={reload} />
				</div>
				<div className={styles.upmed_logo}>upmed</div>
			</div>
		</div>
	)
}
