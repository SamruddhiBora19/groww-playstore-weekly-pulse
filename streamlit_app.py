"""
GROWW Play Store Review Weekly Pulse Generator - Streamlit Web Dashboard
Deployable on Streamlit Community Cloud or local Streamlit server.
Runs 100% in Python using existing Phase 1, 2, and 4 modules.
"""

import sys
import os
import json
import streamlit as st

# Ensure root directory is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Load secrets into os.environ for Streamlit Cloud compatibility
try:
    if hasattr(st, "secrets"):
        for key in ["GEMINI_API_KEY", "GROQ_API_KEY", "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS"]:
            if key in st.secrets and key not in os.environ:
                os.environ[key] = str(st.secrets[key])
except Exception:
    pass

from phase1_ingestion.scraper import fetch_groww_reviews
from phase2_llm_intelligence.gemini_service import generate_weekly_pulse
from phase4_email_dispatcher.email_service import build_html_email, send_pulse_email

# Page Config & Custom Styling
st.set_page_config(
    page_title="GROWW Weekly Pulse Generator",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GROWW Emerald Theme Custom CSS
st.markdown("""
<style>
    /* Dark Glassmorphism Styling */
    .stApp {
        background-color: #0B0F17;
        color: #F3F4F6;
    }
    .main-header {
        background: linear-gradient(135deg, #059669 0%, #00D09C 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(0, 208, 156, 0.2);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 6px 0 0 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }
    .metric-card {
        background: #1F2937;
        border: 1px solid #374151;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #00D09C;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #9CA3AF;
        text-transform: uppercase;
        margin-top: 4px;
    }
    .theme-card {
        background: #111827;
        border-left: 4px solid #00D09C;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .quote-card {
        background: #1F2937;
        border: 1px solid #374151;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-style: italic;
    }
    .action-card {
        background: #064E3B;
        border: 1px solid #059669;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>🌱 GROWW — Weekly Pulse Generator</h1>
    <p>Transforming Play Store Reviews into Strategic Customer Insights via Google Gemini 2.5 Flash LLM</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("⚙️ Pulse Controls")

weeks_option = st.sidebar.selectbox(
    "Time Window Filter",
    options=[12, 8, 4],
    format_func=lambda x: f"Past {x//4} Month(s) ({x} Weeks)",
    index=0
)

recipient_name = st.sidebar.text_input("Recipient Name", value="Samruddhi")
recipient_email = st.sidebar.text_input("Target Email", value="borasamruddhi19@gmail.com")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Execution Model**: Strictly On-Demand & User-Triggered. Click 'Generate Pulse' to fetch & analyze reviews in real-time.")

generate_btn = st.sidebar.button("⚡ Generate Weekly Pulse", type="primary", use_container_width=True)

# Session State for Pulse Storage
if "pulse_data" not in st.session_state:
    st.session_state.pulse_data = None
if "meta_data" not in st.session_state:
    st.session_state.meta_data = None

# Action: Generate Pulse
if generate_btn or st.session_state.pulse_data is None:
    with st.spinner("Ingesting Play Store Reviews, Scrubbing PII & Synthesizing Pulse via Gemini LLM..."):
        try:
            review_data = fetch_groww_reviews(max_count=200, weeks_back=weeks_option, min_words=5)
            res = generate_weekly_pulse(review_data["reviews"])
            
            st.session_state.pulse_data = res.get("weeklyPulse", {})
            st.session_state.meta_data = review_data.get("meta", {})
            st.toast("Weekly Pulse generated successfully!", icon="🌱")
        except Exception as e:
            st.error(f"Error generating weekly pulse: {e}")

pulse = st.session_state.pulse_data
meta = st.session_state.meta_data

if pulse and meta:
    # Summary Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{meta.get('totalFetched', 0)}</div><div class="metric-label">High-Signal Reviews</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{meta.get('avgRating', '4.3')} / 5.0</div><div class="metric-label">Avg Rating</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{meta.get('piiScrubbedCount', 0)}</div><div class="metric-label">PII Redacted</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{weeks_option} Weeks</div><div class="metric-label">Time Window</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Headline Box
    headline = pulse.get("metadata", {}).get("summaryHeadline", "GROWW Executive Pulse")
    st.subheader("📌 Executive Headline")
    st.info(headline)

    # Main Grid Layout
    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.subheader("🔥 Top 3-5 Core Customer Themes")
        themes = pulse.get("topThemes", [])
        for t in themes:
            sentiment_color = "#34D399" if t.get("sentiment") == "POSITIVE" else "#F87171" if t.get("sentiment") == "NEGATIVE" else "#FBBF24"
            st.markdown(f"""
            <div class="theme-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-weight:bold; font-size:1.05rem; color:#F9FAFB;">{t.get('themeName')}</span>
                    <span style="background:#064E3B; color:{sentiment_color}; padding:2px 8px; border-radius:12px; font-size:0.8rem; font-weight:bold;">
                        {t.get('percentage')}% • {t.get('sentiment')}
                    </span>
                </div>
                <p style="color:#D1D5DB; margin:0 0 8px 0; font-size:0.9rem;">{t.get('summary')}</p>
                <div style="color:#9CA3AF; font-size:0.8rem;"><b>Drivers:</b> {', '.join(t.get('keyDrivers', []))}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.subheader("💬 Authentic User Quotes (PII Scrubbed)")
        quotes = pulse.get("userQuotes", [])
        for q in quotes:
            stars = "★" * int(q.get("rating", 1))
            st.markdown(f"""
            <div class="quote-card">
                <div style="color:#F59E0B; font-size:0.8rem; margin-bottom:4px;">{stars} | {q.get('category')} (Ref: {q.get('id')})</div>
                <div style="color:#E5E7EB; font-size:0.9rem;">"{q.get('quote')}"</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("💡 Strategic Action Ideas")
        actions = pulse.get("actionIdeas", [])
        for a in actions:
            st.markdown(f"""
            <div class="action-card">
                <div style="color:#A7F3D0; font-size:0.85rem; font-weight:bold;">[{a.get('team')}] — Impact: {a.get('impact')}</div>
                <div style="color:#F9FAFB; font-size:0.9rem; margin-top:4px;">{a.get('action')}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Section 4: Email Dispatcher Modal / Form
    st.subheader("✉️ Email Dispatch Center")

    # Generate HTML content using email service module
    html_email = build_html_email(pulse, meta, recipient_name=recipient_name)

    e1, e2 = st.columns([1, 1])

    with e1:
        st.markdown(f"**Target Recipient:** `{recipient_name}` (`{recipient_email}`)")
        send_email_btn = st.button("🚀 Dispatch Email Now", type="primary", use_container_width=True)

        if send_email_btn:
            with st.spinner(f"Dispatching pulse email to {recipient_email}..."):
                res = send_pulse_email(
                    recipient=recipient_email,
                    subject=f"[Weekly Pulse] GROWW Play Store Insights - {meta.get('timeframe', 'Past 3 Months')}",
                    html_content=html_email
                )
                if res.get("mode") == "SMTP":
                    st.success(f"✅ Email successfully dispatched to {recipient_email} via SMTP!")
                else:
                    st.warning(f"📝 Local Draft Saved: {res.get('message')}")

    with e2:
        st.download_button(
            label="📥 Download Personalized HTML Email Draft",
            data=html_email,
            file_name=f"groww_pulse_{recipient_name.lower().replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True
        )

    # HTML Preview Expander
    with st.expander("👁️ Preview Rendered HTML Email Draft"):
        st.components.v1.html(html_email, height=600, scrolling=True)
