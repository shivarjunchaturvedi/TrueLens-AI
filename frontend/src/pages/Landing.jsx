import { Link } from 'react-router-dom'

export default function Landing() {
  return (
    <div>
      <div className="hero">
        <h1>See Through Any Image with <span style={{ color: '#4f8cff' }}>TrueLens AI</span></h1>
        <p>
          Upload any image and get an instant, explainable AI-based authenticity
          estimate — Real, AI-Generated, or Manipulated/Deepfake — backed by a
          CNN model and Grad-CAM visual explanations.
        </p>
        <Link to="/register" className="btn btn-primary" style={{ marginRight: 12 }}>
          Try TrueLens AI
        </Link>
        <Link to="/about" className="btn btn-outline">Learn More</Link>
      </div>

      <div className="container">
        <div className="grid grid-4">
          <div className="card">
            <h3>CNN-Based Detection</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: 14 }}>
              EfficientNet-B0 backbone fine-tuned on real, AI-generated, and
              deepfake image data.
            </p>
          </div>
          <div className="card">
            <h3>Explainable AI</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: 14 }}>
              Grad-CAM heatmaps show exactly which regions influenced the
              model's decision.
            </p>
          </div>
          <div className="card">
            <h3>Confidence Scoring</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: 14 }}>
              Full probability breakdown across all three classes, not just a
              single label.
            </p>
          </div>
          <div className="card">
            <h3>Scan History</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: 14 }}>
              Every scan is saved with timestamp, model version, and results
              you can revisit anytime.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
