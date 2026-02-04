import { metadata } from '@/app/layout'

describe('RootLayout', () => {
  test('should have correct metadata title', () => {
    expect(metadata.title).toBe('Firewall Log Monitor')
  })

  test('should have correct metadata description', () => {
    expect(metadata.description).toBe('방화벽 로그 모니터링 웹 어드민')
  })

  test('metadata should be an object', () => {
    expect(typeof metadata).toBe('object')
  })

  test('metadata should have required fields', () => {
    expect(metadata).toHaveProperty('title')
    expect(metadata).toHaveProperty('description')
  })
})
