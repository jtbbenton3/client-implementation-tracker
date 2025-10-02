function ProjectCard({ project }) {
  const { title, client_name, phase, description } = project;

  return (
    <div className="project-card">
      <h3>{title}</h3>
      <p><strong>Client:</strong> {client_name}</p>
      <p><strong>Phase:</strong> {phase}</p>
      {description && <p>{description}</p>}
    </div>
  );
}

export default ProjectCard;