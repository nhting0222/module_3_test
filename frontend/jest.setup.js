import '@testing-library/jest-dom'

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
})

// Mock localStorage
const localStorageMock = (function() {
  let store = {}
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString()
    }),
    removeItem: jest.fn((key) => {
      delete store[key]
    }),
    clear: jest.fn(() => {
      store = {}
    }),
    get length() {
      return Object.keys(store).length
    },
    key: jest.fn((index) => {
      const keys = Object.keys(store)
      return keys[index] || null
    })
  }
})()
global.localStorage = localStorageMock

// Mock window.location for navigation tests
delete window.location
window.location = { href: '', assign: jest.fn(), reload: jest.fn() }
