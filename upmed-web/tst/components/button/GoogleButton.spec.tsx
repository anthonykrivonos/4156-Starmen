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
        render(<GoogleButton text={"yello"} className={"className"} onSuccess={onSuccess} onFailure={onFailure}/>)
        const linkElement = screen.getByText(/yello/i)
        expect(linkElement).toBeInTheDocument()
	  })

})
