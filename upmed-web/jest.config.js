module.exports = {
    preset: 'ts-jest/presets/js-with-babel',
    moduleNameMapper: {
        "\\.(css|less|sass|scss)$": "<rootDir>/__mocks__/styleMock.js",
        "\\.(jpg|png|gif|ttf|eot|svg)$": "<rootDir>/__mocks__/fileMock.js",
    },
    setupFilesAfterEnv: [
        "@testing-library/jest-dom/extend-expect",
    ],
    testPathIgnorePatterns: [
        '<rootDir>/node_modules/',
        '<rootDir>/assets/',
        '<rootDir>/src/',
        '<rootDir>/tst/setupTests.spec.ts'
    ],
    collectCoverageFrom: [
        '<rootDir>/src/components/**',
        '<rootDir>/src/pages/**',
    ],
    transform: {
        '^.+\\.tsx?$': 'ts-jest',
        '\\.(css|less|scss|sass)$': 'jest-transform-css',
    },
};