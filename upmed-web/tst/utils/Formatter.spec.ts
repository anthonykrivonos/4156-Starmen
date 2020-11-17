import { describe } from 'mocha'
import { expect } from 'chai'

import { Formatter } from '../../src/utils'

describe('Formatter', () => {

    it('phone.success', () => {
        expect(Formatter.phone('1234567890')).equal('123-456-7890')
        expect(Formatter.phone('123456789')).equal('123456789')
    })

    it('stringDate.success', () => {
        expect(Formatter.stringDate(new Date(2020, 10 - 1, 15))).equal('2020-10-15')
        expect(Formatter.stringDate(new Date(2020, 8 - 1, 8))).equal('2020-08-08')
    })

})
