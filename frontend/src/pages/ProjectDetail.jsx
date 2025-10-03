import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { 
  getProject, 
  createStatusUpdate, 
  getStatusUpdates, 
  getMilestones, 
  createMilestone,
  getTasks,
  createTask,
  updateTask
} from "../lib/api";

export default function ProjectDetail() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [updates, setUpdates] = useState([]);
  const [milestones, setMilestones] = useState([]);
  const [tasks, setTasks] = useState({});
  const [content, setContent] = useState("");
  const [milestoneName, setMilestoneName] = useState("");
  const [milestoneDate, setMilestoneDate] = useState("");
  const [taskTitle, setTaskTitle] = useState("");
  const [taskAssignee, setTaskAssignee] = useState("");
  const [taskDueDate, setTaskDueDate] = useState("");
  const [selectedMilestone, setSelectedMilestone] = useState("");

  const fetchProject = async () => {
    const res = await getProject(id);
    setProject(res.project);
  };

  const fetchUpdates = async () => {
    const res = await getStatusUpdates(id);
    setUpdates(res.items);
  };

  const fetchMilestones = async () => {
    const res = await getMilestones(id);
    setMilestones(res.items);
  };

  const fetchTasks = async (milestoneId) => {
    const res = await getTasks(id, milestoneId);
    setTasks(prev => ({ ...prev, [milestoneId]: res.items }));
  };

  useEffect(() => {
    fetchProject();
    fetchUpdates();
    fetchMilestones();
  }, [id]);

  const handleStatusUpdate = async (e) => {
    e.preventDefault();
    await createStatusUpdate(id, { content });
    setContent("");
    fetchUpdates();
  };

  const handleMilestoneCreate = async (e) => {
    e.preventDefault();
    await createMilestone(id, { 
      name: milestoneName, 
      target_date: milestoneDate || null 
    });
    setMilestoneName("");
    setMilestoneDate("");
    fetchMilestones();
  };

  const handleTaskCreate = async (e) => {
    e.preventDefault();
    if (!selectedMilestone) return;
    await createTask(id, selectedMilestone, {
      title: taskTitle,
      assignee: taskAssignee,
      due_date: taskDueDate || null
    });
    setTaskTitle("");
    setTaskAssignee("");
    setTaskDueDate("");
    fetchTasks(selectedMilestone);
  };

  const handleTaskToggle = async (taskId, milestoneId, completed) => {
    await updateTask(id, milestoneId, taskId, { completed });
    fetchTasks(milestoneId);
  };

  if (!project) return <p>Loading...</p>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h2>{project.title}</h2>
          <p>Client: {project.client_name}</p>
        </div>
        <div>
          <a href={`/share/${id}`} target="_blank" rel="noopener noreferrer" 
             style={{ 
               padding: '0.5rem 1rem', 
               background: '#17a2b8', 
               color: 'white', 
               textDecoration: 'none', 
               borderRadius: '4px',
               fontSize: '0.9rem'
             }}>
            📤 Share View
          </a>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        {/* Milestones Section */}
        <section>
          <h3>Milestones</h3>
          
          <form onSubmit={handleMilestoneCreate} className="card" style={{ marginBottom: '1rem' }}>
            <input
              type="text"
              placeholder="Milestone name"
              value={milestoneName}
              onChange={(e) => setMilestoneName(e.target.value)}
              required
            />
            <input
              type="date"
              placeholder="Target date"
              value={milestoneDate}
              onChange={(e) => setMilestoneDate(e.target.value)}
            />
            <button type="submit">Add Milestone</button>
          </form>

          {milestones.map((milestone) => (
            <div key={milestone.id} className="card" style={{ marginBottom: '1rem' }}>
              <h4>{milestone.name}</h4>
              {milestone.target_date && (
                <p style={{ color: '#666', fontSize: '0.9rem' }}>
                  Target: {new Date(milestone.target_date).toLocaleDateString()}
                </p>
              )}
              
              {/* Tasks for this milestone */}
              <div style={{ marginTop: '1rem' }}>
                <h5>Tasks</h5>
                {tasks[milestone.id]?.map((task) => (
                  <div key={task.id} style={{ 
                    padding: '0.5rem', 
                    margin: '0.25rem 0', 
                    background: task.completed ? '#d4edda' : '#f8f9fa',
                    border: '1px solid #dee2e6',
                    borderRadius: '4px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={(e) => handleTaskToggle(task.id, milestone.id, e.target.checked)}
                    />
                    <span style={{ flex: 1, textDecoration: task.completed ? 'line-through' : 'none' }}>
                      {task.title}
                    </span>
                    {task.assignee && <small style={{ color: '#666' }}>{task.assignee}</small>}
                  </div>
                )) || (
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>No tasks yet</p>
                )}
              </div>
            </div>
          ))}
        </section>

        {/* Status Updates Section */}
        <section>
          <h3>Status Updates</h3>
          
          <form onSubmit={handleStatusUpdate} className="card" style={{ marginBottom: '1rem' }}>
            <textarea
              placeholder="Write a status update..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows="3"
            />
            <button type="submit">Post Update</button>
          </form>

          {updates.length === 0 && <p>No updates yet.</p>}
          {updates.map((u) => (
            <div key={u.id} className="card" style={{ marginBottom: '0.5rem' }}>
              <p>{u.content}</p>
              <small style={{ color: '#666' }}>
                {new Date(u.created_at).toLocaleString()}
              </small>
            </div>
          ))}
        </section>
      </div>

      {/* Add Task Form */}
      {milestones.length > 0 && (
        <section style={{ marginTop: '2rem' }}>
          <h3>Add Task</h3>
          <form onSubmit={handleTaskCreate} className="card">
            <select
              value={selectedMilestone}
              onChange={(e) => setSelectedMilestone(e.target.value)}
              required
              style={{ marginBottom: '0.5rem' }}
            >
              <option value="">Select a milestone</option>
              {milestones.map((milestone) => (
                <option key={milestone.id} value={milestone.id}>
                  {milestone.name}
                </option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Task title"
              value={taskTitle}
              onChange={(e) => setTaskTitle(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Assignee"
              value={taskAssignee}
              onChange={(e) => setTaskAssignee(e.target.value)}
            />
            <input
              type="date"
              placeholder="Due date"
              value={taskDueDate}
              onChange={(e) => setTaskDueDate(e.target.value)}
            />
            <button type="submit">Add Task</button>
          </form>
        </section>
      )}
    </div>
  );
}