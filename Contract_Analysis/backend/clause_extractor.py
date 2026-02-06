import re
from typing import List, Dict, Optional


# -------------------------------------------------------------------
# CONFIG: keyword banks (extendable, no external legal data)
# -------------------------------------------------------------------

CLAUSE_KEYWORDS = [
    "duration", "term", "tenure",
    "rent", "rental", "payment", "fees", "charges",
    "deposit", "security",
    "termination", "cancellation", "exit",
    "maintenance", "repairs",
    "liability", "indemnity",
    "confidentiality", "non disclosure",
    "jurisdiction", "governing law",
    "dispute", "arbitration",
    "sublet", "subletting", "assignment",
    "usage", "use of premises",
    "electricity", "water",
    "penalty", "damages",
    "lock in", "renewal",
    "intellectual property", "ip",
    "force majeure",
    "notice",
    "ownership",
    "insurance",
    "compliance",
    "warranty",
    "termination of agreement",
]

NOISE_PATTERNS = [
    r"signature",
    r"witness",
    r"signed",
    r"page\s*\d+",
    r"telephone",
    r"fax",
    r"email",
    r"by\s*[:\-]\s*_+",
    r"address",
]

SCHEDULE_WORDS = ["schedule", "annexure", "appendix", "exhibit"]


# -------------------------------------------------------------------
# TEXT NORMALIZATION
# -------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Heavy-duty normalization for OCR + translated docs
    """

    if not text:
        return ""

    # Fix spaced capitals: C O M M I S S I O N
    text = re.sub(
        r'(?<!\w)(?:[A-Z]\s){2,}[A-Z]',
        lambda m: m.group().replace(" ", ""),
        text
    )

    # Normalize punctuation
    text = text.replace("—", "-").replace("–", "-")

    # Fix broken numbering: 1 . Duration
    text = re.sub(r'(\d)\s*\.\s*', r'\1. ', text)

    # Normalize Hindi artifacts (basic)
    text = text.replace("किरायेदार", "tenant").replace("मकान", "property")

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# -------------------------------------------------------------------
# UTILITIES
# -------------------------------------------------------------------

def is_noise(text: str) -> bool:
    text = text.lower()
    return any(re.search(p, text) for p in NOISE_PATTERNS)


def looks_like_heading(text: str) -> bool:
    """
    Detect ALL CAPS or Title Case headings
    """
    text = text.strip()
    if len(text) < 4:
        return False

    if text.isupper():
        return True

    # Title Case heuristic
    words = text.split()
    if len(words) <= 6 and sum(w[0].isupper() for w in words) >= len(words) - 1:
        return True

    return False


def keyword_in_text(text: str) -> Optional[str]:
    for kw in CLAUSE_KEYWORDS:
        if kw in text.lower():
            return kw
    return None


# -------------------------------------------------------------------
# PRIMARY CLAUSE REGEX (NUMBERED)
# -------------------------------------------------------------------

NUMBERED_CLAUSE_REGEX = re.compile(
    r'(?P<num>\d{1,2})\s*[\.\:\)]\s*'
    r'(?P<title>[A-Za-z][A-Za-z\s&/\-]{2,60})\s*:',
    re.IGNORECASE
)

ROMAN_CLAUSE_REGEX = re.compile(
    r'(?P<num>[IVXLC]+)\s*[\.\:\)]\s*'
    r'(?P<title>[A-Za-z][A-Za-z\s&/\-]{2,60})',
    re.IGNORECASE
)


# -------------------------------------------------------------------
# STAGE 1: STRICT NUMBERED EXTRACTION
# -------------------------------------------------------------------

def extract_numbered_clauses(text: str) -> List[Dict]:
    clauses = []
    matches = list(NUMBERED_CLAUSE_REGEX.finditer(text))

    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        title = f"{m.group('num')}. {m.group('title').strip()}"
        body = text[m.end():end].strip()

        if body and not is_noise(body):
            clauses.append({
                "title": title,
                "text": body,
                "confidence": 0.95
            })

    return clauses


# -------------------------------------------------------------------
# STAGE 2: ROMAN NUMERAL CLAUSES
# -------------------------------------------------------------------

def extract_roman_clauses(text: str) -> List[Dict]:
    clauses = []
    matches = list(ROMAN_CLAUSE_REGEX.finditer(text))

    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        title = f"{m.group('num')}. {m.group('title').strip()}"
        body = text[m.end():end].strip()

        clauses.append({
            "title": title,
            "text": body,
            "confidence": 0.9
        })

    return clauses


# -------------------------------------------------------------------
# STAGE 3: HEADING-BASED EXTRACTION
# -------------------------------------------------------------------

def extract_heading_blocks(text: str) -> List[Dict]:
    blocks = re.split(r'\n{2,}', text)
    clauses = []
    current = None

    for block in blocks:
        clean = block.strip()
        if not clean or is_noise(clean):
            continue

        if looks_like_heading(clean):
            if current:
                clauses.append(current)
            current = {"title": clean, "text": "", "confidence": 0.8}
        else:
            if current:
                current["text"] += " " + clean

    if current:
        clauses.append(current)

    return clauses


# -------------------------------------------------------------------
# STAGE 4: INLINE / SENTENCE HEURISTICS
# -------------------------------------------------------------------

def extract_inline_clauses(text: str) -> List[Dict]:
    clauses = []
    sentences = re.split(r'(?<=[.;])\s+', text)
    current = None

    for sent in sentences:
        kw = keyword_in_text(sent)
        if kw:
            if current:
                clauses.append(current)

            current = {
                "title": kw.capitalize(),
                "text": sent,
                "confidence": 0.6
            }
        else:
            if current:
                current["text"] += " " + sent

    if current:
        clauses.append(current)

    return clauses


# -------------------------------------------------------------------
# STAGE 5: SCHEDULE / ANNEXURE HANDLING
# -------------------------------------------------------------------

def extract_schedules(text: str) -> List[Dict]:
    clauses = []
    lower = text.lower()

    for word in SCHEDULE_WORDS:
        if word in lower:
            idx = lower.index(word)
            clauses.append({
                "title": word.capitalize(),
                "text": text[idx:],
                "confidence": 0.7
            })
            break

    return clauses


# -------------------------------------------------------------------
# MASTER EXTRACTOR
# -------------------------------------------------------------------

def extract_clauses(contract_text: str) -> List[Dict]:
    """
    Master clause extractor.
    Multi-pass, defensive, real-world safe.
    """

    text = normalize_text(contract_text)
    if not text:
        return []

    # 1. Strict numbered clauses
    clauses = extract_numbered_clauses(text)
    if len(clauses) >= 3:
        return clauses

    # 2. Roman numerals
    clauses = extract_roman_clauses(text)
    if len(clauses) >= 3:
        return clauses

    # 3. Heading blocks
    clauses = extract_heading_blocks(text)
    if len(clauses) >= 3:
        return clauses

    # 4. Inline heuristics (Hindi / translated)
    clauses = extract_inline_clauses(text)
    if len(clauses) >= 2:
        return clauses

    # 5. Schedule fallback
    clauses = extract_schedules(text)
    if clauses:
        return clauses

    # 6. Absolute fallback
    return [{
        "title": "Agreement",
        "text": text,
        "confidence": 0.4
    }]
def normalize_title(title, text):
    t = title.lower()
    if "terminate" in text.lower():
        return "Termination"
    if "payment" in text.lower():
        return "Payment Terms"
    if "indemn" in text.lower():
        return "Indemnity & Liability"
    if "confidential" in text.lower():
        return "Confidentiality"
    if "non compete" in text.lower() or "shall not engage" in text.lower():
        return "Non-Compete"
    return title
