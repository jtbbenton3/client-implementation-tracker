import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import Signup from '../pages/Signup'
import { AuthProvider } from '../Context/AuthContext'
import * as api from '../lib/api'

// Mock the API module
vi.mock('../lib/api', () => ({
  getMe: vi.fn().mockResolvedValue(null),
  login: vi.fn(),
  signup: vi.fn(),
  logout: vi.fn(),
}))

const MockedSignup = () => (
  <BrowserRouter>
    <AuthProvider>
      <Signup />
    </AuthProvider>
  </BrowserRouter>
)

describe('Signup Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders signup form', () => {
    render(<MockedSignup />)
    
    expect(screen.getByRole('heading', { name: 'Sign Up' })).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Name')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Sign Up' })).toBeInTheDocument()
  })

  it('handles form submission', async () => {
    const mockSignup = vi.fn().mockResolvedValue({ id: 1, email: 'test@test.com' })
    api.signup = mockSignup

    render(<MockedSignup />)
    
    fireEvent.change(screen.getByPlaceholderText('Name'), {
      target: { value: 'Test User' }
    })
    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'test@test.com' }
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign Up' }))
    
    await waitFor(() => {
      expect(mockSignup).toHaveBeenCalledWith({
        name: 'Test User',
        email: 'test@test.com',
        password: 'password123'
      })
    })
  })

  it('shows error message on signup failure', async () => {
    const mockSignup = vi.fn().mockRejectedValue(new Error('User already exists'))
    api.signup = mockSignup

    render(<MockedSignup />)
    
    fireEvent.change(screen.getByPlaceholderText('Name'), {
      target: { value: 'Test User' }
    })
    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'test@test.com' }
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign Up' }))
    
    await waitFor(() => {
      expect(screen.getByText('User already exists')).toBeInTheDocument()
    })
  })
})
