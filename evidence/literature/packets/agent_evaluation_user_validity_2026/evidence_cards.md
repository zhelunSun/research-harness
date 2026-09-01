# Evidence cards: Agent evaluation and user validity

> Packet: `agent-evaluation-user-validity-2026`  
> Full-text state: four official PDFs inspected  
> Zotero state: absent by DOI/exact title; import not authorized  
> Writing state: provisional keys; no contract merge

## S-AEV-001: AgentBoard

- Intake key: `ma_agentboard_2024`; evidence grade: `G1` (NeurIPS 2024).
- Located contribution: progress rate over human-annotated subgoals, trajectory display, long-range interaction analysis, and human verification across 60 trajectories per task.
- Decision value: directly supports the narrow statement that final success rate hides partial progress and failure stage.
- Boundary: the benchmark relies on human-authored subgoals and mainly simulated environments; it is not evidence of target-user utility.
- Official source: https://doi.org/10.52202/079017-2365

## S-AEV-002: ToolSandbox

- Intake key: `lu_toolsandbox_2025`; evidence grade: `G1` (Findings of NAACL 2025).
- Located contribution: mutable world state, implicit tool dependencies, on-policy conversation, milestone DAGs, and minefields for forbidden events.
- Decision value: offers an operational pattern for grading intermediate state and prohibited actions across non-unique trajectories.
- Boundary: milestones are expensive expert annotations; the GPT-4o user simulator has documented hallucination and instruction-following errors.
- Official source: https://doi.org/10.18653/v1/2025.findings-naacl.65

## S-AEV-003: τ-bench

- Intake key: `yao_tau-bench_2025`; evidence grade: `G1` (ICLR 2025).
- Located contribution: domain policies, database tools, simulated users, objective end-state checks, and `pass^k` for consistency across repeated trials.
- Decision value: shows that average one-run success can conceal low repeated-run reliability and policy-following failures.
- Boundary: the user is simulated and the primary reward is based on final database/output state; the paper itself notes simulator limitations and possible policy-violation blind spots.
- Official source: https://openreview.net/forum?id=roNSXZpUDN

## S-AEV-004: PULSE human-agent evaluation

- Intake key: `chen_assess_2026`; evidence grade: `G1` (ICML 2026 paper, arXiv v3).
- Located contribution: user ratings from more than 36,000 OpenHands sessions and 15,000 users, prediction-powered satisfaction estimation, randomized comparisons, and explicit benchmark-to-user comparison.
- Decision value: provides actual-user evidence that benchmark ranking and in-the-wild experience can disagree.
- Boundary: one software-agent platform and user ratings do not establish transfer to urban-forest users, scientific correctness, ecology, or planning outcomes.
- Official source: https://arxiv.org/abs/2510.09801

## Decision synthesis

The four sources should remain separate along two axes:

| Evaluation surface | Direct source | What it does not prove |
| --- | --- | --- |
| Partial process progress | AgentBoard | user utility or real-world domain validity |
| Mutable state and trajectory constraints | ToolSandbox | real-user behavior or scientific sufficiency |
| Repeated-run consistency and policy following | τ-bench | actual-user effectiveness |
| In-the-wild user satisfaction | PULSE | remote-sensing scientific correctness or construct transfer |

Therefore `AEV-C5` remains `needs_review`: Chapter 3 may borrow design patterns, but it must define and validate its own city-forest task dependencies, deterministic checks, scientific-error criteria, target-user outcomes, and any human-participant compliance route.
