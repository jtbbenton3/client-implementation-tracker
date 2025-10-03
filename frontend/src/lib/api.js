const API_BASE = "http://localhost:5555/api";

async function request(endpoint, options = {}) {
  console.log(`Making request to: ${API_BASE}${endpoint}`);
  const res = await fetch(`${API_BASE}${endpoint}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  console.log(`Response status: ${res.status}`);
  console.log(`Response headers:`, Object.fromEntries(res.headers.entries()));
  
  const data = await res.json();
  if (!res.ok) {
    console.error(`Request failed:`, data);
    throw new Error(data.error || data.message || "Request failed");
  }
  return data;
}

// AUTH
export const signup = (body) =>
  request("/signup", { method: "POST", body: JSON.stringify(body) });

export const login = (body) =>
  request("/login", { method: "POST", body: JSON.stringify(body) });

export const logout = () => request("/logout", { method: "POST" });

export const getMe = () => request("/me");

// PROJECTS
export const getProjects = () => request("/projects");
export const createProject = (body) =>
  request("/projects", { method: "POST", body: JSON.stringify(body) });
export const getProject = (id) => request(`/projects/${id}`);
export const updateProject = (id, body) =>
  request(`/projects/${id}`, { method: "PUT", body: JSON.stringify(body) });
export const deleteProject = (id) =>
  request(`/projects/${id}`, { method: "DELETE" });

// MILESTONES
export const getMilestones = (projectId) => request(`/projects/${projectId}/milestones`);
export const createMilestone = (projectId, body) =>
  request(`/projects/${projectId}/milestones`, { method: "POST", body: JSON.stringify(body) });
export const getMilestone = (projectId, milestoneId) => request(`/projects/${projectId}/milestones/${milestoneId}`);
export const updateMilestone = (projectId, milestoneId, body) =>
  request(`/projects/${projectId}/milestones/${milestoneId}`, { method: "PUT", body: JSON.stringify(body) });
export const deleteMilestone = (projectId, milestoneId) =>
  request(`/projects/${projectId}/milestones/${milestoneId}`, { method: "DELETE" });

// TASKS
export const getTasks = (projectId, milestoneId) => request(`/${projectId}/milestones/${milestoneId}/tasks`);
export const createTask = (projectId, milestoneId, body) =>
  request(`/${projectId}/milestones/${milestoneId}/tasks`, { method: "POST", body: JSON.stringify(body) });
export const updateTask = (projectId, milestoneId, taskId, body) =>
  request(`/${projectId}/milestones/${milestoneId}/tasks/${taskId}`, { method: "PATCH", body: JSON.stringify(body) });
export const deleteTask = (projectId, milestoneId, taskId) =>
  request(`/${projectId}/milestones/${milestoneId}/tasks/${taskId}`, { method: "DELETE" });

// COMMENTS
export const getComments = (taskId) => request(`/tasks/${taskId}/comments`);
export const createComment = (taskId, body) =>
  request(`/tasks/${taskId}/comments`, { method: "POST", body: JSON.stringify(body) });
export const deleteComment = (taskId, commentId) =>
  request(`/tasks/${taskId}/comments/${commentId}`, { method: "DELETE" });

// STATUS UPDATES
export const getStatusUpdates = (projectId) => request(`/projects/${projectId}/status_updates`);
export const createStatusUpdate = (projectId, body) =>
  request(`/projects/${projectId}/status_updates`, { method: "POST", body: JSON.stringify(body) });
export const getStatusUpdate = (projectId, statusUpdateId) => request(`/projects/${projectId}/status_updates/${statusUpdateId}`);
export const deleteStatusUpdate = (projectId, statusUpdateId) =>
  request(`/projects/${projectId}/status_updates/${statusUpdateId}`, { method: "DELETE" });