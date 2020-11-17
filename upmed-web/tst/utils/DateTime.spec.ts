import { describe } from 'mocha'
import { expect } from 'chai'

import { DateTime } from '../../src/utils'
import { Hours } from '../../src/models'

describe('DateTime', () => {

    it('safeParseHours.success', () => {
        const HOURS_BAD = {
            sunday: { startTime: '0', endTime: '1440' },
            monday: { startTime: '0', endTime: '1440' },
            tuesday: { startTime: '0', endTime: '1440' },
            wednesday: { startTime: '0', endTime: '1440' },
            thursday: { startTime: '0', endTime: '1440' },
            friday: { startTime: '0', endTime: '1440' },
            saturday: { startTime: '-1', endTime: '-1' },
        }
        const HOURS_GOOD = {
            sunday: { startTime: 0, endTime: 1440 },
            monday: { startTime: 0, endTime: 1440 },
            tuesday: { startTime: 0, endTime: 1440 },
            wednesday: { startTime: 0, endTime: 1440 },
            thursday: { startTime: 0, endTime: 1440 },
            friday: { startTime: 0, endTime: 1440 },
            saturday: { startTime: -1, endTime: -1 },
        }

        expect(JSON.stringify(DateTime.safeParseHours(HOURS_BAD as any as Hours))).equal(JSON.stringify(HOURS_GOOD))
    })

    it('hoursOffset.success', () => {
        expect(DateTime.hoursOffset(new Date())).equal(DateTime.hoursOffset())
    })

    it('getMinutes.success', () => {
        expect(DateTime.getMinutes(new Date(2020, 12, 10, 6))).equal(360)
    })

    it('minutesToHHMMAA.success', () => {
        expect(DateTime.minutesToHHMMAA(60)).equal('01:00 AM')
        expect(DateTime.minutesToHHMMAA(780)).equal('01:00 PM')
        expect(DateTime.minutesToHHMMAA(90)).equal('01:30 AM')
    })

    it('hhmmAAToMinutes.success', () => {
        expect(DateTime.hhmmAAToMinutes('01:00 AM')).equal(60)
        expect(DateTime.hhmmAAToMinutes('01:00 PM')).equal(780)
        expect(DateTime.hhmmAAToMinutes('01:30 AM')).equal(90)
    })

    it('minutesToHHMM.success', () => {
        expect(DateTime.minutesToHHMM(60)).equal('01:00')
        expect(DateTime.minutesToHHMM(780)).equal('13:00')
        expect(DateTime.minutesToHHMM(90)).equal('01:30')
    })

    it('hhmmToMinutes.success', () => {
        expect(DateTime.hhmmToMinutes('01:00')).equal(60)
        expect(DateTime.hhmmToMinutes('13:00')).equal(780)
        expect(DateTime.hhmmToMinutes('01:30')).equal(90)
    })

    it('dateFromStringDate.success', () => {
        // October 15, 2020
        const dt = new Date()
        dt.setFullYear(2020, 10 - 1 /* index version */, 15)
        expect(DateTime.dateFromStringDate('2020-10-15').toString()).equal(dt.toString())
    })

    it('getModifiedDate.success', () => {
        // October 15, 2020
        const dt1 = new Date()
        dt1.setFullYear(2020, 10 - 1 /* index version */, 15)
        const dt2 = new Date()
        dt2.setFullYear(2019, 9 - 1 /* index version */, 14)
        expect(DateTime.getModifiedDate(dt1, -1, -1, -1).toString()).equal(dt2.toString())
    })

    it('prettyDate.success', () => {
        // October 15, 2020
        const dt = new Date()
        dt.setFullYear(2020, 10 - 1 /* index version */, 15)
        expect(DateTime.prettyDate(dt)).equal('Thursday, October 15 2020')
    })

})
