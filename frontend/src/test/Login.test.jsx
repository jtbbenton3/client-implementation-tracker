import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import Login from '../pages/Login'
import { AuthProvider } from '../Context/AuthContext'
import * as api from '../lib/api'

// Mock the API module
vi.mock('../lib/api', () => ({
  getMe: vi.fn().mockResolvedValue(null),
  login: vi.fn(),
  signup: vi.fn(),
  logout: vi.fn(),
}))

const MockedLogin = () => (
  <BrowserRouter>
    <AuthProvider>
      <Login />
    </AuthProvider>
  </BrowserRouter>
)

describe('Login Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders login form', () => {
    render(<MockedLogin />)
    
    expect(screen.getByRole('heading', { name: 'Login' })).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument()
  })

  it('handles form submission', async () => {
    const mockLogin = vi.fn().mockResolvedValue({ id: 1, email: 'test@test.com' })
    api.login = mockLogin

    render(<MockedLogin />)
    
    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'test@test.com' }
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Login' }))
    
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'test@test.com',
        password: 'password123'
      })
    })
  })

  it('shows error message on login failure', async () => {
    const mockLogin = vi.fn().mockRejectedValue(new Error('Invalid credentials'))
    api.login = mockLogin

    render(<MockedLogin />)
    
    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'test@test.com' }
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'wrongpassword' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Login' }))
    
    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument()
    })
  })
})
