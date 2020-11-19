import React from 'react'
import { render, screen } from '@testing-library/react'
import { Avatar } from '../../../src/components/elements/Avatar'
import { Patient } from '../../../src/models'

describe('Avatar', () => {

    test('render.inDocument', () => {

        const patient = {
            id: "100",
            firstName: "kenneth",
            lastName: "chuen",
            calendar: [],
            phone: "347-681-6990",
            email: "kc3334@columbia",
            dateOfBirth: "02/05/1997",
            sex: "M",
            height: 179,
            weight: 154,
            drinker: 0,
            smoker: 0,
            health: [],
            doctors: []
        } as Patient

		render(<Avatar user={patient} size={"500"} />)
		const linkElement = screen.getByTitle('kenneth chuen')
		expect(linkElement).toBeInTheDocument()
	})

})
