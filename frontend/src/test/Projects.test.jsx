import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Projects from '../pages/Projects'
import { AuthProvider } from '../Context/AuthContext'
import * as api from '../lib/api'

// Mock the API module
vi.mock('../lib/api', () => ({
  getMe: vi.fn().mockResolvedValue(null),
  login: vi.fn(),
  signup: vi.fn(),
  logout: vi.fn(),
  getProjects: vi.fn(),
  createProject: vi.fn(),
}))

const MockedProjects = () => (
  <BrowserRouter>
    <AuthProvider>
      <Projects />
    </AuthProvider>
  </BrowserRouter>
)

describe('Projects Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders projects page', () => {
    api.getProjects.mockResolvedValue({ items: [] })
    
    render(<MockedProjects />)
    
    expect(screen.getByText('Projects')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Project Title')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Client Name')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Create Project' })).toBeInTheDocument()
  })

  it('displays projects list', async () => {
    const mockProjects = [
      { id: 1, title: 'Test Project 1', client_name: 'Client 1' },
      { id: 2, title: 'Test Project 2', client_name: 'Client 2' }
    ]
    api.getProjects.mockResolvedValue({ items: mockProjects })
    
    render(<MockedProjects />)
    
    await waitFor(() => {
      expect(screen.getByText('Test Project 1')).toBeInTheDocument()
      expect(screen.getByText('Test Project 2')).toBeInTheDocument()
    })
  })

  it('creates a new project', async () => {
    api.getProjects.mockResolvedValue({ items: [] })
    const mockCreateProject = vi.fn().mockResolvedValue({ project: { id: 1, title: 'New Project', client_name: 'New Client' } })
    api.createProject = mockCreateProject
    
    render(<MockedProjects />)
    
    fireEvent.change(screen.getByPlaceholderText('Project Title'), {
      target: { value: 'New Project' }
    })
    fireEvent.change(screen.getByPlaceholderText('Client Name'), {
      target: { value: 'New Client' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Create Project' }))
    
    await waitFor(() => {
      expect(mockCreateProject).toHaveBeenCalledWith({
        title: 'New Project',
        client_name: 'New Client'
      })
    })
  })

  it('shows error message on project creation failure', async () => {
    api.getProjects.mockResolvedValue({ items: [] })
    const mockCreateProject = vi.fn().mockRejectedValue(new Error('Failed to create project'))
    api.createProject = mockCreateProject
    
    render(<MockedProjects />)
    
    fireEvent.change(screen.getByPlaceholderText('Project Title'), {
      target: { value: 'New Project' }
    })
    fireEvent.change(screen.getByPlaceholderText('Client Name'), {
      target: { value: 'New Client' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Create Project' }))
    
    await waitFor(() => {
      expect(screen.getByText('Failed to create project')).toBeInTheDocument()
    })
  })
})
