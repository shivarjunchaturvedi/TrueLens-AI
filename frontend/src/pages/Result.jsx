import { useLocation, useNavigate, Link } from 'react-router-dom'
import PredictionBadge from '../components/PredictionBadge'
import ProbabilityBars from '../components/ProbabilityBars'

export default function Result() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const result = state?.result

  if (!result) {
    return (
      <div className="container">
        <p>No result to show.</p>
        <Link to="/detect" className="btn btn-primary">Run a Detection</Link>
      </div>
    )
  }

  return (
    <div className="container">
      <h1>Detection Result</h1>

      <div className="card" style={{ marginBottom: 20 }}>
        <PredictionBadge prediction={result.prediction} />
        <h2 style={{ margin: '12px 0 4px' }}>Confidence: {result.confidence.toFixed(1)}%</h2>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Images</h3>
          <div className="result-images">
            <figure>
              <img src={result.original_image_url} alt="original" />
              <figcaption>Uploaded Image</figcaption>
            </figure>
            {result.heatmap_url && (
              <figure>
                <img src={result.heatmap_url} alt="grad-cam heatmap" />
                <figcaption>Grad-CAM Explanation</figcaption>
              </figure>
            )}
          </div>
        </div>

        <div className="card">
          <h3 style={{ marginTop: 0 }}>Probability Distribution</h3>
          <ProbabilityBars probabilities={result.probabilities} />

          <h3>Model Information</h3>
          <table>
            <tbody>
              <tr><td>Model</td><td>{result.model_name}</td></tr>
              <tr><td>Version</td><td>{result.model_version}</td></tr>
              <tr><td>Processing Time</td><td>{result.processing_time_seconds}s</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <h3 style={{ marginTop: 0 }}>AI Explanation</h3>
        <p style={{ color: 'var(--text-dim)' }}>
          The Grad-CAM heatmap highlights the image regions the CNN weighted
          most heavily when producing this prediction — warmer colors (red/yellow)
          mark areas of higher influence on the decision. For manipulated/deepfake
          predictions, this is typically expected around facial boundaries or
          blended regions; for AI-generated predictions, it may highlight areas
          with unnatural texture patterns.
        </p>
      </div>

      <div className="limitations-box">
        <strong>Note:</strong> TrueLens AI provides an AI-based authenticity
        estimate, not absolute proof of image origin. Accuracy can be affected
        by image compression, resizing, unfamiliar generative models not seen
        during training, and deliberate adversarial manipulation. Use results
        as one input among several, not as sole evidence.
      </div>

      <button className="btn btn-outline" style={{ marginTop: 20 }} onClick={() => navigate('/detect')}>
        Analyze Another Image
      </button>
    </div>
  )
}
