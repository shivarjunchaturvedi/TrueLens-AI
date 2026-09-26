import { useEffect, useState } from 'react'
import client from '../api/client'
import PredictionBadge from '../components/PredictionBadge'

export default function History() {
  const [scans, setScans] = useState([])
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(null)

  const loadHistory = () => {
    client.get('/history')
      .then((res) => setScans(res.data))
      .catch(() => setError('Could not load scan history.'))
  }

  useEffect(loadHistory, [])

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this scan permanently?')) return
    try {
      await client.delete(`/history/${id}`)
      setScans(scans.filter((s) => s.id !== id))
      if (selected?.id === id) setSelected(null)
    } catch {
      setError('Could not delete scan.')
    }
  }

  return (
    <div className="container">
      <h1>Scan History</h1>
      {error && <div className="error-banner">{error}</div>}

      <div className="grid grid-2">
        <div className="card">
          <h3 style={{ marginTop: 0 }}>All Scans</h3>
          {scans.length === 0 ? (
            <p style={{ color: 'var(--text-dim)' }}>No scans yet.</p>
          ) : (
            <table>
              <thead>
                <tr><th>Filename</th><th>Result</th><th>Confidence</th><th></th></tr>
              </thead>
              <tbody>
                {scans.map((s) => (
                  <tr key={s.id} style={{ cursor: 'pointer' }}>
                    <td onClick={() => setSelected(s)}>{s.filename}</td>
                    <td onClick={() => setSelected(s)}><PredictionBadge prediction={s.prediction} /></td>
                    <td onClick={() => setSelected(s)}>{s.confidence.toFixed(1)}%</td>
                    <td>
                      <button className="btn btn-danger" onClick={() => handleDelete(s.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="card">
          <h3 style={{ marginTop: 0 }}>Details</h3>
          {selected ? (
            <div>
              <PredictionBadge prediction={selected.prediction} />
              <p>Confidence: {selected.confidence.toFixed(1)}%</p>
              <p>Model version: {selected.model_version}</p>
              <p>Processing time: {selected.processing_time_seconds}s</p>
              <p>Scanned: {new Date(selected.created_at).toLocaleString()}</p>
              <div className="result-images">
                <figure>
                  <img src={selected.original_image_url} alt="original" />
                  <figcaption>Original</figcaption>
                </figure>
                {selected.heatmap_url && (
                  <figure>
                    <img src={selected.heatmap_url} alt="heatmap" />
                    <figcaption>Grad-CAM</figcaption>
                  </figure>
                )}
              </div>
            </div>
          ) : (
            <p style={{ color: 'var(--text-dim)' }}>Select a scan to view details.</p>
          )}
        </div>
      </div>
    </div>
  )
}
