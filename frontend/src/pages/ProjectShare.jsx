import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function ProjectShare() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [milestones, setMilestones] = useState([]);
  const [statusUpdates, setStatusUpdates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProjectData = async () => {
      try {
        // Fetch project details
        const projectRes = await fetch(`http://127.0.0.1:5555/api/projects/${id}`);
        if (projectRes.ok) {
          const projectData = await projectRes.json();
          setProject(projectData.project);
        }

        // Fetch milestones
        const milestonesRes = await fetch(`http://127.0.0.1:5555/api/projects/${id}/milestones`);
        if (milestonesRes.ok) {
          const milestonesData = await milestonesRes.json();
          setMilestones(milestonesData.items || []);
        }

        // Fetch status updates
        const updatesRes = await fetch(`http://127.0.0.1:5555/api/projects/${id}/status_updates`);
        if (updatesRes.ok) {
          const updatesData = await updatesRes.json();
          setStatusUpdates(updatesData.items || []);
        }
      } catch (error) {
        console.error("Failed to load project data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchProjectData();
    }
  }, [id]);

  if (loading) return <div>Loading project...</div>;
  if (!project) return <div>Project not found</div>;

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <header style={{ textAlign: 'center', marginBottom: '2rem', padding: '2rem', background: '#f8f9fa', borderRadius: '8px' }}>
        <h1 style={{ color: '#333', marginBottom: '0.5rem' }}>{project.title}</h1>
        <p style={{ color: '#666', fontSize: '1.1rem', margin: 0 }}>Client: {project.client_name}</p>
        <p style={{ color: '#999', fontSize: '0.9rem', margin: '0.5rem 0 0 0' }}>
          Last updated: {new Date().toLocaleDateString()}
        </p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
        {/* Milestones Section */}
        <section>
          <h2 style={{ color: '#333', borderBottom: '2px solid #007bff', paddingBottom: '0.5rem' }}>
            Project Milestones
          </h2>
          {milestones.length === 0 ? (
            <div style={{ padding: '1rem', background: '#f8f9fa', borderRadius: '4px', color: '#666' }}>
              No milestones defined yet
            </div>
          ) : (
            milestones.map((milestone) => (
              <div key={milestone.id} style={{ 
                padding: '1rem', 
                margin: '0.5rem 0', 
                background: '#fff', 
                border: '1px solid #dee2e6', 
                borderRadius: '4px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}>
                <h3 style={{ margin: '0 0 0.5rem 0', color: '#333' }}>{milestone.name}</h3>
                {milestone.target_date && (
                  <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
                    Target Date: {new Date(milestone.target_date).toLocaleDateString()}
                  </p>
                )}
              </div>
            ))
          )}
        </section>

        {/* Status Updates Section */}
        <section>
          <h2 style={{ color: '#333', borderBottom: '2px solid #28a745', paddingBottom: '0.5rem' }}>
            Recent Updates
          </h2>
          {statusUpdates.length === 0 ? (
            <div style={{ padding: '1rem', background: '#f8f9fa', borderRadius: '4px', color: '#666' }}>
              No status updates yet
            </div>
          ) : (
            statusUpdates.slice(0, 5).map((update) => (
              <div key={update.id} style={{ 
                padding: '1rem', 
                margin: '0.5rem 0', 
                background: '#fff', 
                border: '1px solid #dee2e6', 
                borderRadius: '4px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}>
                <p style={{ margin: '0 0 0.5rem 0', color: '#333' }}>{update.content}</p>
                <small style={{ color: '#666' }}>
                  {new Date(update.created_at).toLocaleString()}
                </small>
              </div>
            ))
          )}
        </section>
      </div>

      {/* Project Summary */}
      <section style={{ 
        padding: '1.5rem', 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
        color: 'white', 
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <h2 style={{ margin: '0 0 1rem 0' }}>Project Overview</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
          <div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '2rem' }}>{milestones.length}</h3>
            <p style={{ margin: 0, opacity: 0.9 }}>Milestones</p>
          </div>
          <div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '2rem' }}>{statusUpdates.length}</h3>
            <p style={{ margin: 0, opacity: 0.9 }}>Status Updates</p>
          </div>
          <div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '2rem' }}>Active</h3>
            <p style={{ margin: 0, opacity: 0.9 }}>Project Status</p>
          </div>
        </div>
      </section>

      <footer style={{ textAlign: 'center', marginTop: '2rem', padding: '1rem', color: '#666', fontSize: '0.9rem' }}>
        <p>This is a read-only view of your project status. For full access, please contact your project manager.</p>
      </footer>
    </div>
  );
}
