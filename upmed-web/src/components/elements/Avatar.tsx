import React from 'react'
import ReactAvatar from 'react-avatar'
import { colors } from '../../constants'
import { Patient, HCP } from '../../models'

interface AvatarProps {
	user: Patient | HCP
	size: string
	className?: string
	onClick?: (user: Patient | HCP) => void
}

export const Avatar = (props: AvatarProps) => {
	const { firstName, lastName, profilePicture } = props.user

	return (
		<ReactAvatar
			name={`${firstName} ${lastName}`}
			initials={`${firstName[0]}${lastName[0]}`}
			color={colors.primary}
			size={props.size}
			round={true}
			src={profilePicture}
			className={`unselectable ${props.className || ''}`}
			onClick={props.onClick ? () => props.onClick!(props.user) : undefined}
		/>
	)
}
