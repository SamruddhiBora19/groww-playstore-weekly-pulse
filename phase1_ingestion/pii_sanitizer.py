"""
Phase 1: PII Sanitizer Engine for GROWW Play Store Reviews (Python)
Redacts personal identifiable information (emails, phone numbers, account IDs, names, links)
to ensure complete privacy compliance before sending data to Groq LLM.
"""

import re
from typing import List, Dict, Any, Tuple

# PII Patterns definition
PII_PATTERNS: List[Tuple[str, re.Pattern, str]] = [
    # Email addresses
    (
        "email",
        re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", re.IGNORECASE),
        "[REDACTED_EMAIL]"
    ),
    # Indian phone numbers (+91-XXXXX-XXXXX, 0XXXXXXXXXX, 9876543210)
    (
        "phone",
        re.compile(r"(?:\+?91[\-\s]?)?[6-9]\d{9}\b"),
        "[REDACTED_PHONE]"
    ),
    # Formatted phone numbers (9876-543-210)
    (
        "formatted_phone",
        re.compile(r"\b\d{4}[\-\s]\d{3}[\-\s]\d{3}\b"),
        "[REDACTED_PHONE]"
    ),
    # PAN Card pattern (5 letters + 4 digits + 1 letter, e.g. ABCDE1234F)
    (
        "pan",
        re.compile(r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", re.IGNORECASE),
        "[REDACTED_PAN]"
    ),
    # Demat / Folio / Account / Order / Client ID
    (
        "account_id",
        re.compile(r"\b(?:demat|folio|account|order|client\s*id|usr|id)\s*[:#\-]?\s*([a-z0-9]{6,16})\b", re.IGNORECASE),
        "[REDACTED_ACCOUNT_ID]"
    ),
    # Social media @mentions
    (
        "social_mention",
        re.compile(r"@[a-zA-Z0-9_]{3,}"),
        "[REDACTED_USER]"
    ),
    # URLs and web links
    (
        "url",
        re.compile(r"https?://[^\s]+|www\.[^\s]+", re.IGNORECASE),
        "[REDACTED_URL]"
    ),
    # Self identification ("my name is John Doe", "I am Rahul Sharma")
    (
        "name_intro",
        re.compile(r"(?:my name is|i am|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", re.IGNORECASE),
        "[REDACTED_NAME]"
    ),
    # Sign-off ("Regards, Amit Kumar", "Thanks, Priya S")
    (
        "sign_off",
        re.compile(r"(?:regards|thanks|thanking you|yours sincerely|cheers),?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", re.IGNORECASE),
        "[REDACTED_NAME]"
    )
]

def sanitize_text(text: str) -> str:
    """Sanitizes a single text string by replacing PII patterns."""
    if not text or not isinstance(text, str):
        return text or ""

    sanitized = text
    for name, pattern, replacement in PII_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)

    # Normalize whitespace
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized
