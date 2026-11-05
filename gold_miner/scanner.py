"""Scan a local CSV export of public surplus records. No scraping or outreach."""
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse
from .models import Lead
from .triage import triage

REQUIRED = {"case_id", "jurisdiction", "source_url", "retrieved_on"}

def scan_csv(path: str, today: date | None = None) -> list[dict]:
    today = today or date.today()
    results = []
    seen = set()
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("CSV requires: " + ", ".join(sorted(REQUIRED)))
        for line, row in enumerate(reader, start=2):
            try:
                key = (row["jurisdiction"].strip().casefold(), row["case_id"].strip().casefold())
                if not all(key):
                    raise ValueError("missing case identity")
                if key in seen:
                    continue
                seen.add(key)
                source = row["source_url"].strip()
                if urlparse(source).scheme not in ("http", "https"):
                    raise ValueError("invalid source URL")
                surplus = row.get("reported_surplus", "").strip()
                deadline = row.get("claim_deadline", "").strip()
                lead = Lead(
                    case_id=row["case_id"].strip(),
                    jurisdiction=row["jurisdiction"].strip(),
                    source_url=source,
                    retrieved_on=date.fromisoformat(row["retrieved_on"].strip()),
                    reported_surplus=Decimal(surplus) if surplus else None,
                    claim_deadline=date.fromisoformat(deadline) if deadline else None,
                )
                result = triage(lead, today)
                result["source_url"] = source
                result["reported_surplus"] = str(lead.reported_surplus) if lead.reported_surplus is not None else None
                results.append(result)
            except (ValueError, InvalidOperation, AttributeError) as exc:
                results.append({"row": line, "status": "invalid_input", "error": str(exc)})
    return sorted(results, key=lambda r: Decimal(r.get("reported_surplus") or "0"), reverse=True)
