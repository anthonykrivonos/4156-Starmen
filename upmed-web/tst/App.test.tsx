import React from 'react'
import { render, screen } from '@testing-library/react'
import { test } from 'mocha'
import App from '../src/pages/App'

test('renders learn react link', () => {
	render(<App />)
	const linkElement = screen.getByText(/learn react/i)
	expect(linkElement).toBeInTheDocument()
})
