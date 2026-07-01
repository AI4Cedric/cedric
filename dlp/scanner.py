import logging
import spacy

logger = logging.getLogger(__name__)

_model = None


def get_model():
    global _model

    if _model is None:

        logger.info("Loading spaCy model...")

        _model = spacy.load(
            #"en_core_web_sm"
            "fr_core_news_sm"
        )
        _model.add_pipe("entity_ruler", before="ner")
        logger.info("spaCy loaded.")

    return _model


LABEL_MAPPING = {
    "PERSON": "person",
    "ORG": "organization",
    "GPE": "address",
    "LOC": "address"
}


def detect_entities(text: str):

    model = get_model()

    doc = model(text)

    entities = []

    for ent in doc.ents:

        if ent.label_ not in LABEL_MAPPING:
            continue

        entities.append({
            "start": ent.start_char,
            "end": ent.end_char,
            "text": ent.text,
            "label": LABEL_MAPPING[ent.label_],
            "score": 1.0
        })

    return entities
