"""
GROWW Play Store Review Weekly Pulse Generator - Unified Command Line Interface (CLI)

Commands:
  python cli.py pulse --weeks 12
  python cli.py email --to borasamruddhi19@gmail.com --name "Samruddhi"
  python cli.py serve
  python cli.py web
"""

import sys
import os
import argparse
import json
import subprocess

# Ensure root directory is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def cmd_pulse(args):
    print("\n====================================================")
    print("   GROWW WEEKLY PULSE GENERATOR - CLI PULSE SYNTHESIS")
    print("====================================================\n")
    print(f"--> Ingesting Play Store reviews for past {args.weeks} weeks...")
    
    from phase1_ingestion import fetch_groww_reviews
    from phase2_llm_intelligence import generate_weekly_pulse

    review_data = fetch_groww_reviews(max_count=200, weeks_back=args.weeks, min_words=5)
    print(f"--> Fetched {review_data['meta']['totalFetched']} reviews ({review_data['meta']['piiScrubbedCount']} PII scrubbed).")
    print("--> Synthesizing Weekly Pulse via Google Gemini LLM...\n")
    
    res = generate_weekly_pulse(review_data["reviews"])
    pulse = res.get("weeklyPulse", {})

    print("====================================================")
    print(f"🌱 HEADLINE: {pulse.get('metadata', {}).get('summaryHeadline')}")
    print("====================================================\n")

    print("🔥 TOP THEMES:")
    for t in pulse.get("topThemes", []):
        print(f"  • {t.get('themeName')} ({t.get('percentage')}%) - [{t.get('sentiment')}]")
        print(f"    Summary: {t.get('summary')}")
        if t.get("keyDrivers"):
            print(f"    Drivers: {', '.join(t.get('keyDrivers'))}")
        print()

    print("💬 REAL USER QUOTES (PII Scrubbed):")
    for q in pulse.get("userQuotes", []):
        print(f"  [{'★' * int(q.get('rating', 1))}] ({q.get('category')}) Ref: {q.get('id')}")
        print(f"  \"{q.get('quote')}\"\n")

    print("💡 STRATEGIC ACTION IDEAS:")
    for a in pulse.get("actionIdeas", []):
        print(f"  • [{a.get('team')}] (Impact: {a.get('impact')}): {a.get('action')}")
    print("\n====================================================\n")

def cmd_email(args):
    recipient = args.to or input("Enter recipient email address: ").strip()
    name = args.name

    print("\n====================================================")
    print("   GROWW WEEKLY PULSE GENERATOR - EMAIL DISPATCH")
    print("====================================================\n")

    from phase4_email_dispatcher.run_phase4 import run_phase4
    run_phase4(recipient=recipient, recipient_name=name)

def cmd_serve(args):
    print("\n🚀 Starting GROWW FastAPI Backend Server on http://localhost:8000 ...\n")
    import uvicorn
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)

def cmd_web(args):
    nextjs_dir = os.path.join(root_dir, "phase5_nextjs_frontend")
    if not os.path.exists(nextjs_dir):
        print(f"❌ Next.js directory not found at {nextjs_dir}")
        return

    print("\n⚡ Starting Next.js Web UI Dev Server on http://localhost:3000 ...\n")
    try:
        subprocess.run("npm run dev", shell=True, cwd=nextjs_dir)
    except KeyboardInterrupt:
        print("\nStopping Next.js server.")

def cmd_streamlit(args):
    print("\n🎈 Launching GROWW Weekly Pulse Streamlit Web App on http://localhost:8501 ...\n")
    try:
        subprocess.run("streamlit run streamlit_app.py", shell=True, cwd=root_dir)
    except KeyboardInterrupt:
        print("\nStopping Streamlit server.")

def main():
    parser = argparse.ArgumentParser(
        description="GROWW Play Store Review Weekly Pulse Generator CLI",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Pulse Command
    pulse_parser = subparsers.add_parser("pulse", help="Generate Weekly Pulse report in terminal")
    pulse_parser.add_argument("--weeks", type=int, default=12, help="Timeframe in weeks (default: 12 weeks / 3 months)")

    # Email Command
    email_parser = subparsers.add_parser("email", help="Dispatch Weekly Pulse HTML email")
    email_parser.add_argument("--to", type=str, help="Target recipient email address")
    email_parser.add_argument("--name", type=str, help="Target recipient name (e.g. Samruddhi)")
    email_parser.add_argument("--weeks", type=int, default=12, help="Timeframe in weeks (default: 12)")

    # Serve Command
    serve_parser = subparsers.add_parser("serve", help="Start FastAPI Backend Server (port 8000)")
    serve_parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port number (default: 8000)")

    # Web Command
    web_parser = subparsers.add_parser("web", help="Start Phase 5 Next.js Web UI Dev Server (port 3000)")

    # Streamlit Command
    streamlit_parser = subparsers.add_parser("streamlit", help="Start Streamlit Web App (port 8501)")

    args = parser.parse_args()

    if args.command == "pulse":
        cmd_pulse(args)
    elif args.command == "email":
        cmd_email(args)
    elif args.command == "serve":
        cmd_serve(args)
    elif args.command == "web":
        cmd_web(args)
    elif args.command == "streamlit":
        cmd_streamlit(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
