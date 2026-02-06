# backend/summary_generator.py

"""
Executive-level AI summary generator
"""

def generate_executive_summary(classification: dict, analysis: dict) -> str:
    risk = analysis["contract_risk"]["overall_risk"]
    avg = analysis["contract_risk"]["average_score"]

    summary = []
    summary.append(
        f"This is a {classification['contract_type']} with an overall "
        f"{risk.lower()} profile."
    )

    if risk == "High Risk":
        summary.append(
            "Several clauses heavily favor one party and may expose the other "
            "to financial, operational, or legal risk."
        )
    elif risk == "Medium Risk":
        summary.append(
            "The contract contains certain clauses that require renegotiation "
            "to ensure balanced obligations."
        )
    else:
        summary.append(
            "The agreement appears largely balanced with manageable risk."
        )

    summary.append(
        "Key risk areas include termination rights, payment conditions, "
        "liability allocation, and intellectual property ownership."
    )

    summary.append(
        "Recommendation: Proceed only after addressing highlighted clauses."
        if risk != "Low Risk"
        else "Recommendation: Safe to proceed with minor clarifications."
    )

    return " ".join(summary)
