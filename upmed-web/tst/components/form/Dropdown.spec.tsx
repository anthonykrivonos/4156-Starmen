import React from 'react'
import { render, screen } from '@testing-library/react'
import { Dropdown } from '../../../src/components/form/Dropdown'

describe('Dropdown', () => {

    const dropdownProps = {
        label: "dropdown label",
        required: true,
        onChange: (option: any, index: number) => {},
        options: [],
        displayOptions: [],
        selectedIdx: 1,
        className: "dropdown class name",
        containerClassName: "dropdown container name"
    }

    test('render.inDocument', () => {

		render(<Dropdown {...dropdownProps}/>)
		const linkElement = screen.getByText(/dropdown label/i)
		expect(linkElement).toBeInTheDocument()
	})

})
