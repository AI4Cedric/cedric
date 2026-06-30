import re

PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "iban": r"[A-Z]{2}[0-9]{2}[A-Z0-9]{10,30}",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "password": r"password\s*[:=]\s*\S+",
    "api_key": r"(sk-[A-Za-z0-9]{20,})"
}


def detect_patterns(text: str):

    findings = []

    for name, pattern in PATTERNS.items():

        if re.search(pattern, text):

            findings.append(name)

    return findings