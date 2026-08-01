'use client';

export default function ExecutiveHeader({
  pulse,
  meta,
  weeks,
  onOpenModal,
  onExportPdf
}) {
  const headline = pulse?.metadata?.summaryHeadline || 'GROWW Play Store Executive Intelligence Briefing';
  const totalFetched = meta?.totalFetched || 45;
  const avgRating = (meta?.avgRating || '2.5') + ' / 5.0';
  const piiScrubbed = (meta?.piiScrubbedCount || 0) + ' Reviews';

  const source = pulse?.metadata?.source || 'GEMINI_LLM';
  const model = pulse?.metadata?.model || 'gemini-2.5-flash';
  let engineText = 'Built-in Engine';
  if (source.includes('GEMINI')) {
    engineText = `Gemini (${model})`;
  } else if (source.includes('GROQ')) {
    engineText = `Groq (${model})`;
  }

  return (
    <section className="exec-card">
      <div className="meta-header">
        <div>
          <span className="badge badge-groww">GROWW Pulse Note</span>
          <span className="badge badge-outline">
            {weeks === '12' ? 'Past 3 Months' : weeks === '8' ? 'Past 2 Months' : 'Past 1 Month'}
          </span>
        </div>
        <div className="header-actions">
          <button id="exportPdfBtn" className="btn secondary-btn" onClick={onExportPdf}>
            📄 Export PDF / Print
          </button>
          <button id="openEmailModalBtn" className="btn accent-btn" onClick={onOpenModal}>
            ✉️ Draft & Send Email
          </button>
        </div>
      </div>

      <h2 id="summaryHeadline" className="headline-text">
        {headline}
      </h2>

      <div className="stats-row">
        <div className="stat-pill">
          <span className="stat-label">Total Reviews</span>
          <span id="statTotal" className="stat-val">{totalFetched}</span>
        </div>
        <div className="stat-pill">
          <span className="stat-label">Avg Rating</span>
          <span id="statAvgRating" className="stat-val">{avgRating}</span>
        </div>
        <div className="stat-pill">
          <span className="stat-label">PII Scrubbed</span>
          <span id="statPii" className="stat-val">{piiScrubbed}</span>
        </div>
        <div className="stat-pill">
          <span className="stat-label">LLM Engine</span>
          <span id="statEngine" className="stat-val green-text">{engineText}</span>
        </div>
      </div>
    </section>
  );
}
