"""
GROWW Play Store Review Weekly Pulse Generator - Main Unified Server Entry Point
Includes modular phase routes:
  - Phase 1: Data Ingestion & PII Anonymization
  - Phase 2: Groq LLM Intelligence Engine
  - Phase 3: Interactive One-Page Web Dashboard
  - Phase 4: UI Email Dispatcher & Drafting Engine
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from phase3_web_dashboard import dashboard_router
from phase4_email_dispatcher import email_router

app = FastAPI(
    title="GROWW Play Store Review Weekly Pulse Generator",
    description="Python FastAPI service turning recent GROWW Play Store reviews into a One-Page Weekly Pulse using Groq LLM",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Phase API Routers
app.include_router(dashboard_router)
app.include_router(email_router)

# Mount Phase 3 Web UI Static Files
static_dir = os.path.join(os.path.dirname(__file__), "phase3_web_dashboard", "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting GROWW Weekly Pulse Server on http://localhost:8000 ...\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
