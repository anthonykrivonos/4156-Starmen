import { describe } from 'mocha'
import { expect } from 'chai'

import { URL } from '../../src/utils'

describe('URL', () => {

    it('getFromQuery.present', () => {
        expect(URL.getFromQuery("http://www.mywebsite.com?key=value", "key")).equal("value")
    })

    it('getFromQuery.absent', () => {
        expect(URL.getFromQuery("http://www.mywebsite.com?key1=value", "key")).equal(null)
        expect(URL.getFromQuery("http://www.mywebsite.com", "key")).equal(null)
        expect(URL.getFromQuery("http://www.mywebsite.com/", "key")).equal(null)
    })

})
