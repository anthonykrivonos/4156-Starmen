import React from 'react'
import { fireEvent, render, screen, } from '@testing-library/react'
import { Popup } from '../../../src/components/elements/Popup'

describe('Popup', () => {

	const popupPropsOpen = {
        children: "hi",
		open: true,
		autoclose: true,
		toggleRef: (toggler: (toggle: boolean) => void) => {},
		onOpen: () => {},
		onClose: () => {},
	}

	const popupPropsNotOpen = {
        children: "hi",
		open: false,
		autoclose: true,
		toggleRef: (toggler: (toggle: boolean) => void) => {},
		onOpen: () => {},
		onClose: () => {},
    }

    test('Popup render.inDocument open', () => {
		render(<Popup {...popupPropsOpen}/>)
	
		const linkElement = screen.getByText(/hi/i)
		const overlay = screen.getByTestId('overlay')
		const dialog = screen.getByRole('dialog')
		const root = document.getElementById('popup-root')

		fireEvent.click(dialog)
		fireEvent.click(overlay)
		fireEvent.click(linkElement)
		fireEvent.click(root as HTMLElement)

		expect(linkElement).toBeInTheDocument()
	})

	test('Popup render.inDocument not open', () => {
		render(<Popup {...popupPropsNotOpen}/>)

		const linkElement = document.getElementById('popup-root')
		fireEvent.click(linkElement as HTMLElement)

		expect(linkElement).toBeInTheDocument()
	})

})
