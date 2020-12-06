// import { describe } from 'mocha'
import { expect } from 'chai'

import { Validator } from '../../src/utils'

describe('Validator', () => {

    it('badWords.valid', () => {
        expect(Validator.badWords('no bad words here')).equal(true)
    })

    it('badWords.invalid', () => {
        expect(Validator.badWords('hell')).equal(false)
    })

    it('realName.valid.full', () => {
        expect(Validator.realName('Bob Saget')).equal(true)
        expect(Validator.realName('Robert F Kennedy')).equal(true)
    })

    it('realName.valid.short', () => {
        expect(Validator.realName('Bob')).equal(true)
        expect(Validator.realName('Robert')).equal(true)
    })

    it('realName.valid.single', () => {
        expect(Validator.realName('A')).equal(true)
        expect(Validator.realName('a')).equal(true)
    })

    it('realName.valid.empty', () => {
        expect(Validator.realName('')).equal(true)
    })

    it('realName.invalid.nonAlpha', () => {
        expect(Validator.realName('Gu$$iM@ne')).equal(false)
    })

    it('realName.invalid.nonAlphaSingle', () => {
        expect(Validator.realName('7')).equal(false)
    })

    it('realName.invalid.badWord', () => {
        expect(Validator.realName('hell')).equal(false)
    })

    it('realName.invalid.spaces', () => {
        expect(Validator.realName(' ')).equal(false)
        expect(Validator.realName('  ')).equal(false)
        expect(Validator.realName('   ')).equal(false)
    })

    it('text.valid.nonempty', () => {
        expect(Validator.text('no bad words here')).equal(true)
    })

    it('text.valid.empty', () => {
        expect(Validator.text('')).equal(true)
    })

    it('text.invalid', () => {
        expect(Validator.text('hell')).equal(false)
    })

    it('phone.valid.nonempty', () => {
        expect(Validator.phone('123-456-7890')).equal(true)
        expect(Validator.phone('')).equal(true)
    })

    it('phone.valid.empty', () => {
        expect(Validator.phone('')).equal(true)
    })

    it('phone.invalid.nonempty', () => {
        expect(Validator.phone('11234567890')).equal(false)
        expect(Validator.phone('(123) 456-7890')).equal(false)
        expect(Validator.phone('(123)4567890')).equal(false)
    })

    it('phone.invalid.nonAlpha', () => {
        expect(Validator.phone('123-ABC-7890')).equal(false)
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

    it('email.invalid.noAtOrDot', () => {
        expect(Validator.email('myemail@com')).equal(false)
        expect(Validator.email('myemail.com')).equal(false)
        expect(Validator.email('myemailcom')).equal(false)
    })

    it('email.invalid.AtYDotZ', () => {
        expect(Validator.email('@email.com')).equal(false)
    })

    it('email.invalid.XAtDotZ', () => {
        expect(Validator.email('myemail@.com')).equal(false)
    })

    it('email.invalid.XAtYDot', () => {
        expect(Validator.email('myemail@email.')).equal(false)
    })

    it('email.invalid.XYDotZ', () => {
        expect(Validator.email('myemailemail.com')).equal(false)
    })

    it('email.invalid.XYZ', () => {
        expect(Validator.email('myemailemailcom')).equal(false)
    })

    it('npi.valid.nonempty', () => {
        expect(Validator.npi('1234567890')).equal(true)
    })

    it('npi.valid.empty', () => {
        expect(Validator.npi('')).equal(true)
    })

    it('npi.invalid.notAllDigits', () => {
        expect(Validator.npi('123456789a')).equal(false)
    })

    it('npi.invalid.extraCharacters', () => {
        expect(Validator.npi('1234567890a')).equal(false)
    })

    it('npi.invalid.lessThanTen', () => {
        expect(Validator.npi('123456789')).equal(false)
    })

    it('npi.invalid.greaterThanTen', () => {
        expect(Validator.npi('12345678901')).equal(false)
    })

    it('hours.valid.normal', () => {
        const HOURS = {
            sunday: { startTime: 12, endTime: 20 },
            monday: { startTime: 13, endTime: 21 },
            tuesday: { startTime: 14, endTime: 22 },
            wednesday: { startTime: 15, endTime: 23 },
            thursday: { startTime: 16, endTime: 24 },
            friday: { startTime: 17, endTime: 25 },
            saturday: { startTime: 18, endTime: 26 },
        }
        expect(Validator.hours(HOURS)).equal(true)
    })

    it('hours.valid.max', () => {
        const HOURS = {
            sunday: { startTime: 0, endTime: 1440 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: 0, endTime: 1440 },
        }
        expect(Validator.hours(HOURS)).equal(true)
    })

    it('hours.valid.equalMin', () => {
        const HOURS = {
            sunday: { startTime: 0, endTime: 0 },
            monday: { startTime: 0, endTime: 0 },
            tuesday: { startTime: 0, endTime: 0 },
            wednesday: { startTime: 0, endTime: 0 },
            thursday: { startTime: 0, endTime: 0 },
            friday: { startTime: 0, endTime: 0 },
            saturday: { startTime: 0, endTime: 0 },
        }
        expect(Validator.hours(HOURS)).equal(true)
    })

    it('hours.valid.equalMax', () => {
        const HOURS = {
            sunday: { startTime: 1440, endTime: 1440 },
            monday: { startTime: 1440, endTime: 1440 },
            tuesday: { startTime: 1440, endTime: 1440 },
            wednesday: { startTime: 1440, endTime: 1440 },
            thursday: { startTime: 1440, endTime: 1440 },
            friday: { startTime: 1440, endTime: 1440 },
            saturday: { startTime: 1440, endTime: 1440 },
        }
        expect(Validator.hours(HOURS)).equal(true)
    })

    it('hours.valid.closed', () => {
        const HOURS = {
            sunday: { startTime: 0, endTime: 1440 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: -1, endTime: -1 },
        }
        expect(Validator.hours(HOURS)).equal(true)
    })

    it('hours.invalid.startTimeLessThanZero', () => {
        const HOURS = {
            sunday: { startTime: -10, endTime: 1440 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: 0, endTime: 1440 },
        }
        expect(Validator.hours(HOURS)).equal(false)
    })

    it('hours.invalid.startTimeGreaterThanEndTime', () => {
        const HOURS = {
            sunday: { startTime: 1200, endTime: 1100 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: 0, endTime: 1440 },
        }
        expect(Validator.hours(HOURS)).equal(false)
    })

    it('hours.invalid.endTimeGreaterThan1440', () => {
        const HOURS = {
            sunday: { startTime: 0, endTime: 1450 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: 0, endTime: 1440 },
        }
        expect(Validator.hours(HOURS)).equal(false)
    })

    it('hours.invalid.closedStartTimeMismatch', () => {
        const HOURS = {
            sunday: { startTime: 0, endTime: -1 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: 0, endTime: 1440 },
        }
        expect(Validator.hours(HOURS)).equal(false)
    })

    it('hours.invalid.closedEndTimeMismatch', () => {
        const HOURS = {
            sunday: { startTime: -1, endTime: 0 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: 0, endTime: 1440 },
        }
        expect(Validator.hours(HOURS)).equal(false)
    })

})
