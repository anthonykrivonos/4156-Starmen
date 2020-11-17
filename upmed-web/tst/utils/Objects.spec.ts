import { describe } from 'mocha'
import { expect } from 'chai'

import { Objects } from '../../src/utils'

describe('Objects', () => {

    it('isNullish.postive', () => {
        expect(Objects.isNullish(null)).equal(true)
        expect(Objects.isNullish(undefined)).equal(true)
    })

    it('isNullish.negative', () => {
        expect(Objects.isNullish(5)).equal(false)
        expect(Objects.isNullish({})).equal(false)
        expect(Objects.isNullish([])).equal(false)
    })

    it('isArray.postive', () => {
        expect(Objects.isArray([])).equal(true)
        expect(Objects.isArray([ 5, 10 ])).equal(true)
    })

    it('isArray.negative', () => {
        expect(Objects.isArray(5)).equal(false)
        expect(Objects.isArray('[4]')).equal(false)
        expect(Objects.isArray({})).equal(false)
        expect(Objects.isArray(null)).equal(false)
        expect(Objects.isArray(undefined)).equal(false)
    })

    it('isString.postive', () => {
        expect(Objects.isString('')).equal(true)
        expect(Objects.isString(' ')).equal(true)
        expect(Objects.isString('test')).equal(true)
    })

    it('isString.negative', () => {
        expect(Objects.isString(5)).equal(false)
        expect(Objects.isString({})).equal(false)
        expect(Objects.isString([])).equal(false)
        expect(Objects.isString(null)).equal(false)
        expect(Objects.isString(undefined)).equal(false)
    })

    it('isNumber.postive', () => {
        expect(Objects.isNumber(34)).equal(true)
        expect(Objects.isNumber(0)).equal(true)
        expect(Objects.isNumber(-1)).equal(true)
        expect(Objects.isNumber(32.5123)).equal(true)
    })

    it('isNumber.negative', () => {
        expect(Objects.isNumber(NaN)).equal(false)
        expect(Objects.isNumber({})).equal(false)
        expect(Objects.isNumber([])).equal(false)
        expect(Objects.isNumber('five')).equal(false)
        expect(Objects.isNumber(null)).equal(false)
        expect(Objects.isNumber(undefined)).equal(false)
    })

    it('objToArray.success', () => {
        expect(JSON.stringify(Objects.objToArray({ 1: 1, 2: 2, 3: 3 }).sort((a, b) => a - b))).equal(JSON.stringify([1, 2, 3]))
    })

    it('copy.nullish', () => {
        expect(Objects.copy(JSON.stringify({}))).equal(JSON.stringify({}))
    })

    it('copy.nonObject', () => {
        expect(Objects.copy(5)).equal(5)
        expect(Objects.copy('six')).equal('six')
        expect(Objects.copy(true)).equal(true)
    })

    it('copy.shallow', () => {
        const obj = {
            1: 1,
            2: {
                '2.a': 2,
                '2.b': {
                    '2.a': 2,
                    '2.b': {
                        '2.a': 2,
                        '2.b': 2,
                    },
                },
            }
        }
        expect(JSON.stringify(Objects.copy(obj, [], true))).equal(JSON.stringify(obj))
    })

    it('copy.nonShallow', () => {
        const obj = {
            1: 1,
            2: {
                '2.a': 2,
                '2.b': {
                    '2.a': 2,
                    '2.b': {
                        '2.a': 2,
                        '2.b': 2,
                    },
                },
            }
        }
        expect(JSON.stringify(Objects.copy(obj, [], false))).equal(JSON.stringify(obj))
    })

    it('copy.withoutProperty', () => {
        const obj = {
            1: 1,
            2: {
                '2.a': 2,
                '2.b': 2,
            }
        }
        expect(JSON.stringify(Objects.copy(obj, ["2"], false))).not.equal(JSON.stringify(obj))
    })

})
