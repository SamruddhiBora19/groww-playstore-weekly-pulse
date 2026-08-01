import './globals.css';

export const metadata = {
  title: 'GROWW Play Store Review Weekly Pulse Generator | Next.js Dashboard',
  description: 'AI-Powered One-Page Weekly Pulse for GROWW Play Store User Reviews using Gemini LLM',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body>
        <div className="app-container">
          {children}
        </div>
      </body>
    </html>
  );
}
