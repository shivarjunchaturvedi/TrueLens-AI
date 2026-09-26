import { useAuth } from '../context/AuthContext'

export default function Profile() {
  const { user, logout } = useAuth()

  return (
    <div className="container">
      <h1>Profile</h1>
      <div className="card" style={{ maxWidth: 480 }}>
        <div className="field">
          <label>Username</label>
          <input value={user?.username || ''} disabled />
        </div>
        <div className="field">
          <label>Email</label>
          <input value={user?.email || ''} disabled />
        </div>
        <button className="btn btn-danger" onClick={logout}>Logout</button>
      </div>
    </div>
  )
}
