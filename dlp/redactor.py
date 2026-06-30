from typing import Tuple


def redact_text(
    text: str,
    entities: list
) -> Tuple[str, dict]:

    entities = sorted(
        entities,
        key=lambda e: e["start"],
        reverse=True
    )

    counters = {}

    mapping = {}

    for entity in entities:

        label = entity["label"].upper()

        counters[label] = (
            counters.get(label, 0) + 1
        )

        placeholder = (
            f"[{label}_{counters[label]}]"
        )

        original = text[
            entity["start"]:
            entity["end"]
        ]

        mapping[placeholder] = original

        text = (
            text[:entity["start"]]
            + placeholder
            + text[entity["end"]:]
        )

    return text, mapping