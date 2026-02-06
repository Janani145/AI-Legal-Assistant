# backend/chatbot.py
# Phase 9: Contract-aware SME Legal Chatbot

from typing import Dict

SYSTEM_NOTE = (
    "This assistant provides business-friendly explanations only. "
    "It does not give legal advice."
)

def answer_question(
    question: str,
    classification: Dict,
    contract_risk: Dict,
    summary: str
) -> str:
    q = question.lower()

    if "risk" in q:
        return (
            f"Overall contract risk is assessed as "
            f"{contract_risk['overall_risk']}. "
            f"There are {contract_risk['high_risk_clauses']} high-risk clauses."
        )

    if "type" in q or "contract" in q:
        return (
            f"This document is classified as a "
            f"{classification['contract_type']} "
            f"with confidence {classification['confidence']}."
        )

    if "safe" in q or "sign" in q:
        if contract_risk["overall_risk"] == "High Risk":
            return (
                "This contract is not recommended for signing "
                "without renegotiating high-risk clauses."
            )
        return (
            "The contract appears reasonably balanced, "
            "but highlighted clauses should be reviewed."
        )

    if "summary" in q:
        return summary

    return (
        "I can help explain risks, contract type, "
        "whether it is safe to sign, or provide a summary."
    )
