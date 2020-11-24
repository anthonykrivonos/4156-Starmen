import React from 'react'
import { render, screen } from '@testing-library/react'
import { Loading } from '../../../src/components/animations/Loading'


describe('Loading', () => {

    test('render.inDocument', () => {
        const LoadingProps = {
            text: "text here",
            size: "5vw",
            containerClassName: "container class name",
            className: "class name",
        }

		render(<Loading {...LoadingProps}/>)
		const linkElement = screen.getByText("text here")
		expect(linkElement).toBeInTheDocument()
    })
    
    test('render.inDocument Default size', () => {
        const LoadingProps = {
            text: "text here",
            containerClassName: "container class name",
            className: "class name",
        }

		render(<Loading {...LoadingProps}/>)
		const linkElement = screen.getByText("text here")
		expect(linkElement).toBeInTheDocument()
	})

})
