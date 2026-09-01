# Evidence cards: knowledge and evidence governance

> Packet: `knowledge-evidence-governance-2026`
>
> Full-text state: four official PDFs inspected
>
> Zotero state: absent by DOI/exact title; import not authorized
>
> Writing state: provisional keys; no contract merge

## Evidence-grade convention

- `G1`: peer-reviewed full text; the claim is limited to the paper's reported model, implementation, or evaluation.
- `G2`: official arXiv full text; the claim is locatable, but peer review, implementation, and independent replication are not upgraded.

## S-KEG-001: provenance-aware openEO workflows

- Intake key: `omidi_provenance-aware_2025`; evidence grade: `G1` (IEEE eScience 2025).
- Located contribution: node-level provenance capture for openEO process graphs, including inputs, outputs, data source, parameter values, timing, agents, and local/remote execution context.
- Decision value: provides the direct EO example that a reproducible Agent workflow must retain observed execution lineage, not only a generated plan or final answer.
- Boundary: the demonstrated Sentinel-1 flood-mapping case is workflow provenance. It does not represent scientific claim support, conflict, applicability, or epistemic status.
- Official source: https://doi.org/10.1109/eScience65000.2025.00016

## S-KEG-002: Micropublications

- Intake key: `clark_micropublications_2014`; evidence grade: `G1` (Journal of Biomedical Semantics 2014).
- Located contribution: a formal argument model connecting claims to attribution, data, methods, qualifiers, supporting representations, and challenging representations across support and challenge graphs.
- Decision value: prevents a citation or attributed statement from being treated as equivalent to direct empirical support, and supplies a representation for preserving disagreement.
- Boundary: the paper develops an ontology and biomedical case patterns; it does not evaluate autonomous agents, retrieval quality, or cross-domain scientific correctness.
- Official source: https://doi.org/10.1186/2041-1480-5-28

## S-KEG-003: SciClaim

- Intake key: `magnusson_extracting_2021`; evidence grade: `G1` (EMNLP 2021).
- Located contribution: a fine-grained scientific-claim graph schema that separates associations, factors, magnitudes, evidence mentions, epistemic status, and qualifiers; qualifiers delimit applicability or scope.
- Decision value: offers a concrete text-to-graph pattern for preventing causal, predictive, comparative, and statistical statements from losing their modality or population/context qualifiers during extraction.
- Boundary: an evidence label means an explicit textual mention of a study, theory, or method. It is not a scientific-validity judgment, contradiction resolver, or proof that downstream reasoning is correct.
- Official source: https://doi.org/10.18653/v1/2021.emnlp-main.381

## S-KEG-004: Action Units

- Intake key: `vogt_actionable_2026`; evidence grade: `G2` (arXiv conceptual framework, 2026).
- Located contribution: action units connect semantic content, contextual information, explicit objectives, procedures, and typed applicability conditions; the framework distinguishes structural actionability, context-specific applicability, and empirically validated applicability, then proposes explicit evidence base and validation history as auditability requirements.
- Decision value: directly constrains scientific-agent reasoning by separating “can execute” from “valid to apply here” and by requiring an applicability check before context-sensitive action.
- Boundary: the paper explicitly defers implementation and empirical evaluation. Its biodiversity examples and TripleA principle are design propositions, not demonstrated Agent effects.
- Official source: https://arxiv.org/abs/2605.01564

## Decision synthesis

| Governance surface | Direct source | What it does not prove |
| --- | --- | --- |
| EO execution provenance | openEO | claim truth, applicability, or conflict handling |
| claim-evidence argument and challenge | Micropublications | autonomous use or Agent benefit |
| epistemic status and scope qualifier extraction | SciClaim | evidence validity or resolved contradiction |
| context-sensitive applicability and validation state | Action Units | implemented or empirically effective system |

The four sources are sufficient to close this acquisition packet, but not to close the thesis gap. `KEG-C5` therefore remains `needs_review`: Chapter 2 must separately test whether the governed representation is available to the Agent, changes its plan or action, and produces a scientifically appropriate change under remote-sensing task conditions.
