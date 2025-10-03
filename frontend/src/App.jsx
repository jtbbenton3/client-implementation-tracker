import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import NavBar from "./Components/NavBar";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Projects from "./pages/Projects";
import ProjectDetail from "./pages/ProjectDetail";
import ClientDashboard from "./pages/ClientDashboard";
import ProjectShare from "./pages/ProjectShare";
import Debug from "./pages/Debug";
import NotFound from "./pages/NotFound";
import { useAuth } from "./Context/AuthContext";

export default function App() {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;

  return (
    <>
      <NavBar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Navigate to="/projects" />} />
          <Route path="/login" element={user ? <Navigate to="/projects" /> : <Login />} />
          <Route path="/signup" element={user ? <Navigate to="/projects" /> : <Signup />} />
          <Route path="/projects" element={user ? <Projects /> : <Navigate to="/login" />} />
          <Route path="/projects/:id" element={user ? <ProjectDetail /> : <Navigate to="/login" />} />
          <Route path="/dashboard" element={user ? <ClientDashboard /> : <Navigate to="/login" />} />
          <Route path="/share/:id" element={<ProjectShare />} />
          <Route path="/debug" element={<Debug />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </>
  );
}