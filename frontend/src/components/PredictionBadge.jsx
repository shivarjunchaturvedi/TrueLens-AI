const CONFIG = {
  REAL: { label: 'AUTHENTIC IMAGE', className: 'badge-real' },
  AI_GENERATED: { label: 'AI-GENERATED IMAGE', className: 'badge-ai' },
  MANIPULATED: { label: 'MANIPULATED / DEEPFAKE IMAGE', className: 'badge-manipulated' },
}

export default function PredictionBadge({ prediction }) {
  const cfg = CONFIG[prediction] || { label: prediction, className: '' }
  return <span className={`badge ${cfg.className}`}>{cfg.label}</span>
}
