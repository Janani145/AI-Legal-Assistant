# 📜 AI Legal Assistant

A **GenAI-inspired Legal Contract Analysis System** designed to help **Small and Medium Enterprises (SMEs)** understand complex contracts, identify legal risks, and receive **plain-English explanations** — without relying on external legal databases or APIs.

---

## ✨ Features

### 🔍 Core Legal NLP Capabilities
- Contract type classification  
- Clause & sub-clause extraction  
- Obligation / Right / Prohibition detection  
- Risk scoring (Clause-level & Contract-level)  
- Unfavorable clause identification  

---

### 🧠 Advanced Analysis
- Plain-English clause explanations  
- SME-friendly renegotiation suggestions  
- Executive summary generation  
- Clause similarity & pattern heuristics  

---

### 🌐 Multilingual Support
- English & Hindi contract handling  
- Offline Hindi → English normalization  
- Mixed-language document support  

---

### 🧾 Named Entity Recognition (NER)
- Parties  
- Dates  
- Financial amounts  
- Locations & jurisdiction  
- Percentages  

---

### 🖥️ Modern User Interface
- Dark SaaS-style UI (Streamlit)  
- Tab-based navigation  
- Risk badges & summary cards  
- Chat-based contract assistant  
- Styled PDF report download  

---

### 🔒 Privacy & Compliance
- 100% local processing  
- No external APIs  
- Confidential audit logs  
- No legal advice disclaimer  

---

## 📁 Project Structure

```text
legal_genai_assistant/
│
├── app.py                      # Streamlit UI
│
├── backend/
│   ├── file_reader.py
│   ├── language_handler.py
│   ├── contract_classifier.py
│   ├── clause_extractor.py
│   ├── risk_analyzer.py
│   ├── explainer.py
│   ├── renegotiation_engine.py
│   ├── summary_generator.py
│   ├── ner_extractor.py
│   ├── chatbot.py
│   ├── report_generator.py
│   └── audit_logger.py
│
├── audit_logs/                 # Local confidential audit logs
├── exports/
│   └── reports/               # Generated PDF reports
│
├── requirements.txt
└── README.md
