import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function NavBar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    fetch("http://localhost:5555/logout", {
      method: "DELETE",
      credentials: "include",
    })
      .then(() => {
        logout();
        navigate("/login");
      })
      .catch((err) => {
        console.error("Logout failed:", err);
      });
  }

  return (
    <nav>
      <Link to="/">Home</Link>
      {user ? (
        <>
          <Link to="/projects">Projects</Link>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login">Log In</Link>
          <Link to="/signup">Sign Up</Link>
        </>
      )}
    </nav>
  );
}

export default NavBar;