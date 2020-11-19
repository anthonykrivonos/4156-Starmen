import React from 'react'
import { render, screen } from '@testing-library/react'
import { Button } from '../../../src/components/button/Button'


describe('Button', () => {

    test('render.inDocument', () => {

        const button = <Button text={'button with text'} />

		render(button)
		const linkElement = screen.getByText(/button with text/i)
		expect(linkElement).toBeInTheDocument()
	})

})
