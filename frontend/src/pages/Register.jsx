import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register(username, email, password)
      setSuccess(true)
      setTimeout(() => navigate('/login'), 1200)
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card auth-card">
        <h2 style={{ marginTop: 0 }}>Create your account</h2>
        {error && <div className="error-banner">{error}</div>}
        {success && (
          <div className="error-banner" style={{ borderColor: '#2ecc71', color: '#a8f0c6' }}>
            Account created! Redirecting to login...
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Username</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} required minLength={3} />
          </div>
          <div className="field">
            <label>Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="field">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>
          <button className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Creating account...' : 'Register'}
          </button>
        </form>
        <p style={{ fontSize: 13, color: 'var(--text-dim)', marginTop: 16 }}>
          Already have an account? <Link to="/login" style={{ color: 'var(--accent)' }}>Login</Link>
        </p>
      </div>
    </div>
  )
}
