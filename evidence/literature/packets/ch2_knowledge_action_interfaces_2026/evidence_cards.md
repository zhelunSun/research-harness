# Evidence cards: knowledge-to-action interfaces

> Packet: `ch2-knowledge-action-interfaces-2026`
>
> Full-text state: four primary full texts inspected
>
> Zotero state: all four absent by stable identifier or exact title; evidence packet created because the selected Zotero target was the library root
>
> Writing state: candidate comparator evidence only; no contract merge

## Evidence-grade convention

- `G1`: peer-reviewed full text; the claim is limited to the reported mechanism and evaluation domain.
- `G2`: official arXiv full text; the mechanism is locatable, but peer review, independent replication, and general scientific validity are not upgraded.

## S-KAI-001: CangLing-KnowFlow

- Intake key: `chen_cangling_2025`; evidence grade: `G2` (arXiv v3, 2026 revision).
- Located mechanism: a procedural knowledge base combines formalized tools with hierarchical workflow DAGs; runtime failures trigger replacement, insertion, or parameter modification; post-task traces yield contextualized successful templates or conditional failure-repair rules.
- Evaluation fact: the paper reports 1,008 expert-validated workflow templates over 162 RS task descriptions and evaluates 324 workflows, including a separate ThinkGeo transfer test.
- Direct Chapter 2 pressure: “expert remote-sensing knowledge guides Agent planning” and “success/failure experience improves workflow repair” are no longer safe novelty claims.
- Boundary: the task descriptions began with LLM generation and expert workflow annotation; its success metrics assess workflow execution and planning quality. They do not directly test source provenance, evidence strength, conflicting scientific claims, conclusion downgrade, or unnecessary intervention.
- Official source: https://arxiv.org/abs/2512.15231

## S-KAI-002: KnowAgent

- Intake key: `zhu_knowagent_2025`; evidence grade: `G1` (Findings of NAACL 2025).
- Located mechanism: an action knowledge base is an action set plus allowed transition rules. The rules are verbalized to guide path generation, and domain experts participate in construction and refinement.
- Decision value: confirms that explicit procedural constraints can shape an Agent before tool execution, rather than remaining passive retrieved text.
- Boundary: HotpotQA and ALFWorld expose transition validity and task success, not scientific applicability, evidence adequacy, or remote-sensing conclusion boundaries.
- Official source: https://doi.org/10.18653/v1/2025.findings-naacl.205

## S-KAI-003: ontology-to-tools compilation

- Intake key: `zhou_ontology-to-tools_2026`; evidence grade: `G2` (arXiv proof-of-principle, 2026).
- Located mechanism: ontology constraints are transformed into tool interfaces that check proposed graph updates at call time and return structured violations for Agent repair.
- Decision value: provides a strong example of knowledge becoming an executable affordance and hard semantic constraint, not just a prompt paragraph.
- Boundary: the system targets ontology-conformant chemistry knowledge-graph construction from 30 papers. Chapter 2 should not use “compilation” unless its scientific constraints acquire comparable formal semantics and enforcement guarantees.
- Official source: https://arxiv.org/abs/2602.03439

## S-KAI-004: ExpeL

- Intake key: `zhao_expel_2024`; evidence grade: `G1` (AAAI 2024).
- Located mechanism: task trajectories are stored; same-task success/failure pairs and cross-task successes are used to create voted natural-language insights; similar successful trajectories and insights are recalled for one-shot inference on unseen tasks.
- Decision value: supports keeping negative experience and case-based reuse in the idea library as an explicit mechanism, rather than treating “memory” as an unexplained store.
- Boundary: outcome feedback in deterministic benchmark environments is enough for task success labels but not for scientific truth. The paper itself notes that hallucinated reflections can mislead insight extraction.
- Official source: https://doi.org/10.1609/aaai.v38i17.29936

## Mechanism map

| Source | Knowledge carrier | Behavioural interface | What is evaluated | Chapter 2 boundary |
| --- | --- | --- | --- | --- |
| CangLing-KnowFlow | workflow template and repair rule | retrieve, instantiate, repair | workflow execution and transfer | procedural RS knowledge is occupied |
| KnowAgent | action set and transition rule | constrain next path | QA/embodied task performance | generic action constraints are occupied |
| Ontology-to-tools | formal ontology constraint | accept/reject tool call with feedback | KG construction fidelity | “compilation” requires stronger formalization |
| ExpeL | trajectory and natural-language insight | retrieve, bias, self-correct | interactive-task success | experience is strategy, not scientific evidence |

The sources justify a comparator map, not the cross-source thesis claim. `KAI-C5` therefore remains `needs_review`.

