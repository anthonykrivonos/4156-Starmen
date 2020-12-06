// import { describe } from 'mocha'
import { expect } from 'chai'

import { Formatter } from '../../src/utils'

describe('Formatter', () => {

    it('phone.formatted', () => {
        expect(Formatter.phone('1234567890')).equal('123-456-7890')
    })

    it('phone.unformatted', () => {
        expect(Formatter.phone('')).equal('')
        expect(Formatter.phone('123456789')).equal('123456789')
    })

    it('stringDate', () => {
        expect(Formatter.stringDate(new Date(2020, 10 - 1, 15))).equal('2020-10-15')
        expect(Formatter.stringDate(new Date(2020, 8 - 1, 8))).equal('2020-08-08')
    })

    it('npi', () => {
        expect(Formatter.npi('12341aa234')).equal('12341234')
        expect(Formatter.npi('aa12341234')).equal('12341234')
        expect(Formatter.npi('12341234aa')).equal('12341234')
        expect(Formatter.npi('aa')).equal('')
        expect(Formatter.npi('')).equal('')
    })

})
