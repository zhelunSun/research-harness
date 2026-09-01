# Opening-report v0.5 literature writing intake, 2026-09-01

This intake reviews two audited literature packets against the current opening-report
draft and its O1 v0.5 writing contract. It records candidate support and unresolved
evidence gaps without editing the draft, merging a contract, removing a
`[REF-MISSING]` marker, or writing to Zotero.

## Authority

1. `thesis/opening_report_draft_zh.md`;
2. `thesis/writing_contracts/opening_report_o1_v0.5.contract.json` and brief;
3. `evidence/opening_evidence_matrix.md` and `claims/key_claims.md`;
4. `evidence/literature/packets/ai4science_frontier_2026/`;
5. `evidence/literature/packets/geospatial_agent_comparators_2026/`.

## Outcome

- Seven literal `[REF-MISSING]` occurrences were observed: one status explanation and six content gaps.
- No content marker is removable under the current O1 contract.
- Sections 1.2 and 2.2 are future paragraph-splitting candidates: verified capability evidence can be separated from the unresolved field-level gap synthesis.
- Three ExpertsRS feasibility statements have direct candidate support from `GAC-C1`, but their BibTeX identity remains provisional until the separately gated Zotero import is authorized and reconciled.
- The OpenAI and Anthropic mathematics reports are deferred from this opening-report pass.

## Contents

- `decision_matrix.json`: machine-readable statement-level decisions;
- `review_summary_zh.md`: researcher-facing Chinese decision packet;
- `candidate_contract_fragment.json`: deterministic guard for the review summary, not a merged opening-report contract;
- `change_ledger.md`: scope and evidence-boundary changes;
- `references.bib`: packet-local bibliography snapshot for candidate identities;
- `review_summary_zh.audit.json` and `.md`: generated writing-audit outputs.

The repository-level `scripts/audit_literature_control.py` checks this intake,
including source-claim identities, marker-count drift, and the no-unmerged-removal gate.
