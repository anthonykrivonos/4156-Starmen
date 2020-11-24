import React from 'react'
import { render, screen } from '@testing-library/react'
import { SignIn } from '../../../src/pages/account/SignIn'

describe('OnSignIn', () => {

    test('render.inDocument', () => {

		render(<SignIn />)
		const linkElement = screen.getByText('Log In')
		expect(linkElement).toBeInTheDocument()
	})

})
