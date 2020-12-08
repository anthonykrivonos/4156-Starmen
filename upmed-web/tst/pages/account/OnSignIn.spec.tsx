import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { OnSignIn } from '../../../src/pages/account/OnSignIn'
import { Hasher, Validator, Objects, Client } from '../../../src/utils'

jest.mock('react-router-dom', () => ({
    useLocation: jest.fn().mockReturnValue({
      pathname: '/another-route',
	}),
	useHistory: () => ({
		push: jest.fn()
    })
}))

jest.mock('../../../src/utils/Client')
jest.mock('../../../src/utils/Users')

Client.Patient.editProfilePicture = jest.fn().mockResolvedValue({ id: "100", token: "token"})
Client.HCP.editProfilePicture = jest.fn().mockResolvedValue({ id: "100", token: "token"})
Client.Patient.signUp = jest.fn().mockResolvedValue('token')
Client.HCP.signUp = jest.fn().mockResolvedValue('token')

Objects.isNullish = jest.fn().mockReturnValue(false)

Validator.realName = jest.fn().mockReturnValue(true)
Validator.email = jest.fn().mockReturnValue(true)
Validator.phone = jest.fn().mockReturnValue(true)
Validator.stringDate = jest.fn().mockReturnValue(true)
Validator.text = jest.fn().mockReturnValue(true)

describe('OnSignIn', () => {

    // test('render.inDocument Doctor', () => {
    //     Hasher.decode = jest.fn().mockReturnValue({
    //         id: "100",
    //         accessToken: "token",
    //         email: "email",
    //         firstName: "first",
    //         lastName: "last",
    //         profilePicture: "profile pic",
    //         isPatient: false,
    //         expiryTime: 0,
    //     })

	// 	render(<OnSignIn />)
    //     const linkElement = screen.getByText('Professional Info')
        
    //     const profilePic = screen.getAllByAltText('first last')[0]
    //     const firstNameInput = screen.getByDisplayValue('first')
    //     const lastNameInput = screen.getByDisplayValue('last')
    //     const emailInput = screen.getByDisplayValue('email')
    //     const phoneInput = screen.getAllByDisplayValue('')[0]
    //     const business = screen.getAllByDisplayValue('')[1]
    //     const specialty = screen.getAllByRole('combobox')[0]
    //     const hours = screen.getAllByDisplayValue('Sunday')[0]
    //     const createAccount = screen.getByText('Create Account')

    //     fireEvent.error(profilePic)
    //     fireEvent.change(firstNameInput, { target: { value: 'Kenneth' } })
    //     fireEvent.change(lastNameInput, { target: { value: 'Chuen' } })
    //     fireEvent.change(emailInput, { target: { value: 'kc@gmail.com' } })
    //     fireEvent.change(phoneInput, { target: { value: '347-619-4852' } })
    //     fireEvent.change(business, { target: { value: 'my own business' } })
    //     fireEvent.change(specialty, { target: { value: 10 } })
    //     fireEvent.click(specialty)
    //     fireEvent.change(hours, { target: { value: '23' } })
    //     fireEvent.click(hours)

    //     fireEvent.click(createAccount)

	// 	expect(linkElement).toBeInTheDocument()
    // })


    test('render.inDocument Patient', () => {
        jest.mock('react-router-dom', () => ({
            useState: jest
                .fn()
                .mockReturnValueOnce('/another-route')
                .mockReturnValueOnce(false)
                .mockReturnValueOnce('')
                .mockReturnValueOnce(false)
                .mockReturnValueOnce("userToken")
                .mockReturnValueOnce("profile pic")
                .mockReturnValueOnce(true)
                .mockReturnValueOnce("id")
                .mockReturnValueOnce("email"),
        }))
        
        Hasher.decode = jest.fn().mockReturnValue({
            id: "id",
            accessToken: "token",
            email: "email",
            firstName: "first",
            lastName: "last",
            profilePicture: "profile pic",
            isPatient: true,
            expiryTime: 0,
        })

		render(<OnSignIn />)
        
        const profilePic = screen.getAllByAltText('first last')[0]
        const firstNameInput = screen.getByDisplayValue('first')
        const lastNameInput = screen.getByDisplayValue('last')
        const emailInput = screen.getByDisplayValue('email')
        const phoneInput = screen.getAllByDisplayValue('')[0]
        const dobInput = screen.getAllByDisplayValue('')[1]
        const male = screen.getAllByDisplayValue(/radio.*/i)[0]
        const female = screen.getAllByDisplayValue(/radio.*/i)[1]
        const drinkerYes = screen.getAllByDisplayValue(/radio.*/i)[2]
        const drinkerPast = screen.getAllByDisplayValue(/radio.*/i)[3]
        const drinkerNever = screen.getAllByDisplayValue(/radio.*/i)[4]
        const smokerYes = screen.getAllByDisplayValue(/radio.*/i)[5]
        const smokerPast = screen.getAllByDisplayValue(/radio.*/i)[6]
        const smokerNever = screen.getAllByDisplayValue(/radio.*/i)[7]
        
        fireEvent.error(profilePic)
        fireEvent.change(firstNameInput, { target: { value: 'Kenneth' } })
        fireEvent.change(lastNameInput, { target: { value: 'Chuen' } })
        fireEvent.change(emailInput, { target: { value: 'kc@gmail.com' } })
        fireEvent.change(phoneInput, { target: { value: '347-619-4852' } })
        fireEvent.change(dobInput, { target: { value: '1988/12/31' } })
        fireEvent.click(male)
        fireEvent.click(female)
        fireEvent.click(drinkerYes)
        fireEvent.click(drinkerPast)
        fireEvent.click(drinkerNever)
        fireEvent.click(smokerYes)
        fireEvent.click(smokerPast)
        fireEvent.click(smokerNever)

        const buttons = screen.getAllByRole('button')
        for (const button of buttons) {
            fireEvent.click(button)
        }

        const create = screen.getByRole('button', { name: "Create Account" } )
        fireEvent.click(create)
        fireEvent.click(create)

        const linkElement = screen.getByText('Basic Information')
		expect(linkElement).toBeInTheDocument()
    })
    
    // test('expired', () => {
    //     Hasher.decode = jest.fn().mockReturnValue(null)

    // 	render(<OnSignIn />)
    
    //     const linkElement = screen.getByText('Basic Information')
	// 	expect(linkElement).toBeInTheDocument()
    // })

})
