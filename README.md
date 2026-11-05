# Gold Miner

Research-first system for identifying and evaluating potential unclaimed foreclosure surplus proceeds.

**Status:** prototype scaffold only; no live records ingestion, legal eligibility determination, outreach, or filing.

## Workflow
1. Import public-record leads with source URLs and retrieval dates.
2. Normalize case data, jurisdiction, sale date, surplus amount and claim deadline.
3. Flag missing evidence and possible competing claims or liens.
4. Prioritize cases for **human review**.
5. Require explicit approval before contacting anyone, spending money, or submitting filings.

## Safety
- No legal advice or guarantees of entitlement.
- Verify each jurisdiction's current rules, deadlines, licensing, fee limits, and privacy obligations.
- No deceptive solicitation, impersonation, or automated outreach.
- Never commit private claimant information or credentials.

Run tests: `python -m unittest discover -s tests` (Python 3.11+).
