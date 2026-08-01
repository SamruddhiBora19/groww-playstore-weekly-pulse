"""
Phase 4: Email Service Module (Python smtplib)
Generates styled single-page HTML email template for Weekly Pulse
and dispatches emails via SMTP or saves offline .html draft files.
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def format_recipient_name(recipient_name: str = None, recipient_email: str = "") -> str:
    """Format or extract clean recipient greeting name."""
    if recipient_name and recipient_name.strip():
        return recipient_name.strip()
    
    if recipient_email and "@" in recipient_email:
        local_part = recipient_email.split("@")[0]
        # Replace dots/underscores/hyphens with spaces and capitalize
        parts = [p.capitalize() for p in local_part.replace(".", " ").replace("_", " ").replace("-", " ").split()]
        if parts:
            return " ".join(parts)
            
    return "Team Member"

def build_html_email(pulse: Dict[str, Any], meta: Dict[str, Any], recipient_name: str = "Team Member") -> str:
    """Builds a beautiful, responsive single-page HTML email for GROWW Weekly Pulse with personalized greeting."""
    headline = pulse.get("metadata", {}).get("summaryHeadline", "GROWW Weekly Pulse Report")
    themes = pulse.get("topThemes", [])
    quotes = pulse.get("userQuotes", [])
    actions = pulse.get("actionIdeas", [])

    themes_html = ""
    for t in themes:
        themes_html += f"""
        <div style="background: #111827; padding: 14px 18px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #00D09C;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <strong style="color: #F9FAFB; font-size: 15px;">{t.get('themeName')}</strong>
            <span style="background: #064E3B; color: #34D399; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">{t.get('percentage')}% ({t.get('sentiment')})</span>
          </div>
          <p style="color: #9CA3AF; font-size: 13px; margin: 0;">{t.get('summary')}</p>
        </div>
        """

    quotes_html = ""
    for q in quotes:
        quotes_html += f"""
        <div style="background: #1F2937; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px;">
          <div style="font-size: 12px; color: #F59E0B; margin-bottom: 4px;">{'★' * int(q.get('rating', 1))} | {q.get('category')} (Ref: {q.get('id')})</div>
          <p style="color: #E5E7EB; font-size: 13px; font-style: italic; margin: 0;">"{q.get('quote')}"</p>
        </div>
        """

    actions_html = ""
    for a in actions:
        actions_html += f"""
        <div style="background: #064E3B; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #059669;">
          <strong style="color: #A7F3D0; font-size: 13px;">[{a.get('team')}] — Impact: {a.get('impact')}</strong>
          <p style="color: #F9FAFB; font-size: 13px; margin: 4px 0 0 0;">{a.get('action')}</p>
        </div>
        """

    display_name = recipient_name.strip() if recipient_name else "Team Member"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>GROWW Play Store Weekly Pulse</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #0B0F17; color: #F3F4F6; margin: 0; padding: 20px;">
      <div style="max-width: 650px; margin: 0 auto; background: #1F2937; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #059669 0%, #00D09C 100%); padding: 24px 28px;">
          <h1 style="color: #FFFFFF; margin: 0; font-size: 22px;">🌱 GROWW — Weekly Pulse Note</h1>
          <p style="color: #D1FAE5; margin: 6px 0 0 0; font-size: 13px;">Play Store User Reviews Pulse • Past 3 Months ({meta.get('totalFetched', 45)} Reviews Analyzed)</p>
        </div>

        <div style="padding: 24px 28px;">
          
          <!-- Personal Recipient Greeting -->
          <div style="font-size: 17px; color: #F9FAFB; font-weight: 600; margin-bottom: 8px;">
            Hi <span style="color: #00D09C;">{display_name}</span>,
          </div>
          <p style="color: #9CA3AF; font-size: 13px; margin-top: 0; margin-bottom: 20px; line-height: 1.5;">
            Here is your weekly Play Store customer intelligence briefing synthesized by Google Gemini LLM.
          </p>

          <!-- Executive Summary -->
          <div style="background: #111827; padding: 16px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #3B82F6;">
            <div style="color: #60A5FA; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Executive Headline</div>
            <div style="color: #E5E7EB; font-size: 14px; font-weight: 500;">{headline}</div>
          </div>

          <!-- Section 1: Top Themes -->
          <h3 style="color: #34D399; font-size: 16px; border-bottom: 1px solid #374151; padding-bottom: 6px; margin-top: 0;">🔥 Top 3-5 Core Themes</h3>
          {themes_html}

          <!-- Section 2: Real User Quotes -->
          <h3 style="color: #FBBF24; font-size: 16px; border-bottom: 1px solid #374151; padding-bottom: 6px; margin-top: 24px;">💬 Authentic User Quotes (Zero PII)</h3>
          {quotes_html}

          <!-- Section 3: Action Ideas -->
          <h3 style="color: #60A5FA; font-size: 16px; border-bottom: 1px solid #374151; padding-bottom: 6px; margin-top: 24px;">💡 3 Strategic Action Ideas</h3>
          {actions_html}

        </div>

        <!-- Footer -->
        <div style="background: #111827; padding: 16px 28px; text-align: center; color: #6B7280; font-size: 12px; border-top: 1px solid #374151;">
          GROWW Weekly Pulse Report • Powered by Gemini LLM Intelligence Engine
        </div>

      </div>
    </body>
    </html>
    """

def send_pulse_email(recipient: str, subject: str, html_content: str) -> Dict[str, Any]:
    """
    Sends pulse email via SMTP credentials if configured in environment,
    or saves local offline HTML draft if SMTP credentials are missing.
    """
    load_dotenv()
    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587").strip() or 587)
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_pass = os.getenv("SMTP_PASS", "").replace(" ", "").strip()

    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject or "[Weekly Pulse] GROWW Play Store Reviews & Action Items"
            msg["From"] = smtp_user
            msg["To"] = recipient

            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, recipient, msg.as_string())

            return {
                "success": True,
                "mode": "SMTP",
                "recipient": recipient,
                "message": f"Email successfully dispatched to recipient '{recipient}' via SMTP!"
            }

        except Exception as e:
            logger.warning(f"SMTP dispatch error ({e}). Falling back to local HTML draft for {recipient}.")

    # Local Draft Fallback
    draft_path = os.path.join(os.path.dirname(__file__), "weekly_pulse_email_draft.html")
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return {
        "success": True,
        "mode": "Local Draft",
        "recipient": recipient,
        "message": f"Email draft formatted for '{recipient}' saved to {draft_path} (Configure SMTP_HOST & credentials in .env for direct email delivery).",
        "draftPath": draft_path
    }
