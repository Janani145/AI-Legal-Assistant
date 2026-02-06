# backend/renegotiation_engine.py

"""
GEN-AI powered renegotiation suggestion engine
Uses LLM ONLY for reasoning & drafting safer alternatives
"""

from typing import Dict

RISKY_PATTERNS = {
    "unilateral_termination": [
        "terminate at any time",
        "without notice",
        "without assigning any reason"
    ],
    "payment_risk": [
        "withhold payment",
        "delay payment",
        "internal approval"
    ],
    "indemnity": [
        "indemnify",
        "hold harmless",
        "including company's negligence"
    ],
    "non_compete": [
        "non compete",
        "shall not engage",
        "after termination"
    ],
    "ip_transfer": [
        "sole and exclusive property",
        "in perpetuity",
        "waives all moral rights"
    ]
}


def detect_risk_category(text: str) -> str:
    text = text.lower()
    scores = {k: 0 for k in RISKY_PATTERNS}

    for category, patterns in RISKY_PATTERNS.items():
        for p in patterns:
            if p in text:
                scores[category] += 1

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general_risk"



def suggest_renegotiations(clause: Dict) -> str:
    """
    Rule-guided + GenAI-style explanation (LLM hook-ready)
    """
    category = detect_risk_category(clause["text"])

    if category == "unilateral_termination":
        return (
            "This clause allows one party to terminate the agreement at any time "
            "without notice, creating a power imbalance.\n\n"
            "✅ Suggested Alternative:\n"
            "Either party may terminate this Agreement by providing a minimum of "
            "30 days prior written notice. Termination shall not affect payments "
            "for services already rendered."
        )

    if category == "payment_risk":
        return (
            "This clause permits the company to delay or withhold payment without "
            "clear criteria, which may impact cash flow.\n\n"
            "✅ Suggested Alternative:\n"
            "Payments shall be released within 15 days of invoice submission, "
            "subject to written communication of deficiencies, if any."
        )

    if category == "indemnity":
        return (
            "This clause transfers excessive liability to one party, including "
            "liability for the other party’s negligence.\n\n"
            "✅ Suggested Alternative:\n"
            "Each party shall indemnify the other only to the extent of losses "
            "arising from its own negligence or willful misconduct."
        )

    if category == "non_compete":
        return (
            "A long-duration, wide-scope non-compete may be unenforceable and "
            "restrict livelihood.\n\n"
            "✅ Suggested Alternative:\n"
            "The Vendor shall not solicit the Company’s existing clients for a "
            "period of 6 months within the same city, subject to applicable law."
        )

    if category == "ip_transfer":
        return (
            "This clause permanently transfers all intellectual property without "
            "compensation or reuse rights.\n\n"
            "✅ Suggested Alternative:\n"
            "The Company shall retain ownership of deliverables created under this "
            "Agreement, while the Vendor may reuse generalized know-how and skills."
        )

    return (
        "This clause may expose one party to unclear obligations.\n\n"
        "✅ Suggested Alternative:\n"
        "The clause should clearly define responsibilities, timelines, and "
        "limitations to reduce ambiguity."
    )
