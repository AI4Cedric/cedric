from .rules import detect_patterns
from .scanner import detect_entities
from .classifier import classify_business
from .scoring import compute_score
from .context_detector import detect_sensitive_terms


def scan_prompt(text: str):

    patterns = detect_patterns(text)

    entities = detect_entities(text)

    categories = classify_business(text)

    sensitive_terms = detect_sensitive_terms(
        text
    )

    score, action = compute_score(
        patterns,
        entities,
        categories,
        sensitive_terms
    )

    return {
        "score": score,
        "action": action,
        "patterns": patterns,
        "entities": entities,
        "categories": categories,
        "sensitive_terms": sensitive_terms
    }