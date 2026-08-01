"""
Phase 1: Standalone Runner and Data Exporter
Fetches GROWW reviews for the past 3 months, scrubs PII, and exports to fetched_groww_reviews.json
"""

import json
import os
from phase1_ingestion.scraper import fetch_groww_reviews

def run_phase1():
    print("====================================================")
    print("   PHASE 1: DATA INGESTION & PII ANONYMIZATION     ")
    print("====================================================\n")

    print("Fetching GROWW Play Store reviews for the PAST THREE MONTHS (Filter: > 5 words, PII Scrubbed)...")
    data = fetch_groww_reviews(max_count=200, weeks_back=12, min_words=5)
    
    # Save to phase1_ingestion directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "fetched_groww_reviews.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Phase 1 Complete!")
    print("----------------------------------------------------")
    print(f"App Name:          {data['meta']['appName']}")
    print(f"Timeframe:         {data['meta']['timeframe']} (Cutoff: {data['meta']['cutoffDate']})")
    print(f"Total Unique:      {data['meta']['totalFetched']} reviews")
    print(f"Average Rating:    {data['meta']['avgRating']} / 5.0")
    print(f"PII Scrubbed:      {data['meta']['piiScrubbedCount']} reviews")
    print(f"Export Path:       {output_path}")
    print("----------------------------------------------------\n")

if __name__ == "__main__":
    run_phase1()
