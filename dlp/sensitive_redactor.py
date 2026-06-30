import re


def redact_sensitive_terms(
    text,
    sensitive_terms
):

    counters = {}

    for term in sensitive_terms:

        category = (
            term["category"]
            .upper()
        )

        counters[category] = (
            counters.get(
                category,
                0
            ) + 1
        )

        placeholder = (
            f"[{category}_{counters[category]}]"
        )

        text = re.sub(
            rf"\b{re.escape(term['term'])}\b",
            placeholder,
            text,
            flags=re.IGNORECASE
        )

    return text