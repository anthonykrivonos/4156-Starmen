import React from 'react'
import { render, screen } from '@testing-library/react'
import { UMNavigationBar } from '../../../src/components/'
// import { Storage } from '../../../src/utils'

// const patient = {
// 	id: "100",
// 	firstName: "kenneth",
// 	lastName: "chuen",
// 	calendar: [],
// 	phone: "347-681-6990",
// 	email: "kc3334@columbia",
// 	dateOfBirth: "02/05/1997",
// 	sex: "M",
// 	height: 179,
// 	weight: 154,
// 	drinker: 0,
// 	smoker: 0,
// 	health: [],
// 	doctors: []
// }

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/another-route',
	}),
	useState: jest
        .fn()
        .mockReturnValueOnce('')
        .mockReturnValueOnce(0)
        .mockReturnValueOnce(false)
        .mockReturnValueOnce(false)
        .mockReturnValueOnce(false),
    Link: 'Link',
	
}))


// jest.mock('react', () => ({
// 	...jest.requireActual('react') as any,
// 	useState: jest
// 		.fn()
		
// }))

// jest.mock('Storage', () => ({
// 	...jest.requireActual('Storage') as any,
// 	get: jest.fn().mockReturnValue("user_token"),
// }))

describe('UMNavigationBar', () => {

    it('render.inDocument', () => {
		render(<UMNavigationBar />)
		const linkElement = screen.getByText(/upmed/i)
		expect(linkElement).toBeInTheDocument()
	})

})


