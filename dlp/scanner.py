from gliner import GLiNER
import logging

logger = logging.getLogger(__name__)

_model = None

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


def get_model():
    global _model

    if _model is not None:
        logger.info("GLiNER already loaded.")
        return _model

    logger.info("Loading GLiNER...")

    _model = GLiNER.from_pretrained(
        "urchade/gliner_small-v2.1"
    )

    logger.info("GLiNER loaded.")

    return _model


def detect_entities(text: str):

    model = get_model()

    return model.predict_entities(
        text,
        LABELS
    )
