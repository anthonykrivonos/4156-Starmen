import React from 'react'

import { GoogleLogin, GoogleLoginResponse } from 'react-google-login'

interface GoogleButtonProps {
	text?: string
	className?: string
	onSuccess: (res: {
		id: string
		accessToken: string
		email: string
		firstName: string
		lastName: string
		profilePicture?: string
	}) => void
	onFailure: (error: Error) => void
}

export const GoogleButton = (props: GoogleButtonProps) => {
	const onSuccess = (res: GoogleLoginResponse) => {
		props.onSuccess({
			id: res.googleId,
			accessToken: res.accessToken,
			email: res.profileObj.email,
			firstName: res.profileObj.givenName,
			lastName: res.profileObj.familyName,
			profilePicture: res.profileObj.imageUrl || '',
		})
	}

	const onFailure = (res: { error: string; details: string }) => {
		props.onFailure(new Error(res.error))
	}

	return (
		<GoogleLogin
			clientId={'23489344756-v5tkc07fvkbv960r26geptuf0nihas7g.apps.googleusercontent.com'}
			buttonText={props.text || 'Log in with Google'}
			onSuccess={onSuccess as any}
			onFailure={onFailure}
			className={props.className}
		/>
	)
}
