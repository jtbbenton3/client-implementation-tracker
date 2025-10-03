import React, { useEffect, useState } from "react";
import { getProjects } from "../lib/api";
import { Link } from "react-router-dom";

export default function ClientDashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const projectsData = await getProjects();
        setProjects(projectsData.items || projectsData);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

  // Calculate KPIs
  const totalProjects = projects.length;
  const activeProjects = projects.filter(p => p.status !== 'completed').length;
  const completedProjects = projects.filter(p => p.status === 'completed').length;
  const completionRate = totalProjects > 0 ? Math.round((completedProjects / totalProjects) * 100) : 0;

  return (
    <div>
      <h2>Client Dashboard</h2>
      
      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ margin: '0 0 0.5rem 0', color: '#007bff' }}>{totalProjects}</h3>
          <p style={{ margin: 0, color: '#666' }}>Total Projects</p>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ margin: '0 0 0.5rem 0', color: '#28a745' }}>{activeProjects}</h3>
          <p style={{ margin: 0, color: '#666' }}>Active Projects</p>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ margin: '0 0 0.5rem 0', color: '#17a2b8' }}>{completionRate}%</h3>
          <p style={{ margin: 0, color: '#666' }}>Completion Rate</p>
        </div>
      </div>

      <section>
        <h3>Your Projects</h3>
        {projects.length === 0 ? (
          <div className="card">
            <p>No projects yet. <Link to="/projects">Create your first project</Link></p>
          </div>
        ) : (
          projects.map((p) => (
            <div key={p.id} className="card">
              <h4>{p.title}</h4>
              <p>Client: {p.client_name}</p>
              <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
                <Link to={`/projects/${p.id}`} className="button">View Details</Link>
                <Link to={`/projects/${p.id}`} className="button" style={{ background: '#28a745' }}>Manage</Link>
              </div>
            </div>
          ))
        )}
      </section>
    </div>
  );
}