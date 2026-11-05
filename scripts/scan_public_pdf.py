"""Usage: python scripts/scan_public_pdf.py https://official.example/list.pdf"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from gold_miner.pdf_scan import scan_pdf

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/scan_public_pdf.py HTTPS_PDF_URL")
    url = sys.argv[1]
    records = scan_pdf(url)
    Path("data/output").mkdir(parents=True, exist_ok=True)
    filename = datetime.now(timezone.utc).strftime("data/output/candidates_%Y%m%dT%H%M%SZ.json")
    Path(filename).write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(records)} unverified candidates to {filename}")

if __name__ == "__main__":
    main()
