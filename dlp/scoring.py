def compute_score(
    patterns,
    entities,
    categories,
    sensitive_terms
):

    score = 0

    score += len(patterns) * 20

    score += len(entities) * 5

    score += len(categories) * 15

    for term in sensitive_terms:

        severity = term.get(
            "severity",
            "medium"
        )

        if severity == "low":
            score += 10

        elif severity == "medium":
            score += 20

        elif severity == "high":
            score += 40

        elif severity == "critical":
            score += 80

    if score >= 80:
        return score, "BLOCK"

    if score >= 40:
        return score, "WARN"

    return score, "ALLOW"