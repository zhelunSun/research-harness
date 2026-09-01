# Intake decision: Agent evaluation and user validity

## Read-only checks completed on 2026-09-01

- Zotero Desktop 9.0.5: local API enabled and healthy; connector healthy.
- Selected target at scan time: `我的文库 / AI_for_Science` (collection `19`).
- Exact DOI searches returned zero matches for:
  - `10.52202/079017-2365`
  - `10.18653/v1/2025.findings-naacl.65`
- Exact-title searches returned zero matches for:
  - `τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains`
  - `How Can We Assess Human-Agent Interactions? Case Studies in Software Agent Design`

## Screening decision

Retain all four sources. Together they satisfy the bounded packet requirement without adding a fifth source: AgentBoard covers fine-grained progress, ToolSandbox covers mutable state and trajectory constraints, τ-bench covers repeated reliability, and PULSE provides actual-user calibration.

## Future Zotero decision gate

No write is authorized by this packet. If the researcher later authorizes import, the recommended target is `我的文库 / AI_for_Science / scientific agent`, with candidate tags `Agent Evaluation`, `Agentic Research`, `Benchmark`, `Human-Agent Interaction`, `Long-Horizon Evaluation`, and `Process Evaluation`. The import must then verify four parent item keys, four stable BibTeX keys, and four official PDFs linked through SeaDrive before registry reconciliation.
