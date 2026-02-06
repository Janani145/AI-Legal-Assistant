# backend/explainer.py
# Phase 7: Plain-English Explanation + Renegotiation Suggestions
# SME-focused, explainable, no legal advice

import re
from typing import Dict, List

DISCLAIMER = (
    "This explanation is for informational purposes only and does not constitute legal advice."
)

# ---------------------------------------------------------
# Explanation Templates
# ---------------------------------------------------------

RISK_EXPLANATIONS = {
    "High": (
        "This clause may expose the business to significant legal or financial risk. "
        "It is strongly recommended to review or renegotiate this clause."
    ),
    "Medium": (
        "This clause could create potential risk depending on how it is enforced. "
        "Clarification or modification may be beneficial."
    ),
    "Low": (
        "This clause appears standard and balanced under normal circumstances."
    ),
}

# ---------------------------------------------------------
# Clause-Specific Explanations
# ---------------------------------------------------------

CLAUSE_KEYWORD_EXPLANATIONS = {
    "terminate": (
        "This clause allows termination of the agreement. "
        "If termination rights are one-sided or without notice, "
        "it may cause sudden business disruption."
    ),
    "penalty": (
        "Penalty clauses can result in financial loss if obligations are not met. "
        "High penalties increase business risk."
    ),
    "indemnify": (
        "Indemnity clauses require one party to cover losses or legal costs. "
        "Unlimited indemnity can be dangerous for small businesses."
    ),
    "non-compete": (
        "Non-compete clauses restrict future business opportunities. "
        "Long durations or wide geographic scope may be unfair."
    ),
    "payment": (
        "Payment terms define when and how money is paid. "
        "Unclear or discretionary payment terms can affect cash flow."
    ),
    "jurisdiction": (
        "Jurisdiction clauses decide where disputes are resolved. "
        "Distant or exclusive courts may increase legal costs."
    ),
    "confidentiality": (
        "Confidentiality clauses protect sensitive information. "
        "Overly broad obligations may restrict normal business operations."
    ),
}

# ---------------------------------------------------------
# Renegotiation Suggestions
# ---------------------------------------------------------

RENOGOTIATION_SUGGESTIONS = {
    "terminate": (
        "Consider adding a mutual termination clause with reasonable notice "
        "(e.g., 30–60 days) for both parties."
    ),
    "penalty": (
        "Penalties may be capped to a reasonable amount linked to actual loss."
    ),
    "indemnify": (
        "Indemnity obligations can be limited to direct damages "
        "and capped at the contract value."
    ),
    "non-compete": (
        "The non-compete period may be reduced or restricted to a smaller geographic area."
    ),
    "payment": (
        "Payment timelines and conditions should be clearly defined and time-bound."
    ),
    "jurisdiction": (
        "A mutually convenient jurisdiction or arbitration mechanism may be considered."
    ),
}

# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def detect_keywords(text: str) -> List[str]:
    detected = []
    for key in CLAUSE_KEYWORD_EXPLANATIONS.keys():
        if key in text:
            detected.append(key)
    return detected

# ---------------------------------------------------------
# Main Explanation Engine
# ---------------------------------------------------------

def explain_clause(clause: Dict) -> Dict:
    """
    Returns:
    - plain_english_explanation
    - business_impact
    - renegotiation_suggestion
    """

    text = normalize(clause["text"])
    risk = clause["risk_level"]

    keywords = detect_keywords(text)

    explanation_parts = []
    suggestions = []

    # Base risk explanation
    explanation_parts.append(RISK_EXPLANATIONS.get(risk, ""))

    # Keyword-based explanation
    for kw in keywords:
        explanation_parts.append(CLAUSE_KEYWORD_EXPLANATIONS.get(kw, ""))

        if kw in RENOGOTIATION_SUGGESTIONS:
            suggestions.append(RENOGOTIATION_SUGGESTIONS[kw])

    if not suggestions:
        suggestions.append(
            "Consider discussing this clause with the other party to ensure fairness."
        )

    return {
        "plain_english_explanation": " ".join(explanation_parts),
        "business_impact": (
            "This clause may affect operational flexibility, cash flow, "
            "or legal exposure."
            if risk != "Low"
            else "This clause is unlikely to significantly impact daily operations."
        ),
        "suggested_alternatives": suggestions,
        "disclaimer": DISCLAIMER,
    }

# ---------------------------------------------------------
# Batch Processing
# ---------------------------------------------------------

def explain_contract_clauses(analyzed_clauses: List[Dict]) -> List[Dict]:
    explained = []

    for clause in analyzed_clauses:
        explanation = explain_clause(clause)

        explained.append({
            **clause,
            **explanation
        })

    return explained
