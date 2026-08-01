# 🌱 GROWW Play Store Review Weekly Pulse Generator

> **Transforming Play Store Customer Feedback into Strategic Executive Intelligence via Google Gemini LLM**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=next.js&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)

---

## 📌 Problem Statement & Goal

**GROWW** is a leading investment and financial platform with thousands of user reviews on the Google Play Store. 

This project ingests raw user reviews from the **past 3 months (12 weeks)**, automatically redacts all **Personally Identifiable Information (PII)**, and leverages **Google Gemini 2.5 Flash LLM** to generate a **One-Page Weekly Pulse Executive Report**.

### Key Deliverables
- 🎯 **3–5 Core Customer Themes**: Percentage weightage, sentiment split (Positive / Negative / Mixed), and underlying key drivers.
- 💬 **3 Authentic Verbatim User Quotes**: Representative customer voices (PII-scrubbed).
- 💡 **3 Strategic Action Ideas**: Direct recommendations tailored for **Product/Growth**, **Customer Support**, and **Leadership** teams.
- ✉️ **Interactive Personalized Email Dispatcher**: Personalization controls (`Hi {recipientName},`) with direct SMTP delivery or offline HTML draft export.
- ⚡ **Strict On-Demand Execution**: No background schedulers or cron tasks—runs solely on user request.

---

## 🏗️ 5-Phase System Architecture

The system is organized into 5 modular, self-contained phase directories:

- **Phase 1: Data Ingestion & PII Redaction (`phase1_ingestion/`)**: Scrapes raw GROWW Play Store user reviews, sanitizes all PII (emails, phones, Demat/PAN IDs, names), and filters high-signal feedback.
- **Phase 2: Gemini LLM Intelligence (`phase2_llm_intelligence/`)**: Sends sanitized reviews to Google Gemini 2.5 Flash LLM to cluster top themes, extract user quotes, and formulate action items.
- **Phase 3: FastAPI REST API Services (`phase3_web_dashboard/`)**: Exposes REST API endpoints (`/api/generate-pulse`) for frontend integration.
- **Phase 4: Personalised Email Dispatcher (`phase4_email_dispatcher/`)**: Formats responsive single-page HTML email drafts and dispatches via Gmail SMTP (`smtplib`).
- **Phase 5: Next.js Web UI & Streamlit Dashboard (`phase5_nextjs_frontend/` & `streamlit_app.py`)**: Modern web dashboard interfaces and CLI tools.

---

## 📁 Repository Structure

```text
groww playstore review weekly report/
│
├── README.md                        # Project Overview & Quick Start Guide
├── ARCHITECTURE.md                  # Detailed Technical Architecture Specifications
├── requirements.txt                 # Python Dependencies
├── main.py                          # Unified FastAPI REST Server Entrypoint (Port 8000)
├── streamlit_app.py                 # Turnkey Streamlit Web Application (Port 8501)
├── cli.py                           # Multi-command CLI Center (pulse, email, serve, web, streamlit)
├── fetched_groww_reviews.json       # Exported PII-Sanitized Review Dataset
├── .env.example                     # Environment Configuration Template
│
├── phase1_ingestion/                # Phase 1: Play Store Ingestion & PII Redaction Engine
├── phase2_llm_intelligence/         # Phase 2: Google Gemini LLM Pipeline & Prompts
├── phase3_web_dashboard/            # Phase 3: FastAPI REST API Dashboard Routes
├── phase4_email_dispatcher/         # Phase 4: HTML Email Builder & SMTP Transport Engine
└── phase5_nextjs_frontend/          # Phase 5: Next.js React Web UI Dashboard
```

---

## 🚀 How to Run

### 1. Setup & Environment
```bash
# Install requirements
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```
*(Add your `GEMINI_API_KEY` in `.env`)*

### 2. Run Commands

```bash
# Launch Streamlit Web App (Port 8501)
python cli.py streamlit

# Or Launch Next.js Dashboard (Port 3000) + FastAPI Backend (Port 8000)
python cli.py serve
python cli.py web

# Or Run in Terminal CLI Mode
python cli.py pulse --weeks 12
python cli.py email --to user@example.com --name "Samruddhi"
```

---

## 🔒 PII Compliance & Security

Before reviews are sent to the Google Gemini LLM API, the `pii_sanitizer.py` engine strips:
- 📧 Email addresses
- 📞 Phone numbers (10-digit formats & country codes)
- 💳 Demat Account numbers & PAN card IDs
- 👤 Personal customer names & account handles

  ##Live Demo - https://groww-weekly-pluse.streamlit.app/
