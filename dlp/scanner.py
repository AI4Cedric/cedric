from gliner import GLiNER

model = GLiNER.from_pretrained(
    "urchade/gliner_medium-v2.1"
)

LABELS = [
    "person",
    "organization",
    "email",
    "phone number",
    "address",
    "bank account",
    "credit card",
    "api key",
    "secret"
]


def detect_entities(text: str):

    entities = model.predict_entities(
        text,
        LABELS
    )

    return entities