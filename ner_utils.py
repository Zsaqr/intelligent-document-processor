# ner_utils.py
from typing import List, Dict
import spacy

# Simple in-memory cache so we don't load the model multiple times
_nlp_cache = {}


def load_model(model_name: str = "en_core_web_sm"):
    """
    Loads a spaCy model and caches it.
    """
    if model_name not in _nlp_cache:
        _nlp_cache[model_name] = spacy.load(model_name)
    return _nlp_cache[model_name]


def extract_entities(text: str, model_name: str = "en_core_web_sm") -> List[Dict]:
    """
    Runs NER on the given text and returns a list of entities with spans.
    """
    nlp = load_model(model_name)
    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        entities.append(
            {
                "text": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
            }
        )
    return entities
