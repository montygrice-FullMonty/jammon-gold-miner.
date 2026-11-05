import unittest
from datetime import date
from decimal import Decimal
from gold_miner.models import Lead
from gold_miner.triage import triage


class TriageTests(unittest.TestCase):
    def test_missing_evidence_blocks_automatic_action(self):
        lead = Lead("CASE-1", "Example County", "https://example.org/record", date(2026, 11, 5))
        result = triage(lead, date(2026, 11, 5))
        self.assertIn("surplus_unverified", result["flags"])
        self.assertFalse(result["contact_allowed"])

    def test_expired_deadline_is_flagged(self):
        lead = Lead("CASE-2", "Example County", "https://example.org/record", date(2026, 11, 5),
                    reported_surplus=Decimal("1200"), claim_deadline=date(2026, 10, 1))
        self.assertIn("deadline_may_have_passed", triage(lead, date(2026, 11, 5))["flags"])


if __name__ == "__main__":
    unittest.main()
