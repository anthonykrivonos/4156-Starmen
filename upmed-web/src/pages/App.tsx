import React, { Component } from 'react'
import { BrowserRouter as Router, Switch, Route as ReactRoute, Redirect } from 'react-router-dom'

import { Footer, UMNavigationBar } from '../components'
import { Home } from './home'
import { SignIn, OnSignIn } from './account'
import { Profile } from './profile'
import { Users } from '../utils'

import './../index.sass'

interface Route {
	name: string
	path: string
	page: React.ReactElement
	auth: boolean
	navbar?: boolean
	footer?: boolean
}

const ROUTES: Route[] = [
	{
		name: 'Sign In',
		path: '/signin',
		page: <SignIn />,
		auth: false,
	},
	{
		name: 'On Sign In',
		path: '/onsignin',
		page: <OnSignIn />,
		auth: false,
	},
	{
		name: 'Profile',
		path: '/profile/*',
		page: <Profile />,
		auth: false,
		navbar: false,
		footer: false,
	},
	{
		name: 'Home',
		path: '/',
		page: <Home />,
		auth: false,
	},
]

export class App extends Component {
	private isLoggedIn: boolean

	constructor(props: any) {
		super(props)
		this.isLoggedIn = Users.hasUserToken()
	}

	public render = () => {
		return (
			<Router>
				<Switch>
					{this.isLoggedIn && <Redirect exact from={'/'} to={'/profile/'} />}
					{!this.isLoggedIn && <Redirect exact from={'/profile/*'} to={'/'} />}
					{ROUTES.filter((r) => this.isLoggedIn || !r.auth).map((route) => (
						<ReactRoute exact key={route.name} path={route.path}>
							{route.navbar !== false && <UMNavigationBar />}
							{route.page}
							{route.footer !== false && <Footer />}
						</ReactRoute>
					))}
					<Redirect exact from={'/*'} to={this.isLoggedIn ? '/profile/' : '/'} />
				</Switch>
			</Router>
		)
	}
}

export default App
