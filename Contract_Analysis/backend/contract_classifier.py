
def classify_contract(contract_text: str) -> dict:
    text = contract_text.lower()

    contract_types = {
        "Employment Agreement": [
            "employee", "employer", "employment", "appointment",
            "salary", "wages", "probation", "notice period",
            "termination of employment", "job role", "designation",
            "human resources", "hr policy", "work hours",
            "leave policy", "code of conduct"
        ],

        "Lease / Rental Agreement": [
            "lease", "rent", "rental", "tenant", "landlord",
            "premises", "property", "security deposit",
            "monthly rent", "lock-in period", "maintenance charges",
            "eviction", "vacate", "rent escalation"
        ],

        "Vendor / Service Agreement": [
            "vendor", "service provider", "services", "scope of work",
            "invoice", "billing", "payment terms", "service level",
            "sla", "deliverables", "work order",
            "outsourcing", "consultancy"
        ],

        "Partnership Deed": [
            "partner", "partnership", "profit sharing",
            "capital contribution", "mutual consent",
            "firm name", "dissolution", "partnership act",
            "management of business", "share of profits"
        ],

        "NDA / Confidentiality Agreement": [
            "confidential", "confidentiality",
            "non disclosure", "nda",
            "confidential information",
            "proprietary information",
            "data protection", "trade secrets"
        ],

        "Purchase / Supply Agreement": [
            "purchase", "buyer", "seller", "supply",
            "goods", "purchase order", "delivery schedule",
            "quantity", "quality standards", "inspection",
            "acceptance of goods"
        ],

        "Franchise Agreement": [
            "franchise", "franchisor", "franchisee",
            "brand usage", "royalty", "franchise fee",
            "territory", "training", "operations manual"
        ]
    }

    scores = {}

    for contract_type, keywords in contract_types.items():
        score = 0
        for word in keywords:
            score += text.count(word)
        scores[contract_type] = score

    best_match = max(scores, key=scores.get)
    total_score = sum(scores.values())

    if scores[best_match] == 0:
        return {
            "contract_type": "General / Unknown Contract",
            "confidence": 0.0
        }

    confidence = round(scores[best_match] / total_score, 2)

    return {
        "contract_type": best_match,
        "confidence": confidence
    }
