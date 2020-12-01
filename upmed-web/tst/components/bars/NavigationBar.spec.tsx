import React from 'react'
import { render, screen } from '@testing-library/react'
import { NavigationBar } from '../../../src/components/bars/NavigationBar'

jest.mock('react-router', () => ({
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
}));

describe('NavigationBar', () => {

    // const NavigationItem = {
    //     title: "title",
    //     url: "url"
    // }

    const NavigationBarProps = {
        homeRef: "homeRef",
        onResize: (width: number, height: number) => {},
    }

    it('render.inDocument', () => {
		render(<NavigationBar {...NavigationBarProps}/>)
		const linkElement = screen.getByText(/upmed/i)
		expect(linkElement).toBeInTheDocument()
	})

})


