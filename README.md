# Client Implementation Tracker

A full-stack web application for managing client onboarding processes. Built with Flask and React, this application helps implementation specialists, business analysts, and project managers track client projects, milestones, tasks, and status updates in a centralized, secure platform.

## Features

- User authentication with session-based security
- Project management with client tracking
- Milestone organization with target dates
- Task management with assignments and due dates
- Status updates and project communication
- Task comments for collaboration
- User ownership controls for data security

## Tech Stack

**Backend**: Flask, SQLAlchemy, Flask-Login, Flask-Migrate, Flask-CORS
**Frontend**: React, React Router, Vite
**Database**: SQLite (development)

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask db migrate -m "Initial migration"
flask db upgrade
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

**Access**: Frontend at `http://localhost:5173`, Backend at `http://localhost:5555`

## API Overview

All endpoints are namespaced under `/api/`:

**Authentication**: `/api/signup`, `/api/login`, `/api/logout`, `/api/me`
**Projects**: `/api/projects` (GET, POST), `/api/projects/{id}` (GET, PUT, DELETE)
**Milestones**: `/api/projects/{project_id}/milestones` (GET, POST), `/api/projects/{project_id}/milestones/{id}` (GET, PUT, DELETE)
**Tasks**: `/api/{project_id}/milestones/{milestone_id}/tasks` (GET, POST), `/api/{project_id}/milestones/{milestone_id}/tasks/{id}` (PATCH, DELETE)
**Comments**: `/api/tasks/{task_id}/comments` (GET, POST), `/api/tasks/{task_id}/comments/{id}` (DELETE)
**Status Updates**: `/api/projects/{project_id}/status_updates` (GET, POST), `/api/projects/{project_id}/status_updates/{id}` (GET, DELETE)

## Response Format

- Collections: `{"items": [...]}`
- Single resources: `{"<resource>": {...}}`
- Errors: `{"error": "message"}`

## Security

- Session-based authentication with Flask-Login
- User ownership verification for all data access
- Password hashing with Werkzeug
- CORS configuration for cross-origin requests
- Input validation on all endpoints

## Development

**Run Tests**: `pytest` (backend), `npm test` (frontend)
**Database Migrations**: `flask db migrate -m "message"` then `flask db upgrade`

## Environment Variables

Set `SECRET_KEY` and `DATABASE_URL` as needed for production deployment.