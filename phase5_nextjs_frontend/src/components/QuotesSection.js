'use client';

export default function QuotesSection({ quotes }) {
  if (!quotes || quotes.length === 0) return null;

  return (
    <section className="card">
      <div className="card-header">
        <h3>💬 3 Real User Quotes</h3>
        <span className="card-tag tag-gold">PII Redacted</span>
      </div>
      <div id="quotesList" className="quotes-list">
        {quotes.map((q, idx) => (
          <div key={idx} className="quote-item">
            <div className="quote-cat">
              {'★'.repeat(q.rating)} • {q.category} (Ref: {q.id})
            </div>
            <div className="quote-text">"{q.quote}"</div>
          </div>
        ))}
      </div>
    </section>
  );
}
