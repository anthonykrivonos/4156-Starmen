import React from 'react'
import { render, screen } from '@testing-library/react'
import { Popup } from '../../../src/components/elements/Popup'

describe('Popup', () => {

    test('render.inDocument', () => {

		render(<Popup children={"hi"} open={true} autoclose={true}/>)
		const linkElement = screen.getByText(/hi/i)
		expect(linkElement).toBeInTheDocument()
	})

})
