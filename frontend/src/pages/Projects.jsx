import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchProjects() {
      try {
        const res = await fetch("http://localhost:5555/projects", {
          credentials: "include",
        });
        if (!res.ok) {
          throw new Error("Failed to fetch projects");
        }
        const data = await res.json();
        setProjects(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchProjects();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div className="projects-page">
      <h2>Projects</h2>
      <ul>
        {projects.map((project) => (
          <li key={project.id} onClick={() => navigate(`/projects/${project.id}`)}>
            <strong>{project.title}</strong> — {project.client_name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Projects;