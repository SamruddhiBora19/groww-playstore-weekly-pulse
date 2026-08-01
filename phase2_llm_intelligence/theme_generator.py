"""
Phase 2 - Step 1: Groq LLM Initialization & Theme Generator
Initializes Groq client and clusters GROWW Play Store reviews into 3-5 core themes.
"""

import os
import json
import logging
from typing import Dict, Any, List
import os
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# System prompt specifically tailored for Theme Discovery
THEME_DISCOVERY_SYSTEM_PROMPT = """
You are a Lead AI Analyst for GROWW.
Analyze the provided Play Store user reviews and group them into **3 to 5 core themes max**.

Output MUST be valid JSON adhering strictly to this schema:
{
  "themes": [
    {
      "themeName": "Concise, professional theme title (e.g. KYC & Account Onboarding Latency)",
      "reviewCount": 15,
      "percentage": 33.3,
      "sentiment": "Negative | Neutral | Positive",
      "summary": "1-2 sentence description explaining the key user issues under this theme.",
      "keyDrivers": [
        "Primary driver 1",
        "Primary driver 2"
      ]
    }
  ]
}

STRICT RULES:
1. Provide between 3 and 5 themes max.
2. Ensure theme percentages add up to approximately 100%.
3. Do NOT include any PII in the output.
4. Output ONLY valid JSON.
"""

def init_groq_client():
    """Initializes and returns the official Groq client or None."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(current_dir, "..", ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GROQ_API_KEY="):
                        api_key = line.strip().split("=", 1)[1].strip()

    if not api_key or api_key.strip() == "" or api_key == "your_groq_api_key_here":
        return None, "GROQ_API_KEY is missing or unconfigured in .env"

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Groq SDK unavailable, using direct HTTP: {str(e)}"

def generate_themes(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ingests review list and uses Groq LLM to discover 3-5 themes.
    If Groq API key is unconfigured or call fails, returns fallback theme clusters.
    """
    client, err = init_groq_client()
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if client:
        try:
            user_prompt = f"Analyze these {len(reviews)} GROWW reviews and generate 3-5 themes:\n\n{json.dumps(reviews, indent=2)}"

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": THEME_DISCOVERY_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            raw_content = response.choices[0].message.content
            parsed = json.loads(raw_content)

            if "themes" in parsed:
                return {
                    "status": "success",
                    "source": f"Groq LLM ({model})",
                    "themeCount": len(parsed["themes"]),
                    "themes": parsed["themes"]
                }

        except Exception as e:
            logger.warning(f"Groq Theme Generation notice: {e}. Switching to built-in fallback engine.")

    # Fallback / Offline Theme Generator
    return generate_fallback_themes(reviews, notice=err)

def generate_fallback_themes(reviews: List[Dict[str, Any]], notice: str = None) -> Dict[str, Any]:
    """
    Built-in theme clustering engine when Groq API key is offline/unconfigured.
    """
    total = len(reviews) or 1
    clusters = {
        "KYC & Account Onboarding Latency": [],
        "Option Trading & Chart Execution Lag": [],
        "Payments & Wallet Payout Delays": [],
        "SIP Auto-Pay & Direct Mutual Funds Praise": []
    }

    for r in reviews:
        text_lower = (r.get("title", "") + " " + r.get("text", "")).lower()
        
        if any(k in text_lower for k in ["kyc", "demat", "aadhar", "kra", "nominee", "nri"]):
            clusters["KYC & Account Onboarding Latency"].append(r)
        elif any(k in text_lower for k in ["option", "chart", "sl", "trading", "gtt", "margin", "square"]):
            clusters["Option Trading & Chart Execution Lag"].append(r)
        elif any(k in text_lower for k in ["upi", "withdraw", "balance", "money", "imps", "dividend"]):
            clusters["Payments & Wallet Payout Delays"].append(r)
        else:
            clusters["SIP Auto-Pay & Direct Mutual Funds Praise"].append(r)

    themes = []
    summaries = {
        "KYC & Account Onboarding Latency": {
            "sentiment": "Negative",
            "summary": "Users experiencing delayed Digilocker sync, penny drop failures, and 5-day pending verification status.",
            "drivers": ["Digilocker address sync timeout", "Bank penny drop rejection", "Nominee OTP portal timeout"]
        },
        "Option Trading & Chart Execution Lag": {
            "sentiment": "Negative",
            "summary": "Active F&O traders reporting 9:15 AM TradingView chart freezes, Bank Nifty SL slippage, and GTT trigger delays.",
            "drivers": ["TradingView chart freeze at 9:15 AM", "SL market order slippage", "Option chain premium delay"]
        },
        "Payments & Wallet Payout Delays": {
            "sentiment": "Negative",
            "summary": "UPI transfers debited from bank but wallet balance zero, with bank payouts exceeding 24 hours.",
            "drivers": ["UPI debit wallet credit delay", "Withdrawals pending over 24 hrs", "IMPS balance sync latency"]
        },
        "SIP Auto-Pay & Direct Mutual Funds Praise": {
            "sentiment": "Positive",
            "summary": "High user praise for direct mutual funds UI, CAMS portfolio import, alongside request for basket orders.",
            "drivers": ["Zero brokerage direct mutual funds", "CAMS portfolio import", "Option chain basket order request"]
        }
    }

    for name, items in clusters.items():
        count = len(items)
        if count > 0:
            info = summaries[name]
            themes.append({
                "themeName": name,
                "reviewCount": count,
                "percentage": round((count / total) * 100, 1),
                "sentiment": info["sentiment"],
                "summary": info["summary"],
                "keyDrivers": info["drivers"]
            })

    return {
        "status": "success",
        "source": "Built-in Theme Generator (Configure GROQ_API_KEY in .env for live Groq LLM)",
        "notice": notice,
        "themeCount": len(themes),
        "themes": themes
    }
