import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../Context/AuthContext";
import { logout } from "../lib/api";

export default function NavBar() {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    await refreshUser();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <h1>Client Implementation Tracker</h1>
      <div>
        {user ? (
          <>
            <Link to="/projects">Projects</Link>
            <Link to="/dashboard">Dashboard</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </>
        )}
      </div>
    </nav>
  );
}