import pytest
from app import create_app, db

@pytest.fixture(scope="function")
def test_client():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "testkey"
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_signup_and_login(test_client):
    # test signup
    res = test_client.post("/api/signup", json={
        "name": "Test User",
        "email": "testuser@test.com",
        "password": "password123"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["email"] == "testuser@test.com"
    assert "id" in data

    # test login
    res = test_client.post("/api/login", json={
        "email": "testuser@test.com",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["email"] == "testuser@test.com"

    # check current user
    res = test_client.get("/api/me")
    assert res.status_code == 200
    user_data = res.get_json()
    assert user_data["email"] == "testuser@test.com"

    # test logout
    res = test_client.post("/api/logout")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Logged out"


def test_create_and_get_project(test_client):
    # create user first
    test_client.post("/api/signup", json={
        "name": "Test User",
        "email": "testuser@test.com",
        "password": "password123"
    })

    # create project
    res = test_client.post("/api/projects", json={
        "title": "Test Project",
        "client_name": "Test Client"
    })
    assert res.status_code == 201
    project_data = res.get_json()["project"]
    assert project_data["title"] == "Test Project"

    # get projects list
    res = test_client.get("/api/projects")
    assert res.status_code == 200
    projects = res.get_json()["items"]
    assert len(projects) == 1
    assert projects[0]["title"] == "Test Project"

    # get one project
    project_id = projects[0]["id"]
    res = test_client.get(f"/api/projects/{project_id}")
    assert res.status_code == 200
    assert res.get_json()["project"]["title"] == "Test Project"


def test_milestones_flow(test_client):
    # create user and project first
    test_client.post("/api/signup", json={
        "name": "Test User",
        "email": "testuser@test.com",
        "password": "password123"
    })
    
    project_res = test_client.post("/api/projects", json={
        "title": "Test Project",
        "client_name": "Test Client"
    })
    project_id = project_res.get_json()["project"]["id"]

    # add milestone
    res = test_client.post(f"/api/projects/{project_id}/milestones", json={
        "name": "Phase 1",
        "target_date": "2025-12-01"
    })
    assert res.status_code == 201
    data = res.get_json()["milestone"]
    assert data["name"] == "Phase 1"

    # get milestones
    res = test_client.get(f"/api/projects/{project_id}/milestones")
    assert res.status_code == 200
    milestones = res.get_json()["items"]
    assert len(milestones) > 0


def test_tasks_flow(test_client):
    # create user, project, and milestone first
    test_client.post("/api/signup", json={
        "name": "Test User",
        "email": "testuser@test.com",
        "password": "password123"
    })
    
    project_res = test_client.post("/api/projects", json={
        "title": "Test Project",
        "client_name": "Test Client"
    })
    project_id = project_res.get_json()["project"]["id"]
    
    milestone_res = test_client.post(f"/api/projects/{project_id}/milestones", json={
        "name": "Phase 1",
        "target_date": "2025-12-01"
    })
    milestone_id = milestone_res.get_json()["milestone"]["id"]

    # add task
    res = test_client.post(f"/api/{project_id}/milestones/{milestone_id}/tasks", json={
        "title": "Do backend setup",
        "assignee": "dev1",
        "due_date": "2025-12-15"
    })
    assert res.status_code == 201
    task_data = res.get_json()["task"]
    assert task_data["title"] == "Do backend setup"

    # get tasks
    res = test_client.get(f"/api/{project_id}/milestones/{milestone_id}/tasks")
    assert res.status_code == 200
    tasks = res.get_json()["items"]
    assert len(tasks) > 0

    # update task
    task_id = task_data["id"]
    res = test_client.patch(f"/api/{project_id}/milestones/{milestone_id}/tasks/{task_id}", json={
        "title": "Do frontend setup"
    })
    assert res.status_code == 200
    assert res.get_json()["task"]["title"] == "Do frontend setup"

    # delete task
    res = test_client.delete(f"/api/{project_id}/milestones/{milestone_id}/tasks/{task_id}")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Task deleted"


def test_comments_flow(test_client):
    # create user, project, milestone, and task first
    test_client.post("/api/signup", json={
        "name": "Test User",
        "email": "testuser@test.com",
        "password": "password123"
    })
    
    project_res = test_client.post("/api/projects", json={
        "title": "Test Project",
        "client_name": "Test Client"
    })
    project_id = project_res.get_json()["project"]["id"]
    
    milestone_res = test_client.post(f"/api/projects/{project_id}/milestones", json={
        "name": "Phase 1",
        "target_date": "2025-12-01"
    })
    milestone_id = milestone_res.get_json()["milestone"]["id"]
    
    task_res = test_client.post(f"/api/{project_id}/milestones/{milestone_id}/tasks", json={
        "title": "Task with comments",
        "assignee": "dev2",
        "due_date": "2025-12-20"
    })
    task_id = task_res.get_json()["task"]["id"]

    # add comment
    res = test_client.post(f"/api/tasks/{task_id}/comments", json={"body": "Looks good"})
    assert res.status_code == 201
    comment_data = res.get_json()["comment"]
    assert comment_data["body"] == "Looks good"

    # get comments
    res = test_client.get(f"/api/tasks/{task_id}/comments")
    assert res.status_code == 200
    comments = res.get_json()["items"]
    assert len(comments) > 0

    # delete comment
    comment_id = comment_data["id"]
    res = test_client.delete(f"/api/tasks/{task_id}/comments/{comment_id}")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Comment deleted"