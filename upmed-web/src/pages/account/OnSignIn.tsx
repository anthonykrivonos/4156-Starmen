import React, { useState, useEffect } from 'react'
import { useLocation, useHistory } from 'react-router-dom'
import {
	Button,
	TextInput,
	Loading,
	DateInput,
	RadioButtons,
	Counter,
	HoursInputs,
	SuggestionInput,
	Error as ErrorPage,
} from '../../components'
import { INITIAL_HOURS, SPECIALTIES, TIMEOUT_MS } from '../../constants'
import { Hasher, URL, Validator, Formatter, Users, Objects, DateTime, Client } from '../../utils'
import styles from './OnSignIn.module.sass'
import { Status } from '../../models'

export const OnSignIn = () => {
	const location = useLocation()
	const history = useHistory()

	const [status, setStatus] = useState(location.pathname)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState('')
	const [showError, setShowError] = useState(false)

	/**
	 * Keeps track of the user's login webtoken.
	 * undefined: user has not tried logging in yet
	 * null: the user needs to create an account
	 * string: the user has successfully logged in
	 */
	const [userToken, setUserToken] = useState(undefined as string | null | undefined)

	/**
	 * User data properties
	 */
	const [profilePicture, setProfilePicture] = useState(null as string | null)
	const [isPatient, setIsPatient] = useState(true)
	const [id, setId] = useState('')
	const [email, setEmail] = useState('')
	const [phone, setPhone] = useState('')
	const [firstName, setFirstName] = useState('')
	const [lastName, setLastName] = useState('')
	const [specialty, setSpecialty] = useState(undefined as string | undefined)
	const [title, setTitle] = useState(undefined as string | undefined)
	const [dateOfBirth, setDateOfBirth] = useState(Formatter.stringDate(new Date()))
	const [height, setHeight] = useState(165)
	const [weight, setWeight] = useState(65)
	const [sex, setSex] = useState('M')
	const [drinker, setDrinker] = useState(Status.NEVER)
	const [smoker, setSmoker] = useState(Status.NEVER)
	const [hours, setHours] = useState(INITIAL_HOURS)
	const [hoursValid, setHoursValid] = useState(true)

	// Can the user create an account?
	const [isValid, setIsValid] = useState(false)

	useEffect(() => {
		setLoading(true)
		setStatus(location.pathname)

		const timeout = setTimeout(() => setShowError(true), TIMEOUT_MS)

		// Try to unhash the account details
		try {
			const decodedDetails = Hasher.decode(URL.getFromQuery(window.location.href, 'details') as string) as {
				id: string
				accessToken: string
				email: string
				firstName: string
				lastName: string
				profilePicture?: string
				isPatient?: boolean
				expiryTime?: number
			}

			// If expired, prompt a log in again
			if (!decodedDetails || (decodedDetails.expiryTime && decodedDetails.expiryTime < Date.now())) {
				clearTimeout(timeout)
				history.push('/signin')
			} else {
				setId(decodedDetails.id)
				setProfilePicture(decodedDetails.profilePicture ? decodedDetails.profilePicture : null)
				setEmail(decodedDetails.email)
				setFirstName(decodedDetails.firstName)
				setLastName(decodedDetails.lastName)
				setIsPatient(decodedDetails.isPatient || false)
				// Attempt to log in
				isPatient
					? Client.Patient.logIn(id, email)
							.then(({ token }) => {
								if (!token) {
									throw new Error()
								}
								setUserToken(token)
								clearTimeout(timeout)
							})
							.catch((e) => {
								console.error(e)
								clearTimeout(timeout)
							})
					: Client.HCP.logIn(id, email)
							.then(({ token }) => {
								if (!token) {
									throw new Error()
								}
								setUserToken(token)
								clearTimeout(timeout)
							})
							.catch((e) => {
								clearTimeout(timeout)
							})
			}
		} catch (e) {
			// In case something goes wrong, go to sign-in
			clearTimeout(timeout)
			setLoading(false)
			history.push('/signin')
		}
	}, [location.pathname, history, status, id, email, isPatient])

	const createAccount = async () => {
		setLoading(true)
		const timeout = setTimeout(() => setShowError(true), TIMEOUT_MS)

		try {
			const { token } = isPatient
				? await Client.Patient.signUp(
						id,
						firstName,
						lastName,
						phone,
						email,
						dateOfBirth,
						sex,
						height,
						weight,
						drinker,
						smoker,
						profilePicture || undefined,
				  )
				: await Client.HCP.signUp(
						id,
						hours,
						firstName,
						lastName,
						phone,
						email,
						specialty,
						title,
						profilePicture || undefined,
				  )
			setUserToken(token)
			clearTimeout(timeout)
		} catch (e) {
			setLoading(false)
			clearTimeout(timeout)
			setShowError(true)
			setError(e)
		}
	}

	// Search for specialties by substring
	const getSpecialties = async (v: string) => {
		const results: string[] = []
		for (const spec of SPECIALTIES) {
			if (spec.toLowerCase().startsWith(v.toLowerCase())) {
				results.push(spec)
			}
		}
		return results
	}

	// Loading and error when creating the account
	useEffect(() => {
		if (!Objects.isNullish(userToken)) {
			Users.setUserToken(userToken!)
			if (isPatient) {
				Client.Patient.editProfilePicture(id, userToken!, profilePicture!)
					.then(() => window.open('/profile/', '_self'))
					.catch(() => window.open('/profile/', '_self'))
			} else {
				Client.HCP.editProfilePicture(id, userToken!, profilePicture!)
					.then(() => window.open('/profile/', '_self'))
					.catch(() => window.open('/profile/', '_self'))
			}
		}
	}, [userToken, history])

	useEffect(() => {
		// Perform one-line validation on all the inputs
		setIsValid(
			firstName.length > 0 &&
				Validator.realName(firstName) &&
				lastName.length > 0 &&
				Validator.realName(lastName) &&
				email.length > 0 &&
				Validator.email(email) &&
				phone.length > 0 &&
				Validator.phone(phone) &&
				// Patient validation
				(isPatient ? Validator.stringDate(dateOfBirth) : true) &&
				(isPatient ? Validator.text(sex) : true) &&
				(isPatient ? weight > 0 : true) &&
				(isPatient ? height > 0 : true) &&
				(isPatient ? !Objects.isNullish(drinker) : true) &&
				(isPatient ? !Objects.isNullish(smoker) : true) &&
				// Doctor validation
				(!isPatient ? hoursValid : true) &&
				(!isPatient ? (specialty ? Validator.text(specialty) : true) : true) &&
				(!isPatient ? (title ? Validator.text(title) : true) : true),
		)
	}, [
		profilePicture,
		firstName,
		lastName,
		email,
		specialty,
		title,
		phone,
		isPatient,
		dateOfBirth,
		sex,
		weight,
		height,
		drinker,
		smoker,
		hours,
		hoursValid,
	])

	return showError ? (
		<ErrorPage />
	) : loading ? (
		<Loading containerClassName={styles.loading} text={'Loading...'} />
	) : email ? (
		<main id="onSignIn">
			<section className={styles.onsignin}>
				<div className={'row'}>
					<div className={'d-flex d-sm-none col-md-4 justify-content-between'}>
						{profilePicture && (
							<img
								className={`${styles.pfp} mb-4`}
								src={profilePicture}
								alt={`${firstName} ${lastName}`}
								onError={() => setProfilePicture(null)}
							/>
						)}
					</div>
					<div className={`col-md-8 ${styles.info_col}`}>
						<div>
							<h1 className="font-title">Finish Up Your {isPatient ? 'Patient' : 'Provider'} Profile</h1>
							<div>
								Welcome, <b>{firstName}</b>! Before we create your account, let's just make sure we get
								your basic info right.
							</div>
						</div>
						<div className={styles.basic_info}>
							<h4 className={`${styles.section_title} font-title`}>Basic Information</h4>
							<TextInput
								containerClassName={styles.input_short}
								value={firstName}
								label={'First Name'}
								errorLabel={'Invalid first name.'}
								validator={Validator.realName}
								onChange={(t) => setFirstName(t)}
								required
							/>
							<TextInput
								containerClassName={styles.input_short}
								value={lastName}
								label={'Last Name'}
								errorLabel={'Invalid last name.'}
								validator={Validator.realName}
								onChange={(t) => setLastName(t)}
								required
							/>
							<TextInput
								containerClassName={styles.input_short}
								value={email}
								label={'Email'}
								errorLabel={'Invalid email.'}
								validator={Validator.email}
								onChange={(t) => setEmail(t)}
								required
							/>
							<TextInput
								containerClassName={styles.input_short}
								value={phone}
								label={'Phone Number'}
								errorLabel={'Invalid phone number.'}
								validator={Validator.phone}
								formatter={Formatter.phone}
								onChange={(t) => setPhone(t)}
								required
							/>
							{isPatient && (
								<DateInput
									label={'Date of Birth'}
									containerClassName={styles.input_short}
									onDateChange={(d) => setDateOfBirth(Formatter.stringDate(d))}
									maxDate={DateTime.getModifiedDate(new Date(), -18)}
									required
								/>
							)}
						</div>
						{isPatient && (
							<div className={styles.basic_info}>
								<h4 className={`${styles.section_title} font-title`}>Personal Information</h4>
								<RadioButtons
									displayOptions={['Male', 'Female']}
									options={['M', 'F']}
									label={'Sex'}
									className={styles.input_short}
									onChange={(option) => setSex(option)}
									required
								/>
								<div className={'d-flex flex-row align-items-start'}>
									<Counter
										containerClassName={styles.input_tiny}
										value={height}
										label={'Height (cm)'}
										errorLabel={'Invalid height.'}
										onChange={(t) => setHeight(Number(t))}
										min={0}
										required
									/>
									<Counter
										containerClassName={styles.input_tiny_2}
										value={weight}
										label={'Weight (kg)'}
										errorLabel={'Invalid weight.'}
										onChange={(t) => setWeight(Number(t))}
										min={0}
										required
									/>
								</div>
								<RadioButtons
									options={[Status.ACTIVE, Status.PAST, Status.NEVER]}
									displayOptions={['Yes', 'Past', 'Never']}
									label={'Are you a drinker?'}
									className={styles.input_short}
									selectedIdx={2}
									onChange={(option) => setDrinker(option)}
									required
								/>
								<RadioButtons
									options={[Status.ACTIVE, Status.PAST, Status.NEVER]}
									displayOptions={['Yes', 'Past', 'Never']}
									label={'Are you a smoker?'}
									className={styles.input_short}
									selectedIdx={2}
									onChange={(option) => setSmoker(option)}
									required
								/>
							</div>
						)}
						{!isPatient && (
							<div className={styles.basic_info}>
								<h4 className={`${styles.section_title} font-title`}>Professional Info</h4>
								<TextInput
									containerClassName={styles.input_short}
									value={title}
									label={'Business Name'}
									errorLabel={'Invalid first name.'}
									validator={Validator.text}
									onChange={(t) => setTitle(t)}
									required={false}
								/>
								<SuggestionInput
									containerClassName={styles.input_short}
									value={specialty}
									label={'Specialty'}
									onChange={(t) => setSpecialty(t)}
									required={false}
									suggestionLimit={4}
									getSuggestions={getSpecialties}
								/>
								<HoursInputs
									label={'Business Hours'}
									onChange={(hrs, valid) => {
										setHours(hrs)
										setHoursValid(valid)
									}}
									className={styles.input_mid}
									required
								/>
							</div>
						)}
					</div>
					<div className={'d-flex col-md-4 flex-column-reverse justify-content-between'}>
						<div className={'d-flex flex-row justify-content-end'}>
							<div>
								<Button
									disabled={!isValid}
									className={`${styles.create_account} ${!isValid ? styles.disabled : ''}`}
									onClick={createAccount}
									text={'Create Account'}
								/>
								{error && <div className={'mt-3 color-quaternary'}>{error}</div>}
							</div>
						</div>
						{profilePicture && (
							<img
								className={`d-none d-sm-block ${styles.pfp}`}
								src={profilePicture}
								alt={`${firstName} ${lastName}`}
							/>
						)}
					</div>
				</div>
			</section>
		</main>
	) : null
}
