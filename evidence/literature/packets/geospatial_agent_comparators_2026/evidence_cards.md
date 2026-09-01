# Evidence cards: geospatial agent comparators 2026

> Packet: `geospatial-agent-comparators-2026`  
> Full-text source: publisher HTML or arXiv HTML v1  
> Zotero state: absent from current library; import not authorized  
> Writing state: provisional keys; not eligible for contract merge

## Evidence-grade convention

- `G1`: peer-reviewed full text; claim is limited to the paper's reported design and evaluation.
- `G2`: official arXiv full text; method and reported evaluation are locatable, but publication and independent replication are not upgraded.

## S-GAC-001: ExpertsRS

- Intake BibTeX key: `sun_llm-based_2026`
- Zotero item key: `null`
- Evidence grade: `G1`
- Verified coverage: Data--Tools--Brain; three specialized agents; four sequential workflow states; two case studies; 20-request lightweight comparison.
- Thesis route: published historical feasibility evidence for Chapter 1.
- Boundary: it does not verify typed workflow semantics, plan/observed process graphs, checkpoint recovery, general reliability, or cross-task generalization.
- Source: https://doi.org/10.1080/20964471.2025.2600178

## S-GAC-002: Spatial-Agent

- Intake BibTeX key: `bao_spatial-agent_2026`
- Zotero item key: `null`
- Evidence grade: `G2`
- Verified coverage: natural-language question to GeoFlow Graph; core spatial concepts and functional roles; five workflow well-formedness constraints; concrete tool execution; template and fine-tuning ablations.
- Thesis route: closest Chapter 1 workflow-representation comparator.
- Boundary: API/data quality, finite templates, annotated-data scaling, and English urban-only evaluation remain explicit limitations. A workflow graph alone is no longer a defensible thesis novelty claim.
- Source: https://arxiv.org/abs/2601.16965

## S-GAC-003: GeoAgentBench

- Intake BibTeX key: `yu_geoagentbench_2026`
- Zotero item key: `null`
- Evidence grade: `G2`
- Verified coverage: dynamic interactive sandbox; 117 atomic tools; 53 tasks across six GIS domains; runtime feedback; stepwise tool/parameter metrics; reference-based VLM grading of final maps.
- Thesis route: direct Chapter 3 dynamic-execution and grader comparator; also informs Chapter 1 Plan-and-React baseline design.
- Boundary: current scope remains GIS task execution and map-product verification; multi-agent collaboration is future work, and scientific-intent validity or real-user utility is not established by its metrics.
- Source: https://arxiv.org/abs/2604.13888

## S-GAC-004: GeoDisaster

- Intake BibTeX key: `hasan_geodisaster_2026`
- Zotero item key: `null`
- Evidence grade: `G2`
- Verified coverage: 2,921 instances, 43 question types, five disaster families, heterogeneous EO/GIS evidence, executable ground truth, deterministic checks, 18 tools, execution contracts, and step-level alignment/evaluation.
- Thesis route: strongest direct comparator for Chapter 3 operational task chains and contract-aware evaluation.
- Boundary: its domain is disaster geo-intelligence; remaining failures include ambiguous evidence, metric selection, constraint-aware synthesis, and uncertainty-aware multi-source reasoning. It does not establish urban-forest task or user validity.
- Source: https://arxiv.org/abs/2606.17246

## Decision synthesis

The four sources already occupy much of the generic capability space:

| Capability | Prior-art coverage |
| --- | --- |
| Natural-language access and multi-agent roles | ExpertsRS |
| Structured executable workflow graph and explicit well-formedness constraints | Spatial-Agent |
| Dynamic tool sandbox, runtime feedback, parameter and product grading | GeoAgentBench |
| Heterogeneous EO/GIS evidence, deterministic checks, role contracts and step-level alignment | GeoDisaster |

Consequently, the thesis must not sell those capabilities as novelty in isolation. The candidate remaining space is narrower: city-forest scientific tasks, task-conditioned evidence/applicability boundaries, planned-versus-observed process records, targeted repair/checkpoint recovery, and evaluation that separates executable workflow, product correctness, scientific intent, serious error, unnecessary intervention, and real-user validity. This synthesis remains `needs_review` as `[REF-MISSING:GAC-C6]` until the Chapter 1/3 claim comparison is accepted.
