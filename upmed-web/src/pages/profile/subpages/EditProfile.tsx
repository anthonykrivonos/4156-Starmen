import React, { useState, useEffect } from 'react'

import { ProfileSubpageProps } from '../Profile'

import {
	Button,
	TextInput,
	Loading,
	DateInput,
	RadioButtons,
	Counter,
	HoursInputs,
	SuggestionInput,
} from '../../../components'
import { SPECIALTIES } from '../../../constants'
import { Validator, Formatter, Objects, DateTime, Client, Users } from '../../../utils'
import styles from './EditProfile.module.sass'
import { HCP, Patient, Status } from '../../../models'

export const EditProfile = (props: ProfileSubpageProps) => {
	const [loadingUpdate, setLoadingUpdate] = useState(false)
	const [error, setError] = useState('')

	const patient = props.user as Patient
	const hcp = props.user as HCP

	const [email, setEmail] = useState(props.user.email)
	const [phone, setPhone] = useState(props.user.phone)
	const [firstName, setFirstName] = useState(props.user.firstName)
	const [lastName, setLastName] = useState(props.user.lastName)
	const [specialty, setSpecialty] = useState(hcp.specialty)
	const [title, setTitle] = useState(hcp.title)
	const [hours, setHours] = useState(hcp.hours)
	const [hoursValid, setHoursValid] = useState(true)
	const [dateOfBirth, setDateOfBirth] = useState(patient.dateOfBirth)
	const [height, setHeight] = useState(patient.height)
	const [weight, setWeight] = useState(patient.weight)
	const [drinker, setDrinker] = useState(patient.drinker)
	const [smoker, setSmoker] = useState(patient.smoker)

	// Can the user create an account?
	const [isValid, setIsValid] = useState(false)

	const updateAccount = async () => {
		setLoadingUpdate(true)
		try {
			const token = Users.getUserToken()
			if (props.isPatient) {
				await Client.Patient.editProfile(
					props.user.id,
					token,
					firstName,
					lastName,
					phone,
					email,
					height,
					weight,
					drinker,
					smoker,
					props.user.profilePicture,
				)
			} else {
				await Client.HCP.editProfile(
					props.user.id,
					token,
					hours,
					firstName,
					lastName,
					phone,
					email,
					specialty,
					title ? title : undefined,
					props.user.profilePicture,
				)
			}
			window.location.reload()
		} catch (e) {
			console.error(e)
			setError('An error occurred.')
			setLoadingUpdate(false)
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

	useEffect(() => {
		// Perform one-line validation on all the inputs
		setIsValid(
			!Objects.isNullish(firstName) &&
				firstName.length > 0 &&
				Validator.realName(firstName) &&
				!Objects.isNullish(lastName) &&
				lastName.length > 0 &&
				Validator.realName(lastName) &&
				!Objects.isNullish(email) &&
				email.length > 0 &&
				Validator.email(email) &&
				!Objects.isNullish(phone) &&
				phone.length > 0 &&
				Validator.phone(phone) &&
				// Patient validation
				(props.isPatient ? Validator.stringDate(dateOfBirth) : true) &&
				(props.isPatient ? weight > 0 : true) &&
				(props.isPatient ? height > 0 : true) &&
				(props.isPatient ? !Objects.isNullish(drinker) : true) &&
				(props.isPatient ? !Objects.isNullish(smoker) : true) &&
				// Doctor validation
				(!props.isPatient ? hoursValid : true) &&
				(!props.isPatient ? (specialty ? Validator.text(specialty) : true) : true) &&
				(!props.isPatient ? (title ? Validator.text(title) : true) : true),
		)
	}, [
		firstName,
		lastName,
		email,
		specialty,
		title,
		phone,
		dateOfBirth,
		weight,
		height,
		drinker,
		smoker,
		hours,
		hoursValid,
		props.isPatient,
	])

	return (
		<main id="editProfile">
			<section className={styles.edit_profile_outter}>
				<div className={''}>
					<div className={styles.info_col}>
						<h2 className="font-title">Edit Profile</h2>
						<div className={`${styles.basic_info} ${styles.container}`}>
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
							{props.isPatient && dateOfBirth !== '' && (
								<DateInput
									label={'Date of Birth'}
									containerClassName={styles.input_short}
									onDateChange={(d) => setDateOfBirth(Formatter.stringDate(d))}
									maxDate={DateTime.getModifiedDate(new Date(), -18)}
									value={DateTime.dateFromStringDate(dateOfBirth)}
									required
								/>
							)}
						</div>
						{props.isPatient && (
							<div className={`${styles.basic_info} ${styles.container}`}>
								<h4 className={`${styles.section_title} font-title`}>Personal Information</h4>
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
									selectedIdx={[Status.ACTIVE, Status.PAST, Status.NEVER].indexOf(drinker)}
									onChange={(option) => setDrinker(option)}
									required
								/>
								<RadioButtons
									options={[Status.ACTIVE, Status.PAST, Status.NEVER]}
									displayOptions={['Yes', 'Past', 'Never']}
									label={'Are you a smoker?'}
									className={styles.input_short}
									selectedIdx={[Status.ACTIVE, Status.PAST, Status.NEVER].indexOf(smoker)}
									onChange={(option) => setSmoker(option)}
									required
								/>
							</div>
						)}
						{!props.isPatient && (
							<div className={`${styles.basic_info} ${styles.container}`}>
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
									initialHours={hours}
									required
								/>
							</div>
						)}
					</div>
					<div className={'d-flex flex-column-reverse justify-content-between mt-4'}>
						<div className={'d-flex flex-row justify-content-end align-items-center'}>
							{loadingUpdate && <Loading size={'50px'} className={'w-25 mr-4'} />}
							<div>
								<Button
									disabled={!isValid || loadingUpdate}
									className={`${styles.update_account} ${!isValid ? styles.disabled : ''}`}
									onClick={updateAccount}
									text={'Update Account'}
								/>
								{error && <div className={'mt-3 color-quaternary'}>{error}</div>}
							</div>
						</div>
					</div>
				</div>
			</section>
		</main>
	)
}
