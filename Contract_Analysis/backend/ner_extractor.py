# backend/ner_extractor.py
# Cloud-safe Legal NER (spaCy optional, regex primary)

import re
from typing import Dict, List

# -------------------------------------------------
# REGEX PATTERNS (PRIMARY – ALWAYS WORKS)
# -------------------------------------------------

DATE_REGEX = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
MONEY_REGEX = r"(₹|\$|rs\.?)\s?\d+(?:,\d+)*(?:\.\d+)?"
PERCENT_REGEX = r"\b\d{1,3}%\b"

ORG_HINTS = [
    "pvt", "private limited", "ltd", "limited",
    "solutions", "technologies", "enterprises",
    "company", "firm"
]

JURISDICTION_HINTS = [
    "courts at", "jurisdiction", "governed by",
    "india", "tamil nadu", "karnataka",
    "chennai", "bengaluru", "bangalore",
    "mumbai", "delhi"
]

# -------------------------------------------------
# OPTIONAL spaCy (ONLY IF AVAILABLE)
# -------------------------------------------------

def load_spacy():
    try:
        import spacy
        return spacy.load("en_core_web_sm")
    except Exception:
        return None

nlp = load_spacy()

# -------------------------------------------------
# MAIN ENTITY EXTRACTION
# -------------------------------------------------

def extract_entities(text: str) -> Dict[str, List[str]]:
    entities = {
        "Parties": set(),
        "Dates": set(),
        "Money": set(),
        "Percentages": set(),
        "Jurisdiction": set(),
    }

    lower = text.lower()

    # -------- REGEX BASED (ALWAYS WORKS) --------

    for d in re.findall(DATE_REGEX, text):
        entities["Dates"].add(d)

    for m in re.findall(MONEY_REGEX, text, flags=re.IGNORECASE):
        entities["Money"].add(m)

    for p in re.findall(PERCENT_REGEX, text):
        entities["Percentages"].add(p)

    for j in JURISDICTION_HINTS:
        if j in lower:
            entities["Jurisdiction"].add(j.title())

    # -------- HEURISTIC PARTY DETECTION --------

    lines = text.splitlines()
    for line in lines:
        l = line.lower()
        if any(h in l for h in ORG_HINTS):
            clean = line.strip()
            if len(clean) < 120:
                entities["Parties"].add(clean)

    # -------- spaCy (ENHANCEMENT ONLY) --------

    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                entities["Parties"].add(ent.text)
            elif ent.label_ == "GPE":
                entities["Jurisdiction"].add(ent.text)
            elif ent.label_ == "DATE":
                entities["Dates"].add(ent.text)
            elif ent.label_ == "MONEY":
                entities["Money"].add(ent.text)

    return {k: sorted(v) for k, v in entities.items()}
