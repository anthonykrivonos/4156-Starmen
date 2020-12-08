import React from 'react'
import { render, screen } from '@testing-library/react'
import App from '../../src/pages/App'
import { Users } from '../../src/utils'

jest.mock('../../src/utils/Client')

Users.hasUserToken = jest.fn().mockReturnValueOnce(true).mockReturnValueOnce(false)

describe('App', () => {

    test('App render.inDocument token', () => {
		render(<App />)
		const linkElement = screen.getByText(/Loading.../i)
		expect(linkElement).toBeInTheDocument()
	})

	test('App render.inDocument no token', () => {
		render(<App />)
		const linkElement = screen.getByText(/Created for COMS W4156 at Columbia University/i)
		expect(linkElement).toBeInTheDocument()
	})

})
