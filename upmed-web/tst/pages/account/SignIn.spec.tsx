import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { SignIn } from '../../../src/pages/account/SignIn'

jest.mock('../../../src/utils/Client')

describe('OnSignIn', () => {

    test('render.inDocument', () => {

		render(<SignIn />)
		const patientButton = screen.getByText('Log in as a Patient')
		const hcpButton = screen.getByText('Log in as a Healthcare Provider')
		
		fireEvent.click(patientButton)
		fireEvent.click(hcpButton)

		expect(patientButton).toBeInTheDocument()
	})

})
