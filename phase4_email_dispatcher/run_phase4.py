"""
Phase 4: Standalone Runner
Loads Phase 2 Weekly Pulse output, renders the HTML email template,
and dispatches email via SMTP or outputs a local HTML draft file.
"""

import json
import os
import sys

# Ensure root directory is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from phase4_email_dispatcher.email_service import build_html_email, send_pulse_email, format_recipient_name

def run_phase4(recipient: str = "product-team@groww.in", recipient_name: str = None):
    print("====================================================")
    print("   PHASE 4: EMAIL DRAFTING & DISPATCH ENGINE        ")
    print("====================================================\n")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    phase2_path = os.path.join(os.path.dirname(current_dir), "phase2_llm_intelligence", "phase2_output.json")
    phase1_path = os.path.join(os.path.dirname(current_dir), "phase1_ingestion", "fetched_groww_reviews.json")

    if not os.path.exists(phase2_path):
        print(f"Phase 2 output file not found at {phase2_path}. Running Phase 2 first...")
        from phase2_llm_intelligence.run_phase2 import run_phase2
        run_phase2()

    with open(phase2_path, "r", encoding="utf-8") as f:
        pulse = json.load(f)

    meta = {}
    if os.path.exists(phase1_path):
        with open(phase1_path, "r", encoding="utf-8") as f:
            meta = json.load(f).get("meta", {})

    rec_name = format_recipient_name(recipient_name, recipient)
    print(f"1. Rendering personalized single-page HTML email template (Hi {rec_name})...")
    html_content = build_html_email(pulse.get("weeklyPulse", pulse), meta, recipient_name=rec_name)

    subject = f"[Weekly Pulse] GROWW Play Store Customer Insights & Action Items"
    print(f"2. Dispatching email to: {recipient} ({rec_name})")
    res = send_pulse_email(recipient, subject, html_content)

    print("\n====================================================")
    print(f"[SUCCESS] {res.get('message')}")
    if res.get("draftPath"):
        print(f"   Draft Saved: {res.get('draftPath')}")
    print("====================================================\n")

if __name__ == "__main__":
    target_email = sys.argv[1] if len(sys.argv) > 1 else "product-team@groww.in"
    target_name = sys.argv[2] if len(sys.argv) > 2 else None
    run_phase4(recipient=target_email, recipient_name=target_name)
