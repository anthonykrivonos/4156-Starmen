import React from 'react'
import { render, screen } from '@testing-library/react'
import { Counter } from '../../../src/components/form/Counter'

describe('Counter', () => {

    const counterProps = {
        label: "label",
        errorLabel: "errorLabel",
        value: 5,
        onChange: (val: number) => {},
        onFocus: (val: number) => {},
        onBlur: (val: number) => {},
        min: 0,
        max: 100,
        containerClassName: "containerClassName",
        required: true
    }

    test('render.inDocument', () => {

		render(<Counter {...counterProps}/>)
		const linkElement = screen.getByText(/\+/i)
		expect(linkElement).toBeInTheDocument()
	})

})
