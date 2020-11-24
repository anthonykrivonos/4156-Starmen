import React from 'react'
import { render, screen } from '@testing-library/react'
import { OnSignIn } from '../../../src/pages/account/OnSignIn'

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

describe('OnSignIn', () => {

    test('render.inDocument', () => {
        // mock the module, mock location

		render(<OnSignIn />)
		const linkElement = screen.getByText('Loading...')
		expect(linkElement).toBeInTheDocument()
	})

})
