import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { NavigationBar } from '../../../src/components/bars/NavigationBar'

// interface NavigationItem {
// 	title: string
// 	url: string
// }

jest.mock('react-router', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/signIn',
    }),
    Link: 'link',
}))

describe('NavigationBar', () => {

    // const navItem = {
    //     title: "Sign In",
    //     url: "/signIn",
    // } as NavigationItem

    // const NavigationBarProps = {
    //     homeRef: "homeRef",
    //     items: [navItem],
    //     onResize: (width: number, height: number) => {},
    // }

    const NavigationBarPropsNoItems = {
        homeRef: "homeRef",
        items: [],
        onResize: (width: number, height: number) => {},
    }

    it('NavigationBar render.inDocument', () => {
        render(<NavigationBar {...NavigationBarPropsNoItems}/>)
                      
		const linkElement = screen.getByText(/upmed/i)
		expect(linkElement).toBeInTheDocument()
    })

    it('NavigationBar trigger resize', () => {
        render(<NavigationBar {...NavigationBarPropsNoItems}/>)

        window.dispatchEvent(new Event('resize'));
        Object.defineProperty(window, 'innerWidth', {writable: true, configurable: true, value: 400})
        Object.defineProperty(window, 'innerHeight', {writable: true, configurable: true, value: 400})
        window.dispatchEvent(new Event('resize'));
        Object.defineProperty(window, 'innerWidth', {writable: true, configurable: true, value: 600})
        Object.defineProperty(window, 'innerHeight', {writable: true, configurable: true, value: 600})
        window.dispatchEvent(new Event('resize'));


        const linkElement = screen.getByText('upmed')
        expect(linkElement).toBeInTheDocument()
    })

    it('NavigationBar toggleNavBar', () => {
        render(<NavigationBar {...NavigationBarPropsNoItems}/>)

        const button = screen.getByLabelText('toggleNavBar')
        fireEvent.mouseDown(button)
        fireEvent.click(button)
        expect(button).toBeInTheDocument()
    })

})


