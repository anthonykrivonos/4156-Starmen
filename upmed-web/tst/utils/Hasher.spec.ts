// import { describe } from 'mocha'
import { expect } from 'chai'

import { Hasher } from '../../src/utils'

describe('Hasher', () => {

    it('encode', () => {
        expect(Hasher.encode('12345')).equal('IjEyMzQ1Ig==')
        expect(Hasher.encode({ key: 'value' })).equal('eyJrZXkiOiJ2YWx1ZSJ9')
    })

    it('decode.success', () => {
        expect(Hasher.decode('IjEyMzQ1Ig==')).equal('12345')
    })

    it('decode.failure', () => {
        expect(Hasher.decode(12341234 as any)).equal(null)
    })

})
