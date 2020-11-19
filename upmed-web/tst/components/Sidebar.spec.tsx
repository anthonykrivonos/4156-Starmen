import React from 'react'
import { render, screen } from '@testing-library/react'
import { Sidebar } from '../../src/components/bars/Sidebar'

describe('Sidebar', () => {

    const buttonA = {
        text: "string"
    }

    it('render.inDocument', () => {
		render(<Sidebar buttons={[buttonA]} isPatient={true}/>)
		const linkElement = screen.getByText(/upmed/i)
		expect(linkElement).toBeInTheDocument()
	})

})


