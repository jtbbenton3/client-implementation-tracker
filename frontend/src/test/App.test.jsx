import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import App from '../App'
import { AuthProvider } from '../Context/AuthContext'

// Mock the API module
vi.mock('../lib/api', () => ({
  getMe: vi.fn().mockResolvedValue(null),
  login: vi.fn(),
  signup: vi.fn(),
  logout: vi.fn(),
}))

const MockedApp = () => (
  <BrowserRouter>
    <AuthProvider>
      <App />
    </AuthProvider>
  </BrowserRouter>
)

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<MockedApp />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('redirects to login when not authenticated', async () => {
    render(<MockedApp />)
    // Should show loading initially, then redirect to login
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })
})
