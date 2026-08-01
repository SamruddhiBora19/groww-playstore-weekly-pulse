"""
Phase 3: FastAPI Routes for Web Dashboard UI
Handles API requests for generating pulse and retrieving raw reviews.
"""

from fastapi import APIRouter, Query, HTTPException
from phase1_ingestion import fetch_groww_reviews
from phase2_llm_intelligence import generate_weekly_pulse

router = APIRouter(prefix="/api", tags=["Dashboard"])

@router.get("/generate-pulse")
def generate_pulse_api(
    weeks: int = Query(12, ge=4, le=16, description="Timeframe in weeks (default: 12 weeks / 3 months)")
):
    """
    Triggers Phase 1 (Data Ingestion & PII Redaction) and Phase 2 (Groq LLM Intelligence)
    to return the complete One-Page Weekly Pulse in JSON format.
    """
    try:
        data = fetch_groww_reviews(max_count=200, weeks_back=weeks, min_words=5)
        pulse = generate_weekly_pulse(data["reviews"])
        
        return {
            "success": True,
            "meta": data["meta"],
            "pulse": pulse["weeklyPulse"],
            "rawReviews": data["reviews"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate pulse: {str(e)}")
