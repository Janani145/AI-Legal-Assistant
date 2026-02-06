# backend/risk_analyzer.py
# Phase 6: Obligation + Risk + Unfavorable Clause Analysis
# Production-grade, hackathon-ready, edge-case safe

import re
from typing import List, Dict

# ==========================================================
# CONFIGURATION
# ==========================================================

OBLIGATION_WORDS = [
    "shall", "must", "is required to", "agrees to",
    "undertakes to", "is obligated to"
]

RIGHT_WORDS = [
    "may", "is entitled to", "has the right to",
    "at its discretion", "reserves the right"
]

PROHIBITION_WORDS = [
    "shall not", "must not", "is prohibited from",
    "may not", "will not"
]

# High-risk legal indicators (SME-unfriendly)
HIGH_RISK_PATTERNS = [
    r"terminate.*without notice",
    r"sole discretion",
    r"unilateral",
    r"penalty",
    r"liquidated damages",
    r"indemnif(y|ication)",
    r"hold harmless",
    r"non[-\s]?compete",
    r"perpetual",
    r"irrevocable",
    r"without assigning any reason",
    r"withhold payment",
    r"exclusive property",
    r"waives all rights",
]

# Medium-risk indicators
MEDIUM_RISK_PATTERNS = [
    r"terminate",
    r"arbitration",
    r"jurisdiction",
    r"lock[-\s]?in",
    r"auto[-\s]?renew",
    r"notice period",
    r"confidentiality",
    r"exclusive jurisdiction",
]

# Low-risk / balancing indicators
LOW_RISK_PATTERNS = [
    r"mutual",
    r"by agreement",
    r"with consent",
    r"reasonable",
    r"subject to law",
]

# Critical terms that alone can escalate contract risk
CRITICAL_DOMINANT_TERMS = [
    "indemnify",
    "terminate",
    "penalty",
    "non-compete",
    "sole discretion",
    "without notice",
    "perpetual",
    "irrevocable",
    "withhold payment",
]

# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ==========================================================
# OBLIGATION / RIGHT / PROHIBITION
# ==========================================================

def classify_obligation_type(text: str) -> str:
    t = normalize_text(text)

    for w in PROHIBITION_WORDS:
        if w in t:
            return "Prohibition"

    for w in OBLIGATION_WORDS:
        if w in t:
            return "Obligation"

    for w in RIGHT_WORDS:
        if w in t:
            return "Right"

    return "Neutral"

# ==========================================================
# CLAUSE-LEVEL RISK SCORING
# ==========================================================

def score_clause_risk(text: str) -> Dict:
    t = normalize_text(text)

    high_hits = []
    medium_hits = []
    low_hits = []

    for p in HIGH_RISK_PATTERNS:
        if re.search(p, t):
            high_hits.append(p)

    for p in MEDIUM_RISK_PATTERNS:
        if re.search(p, t):
            medium_hits.append(p)

    for p in LOW_RISK_PATTERNS:
        if re.search(p, t):
            low_hits.append(p)

    if high_hits:
        return {
            "risk_level": "High",
            "reason": "Clause contains potentially one-sided or severe legal terms",
            "matched_patterns": high_hits
        }

    if medium_hits:
        return {
            "risk_level": "Medium",
            "reason": "Clause requires attention or clarification",
            "matched_patterns": medium_hits
        }

    if low_hits:
        return {
            "risk_level": "Low",
            "reason": "Clause appears balanced or mutual",
            "matched_patterns": low_hits
        }

    return {
        "risk_level": "Low",
        "reason": "No obvious legal risk detected",
        "matched_patterns": []
    }

# ==========================================================
# UNFAVORABLE CLAUSE FLAGGING
# ==========================================================

def is_unfavorable(risk_level: str, obligation_type: str) -> bool:
    if risk_level == "High":
        return True
    if obligation_type == "Prohibition":
        return True
    return False

# ==========================================================
# SINGLE CLAUSE ANALYSIS
# ==========================================================

def analyze_clause(clause: Dict) -> Dict:
    text = clause.get("text", "")

    obligation_type = classify_obligation_type(text)
    risk_info = score_clause_risk(text)

    return {
        "title": clause.get("title", "Clause"),
        "text": text,
        "obligation_type": obligation_type,
        "risk_level": risk_info["risk_level"],
        "risk_reason": risk_info["reason"],
        "unfavorable": is_unfavorable(
            risk_info["risk_level"], obligation_type
        ),
    }

# ==========================================================
# CONTRACT-LEVEL RISK AGGREGATION (CRITICAL PART)
# ==========================================================

def compute_contract_risk(analyzed_clauses: List[Dict]) -> Dict:
    score_map = {"Low": 1, "Medium": 2, "High": 3}

    total_score = 0
    high_risk_count = 0
    critical_flag_count = 0

    for clause in analyzed_clauses:
        level = clause["risk_level"]
        total_score += score_map.get(level, 1)

        if level == "High":
            high_risk_count += 1

        text = normalize_text(clause["text"])
        for term in CRITICAL_DOMINANT_TERMS:
            if term in text:
                critical_flag_count += 1

    avg_score = total_score / max(len(analyzed_clauses), 1)

    # 🔴 DOMINANT LEGAL RISK OVERRIDE
    if high_risk_count >= 3 or critical_flag_count >= 4:
        overall_risk = "High Risk"
    elif avg_score >= 1.7:
        overall_risk = "Medium Risk"
    else:
        overall_risk = "Low Risk"

    return {
        "overall_risk": overall_risk,
        "average_score": round(avg_score, 2),
        "high_risk_clauses": high_risk_count,
        "critical_flags": critical_flag_count,
        "total_clauses": len(analyzed_clauses),
    }

# ==========================================================
# PHASE-6 ENTRY POINT (CALL THIS FROM fapp.py)
# ==========================================================

def analyze_contract_clauses(clauses: List[Dict]) -> Dict:
    analyzed_clauses = []

    for clause in clauses:
        analyzed_clauses.append(analyze_clause(clause))

    contract_risk = compute_contract_risk(analyzed_clauses)

    return {
        "clauses": analyzed_clauses,
        "contract_risk": contract_risk
    }
