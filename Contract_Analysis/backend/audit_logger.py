# backend/audit_logger.py
# Phase 8: Confidential Audit Logging (Local Only)

import json
import os
from datetime import datetime
from typing import Dict

AUDIT_DIR = "audit_logs"

if not os.path.exists(AUDIT_DIR):
    os.makedirs(AUDIT_DIR)

def generate_audit_id() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")

def log_event(
    filename: str,
    contract_type: str,
    risk_summary: Dict,
    total_clauses: int
) -> None:
    audit_record = {
        "audit_id": generate_audit_id(),
        "timestamp": datetime.now().isoformat(),
        "filename": filename,
        "contract_type": contract_type,
        "total_clauses": total_clauses,
        "risk_summary": risk_summary,
        "storage_policy": "Local storage only. No data shared externally."
    }

    filepath = os.path.join(
        AUDIT_DIR,
        f"audit_{audit_record['audit_id']}.json"
    )

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(audit_record, f, indent=2)
