export default function About() {
  return (
    <div className="container">
      <h1>About TrueLens AI</h1>
      <div className="card" style={{ marginBottom: 20 }}>
        <p>
          TrueLens AI is an AI-powered image authenticity detection system built
          as a B.Tech final-year project. It classifies uploaded images as
          <strong> Real</strong>, <strong> AI-Generated</strong>, or
          <strong> Manipulated/Deepfake</strong> using a fine-tuned CNN
          (EfficientNet-B0 backbone), and explains its decision using Grad-CAM
          visual heatmaps.
        </p>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <h3 style={{ marginTop: 0 }}>How it works</h3>
        <ol style={{ color: 'var(--text-dim)' }}>
          <li>Image upload and validation (type, size, integrity)</li>
          <li>Face detection and cropping (for the deepfake-detection path)</li>
          <li>Preprocessing (resize, normalize)</li>
          <li>CNN forward pass and softmax probability calculation</li>
          <li>Grad-CAM heatmap generation for the predicted class</li>
          <li>Result storage and dashboard aggregation</li>
        </ol>
      </div>

      <div className="limitations-box">
        <strong>Limitations:</strong> TrueLens AI provides an AI-based
        authenticity estimate, not absolute proof of image origin. Its
        training data cannot cover every generative model in existence,
        newer generators may not be reliably detected, heavy compression or
        resizing can remove the artifacts the model relies on, and
        deliberately adversarial images can mislead any CNN-based detector.
        False positives and false negatives are possible — treat results as
        a decision aid, not a verdict.
      </div>
    </div>
  )
}
