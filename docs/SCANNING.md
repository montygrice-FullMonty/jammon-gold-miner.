# Scanner usage

## CSV records
`python -m gold_miner examples/sample_records.csv`

## Public PDF records
`pip install -r requirements.txt`
`python scripts/scan_public_pdf.py 'https://OFFICIAL-AGENCY/PUBLIC-LIST.pdf'`

PDF scanning extracts case IDs and monetary strings from lines. It does **not** determine whether amounts are balances, whether money remains available, or who is entitled to it. Always check the current official county record and court docket. Do not use old mirrored PDFs as current leads.

Output: `data/output/candidates_*.json`. Never publish personal contact information. This initial scanner is manual and has not been run against a live county source.
