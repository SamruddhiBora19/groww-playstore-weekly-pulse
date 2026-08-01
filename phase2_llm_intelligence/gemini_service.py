"""
Phase 2: Gemini LLM Service Component
Interfaces with Google Gemini API (gemini-2.5-flash) to cluster GROWW reviews into 3-5 themes,
extract 3 verbatim user quotes, and synthesize 3 strategic action ideas.
Includes fallback support for Groq API and local deterministic intelligence engine.
"""

import json
import os
import sys
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    def load_dotenv():
        pass

from phase2_llm_intelligence.prompt_templates import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

def get_gemini_config():
    """Reads GEMINI_API_KEY and GEMINI_MODEL from os.environ or .env file."""
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY", "")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not key or key == "your_gemini_api_key_here":
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for env_path in [
            os.path.join(current_dir, ".env"),
            os.path.join(current_dir, "..", ".env"),
        ]:
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            if k.strip() == "GEMINI_API_KEY":
                                key = v.strip()
                            elif k.strip() == "GEMINI_MODEL":
                                model = v.strip()

    return key, model

def generate_weekly_pulse(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generates the One-Page Weekly Pulse using Google Gemini LLM.
    Falls back to Groq or deterministic engine if GEMINI_API_KEY is unconfigured or fails.
    """
    api_key, model = get_gemini_config()

    print(f"[Gemini Service] Checking Gemini API Key... Loaded: {'Yes (' + api_key[:8] + '...)' if (api_key and api_key != 'your_gemini_api_key_here') else 'No (using fallback)'}")

    if api_key and api_key.strip() and api_key != "your_gemini_api_key_here":
        # 1. Try google-genai SDK if available
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = SYSTEM_PROMPT + "\n\n" + build_user_prompt(reviews)

            print(f"[Gemini Service] Sending request via google-genai SDK ({model}) with {len(reviews)} reviews...")
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            parsed = json.loads(response.text)
            print("[Gemini Service] [SUCCESS] Successfully received live response from Gemini LLM via SDK!")
            parsed.setdefault("weeklyPulse", {}).setdefault("metadata", {})["source"] = "LIVE_GEMINI_LLM"
            parsed["weeklyPulse"]["metadata"]["model"] = model
            return parsed if "weeklyPulse" in parsed else {"weeklyPulse": parsed}
        except ImportError:
            pass
        except Exception as e:
            print(f"[Gemini Service Warning] Gemini SDK call error: {e}. Trying direct REST API endpoint...")

        # 2. Direct HTTP call via urllib to Gemini REST API (zero external dependencies)
        try:
            prompt_text = SYSTEM_PROMPT + "\n\n" + build_user_prompt(reviews)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            print(f"[Gemini Service] Sending direct REST request to Gemini API ({model}) with {len(reviews)} reviews...")

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt_text}
                        ]
                    }
                ],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "temperature": 0.2
                }
            }

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "GrowwPulse/1.0"
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(raw_text)
                print("[Gemini Service] [SUCCESS] Successfully received live response from Gemini LLM via REST API!")
                if "weeklyPulse" not in parsed:
                    parsed = {"weeklyPulse": parsed}
                parsed["weeklyPulse"]["metadata"]["source"] = "LIVE_GEMINI_LLM"
                parsed["weeklyPulse"]["metadata"]["model"] = model
                return parsed
        except Exception as e:
            print(f"[Gemini Service Warning] Gemini HTTP call error: {e}. Trying Groq/Fallback engine...")
            logger.warning(f"Gemini API call notice ({e}). Trying fallback intelligence engine.")

    # 3. Fallback to Groq if available
    from phase2_llm_intelligence.groq_service import generate_weekly_pulse as generate_groq_pulse
    return generate_groq_pulse(reviews)
