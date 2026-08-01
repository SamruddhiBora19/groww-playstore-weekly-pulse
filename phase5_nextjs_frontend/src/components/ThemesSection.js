'use client';

export default function ThemesSection({ themes }) {
  if (!themes || themes.length === 0) return null;

  return (
    <section className="card">
      <div className="card-header">
        <h3>🔥 Top 3–5 Core Themes</h3>
        <span className="card-tag">Gemini LLM Categorized</span>
      </div>
      <div id="themesList" className="themes-list">
        {themes.map((t, idx) => {
          const sentLower = (t.sentiment || '').toLowerCase();
          let sentClass = 'sentiment-neutral';
          if (sentLower.includes('neg')) sentClass = 'sentiment-negative';
          else if (sentLower.includes('pos')) sentClass = 'sentiment-positive';

          return (
            <div key={idx} className="theme-item">
              <div className="theme-top">
                <strong>{t.themeName}</strong>
                <div>
                  <span className={`sentiment-pill ${sentClass}`}>
                    {t.sentiment || 'Neutral'}
                  </span>
                  <strong style={{ color: '#00D09C', marginLeft: '8px' }}>
                    {t.percentage}%
                  </strong>
                </div>
              </div>
              <div className="progress-bar-bg">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${t.percentage}%` }}
                ></div>
              </div>
              <div className="theme-summary">{t.summary}</div>
              {t.keyDrivers && t.keyDrivers.length > 0 && (
                <div className="driver-tags-row">
                  {t.keyDrivers.map((d, dIdx) => (
                    <span key={dIdx} className="driver-tag">{d}</span>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
