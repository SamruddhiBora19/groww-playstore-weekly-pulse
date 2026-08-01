"""
Phase 2: Standalone Runner
Loads Phase 1 sanitized reviews and executes Gemini LLM Weekly Pulse generation.
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

from phase2_llm_intelligence.gemini_service import generate_weekly_pulse

def run_phase2():
    print("====================================================")
    print("   PHASE 2: GEMINI LLM INTELLIGENCE PIPELINE        ")
    print("====================================================\n")

    # Load Phase 1 reviews
    current_dir = os.path.dirname(os.path.abspath(__file__))
    phase1_path = os.path.join(os.path.dirname(current_dir), "phase1_ingestion", "fetched_groww_reviews.json")

    if not os.path.exists(phase1_path):
        print(f"Phase 1 data file not found at {phase1_path}. Please run Phase 1 first.")
        return

    with open(phase1_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    reviews = data.get("reviews", [])
    print(f"1. Loaded {len(reviews)} sanitized GROWW reviews from Phase 1.")
    print("2. Generating Weekly Pulse with Gemini LLM (gemini-2.5-flash)...\n")

    pulse = generate_weekly_pulse(reviews)
    meta = pulse["weeklyPulse"]["metadata"]
    themes = pulse["weeklyPulse"]["topThemes"]
    quotes = pulse["weeklyPulse"]["userQuotes"]
    actions = pulse["weeklyPulse"]["actionIdeas"]

    print("====================================================")
    print(f"[PULSE NOTE] WEEKLY PULSE NOTE FOR {meta.get('product', 'GROWW')} ({meta.get('timeframe', 'Past 3 Months')})")
    print("====================================================")
    print(f"Headline: {meta.get('summaryHeadline', '')}\n")

    print("[TOP THEMES] TOP THEMES (3-5 Max):")
    for t in themes:
        print(f"  * {t.get('themeName')} [{t.get('percentage')}%] ({t.get('sentiment')})")
        print(f"    Summary: {t.get('summary')}\n")

    print("[USER QUOTES] 3 RECENT USER QUOTES:")
    for q in quotes:
        print(f"  * [{q.get('category')}] ({q.get('rating')} Stars) - Ref: {q.get('id')}")
        print(f"    \"{q.get('quote')}\"\n")

    print("[ACTION IDEAS] 3 STRATEGIC ACTION IDEAS:")
    for a in actions:
        print(f"  * [{a.get('team')}] Impact: {a.get('impact')}")
        print(f"    Action: {a.get('action')}\n")

    print("====================================================")
    print("[SUCCESS] PHASE 2 INTELLIGENCE PIPELINE COMPLETED!")
    print("====================================================\n")

if __name__ == "__main__":
    run_phase2()
