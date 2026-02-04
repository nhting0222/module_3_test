import apiClient from '@/lib/api'

describe('ApiClient', () => {
  let originalFetch
  let originalToken

  beforeEach(() => {
    // Save original state
    originalToken = apiClient.token

    // Mock fetch
    originalFetch = global.fetch
    global.fetch = jest.fn()

    // Clear localStorage
    localStorage.clear()
  })

  afterEach(() => {
    global.fetch = originalFetch
    apiClient.token = originalToken
  })

  describe('Token Management', () => {
    test('should set token', () => {
      const token = 'test-token-123'
      apiClient.setToken(token)

      expect(apiClient.token).toBe(token)
      // Verify token is stored in localStorage
      expect(localStorage.getItem('token')).toBe(token)
    })

    test('should get token from memory', () => {
      apiClient.token = 'memory-token'

      expect(apiClient.getToken()).toBe('memory-token')
    })

    test('should get token from localStorage if not in memory', () => {
      apiClient.token = null
      localStorage.setItem('token', 'stored-token')

      const token = apiClient.getToken()
      expect(token).toBe('stored-token')
      expect(apiClient.token).toBe('stored-token')
    })

    test('should clear token', () => {
      apiClient.token = 'test-token'
      localStorage.setItem('token', 'test-token')

      apiClient.clearToken()

      expect(apiClient.token).toBeNull()
      expect(localStorage.getItem('token')).toBeNull()
    })
  })

  describe('HTTP Methods', () => {
    beforeEach(() => {
      global.fetch.mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => ({ data: 'test-data' }),
      })
    })

    test('should make GET request', async () => {
      const result = await apiClient.get('/test-endpoint')

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test-endpoint',
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      )
      expect(result).toEqual({ data: 'test-data' })
    })

    test('should make GET request with query parameters', async () => {
      await apiClient.get('/test-endpoint', { page: 1, limit: 10 })

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test-endpoint?page=1&limit=10',
        expect.any(Object)
      )
    })

    test('should make POST request', async () => {
      const postData = { name: 'test', value: 123 }
      await apiClient.post('/test-endpoint', postData)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test-endpoint',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(postData),
        })
      )
    })

    test('should make PATCH request', async () => {
      const patchData = { status: 'updated' }
      await apiClient.patch('/test-endpoint', patchData)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test-endpoint',
        expect.objectContaining({
          method: 'PATCH',
          body: JSON.stringify(patchData),
        })
      )
    })

    test('should make DELETE request', async () => {
      await apiClient.delete('/test-endpoint')

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test-endpoint',
        expect.objectContaining({
          method: 'DELETE',
        })
      )
    })

    test('should include Authorization header when token exists', async () => {
      apiClient.setToken('test-token')
      await apiClient.get('/test-endpoint')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-token',
          }),
        })
      )
    })
  })

  describe('Error Handling', () => {
    test('should handle 401 Unauthorized', async () => {
      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ detail: 'Unauthorized' }),
      })

      apiClient.setToken('invalid-token')

      await expect(apiClient.get('/test-endpoint')).rejects.toThrow('Unauthorized')
      expect(apiClient.token).toBeNull()
      expect(localStorage.getItem('token')).toBeNull()
    })

    test('should handle other HTTP errors', async () => {
      global.fetch.mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Bad Request' }),
      })

      await expect(apiClient.get('/test-endpoint')).rejects.toThrow('Bad Request')
    })

    test('should handle network errors', async () => {
      global.fetch.mockRejectedValue(new Error('Network error'))

      await expect(apiClient.get('/test-endpoint')).rejects.toThrow('Network error')
    })
  })

  describe('Authentication API', () => {
    test('should login successfully', async () => {
      const mockResponse = {
        access_token: 'new-token',
        token_type: 'bearer',
      }

      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await apiClient.login('testuser', 'testpass')

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/auth/login',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        })
      )
      expect(result).toEqual(mockResponse)
      expect(apiClient.token).toBe('new-token')
    })

    test('should handle login failure', async () => {
      global.fetch.mockResolvedValue({
        ok: false,
        json: async () => ({ detail: 'Invalid credentials' }),
      })

      await expect(apiClient.login('user', 'wrong')).rejects.toThrow('Invalid credentials')
    })

    test('should logout', async () => {
      apiClient.setToken('test-token')
      await apiClient.logout()

      expect(apiClient.token).toBeNull()
      expect(localStorage.getItem('token')).toBeNull()
    })
  })

  describe('Firewall Logs API', () => {
    beforeEach(() => {
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ data: 'success' }),
      })
    })

    test('should get logs', async () => {
      await apiClient.getLogs({ page: 1 })

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs?page=1',
        expect.any(Object)
      )
    })

    test('should get single log', async () => {
      await apiClient.getLog(123)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs/123',
        expect.any(Object)
      )
    })

    test('should create log', async () => {
      const logData = { action: 'DENY', source_ip: '192.168.1.1' }
      await apiClient.createLog(logData)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(logData),
        })
      )
    })

    test('should get log count', async () => {
      await apiClient.getLogCount()

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs/count/total',
        expect.any(Object)
      )
    })
  })

  describe('Users API', () => {
    beforeEach(() => {
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ data: 'success' }),
      })
    })

    test('should get users', async () => {
      await apiClient.getUsers()

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/users',
        expect.any(Object)
      )
    })

    test('should get single user', async () => {
      await apiClient.getUser(1)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/users/1',
        expect.any(Object)
      )
    })

    test('should create user', async () => {
      const userData = { username: 'newuser', email: 'test@example.com' }
      await apiClient.createUser(userData)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/users',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(userData),
        })
      )
    })
  })

  describe('Alert Rules API', () => {
    beforeEach(() => {
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ data: 'success' }),
      })
    })

    test('should get alert rules', async () => {
      await apiClient.getAlertRules()

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/alert-rules',
        expect.any(Object)
      )
    })

    test('should get single alert rule', async () => {
      await apiClient.getAlertRule(1)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/alert-rules/1',
        expect.any(Object)
      )
    })

    test('should create alert rule', async () => {
      const ruleData = { name: 'High Traffic Alert', condition: 'traffic > 100' }
      await apiClient.createAlertRule(ruleData)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/alert-rules',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(ruleData),
        })
      )
    })

    test('should update alert rule', async () => {
      const updateData = { enabled: false }
      await apiClient.updateAlertRule(1, updateData)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/alert-rules/1',
        expect.objectContaining({
          method: 'PATCH',
          body: JSON.stringify(updateData),
        })
      )
    })
  })
})
