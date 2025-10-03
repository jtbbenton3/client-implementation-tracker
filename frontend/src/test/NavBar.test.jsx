import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import NavBar from '../Components/NavBar'
import { AuthProvider } from '../Context/AuthContext'
import * as api from '../lib/api'

// Mock the API module
vi.mock('../lib/api', () => ({
  getMe: vi.fn().mockResolvedValue(null),
  login: vi.fn(),
  signup: vi.fn(),
  logout: vi.fn(),
}))

const MockedNavBar = () => (
  <BrowserRouter>
    <AuthProvider>
      <NavBar />
    </AuthProvider>
  </BrowserRouter>
)

describe('NavBar Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders navigation bar', () => {
    render(<MockedNavBar />)
    
    expect(screen.getByText('Client Implementation Tracker')).toBeInTheDocument()
  })

  it('shows login/signup links when not authenticated', () => {
    render(<MockedNavBar />)
    
    expect(screen.getByText('Login')).toBeInTheDocument()
    expect(screen.getByText('Signup')).toBeInTheDocument()
  })

  it('shows user menu when authenticated', async () => {
    // Mock authenticated user
    vi.spyOn(api, 'getMe').mockResolvedValue({ id: 1, email: 'test@test.com', name: 'Test User' })
    
    render(<MockedNavBar />)
    
    await waitFor(() => {
      expect(screen.getByText('Projects')).toBeInTheDocument()
      expect(screen.getByText('Dashboard')).toBeInTheDocument()
      expect(screen.getByText('Logout')).toBeInTheDocument()
    })
  })

  it('handles logout', async () => {
    const mockLogout = vi.fn().mockResolvedValue({ message: 'Logged out' })
    api.logout = mockLogout
    
    // Mock authenticated user
    vi.spyOn(api, 'getMe').mockResolvedValue({ id: 1, email: 'test@test.com', name: 'Test User' })
    
    render(<MockedNavBar />)
    
    await waitFor(() => {
      expect(screen.getByText('Logout')).toBeInTheDocument()
    })
    
    fireEvent.click(screen.getByText('Logout'))
    
    await waitFor(() => {
      expect(mockLogout).toHaveBeenCalled()
    })
  })
})
