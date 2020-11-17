import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Button } from '../button'
import { NavigationBar } from './NavigationBar'
import { STORAGE_KEYS } from '../../constants'
import { Storage } from '../../utils'
import { Users } from '../../utils/Users'
import { Avatar } from '../elements'
import { Patient, HCP } from '../../models'
import './NavigationBar.sass'

const PUBLIC_NAV_ITEMS = [
	<Link to="/signin">
		<Button className={'upmed_btn pl-3 pr-3 pt-2 pb-2 color-white'} text="Sign In" />
	</Link>,
]

export const UMNavigationBar = () => {
	const location = useLocation()
	const [userToken, setUserToken] = useState(Storage.get(STORAGE_KEYS.USER_TOKEN) as string | null)

	const [user, setUser] = useState(null as (Patient | HCP) | null)

	useEffect(() => {
		Users.getCurrentUser().then((u) => setUser(u))
	})

	useEffect(() => {
		const newToken = Storage.get(STORAGE_KEYS.USER_TOKEN)
		setUserToken(newToken)
		// Update user
		Users.getCurrentUser().then((u) => setUser(u))
	}, [location.pathname])

	const authNavItems = [
		user ? (
			<Link className={`d-flex justify-content-start align-items-center p-0 ml-0 mr-0`} to="/profile">
				<Avatar user={user} size={'42px'} />
				<div className={`font-title ml-3`}>{user.firstName}</div>
			</Link>
		) : (
			{
				title: 'Profile',
				url: '/Profile',
			}
		),
	]

	return <NavigationBar items={userToken ? authNavItems : PUBLIC_NAV_ITEMS} homeRef={userToken ? '/profile' : '/'} />
}
