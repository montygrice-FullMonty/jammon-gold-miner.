"""Conservative triage for review; never determines legal eligibility."""
from datetime import date
from .models import Lead


def triage(lead: Lead, today: date) -> dict:
    checks = list(lead.missing_checks())
    if lead.claim_deadline is not None and lead.claim_deadline < today:
        checks.append("deadline_may_have_passed")
    if lead.reported_surplus is not None and lead.reported_surplus <= 0:
        checks.append("no_positive_surplus")
    return {
        "case_id": lead.case_id,
        "status": "needs_review",
        "flags": checks,
        "contact_allowed": False,
        "filing_allowed": False,
    }
