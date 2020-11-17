import { describe } from 'mocha'
import { expect } from 'chai'

import { Validator } from '../../src/utils'

describe('Validator', () => {

    it('badWords.valid', () => {
        expect(Validator.badWords('no bad words here')).equal(true)
    })

    it('badWords.invalid', () => {
        expect(Validator.badWords('hell')).equal(false)
    })

    it('realName.valid', () => {
        expect(Validator.realName('Bob')).equal(true)
        expect(Validator.realName('Bob Saget')).equal(true)
    })

    it('realName.invalid', () => {
        expect(Validator.realName('Gu$$iM@ne')).equal(false)
        expect(Validator.realName('7')).equal(false)
        expect(Validator.realName('hell')).equal(false)
    })

    it('text.valid', () => {
        expect(Validator.text('no bad words here')).equal(true)
    })

    it('text.invalid', () => {
        expect(Validator.text('hell')).equal(false)
    })

    it('phone.valid', () => {
        expect(Validator.phone('123-456-7890')).equal(true)
        expect(Validator.phone('')).equal(true)
    })

    it('phone.invalid', () => {
        expect(Validator.phone('11234567890')).equal(false)
        expect(Validator.phone('(123) 456-7890')).equal(false)
        expect(Validator.phone('(123)4567890')).equal(false)
    })

    it('stringDate.valid', () => {
        expect(Validator.stringDate('2020-10-04')).equal(true)
        expect(Validator.stringDate('')).equal(true)
    })

    it('stringDate.invalid', () => {
        expect(Validator.stringDate('2020-10-4')).equal(false)
        expect(Validator.stringDate('20201004')).equal(false)
        expect(Validator.stringDate('2020/10/04')).equal(false)
    })

    it('email.valid', () => {
        expect(Validator.email('my@email.com')).equal(true)
        expect(Validator.email('firstname@gmail.net')).equal(true)
    })

    it('email.invalid', () => {
        expect(Validator.email('myemail.com')).equal(false)
        expect(Validator.email('firstnamegmail.net')).equal(false)
        expect(Validator.email('first@namegmailnet')).equal(false)
    })

})
