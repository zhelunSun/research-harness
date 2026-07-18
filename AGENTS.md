# AGENTS.md · Thesis Idea Control Plane

This repository has two deliberately separated surfaces:

1. the reusable `research-harness` skill (`SKILL.md`, `references/`);
2. the local thesis idea control plane (`THESIS_STATE.md`, `ideas/`, `claims/`,
   `decisions/`).

For thesis-facing work, read in this order:

1. `THESIS_STATE.md`;
2. `decisions/DEC-2026-0717-three-layer-storyline.md`;
3. `ideas/chapter_ideas.md`;
4. `claims/key_claims.md`;

The formal Chinese thesis outline is maintained separately in
`thesis/outline_zh.md` once created. It must translate an accepted idea version;
it must not silently redefine the idea.

## Boundaries

- This repo owns thesis-wide questions, the relationship among the three
  research contents, chapter-level boundaries and working propositions.
- It does not own raw runs, chapter-local baselines, rubrics or result files.
- It does not prescribe chapter-local algorithms, experiment groups, task counts
  or execution schedules at the idea stage.
- Downstream repositories may propose framing changes; accepted changes are
  reflected here before the Chinese outline or downstream plans are updated.
- Never rewrite a downstream result or evidence status merely to fit the current
  storyline.
- The reusable skill remains domain-agnostic. Thesis-specific scientific content
  belongs in the thesis control-plane files, not in `SKILL.md` or `references/`.

## Downstream map

- Research content 1 prototype/method: `D:/projects/phd-thesis/URSA/`
- Research content 2 execution: `D:/projects/phd-thesis/chapter2-urban-forest-knowledge/`
- Research content 2 product substrate: `D:/projects/phd-thesis/sheaf-ai/`
- Research content 3 application: `D:/projects/phd-thesis/urbfo-agent-demo/`
