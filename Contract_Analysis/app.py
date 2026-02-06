import streamlit as st

from backend.file_reader import extract_text
from backend.language_handler import normalize_language
from backend.contract_classifier import classify_contract
from backend.clause_extractor import extract_clauses
from backend.risk_analyzer import analyze_contract_clauses
from backend.explainer import explain_contract_clauses
from backend.summary_generator import generate_executive_summary
from backend.audit_logger import log_event
from backend.ner_extractor import extract_entities
from backend.chatbot import answer_question
from backend.report_generator import generate_pdf_report

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Legal Assistant for SMEs",
    page_icon="📜",
    layout="wide"
)

# -------------------------------------------------
# MODERN DARK SAAS CSS (NO TOGGLES)
# -------------------------------------------------

st.markdown("""
<style>
.main {
    background-color: #0b0f19;
    color: #e5e7eb;
}

h1, h2, h3, h4 {
    color: #f9fafb;
    font-family: Inter, sans-serif;
}

.card {
    background: linear-gradient(135deg, #111827, #020617);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    margin-bottom: 22px;
}

.metric-card {
    background: linear-gradient(135deg, #111827, #020617);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 16px 36px rgba(0,0,0,0.55);
}

.badge-low {
    background: #16a34a;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 600;
}

.badge-medium {
    background: #f59e0b;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 600;
}

.badge-high {
    background: #dc2626;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 600;
}

.chat-bubble {
    background: #020617;
    border-left: 6px solid #6366f1;
    padding: 18px;
    border-radius: 14px;
    margin-top: 12px;
}

.download-btn {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: white;
    padding: 14px 26px;
    border-radius: 14px;
    font-weight: 600;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("📜 AI Legal Assistant for SMEs")
st.caption(
    "Understand contracts • Detect legal risk • Plain-English explanations • "
    "Private & Confidential"
)

st.divider()

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------

uploaded = st.file_uploader(
    "Upload Contract (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

if not uploaded:
    st.info("⬆️ Upload a contract to start analysis")
    st.stop()

# -------------------------------------------------
# ANALYSIS PIPELINE
# -------------------------------------------------

with st.spinner("Analyzing contract…"):
    raw_text = extract_text(uploaded)
    lang_info = normalize_language(raw_text)
    text_en = lang_info["normalized_english_text"]

    classification = classify_contract(text_en)
    clauses = extract_clauses(text_en)
    analysis = analyze_contract_clauses(clauses)
    explained = explain_contract_clauses(analysis["clauses"])
    summary = generate_executive_summary(classification, analysis)
    entities = extract_entities(text_en)

# -------------------------------------------------
# OVERVIEW CARDS
# -------------------------------------------------

st.subheader("📌 Contract Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"<div class='metric-card'>📄<br><b>Type</b><br>"
        f"{classification['contract_type']}</div>",
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"<div class='metric-card'>🎯<br><b>Confidence</b><br>"
        f"{classification['confidence']}</div>",
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"<div class='metric-card'>🧩<br><b>Clauses</b><br>"
        f"{analysis['contract_risk']['total_clauses']}</div>",
        unsafe_allow_html=True
    )

risk = analysis["contract_risk"]["overall_risk"]
badge = (
    "badge-low" if "Low" in risk else
    "badge-medium" if "Medium" in risk else
    "badge-high"
)

with c4:
    st.markdown(
        f"<div class='metric-card'>⚠️<br><b>Risk</b><br>"
        f"<span class='{badge}'>{risk}</span></div>",
        unsafe_allow_html=True
    )

st.divider()

# -------------------------------------------------
# TABS (CLEAN, NO TOGGLES)
# -------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📝 Summary", "🧠 Entities", "📄 Clauses", "⚠️ Risks", "💬 Chat"]
)

# ---------------- SUMMARY ----------------

with tab1:
    st.markdown(
        f"<div class='card'><h4>Executive Summary</h4>"
        f"<p>{summary}</p></div>",
        unsafe_allow_html=True
    )

# ---------------- ENTITIES ----------------

with tab2:
    for key, values in entities.items():
        st.markdown(f"**{key}**")
        if values:
            st.markdown(", ".join(f"`{v}`" for v in values))
        else:
            st.caption("Not detected")
        st.divider()

# ---------------- CLAUSES ----------------

with tab3:
    for i, clause in enumerate(explained, start=1):
        icon = "🔴" if clause["risk_level"] == "High" else "🟡" if clause["risk_level"] == "Medium" else "🟢"
        with st.expander(f"{icon} Clause {i}: {clause['title']}"):
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.markdown("**Clause Text**")
            st.write(clause["text"])

            st.markdown("**What this means**")
            st.write(clause["plain_english_explanation"])

            st.markdown("**Business Impact**")
            st.write(clause["business_impact"])

            st.markdown("**Safer Alternatives**")
            for s in clause["suggested_alternatives"]:
                st.write("✅", s)

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RISKS ----------------

with tab4:
    r = analysis["contract_risk"]

    st.metric("High-Risk Clauses", r["high_risk_clauses"])
    st.metric("Critical Flags", r["critical_flags"])
    st.metric("Average Risk Score", r["average_score"])

# ---------------- CHAT ----------------

with tab5:
    q = st.text_input("Ask about safety, risk, summary, or contract type")

    if q:
        response = answer_question(
            q,
            classification,
            analysis["contract_risk"],
            summary
        )

        st.markdown(
            f"<div class='chat-bubble'><b>AI Assistant</b><br>{response}</div>",
            unsafe_allow_html=True
        )

# -------------------------------------------------
# DOWNLOAD REPORT
# -------------------------------------------------

st.divider()

pdf_path = generate_pdf_report(
    uploaded.name,
    classification,
    analysis["contract_risk"],
    explained
)

with open(pdf_path, "rb") as f:
    st.download_button(
        "⬇️ Download Full Legal Report (PDF)",
        f,
        file_name=pdf_path.split("/")[-1],
        mime="application/pdf"
    )

# -------------------------------------------------
# AUDIT LOG
# -------------------------------------------------

log_event(
    filename=uploaded.name,
    contract_type=classification["contract_type"],
    risk_summary=analysis["contract_risk"],
    total_clauses=len(explained)
)

st.caption("🔒 Local analysis • No data shared • Not legal advice")
