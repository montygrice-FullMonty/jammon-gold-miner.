"""Evidence-oriented lead model; no entitlement conclusions."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Lead:
    case_id: str
    jurisdiction: str
    source_url: str
    retrieved_on: date
    sale_date: date | None = None
    reported_surplus: Decimal | None = None
    claim_deadline: date | None = None
    competing_claims_reviewed: bool = False
    jurisdiction_rules_verified: bool = False

    def missing_checks(self) -> tuple[str, ...]:
        missing = []
        if not self.case_id or not self.jurisdiction or not self.source_url:
            missing.append("source_identity")
        if self.reported_surplus is None:
            missing.append("surplus_unverified")
        if self.claim_deadline is None:
            missing.append("deadline_unverified")
        if not self.competing_claims_reviewed:
            missing.append("competing_claims_unreviewed")
        if not self.jurisdiction_rules_verified:
            missing.append("jurisdiction_rules_unverified")
        return tuple(missing)
