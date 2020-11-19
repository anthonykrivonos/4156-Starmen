import React from 'react'
import { render, screen } from '@testing-library/react'
import { GoogleButton } from '../../../src/components/button/GoogleButton'

describe('GoogleButton', () => {

    const onSuccess = (res: {
		id: string
		accessToken: string
		email: string
		firstName: string
		lastName: string
		profilePicture?: string
    }) => {}
    
    const onFailure = (error: Error) => {}

    test('render.inDocument', () => {
		render(<GoogleButton onSuccess={onSuccess} onFailure={onFailure}/>)
		const linkElement = screen.getByText(/Log in with Google/i)
		expect(linkElement).toBeInTheDocument()
	})

})
