import { describe } from 'mocha'
import { expect } from 'chai'

import { Validator } from '../../src/utils'

describe('Validator', () => {

    it('badWords.positive', () => {
        expect(Validator.badWords('hell')).equal(true)
    })

    it('badWords.negative', () => {
        expect(Validator.badWords('no bad words here')).equal(false)
    })

    it('realName.positive', () => {
        expect(Validator.realName('Bob Saget')).equal(true)
    })

    it('realName.negative', () => {
        expect(Validator.realName('Gu$$iM@ne')).equal(false)
        expect(Validator.realName('My Name')).equal(false)
        expect(Validator.realName('7')).equal(false)
        expect(Validator.realName('hell')).equal(false)
    })

    it('text.positive', () => {
        expect(Validator.text('hell')).equal(true)
    })

    it('text.negative', () => {
        expect(Validator.text('no bad words here')).equal(false)
    })

    it('phone.positive', () => {
        expect(Validator.phone('123-456-7890')).equal(true)
        expect(Validator.phone('')).equal(true)
    })

    it('phone.negative', () => {
        expect(Validator.phone('1234567890')).equal(false)
        expect(Validator.phone('(123) 456-7890')).equal(false)
        expect(Validator.phone('(123)4567890')).equal(false)
    })

    it('stringDate.positive', () => {
        expect(Validator.stringDate('2020-10-04')).equal(true)
        expect(Validator.stringDate('')).equal(true)
    })

    it('stringDate.negative', () => {
        expect(Validator.stringDate('2020-10-4')).equal(true)
        expect(Validator.stringDate('20201004')).equal(true)
        expect(Validator.stringDate('2020/10/04')).equal(true)
    })

    it('email.positive', () => {
        expect(Validator.email('my@email.com')).equal(true)
        expect(Validator.email('firstname@gmail.net')).equal(true)
    })

    it('email.negative', () => {
        expect(Validator.email('myemail.com')).equal(true)
        expect(Validator.email('firstnamegmail.net')).equal(true)
        expect(Validator.email('first@namegmailnet')).equal(true)
    })

})
