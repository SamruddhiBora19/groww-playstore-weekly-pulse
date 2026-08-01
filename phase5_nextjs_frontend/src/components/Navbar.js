'use client';

export default function Navbar({
  recipientName,
  setRecipientName,
  recipientEmail,
  setRecipientEmail,
  weeks,
  setWeeks,
  onGenerate,
  isLoading
}) {
  return (
    <header className="navbar glass-card">
      <div className="brand">
        <div className="logo-icon">🌱</div>
        <div className="brand-text">
          <h1>GROWW <span>Weekly Pulse</span></h1>
          <p className="subtitle">Play Store Customer Insights & Gemini LLM Intelligence (Next.js Dashboard)</p>
        </div>
      </div>
      <div className="nav-controls">
        <div className="control-group">
          <label htmlFor="headerNameInput">Recipient Name:</label>
          <input
            type="text"
            id="headerNameInput"
            className="input-control"
            style={{ width: '130px' }}
            value={recipientName}
            onChange={(e) => setRecipientName(e.target.value)}
            placeholder="e.g. Samruddhi"
          />
        </div>
        <div className="control-group">
          <label htmlFor="headerEmailInput">Target Email:</label>
          <input
            type="email"
            id="headerEmailInput"
            className="input-control"
            style={{ width: '210px' }}
            value={recipientEmail}
            onChange={(e) => setRecipientEmail(e.target.value)}
            placeholder="Enter target email"
          />
        </div>
        <div className="control-group">
          <label htmlFor="weeksSelect">Time Window:</label>
          <select
            id="weeksSelect"
            value={weeks}
            onChange={(e) => setWeeks(e.target.value)}
          >
            <option value="12">Past 3 Months (12 Weeks)</option>
            <option value="8">Past 2 Months (8 Weeks)</option>
            <option value="4">Past 1 Month (4 Weeks)</option>
          </select>
        </div>
        <button
          id="generateBtn"
          className="btn primary-btn"
          onClick={onGenerate}
          disabled={isLoading}
        >
          <span className="btn-icon">⚡</span>
          <span>{isLoading ? 'Generating...' : 'Generate Weekly Pulse'}</span>
        </button>
      </div>
    </header>
  );
}
