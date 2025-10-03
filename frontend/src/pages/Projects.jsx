import React, { useEffect, useState } from "react";
import { getProjects, createProject } from "../lib/api";
import { Link } from "react-router-dom";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [title, setTitle] = useState("");
  const [clientName, setClientName] = useState("");
  const [error, setError] = useState(null);

  const fetchProjects = async () => {
    try {
      const res = await getProjects();
      setProjects(res.items);
    } catch (err) {
      setError("Failed to load projects");
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createProject({ title, client_name: clientName });
      setTitle("");
      setClientName("");
      fetchProjects();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Projects</h2>
      <form onSubmit={handleSubmit} className="card">
        <input
          placeholder="Project Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          placeholder="Client Name"
          value={clientName}
          onChange={(e) => setClientName(e.target.value)}
        />
        <button type="submit">Create Project</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div>
        {projects.map((p) => (
          <div key={p.id} className="card">
            <h3>{p.title}</h3>
            <p>Client: {p.client_name}</p>
            <Link to={`/projects/${p.id}`}>View Details</Link>
          </div>
        ))}
      </div>
    </div>
  );
}