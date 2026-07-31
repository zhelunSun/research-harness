# AGENTS.md · Thesis Idea Control Plane

This repository has three deliberately separated surfaces:

1. the reusable `research-harness` skill (`SKILL.md`, `references/`);
2. the local thesis idea control plane (`THESIS_STATE.md`, `ideas/`, `claims/`,
   `decisions/`);
3. the research incubation surface (`studies/`), whose findings remain
   non-canonical until accepted through an explicit proposal.

For thesis-facing work, read in this order:

1. `THESIS_STATE.md`;
2. `decisions/DEC-2026-0729-eval-driven-experience-ready-storyline.md`;
3. `decisions/DEC-2026-0730-working-title-and-content-names.md`;
4. `ideas/chapter_ideas.md`;
5. `ideas/agent_frontier_alignment.md`;
6. `claims/key_claims.md`;
7. `evidence/opening_evidence_matrix.md`;

`decisions/DEC-2026-0717-three-layer-storyline.md` remains historical context.
Its planning--constraint relationship is retained, while its third-content
"scenario application" role is partially superseded by the 2026-07-29 decision.

The formal Chinese thesis outline is maintained separately in
`thesis/outline_zh.md` once created. It must translate an accepted idea version;
it must not silently redefine the idea.

For cross-repository outline-freeze execution, also read
`process/outline_freeze_parallel_protocol_20260730.md`. For the non-blocking
meta-harness study brief, read
`ideas/scientific_research_harness_research_brief.md`. When working on that
study, enter through `studies/scientific-harness/README.md`, then read only the
target study file and its referenced rows in `sources.csv`.

## Boundaries

- This repo owns thesis-wide questions, the relationship among the three
  research contents, chapter-level boundaries, working propositions and
  cross-repository evidence pointers/status.
- It does not own raw runs, chapter-local baselines, rubrics or result files.
- It does not prescribe chapter-local algorithms, experiment groups, task counts
  or execution schedules at the idea stage.
- Downstream repositories may propose framing changes; accepted changes are
  reflected here before the Chinese outline or downstream plans are updated.
- Never rewrite a downstream result or evidence status merely to fit the current
  storyline.
- The reusable skill remains domain-agnostic. Thesis-specific scientific content
  belongs in the thesis control-plane files, not in `SKILL.md` or `references/`.
- `studies/` is an incubation surface between idea and stable reference.
  Study findings do not change thesis claims or the reusable skill until a human
  accepts an explicit proposal.

## Downstream map

- Research content 1 prototype/method: `D:/projects/phd-thesis/URSA/`
- Research content 2 execution: `D:/projects/phd-thesis/chapter2-urban-forest-knowledge/`
- Research content 2 product substrate: `D:/projects/phd-thesis/sheaf-ai/`
- Research content 3 task/evaluation assets and mapping case:
  `D:/projects/phd-thesis/urbfo-agent-demo/`
