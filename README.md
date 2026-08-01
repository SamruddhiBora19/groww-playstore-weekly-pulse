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
- ✉️ **Interactive Personalized Email Dispatcher**: Personalization controls (`Hi {recipientName},`) in Web UI, Streamlit, and CLI with direct SMTP delivery or offline HTML draft export.
- ⚡ **Strict On-Demand Execution**: No background schedulers, cron tasks, or unwanted automation—runs solely on user request.

---

## 🏗️ 5-Phase System Architecture

```mermaid
flowchart TD
    subgraph UI Layer
        NEXT[Next.js React Dashboard :3000]
        ST[Streamlit App :8501]
        CLI[Python CLI : cli.py]
    end

    subgraph Backend Services (FastAPI :8000)
        API1[dashboard_routes.py : /api/generate-pulse]
        API2[email_routes.py : /api/send-email]
    end

    subgraph Core Pipeline Modules
        P1[phase1_ingestion : Scraper & PII Sanitizer]
        P2[phase2_llm_intelligence : Gemini 2.5 Flash]
        P4[phase4_email_dispatcher : SMTP & HTML Builder]
    end

    NEXT -->|API Requests| API1
    NEXT -->|Email Requests| API2
    ST -->|Direct Integration| P1 & P2 & P4
    CLI -->|Command Dispatcher| P1 & P2 & P4
    API1 --> P1 --> P2
    API2 --> P4
```

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

## 🚀 Quick Start Guide

### 1. Prerequisites & Installation

Clone the repository and install the Python dependencies:

```bash
git clone https://github.com/your-username/groww-playstore-weekly-pulse.git
cd groww-playstore-weekly-pulse

# Install Python requirements
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and set your **Google Gemini API Key**:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Required for Gemini LLM Inference
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Optional: Email Dispatch Configuration via SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

---

## 💻 Running the Application

You can interact with the system using any of the following interfaces:

### Option A: Streamlit Web App (Recommended for Quick Cloud Deployment)

Launch the single-file Streamlit web app on `http://localhost:8501`:

```bash
python cli.py streamlit
# or
streamlit run streamlit_app.py
```

### Option B: Next.js Dashboard + FastAPI Backend

1. **Start FastAPI Backend (Port 8000)**:
   ```bash
   python cli.py serve
   ```
2. **Start Next.js Web UI (Port 3000)**:
   ```bash
   python cli.py web
   ```

### Option C: Unified Python CLI (`cli.py`)

Run commands directly from your terminal:

```bash
# 1. Synthesize Pulse report in terminal
python cli.py pulse --weeks 12

# 2. Dispatch personalized HTML email
python cli.py email --to user@example.com --name "Samruddhi"

# 3. View CLI options
python cli.py --help
```

---

## 🌐 Deploying to Streamlit Community Cloud

Deploying to **Streamlit Community Cloud** requires **zero Node.js or server setup**:

1. Push your repository to GitHub.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and click **New App**.
3. Point to repository and set **Main file path** to `streamlit_app.py`.
4. Add your environment keys under **Advanced settings → Secrets**:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   SMTP_HOST = "smtp.gmail.com"
   SMTP_PORT = "587"
   SMTP_USER = "your_email@gmail.com"
   SMTP_PASS = "your_app_password"
   ```
5. Click **Deploy!**

---

## 🔒 PII Compliance & Security

Before reviews are sent to the Google Gemini LLM API, the `pii_sanitizer.py` engine strips:
- 📧 Email addresses
- 📞 Phone numbers (10-digit formats & country codes)
- 💳 Demat Account numbers & PAN card IDs
- 👤 Personal customer names & account handles

All verbatim quotes presented in the report and emails are guaranteed PII-free.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
