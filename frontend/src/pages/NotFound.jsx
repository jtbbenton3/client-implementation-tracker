import React from "react";
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="card">
      <h2>404 - Page Not Found</h2>
      <Link to="/projects">Go back to projects</Link>
    </div>
  );
}