import { useEffect, useState } from 'react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { Link } from 'react-router-dom'
import client from '../api/client'
import PredictionBadge from '../components/PredictionBadge'

const COLORS = ['#2ecc71', '#f5a623', '#ff5c5c']

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    client.get('/dashboard/stats')
      .then((res) => setStats(res.data))
      .catch(() => setError('Could not load dashboard statistics.'))
  }, [])

  if (error) return <div className="container"><div className="error-banner">{error}</div></div>
  if (!stats) return <div className="container">Loading dashboard...</div>

  const pieData = [
    { name: 'Authentic', value: stats.authentic_count },
    { name: 'AI Generated', value: stats.ai_generated_count },
    { name: 'Manipulated', value: stats.manipulated_count },
  ]

  return (
    <div className="container">
      <h1>Dashboard</h1>

      <div className="grid grid-4" style={{ marginBottom: 24 }}>
        <div className="card stat-card">
          <span className="stat-label">Total Scans</span>
          <span className="stat-value">{stats.total_scans}</span>
        </div>
        <div className="card stat-card">
          <span className="stat-label">Authentic</span>
          <span className="stat-value" style={{ color: '#2ecc71' }}>{stats.authentic_count}</span>
        </div>
        <div className="card stat-card">
          <span className="stat-label">AI Generated</span>
          <span className="stat-value" style={{ color: '#f5a623' }}>{stats.ai_generated_count}</span>
        </div>
        <div className="card stat-card">
          <span className="stat-label">Manipulated</span>
          <span className="stat-value" style={{ color: '#ff5c5c' }}>{stats.manipulated_count}</span>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Detection Breakdown</h3>
          {stats.total_scans === 0 ? (
            <p style={{ color: 'var(--text-dim)' }}>No scans yet — run your first detection.</p>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={90}>
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="card">
          <h3 style={{ marginTop: 0 }}>Average Confidence</h3>
          <div style={{ fontSize: 48, fontWeight: 700, color: 'var(--accent)' }}>
            {stats.average_confidence}%
          </div>
          <p style={{ color: 'var(--text-dim)', fontSize: 13 }}>
            Across all {stats.total_scans} scan(s) performed by your account.
          </p>
          <Link to="/detect" className="btn btn-primary">Run New Detection</Link>
        </div>
      </div>

      <div className="card" style={{ marginTop: 24 }}>
        <h3 style={{ marginTop: 0 }}>Recent Scans</h3>
        {stats.recent_scans.length === 0 ? (
          <p style={{ color: 'var(--text-dim)' }}>No recent scans.</p>
        ) : (
          <table>
            <thead>
              <tr><th>Filename</th><th>Prediction</th><th>Confidence</th><th>Date</th></tr>
            </thead>
            <tbody>
              {stats.recent_scans.map((s) => (
                <tr key={s.id}>
                  <td>{s.filename}</td>
                  <td><PredictionBadge prediction={s.prediction} /></td>
                  <td>{s.confidence.toFixed(1)}%</td>
                  <td>{new Date(s.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
