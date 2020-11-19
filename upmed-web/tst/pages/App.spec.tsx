import React from 'react'
import { render, screen } from '@testing-library/react'
import App from '../../src/pages/App'

describe('App', () => {

    test('render.inDocument', () => {
		render(<App />)
		const linkElement = screen.getByText(/Created for COMS W4156 at Columbia University/i)
		expect(linkElement).toBeInTheDocument()
	})

})
