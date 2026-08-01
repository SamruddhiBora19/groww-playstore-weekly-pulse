'use client';

export default function ActionIdeasSection({ actions }) {
  if (!actions || actions.length === 0) return null;

  return (
    <section className="card">
      <div className="card-header">
        <h3>💡 3 Strategic Action Ideas</h3>
        <span className="card-tag tag-blue">Cross-Team Priority</span>
      </div>
      <div id="actionsList" className="actions-list">
        {actions.map((a, idx) => (
          <div key={idx} className="action-item">
            <div className="action-team">[{a.team}] — Impact: {a.impact}</div>
            <div style={{ fontSize: '13px' }}>{a.action}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
