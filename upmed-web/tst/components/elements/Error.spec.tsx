import React from 'react'
import { render, screen } from '@testing-library/react'
import { Error } from '../../../src/components/elements/Error'

describe('Error', () => {

    test('render.inDocument', () => {

		render(<Error />)
		const linkElement = screen.getByText(/upmed/i)
		expect(linkElement).toBeInTheDocument()
	})

})
