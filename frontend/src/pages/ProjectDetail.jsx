// frontend/src/pages/ProjectDetail.jsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchWithAuth } from "../lib/fetchWithAuth";
import { Card, CardContent } from "../components/ui/card";

function ProjectDetail() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);

  useEffect(() => {
    fetchWithAuth(`/api/projects/${projectId}`)
      .then((res) => setProject(res))
      .catch((err) => console.error(err));
  }, [projectId]);

  if (!project) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-2">{project.title}</h1>
      <p className="text-gray-600 mb-4">{project.description}</p>

      <Card className="mb-6">
        <CardContent className="p-4">
          <p>
            <strong>Client:</strong> {project.client_name}
          </p>
          <p>
            <strong>Phase:</strong> {project.phase}
          </p>
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl font-semibold mb-2">Milestones</h2>
          <ul className="list-disc ml-5 space-y-1">
            {project.milestones?.map((m) => (
              <li key={m.id}>
                <strong>{m.title}</strong> – {m.status}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-2">Status Updates</h2>
          <ul className="list-disc ml-5 space-y-1">
            {project.status_updates?.map((s) => (
              <li key={s.id}>
                <strong>{s.title}</strong> – {s.content}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ProjectDetail;