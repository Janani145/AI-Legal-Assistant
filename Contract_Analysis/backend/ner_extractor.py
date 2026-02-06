# backend/ner_extractor.py
# Phase 4: Named Entity Recognition (NER)
# SME-focused entities, no external legal DBs

import re
import spacy
from typing import Dict, List

def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # Fallback: blank English pipeline (NER via regex still works)
        nlp = spacy.blank("en")
        return nlp

nlp = load_spacy_model()

# -------------------------------
# Custom Regex for Legal Entities
# -------------------------------

MONEY_REGEX = r"(₹|\$|rs\.?)\s?\d+(?:,\d+)*(?:\.\d+)?"
DATE_REGEX = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
PERCENT_REGEX = r"\b\d{1,2}%\b"

JURISDICTION_KEYWORDS = [
    "india", "tamil nadu", "karnataka",
    "delhi", "mumbai", "chennai",
    "jurisdiction", "courts at"
]

# -------------------------------
# Core NER Function
# -------------------------------

def extract_entities(text: str) -> Dict[str, List[str]]:
    doc = nlp(text)

    entities = {
        "Parties": set(),
        "Dates": set(),
        "Money": set(),
        "Locations": set(),
        "Percentages": set(),
        "Jurisdiction": set(),
    }

    # spaCy entities
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["Parties"].add(ent.text)
        elif ent.label_ == "DATE":
            entities["Dates"].add(ent.text)
        elif ent.label_ in ("GPE", "LOC"):
            entities["Locations"].add(ent.text)
        elif ent.label_ == "MONEY":
            entities["Money"].add(ent.text)

    # Regex-based (legal docs are messy)
    for m in re.findall(MONEY_REGEX, text, flags=re.IGNORECASE):
        entities["Money"].add(m)

    for d in re.findall(DATE_REGEX, text):
        entities["Dates"].add(d)

    for p in re.findall(PERCENT_REGEX, text):
        entities["Percentages"].add(p)

    lower = text.lower()
    for j in JURISDICTION_KEYWORDS:
        if j in lower:
            entities["Jurisdiction"].add(j.title())

    # Convert sets → lists
    return {k: sorted(list(v)) for k, v in entities.items()}

