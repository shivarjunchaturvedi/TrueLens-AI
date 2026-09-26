const COLORS = {
  real: '#2ecc71',
  ai_generated: '#f5a623',
  manipulated: '#ff5c5c',
}

const LABELS = {
  real: 'Real',
  ai_generated: 'AI Generated',
  manipulated: 'Manipulated',
}

export default function ProbabilityBars({ probabilities }) {
  return (
    <div>
      {Object.entries(probabilities).map(([key, value]) => {
        const percentage = Number(value) * 100

        return (
          <div className="prob-row" key={key}>
            <div className="prob-label">{LABELS[key]}</div>

            <div className="prob-bar-bg">
              <div
                className="prob-bar-fill"
                style={{
                  width: `${percentage}%`,
                  background: COLORS[key],
                }}
              />
            </div>

            <div className="prob-value">
              {percentage.toFixed(2)}%
            </div>
          </div>
        )
      })}
    </div>
  )
}
