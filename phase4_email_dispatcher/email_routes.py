"""
Phase 4: FastAPI Router for UI Email Modal Trigger
Serves API endpoints to send emails or preview HTML drafts.
"""

import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from phase4_email_dispatcher.email_service import build_html_email, send_pulse_email, format_recipient_name

router = APIRouter(prefix="/api", tags=["Email"])

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def validate_recipient(email: str) -> str:
    cleaned = (email or "").strip()
    if not cleaned or not EMAIL_REGEX.match(cleaned):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid target email address: '{email}'. Please enter a valid email ID (e.g., user@example.com)."
        )
    return cleaned

class SendEmailRequest(BaseModel):
    recipient: str
    recipientName: Optional[str] = None
    subject: Optional[str] = "[Weekly Pulse] GROWW Play Store Reviews & Action Items"
    pulseData: Dict[str, Any]
    metaData: Dict[str, Any]

@router.post("/send-email")
def send_email_api(req: SendEmailRequest):
    """
    Triggers sending the Weekly Pulse HTML email directly to the recipient email ID specified from the Web UI.
    Includes personalized recipient greeting (Hi {recipientName}).
    """
    recipient = validate_recipient(req.recipient)
    rec_name = format_recipient_name(req.recipientName, recipient)
    try:
        html = build_html_email(req.pulseData, req.metaData, recipient_name=rec_name)
        res = send_pulse_email(recipient, req.subject, html)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to dispatch email to {recipient}: {str(e)}")

@router.post("/preview-email")
def preview_email_api(req: SendEmailRequest):
    """
    Returns rendered HTML string for live preview inside Web UI modal with personalized greeting.
    """
    recipient = validate_recipient(req.recipient)
    rec_name = format_recipient_name(req.recipientName, recipient)
    try:
        html = build_html_email(req.pulseData, req.metaData, recipient_name=rec_name)
        return {"success": True, "recipient": recipient, "recipientName": rec_name, "html": html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render preview: {str(e)}")

