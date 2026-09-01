# Knowledge and evidence governance evidence packet

## Question

哪些科学或遥感知识系统把来源、适用条件、证据状态、冲突、验证义务和结论边界显式带入检索或推理，而不是仅提供普通 RAG？

## Current state

- Four official full texts were inspected: one IEEE Earth-observation workflow paper, one peer-reviewed biomedical semantic-model paper, one EMNLP scientific-claim extraction paper, and one 2026 biodiversity/AI conceptual preprint.
- DOI or exact-title Zotero searches returned no parent-item matches on 2026-09-01.
- No Zotero write, tag change, attachment import, citation insertion, REF-MISSING removal, or writing-contract merge was performed.
- The four BibTeX keys are intake identities until a separately authorized Zotero import returns stable item and citation keys.
- `KEG-C1` through `KEG-C4` are narrow full-text claims. The cross-source transfer statement `KEG-C5` remains `needs_review` as `[REF-MISSING:KEG-C5]`.

## Contents

- `references.bib`: publisher, conference, and arXiv intake metadata without machine paths.
- `ledger.json`: full-text-located source and claim relations.
- `evidence_cards.md`: source-specific mechanism, decision value, and transfer boundary.
- `intake_decision.md`: Zotero deduplication evidence, screened exclusion, and exact future write gate.
- `audit.json`: deterministic ledger audit.
- `writing_bridge.json`: provisional citation constraints, not a writing authorization.

## Non-goals

This packet does not establish one integrated evidence-governance architecture, prove that structured representation improves an Agent, or authorize a Chapter 2 method or scientific-gold decision. Its role is narrower: separate provenance, claim qualification, conflict representation, contextual applicability, empirical validation state, and auditable conclusion boundaries so that Chapter 2 cannot treat a knowledge graph name or ordinary RAG as evidence governance by default.
