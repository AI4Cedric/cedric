from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).parent

JSON_FILE = (
    BASE_DIR / "sensitive_terms.json"
)

with open(
    JSON_FILE,
    "r",
    encoding="utf-8"
) as f:

    CONFIG = json.load(f)

TERMS = CONFIG["terms"]

COMPILED_TERMS = []

for item in TERMS:

    COMPILED_TERMS.append(
        (
            re.compile(
                rf"\b{re.escape(item['term'])}\b",
                re.IGNORECASE
            ),
            item
        )
    )


def detect_sensitive_terms(
    text: str
):

    matches = []

    for pattern, item in COMPILED_TERMS:

        if pattern.search(text):

            matches.append(item)

    return matches