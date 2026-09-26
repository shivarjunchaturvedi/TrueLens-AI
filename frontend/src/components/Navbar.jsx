import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <Link to="/" className="brand">
        True<span className="dot">Lens</span> AI
      </Link>
      <div className="nav-links">
        {user ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/detect">Detect</Link>
            <Link to="/history">History</Link>
            <Link to="/profile">Profile</Link>
            <Link to="/about">About</Link>
            <button className="btn btn-outline" onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/about">About</Link>
            <Link to="/login">Login</Link>
            <Link to="/register" className="btn btn-primary">Get Started</Link>
          </>
        )}
      </div>
    </nav>
  )
}
