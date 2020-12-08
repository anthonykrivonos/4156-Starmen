import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '../../../src/components/button/Button'


describe('Button', () => {

	test('Button render.inDocument no OnClick', () => {
        const button = <Button text={'button with text'} disabled={false} iconName={"icon name"}/>
		render(button)

		const linkElement = screen.getByText(/button with text/i)

		fireEvent.mouseDown(linkElement)
		fireEvent.mouseUp(linkElement)
		fireEvent.mouseEnter(linkElement)
		fireEvent.mouseLeave(linkElement)
		fireEvent.click(linkElement)

		expect(linkElement).toBeInTheDocument()
	})

    test('Button render.inDocument with OnClick', () => {
        const button = <Button text={'button with text'} disabled={false} iconName={"icon name"} onClick={() => {}}/>
		render(button)

		const linkElement = screen.getByText(/button with text/i)

		fireEvent.mouseDown(linkElement)
		fireEvent.mouseUp(linkElement)
		fireEvent.mouseEnter(linkElement)
		fireEvent.mouseLeave(linkElement)
		fireEvent.click(linkElement)

		expect(linkElement).toBeInTheDocument()
	})

})
