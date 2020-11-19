import React from 'react'
import { render, screen } from '@testing-library/react'
import { RadioButtons } from '../../../src/components/form/RadioButtons'

describe('RadioButtons', () => {

    const radioButtonsProps = {
        label: "radioButtons label",
        required: true,
        onChange: (option: any, index: number) => {},
        options: [],
        displayOptions: [],
        selectedIdx: 0,
        className: "radioButtons class name",
    }

    test('render.inDocument', () => {
		render(<RadioButtons {...radioButtonsProps}/>)
		const linkElement = screen.getByText(/radioButtons label/i)
		expect(linkElement).toBeInTheDocument()
	})

})
