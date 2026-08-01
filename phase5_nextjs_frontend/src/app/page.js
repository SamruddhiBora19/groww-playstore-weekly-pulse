'use client';

import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import ExecutiveHeader from '../components/ExecutiveHeader';
import ThemesSection from '../components/ThemesSection';
import QuotesSection from '../components/QuotesSection';
import ActionIdeasSection from '../components/ActionIdeasSection';
import EmailModal from '../components/EmailModal';

export default function Home() {
  const [recipientName, setRecipientName] = useState('Samruddhi');
  const [recipientEmail, setRecipientEmail] = useState('borasamruddhi19@gmail.com');
  const [weeks, setWeeks] = useState('12');
  const [isLoading, setIsLoading] = useState(false);
  const [pulseData, setPulseData] = useState(null);
  const [metaData, setMetaData] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchPulse = async (selectedWeeks = weeks) => {
    setIsLoading(true);
    try {
      const res = await fetch(`/api/generate-pulse?weeks=${selectedWeeks}`);
      const data = await res.json();
      if (data.success) {
        setPulseData(data.pulse);
        setMetaData(data.meta);
      } else {
        alert('Failed to generate weekly pulse: ' + (data.detail || 'Unknown error'));
      }
    } catch (err) {
      console.error('Error fetching pulse:', err);
      alert('Error fetching pulse from server. Make sure FastAPI backend is running (python cli.py serve).');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPulse('12');
  }, []);

  const handleExportPdf = () => {
    window.print();
  };

  return (
    <main>
      <Navbar
        recipientName={recipientName}
        setRecipientName={setRecipientName}
        recipientEmail={recipientEmail}
        setRecipientEmail={setRecipientEmail}
        weeks={weeks}
        setWeeks={setWeeks}
        onGenerate={() => fetchPulse(weeks)}
        isLoading={isLoading}
      />

      {isLoading && (
        <div className="loading-bar">
          <div className="spinner"></div>
          <span>Ingesting Play Store Reviews, Redacting PII & Synthesizing Pulse via Gemini LLM...</span>
        </div>
      )}

      {pulseData && !isLoading && (
        <>
          <ExecutiveHeader
            pulse={pulseData}
            meta={metaData}
            weeks={weeks}
            onOpenModal={() => setIsModalOpen(true)}
            onExportPdf={handleExportPdf}
          />

          <div className="grid-2col">
            <ThemesSection themes={pulseData.topThemes} />

            <div className="col-stack">
              <QuotesSection quotes={pulseData.userQuotes} />
              <ActionIdeasSection actions={pulseData.actionIdeas} />
            </div>
          </div>
        </>
      )}

      <EmailModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        recipientName={recipientName}
        setRecipientName={setRecipientName}
        recipientEmail={recipientEmail}
        setRecipientEmail={setRecipientEmail}
        currentPulseData={pulseData}
        currentMetaData={metaData}
      />
    </main>
  );
}
