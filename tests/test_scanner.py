import tempfile
import unittest
from datetime import date
from pathlib import Path
from gold_miner.scanner import scan_csv

class ScannerTests(unittest.TestCase):
    def test_scan_deduplicates_and_flags(self):
        data = ("case_id,jurisdiction,source_url,retrieved_on,reported_surplus,claim_deadline\n"
                "A,Example County,https://example.org/a,2026-11-05,5000,2027-01-01\n"
                "A,Example County,https://example.org/a,2026-11-05,5000,2027-01-01\n"
                "B,Example County,https://example.org/b,2026-11-05,,\n")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records.csv"
            path.write_text(data, encoding="utf-8")
            rows = scan_csv(str(path), date(2026, 11, 5))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["case_id"], "A")
        self.assertFalse(rows[0]["contact_allowed"])
        self.assertIn("surplus_unverified", rows[1]["flags"])

if __name__ == "__main__":
    unittest.main()
