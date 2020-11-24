import React from 'react'
import { render, screen } from '@testing-library/react'
import { Profile } from '../../../src/pages/profile/Profile'

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/another-route',
      search: '',
      hash: '',
      state: null,
      key: '5nvxpbdafa',
	}),
	useHistory: () => ({
		push: jest.fn()
	})

	
}));

describe('Profile', () => {

    test('render.inDocument', () => {

		render(<Profile />)
		const linkElement = screen.getByText('Loading...')
		expect(linkElement).toBeInTheDocument()
	})

})
