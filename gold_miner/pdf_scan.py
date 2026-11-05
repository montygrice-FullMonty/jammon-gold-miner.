"""Extract candidate surplus cases from a publicly accessible PDF URL.

Only use sources you are authorized to access. Extracted rows require human verification.
"""
import io
import re
from urllib.request import Request, urlopen
import pdfplumber

CASE = re.compile(r"\bCV\d{4}-\d{5,6}\b")
MONEY = re.compile(r"(?<!\w)(?:\$\s*)?\d{1,3}(?:,\d{3})*\.\d{2}\b")

def scan_pdf(url: str) -> list[dict]:
    if not url.startswith("https://"):
        raise ValueError("Only HTTPS PDF sources are supported")
    req = Request(url, headers={"User-Agent": "GoldMinerResearch/0.1 (public-records review)"})
    with urlopen(req, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f"HTTP {response.status}")
        data = response.read(20_000_001)
    if len(data) > 20_000_000 or not data.startswith(b"%PDF"):
        raise ValueError("Not a supported PDF or PDF exceeds 20 MB")
    rows = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page_number, page in enumerate(pdf.pages, 1):
            for line in (page.extract_text() or "").splitlines():
                cases = CASE.findall(line)
                amounts = MONEY.findall(line)
                if cases:
                    rows.append({
                        "case_id": cases[-1],
                        "amount_candidates": amounts,
                        "source_url": url,
                        "page": page_number,
                        "raw_line": line,
                        "status": "unverified_candidate",
                    })
    return rows
