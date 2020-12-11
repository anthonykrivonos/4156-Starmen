import { Hours } from '../models'

// Unset value of hours
export const INITIAL_HOURS = {
	sunday: { startTime: 0, endTime: 1440 },
	monday: { startTime: 0, endTime: 1440 },
	tuesday: { startTime: 0, endTime: 1440 },
	wednesday: { startTime: 0, endTime: 1440 },
	thursday: { startTime: 0, endTime: 1440 },
	friday: { startTime: 0, endTime: 1440 },
	saturday: { startTime: 0, endTime: 1440 },
} as Hours

// All day hours
export const HOURS_ALL_DAY = {
	sunday: { startTime: 0, endTime: 1410 },
	monday: { startTime: 0, endTime: 1410 },
	tuesday: { startTime: 0, endTime: 1410 },
	wednesday: { startTime: 0, endTime: 1410 },
	thursday: { startTime: 0, endTime: 1410 },
	friday: { startTime: 0, endTime: 1410 },
	saturday: { startTime: 0, endTime: 1410 },
} as Hours

// List of potential specialties
export const SPECIALTIES = [
	'Anesthesiology',
	'Dentistry',
	'Dermatology',
	'Diagnostic Radiology',
	'Emergency Medicine',
	'Family Medicine',
	'Gynecology',
	'Immunology',
	'Internal Medicine',
	'Medical Genetics',
	'Neurology',
	'Nuclear Medicine',
	'Obstetrics',
	'Ophthalmology',
	'Pathology',
	'Pediatrics',
	'Rehabilitation',
	'Preventive Medicine',
	'Psychiatry',
	'Radiation Oncology',
	'Surgery',
	'Urology',
]

export const STATUS = ['ACTIVE', 'NEVER', 'PAST', 'REMISSION', 'CURED']
