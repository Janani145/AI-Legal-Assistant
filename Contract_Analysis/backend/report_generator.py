import os
from datetime import datetime
from typing import Dict, List

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# ✅ Absolute-safe export directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DIR = os.path.join(BASE_DIR, "exports", "reports")

os.makedirs(EXPORT_DIR, exist_ok=True)


def generate_pdf_report(
    filename: str,
    classification: Dict,
    contract_risk: Dict,
    explained_clauses: List[Dict]
) -> str:
    """
    Generates a PDF report and RETURNS the file path.
    """

    pdf_filename = f"Contract_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(EXPORT_DIR, pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 1 * inch

    def draw(text: str):
        nonlocal y
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch
        c.drawString(1 * inch, y, text)
        y -= 14

    # ------------------ TITLE ------------------
    c.setFont("Helvetica-Bold", 16)
    draw("Contract Risk Analysis Report")
    y -= 10

    c.setFont("Helvetica", 11)
    draw(f"Source File: {filename}")
    draw(f"Contract Type: {classification['contract_type']}")
    draw(f"Confidence Score: {classification['confidence']}")
    draw(f"Overall Risk: {contract_risk['overall_risk']}")
    draw(f"Total Clauses: {contract_risk['total_clauses']}")
    y -= 15

    # ------------------ CLAUSES ------------------
    for idx, clause in enumerate(explained_clauses, start=1):
        c.setFont("Helvetica-Bold", 12)
        draw(f"Clause {idx}: {clause['title']}")

        c.setFont("Helvetica", 10)
        draw(f"Risk Level: {clause['risk_level']}")
        draw(f"Obligation Type: {clause['obligation_type']}")
        draw("")

        draw("Clause Text:")
        draw(clause["text"][:800])

        draw("Explanation:")
        draw(clause["plain_english_explanation"][:800])

        draw("Suggested Alternatives:")
        for s in clause["suggested_alternatives"]:
            draw(f"- {s}")

        y -= 12

    c.save()
    return pdf_path
