'use client';

import { useState, useEffect } from 'react';

export default function EmailModal({
  isOpen,
  onClose,
  recipientName,
  setRecipientName,
  recipientEmail,
  setRecipientEmail,
  currentPulseData,
  currentMetaData
}) {
  const [subject, setSubject] = useState('[Weekly Pulse] GROWW Play Store Reviews & Action Items');
  const [previewHtml, setPreviewHtml] = useState('');
  const [isSending, setIsSending] = useState(false);

  // Fetch live preview whenever modal opens or inputs change
  useEffect(() => {
    if (!isOpen || !currentPulseData) return;

    async function fetchPreview() {
      try {
        const res = await fetch('/api/preview-email', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            recipient: recipientEmail,
            recipientName: recipientName,
            subject: subject,
            pulseData: currentPulseData,
            metaData: currentMetaData
          })
        });
        const data = await res.json();
        if (data.success) {
          setPreviewHtml(data.html);
        }
      } catch (err) {
        console.error('Failed to fetch preview:', err);
      }
    }

    fetchPreview();
  }, [isOpen, recipientName, recipientEmail, subject, currentPulseData, currentMetaData]);

  if (!isOpen) return null;

  const handleSendEmail = async () => {
    if (!recipientEmail || !recipientEmail.includes('@')) {
      alert('Please enter a valid recipient email address.');
      return;
    }

    setIsSending(true);

    try {
      const res = await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipient: recipientEmail,
          recipientName: recipientName,
          subject: subject,
          pulseData: currentPulseData,
          metaData: currentMetaData
        })
      });

      const data = await res.json();
      if (data.success) {
        alert(`✅ Email Dispatched Successfully to ${recipientEmail}!\n\n` + data.message);
        onClose();
      } else {
        alert('❌ Failed to send email: ' + (data.detail || 'Unknown error'));
      }
    } catch (err) {
      console.error('Error sending email:', err);
      alert('Error sending email from server.');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-header">
          <h3>✉️ Compose & Send Personalized Email</h3>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="form-group">
              <label htmlFor="modalRecipientName">Recipient Name (Greeting):</label>
              <input
                type="text"
                id="modalRecipientName"
                value={recipientName}
                onChange={(e) => setRecipientName(e.target.value)}
                placeholder="e.g. Samruddhi / Product Lead"
              />
            </div>
            <div className="form-group">
              <label htmlFor="modalRecipientEmail">Recipient Email / Alias:</label>
              <input
                type="email"
                id="modalRecipientEmail"
                value={recipientEmail}
                onChange={(e) => setRecipientEmail(e.target.value)}
                placeholder="Enter recipient email"
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="modalSubject">Subject Line:</label>
            <input
              type="text"
              id="modalSubject"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Live HTML Email Preview:</label>
            <iframe
              title="Email Preview"
              srcDoc={previewHtml}
              className="email-preview-frame"
            ></iframe>
          </div>
        </div>
        <div className="modal-footer">
          <button
            className="btn accent-btn"
            onClick={handleSendEmail}
            disabled={isSending}
          >
            {isSending ? 'Sending...' : '🚀 Send Email Now'}
          </button>
        </div>
      </div>
    </div>
  );
}
