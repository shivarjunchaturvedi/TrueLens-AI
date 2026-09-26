import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'

export default function Detect() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef(null)
  const navigate = useNavigate()

  const handleFile = (f) => {
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setError('')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }

  const handleSubmit = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await client.post('/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      navigate('/result', { state: { result: res.data } })
    } catch (err) {
      setError(err.response?.data?.detail || 'Detection failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Image Authenticity Detection</h1>
      <p style={{ color: 'var(--text-dim)' }}>
        Upload a JPG, PNG, or WEBP image (max 10 MB) to analyze it with TrueLens AI.
      </p>

      {error && <div className="error-banner">{error}</div>}

      <div
        className={`dropzone ${dragging ? 'dragging' : ''}`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        {preview ? (
          <img src={preview} alt="preview" style={{ maxWidth: '100%', maxHeight: 300, borderRadius: 8 }} />
        ) : (
          <>
            <p style={{ fontSize: 18 }}>Drag & drop an image here, or click to browse</p>
            <p style={{ color: 'var(--text-dim)', fontSize: 13 }}>JPG · PNG · WEBP — up to 10MB</p>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png,.webp"
          style={{ display: 'none' }}
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>

      <button
        className="btn btn-primary"
        style={{ marginTop: 20 }}
        disabled={!file || loading}
        onClick={handleSubmit}
      >
        {loading ? 'Analyzing...' : 'Run Detection'}
      </button>
    </div>
  )
}
