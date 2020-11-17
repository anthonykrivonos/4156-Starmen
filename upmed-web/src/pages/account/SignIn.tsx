import React, { useState } from 'react'
import { useHistory } from 'react-router-dom'
import { Hasher, DateTime } from '../../utils'
import { LOGIN } from '../../assets'
import styles from './SignIn.module.sass'
import { GoogleButton } from '../../components'

export const SignIn = () => {
	const history = useHistory()

	const [error, setError] = useState('')

	const onSuccess = (
		isPatient: boolean,
		res: {
			id: string
			accessToken: string
			email: string
			firstName: string
			lastName: string
			profilePicture?: string
			isPatient?: boolean
			expiryTime?: number
		},
	) => {
		res.isPatient = isPatient
		// Expire in 10 minutes
		res.expiryTime = DateTime.getModifiedDate(new Date(), 0, 0, 0, 0, 10).getTime()
		const hash = Hasher.encode(res)
		history.push(`/onsignin?details=${hash}`)
	}
	const onFailure = (err: Error) => setError(err.message)

	return (
		<main id="signup">
			<section className={styles.signup}>
				<h2 className="font-title">Log In</h2>
				<div className={styles.tile}>
					<div className={styles.card_text}>
						<p>As an authenticity measure, please create an account or log back in through Google.</p>
						<GoogleButton
							text={'Log in as a Patient'}
							onSuccess={(res) => onSuccess(true, res)}
							onFailure={onFailure}
							className={styles.login_patient}
						/>
						<GoogleButton
							text={'Log in as a Healthcare Provider'}
							onSuccess={(res) => onSuccess(false, res)}
							onFailure={onFailure}
							className={styles.login_hcp}
						/>
						{error && (
							<div className={styles.login_error}>
								Google is having trouble connecting to its servers...
							</div>
						)}
						<p className={styles.bottom_text}>
							Don't have an account? Logging in through Google automatically creates one for you!
						</p>
					</div>
					<img className={styles.tile_img} src={LOGIN} alt="B&W sand dune" />
				</div>
			</section>
		</main>
	)
}
