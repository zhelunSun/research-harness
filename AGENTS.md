# AGENTS.md · Thesis Idea Control Plane

This repository has three deliberately separated surfaces:

1. the reusable `research-harness` skill (`SKILL.md`, `references/`);
2. the local thesis idea control plane (`THESIS_STATE.md`, `ideas/`, `claims/`,
   `decisions/`);
3. the research incubation surface (`studies/`), whose findings remain
   non-canonical until accepted through an explicit proposal.

For thesis-facing work, read in this order:

1. `IDEA_VERSION.md`;
2. `THESIS_STATE.md`;
3. `process/current_execution_plan_20260802.md`;
4. `ideas/chapter_ideas.md`;
5. `claims/key_claims.md`;
6. `evidence/opening_evidence_matrix.md`.

`THESIS_STATE.md` and `process/current_execution_plan_20260802.md` are the only
thesis-wide surfaces that should be maintained continuously. The former is the
slow strategic source; the latter is the fast execution and session-resume
source. Keep the dated execution-plan filename as a stable entry point. Do not
create a new thesis-wide roadmap, status memo, or handoff merely because a new
chat or calendar date begins.

For a routine continuation, read `THESIS_STATE.md` and the execution plan's
`## 0. Resume here` first, then enter only the chapter repository and active
brief named there. At the end of any session with material progress, update the
snapshot and single next action in that section. Chat history is not a source
of truth.

Use `decisions/README.md` when a task changes the idea or needs historical
rationale. Read only the linked decisions relevant to that change. Read
`ideas/agent_frontier_alignment.md` when evaluating a frontier direction; it is
context, not an additional thesis commitment.

The formal Chinese thesis outline is maintained separately in
`thesis/outline_zh.md` once created. It must translate an accepted idea version;
it must not silently redefine the idea.

For cross-repository coordination, parallel chapter work, session routing, or
researcher-approval bandwidth, also read
`process/outline_freeze_parallel_protocol_20260730.md`. For the non-blocking
meta-harness study brief, read
`ideas/scientific_research_harness_research_brief.md`. When working on that
study, enter through `studies/scientific-harness/README.md`, then read only the
target study file and its referenced rows in `sources.csv`.

Before dispatching parallel writers, register their owning repository, file
scope, dependency, and stop condition in `registry/active_work.json`. Do not
dispatch overlapping locks. Close or expire the lock after review; the registry
coordinates work but never changes a scientific claim or evidence status.

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
- Thesis idea releases use date-based labels such as `idea-v2026.08.02`.
  They are independent from the reusable skill version in `SKILL.md`.
- A substantive change to titles, chapter roles, core claims, evidence status or
  execution priority requires a new decision, then synchronized updates to
  `IDEA_VERSION.md`, `THESIS_STATE.md`, canonical idea, claims and evidence.
- Historical decisions and reports remain immutable in substance. Add status or
  supersession metadata instead of rewriting the earlier record.
- A cloud-ready thesis release contains governance and cross-repository pointers
  only. Downstream code, runs and result changes are committed in their owning
  repositories.

## Downstream map

- Required core workspace uses the portable `sibling-v1` layout documented in
  `process/workspace_bootstrap.md`: this control plane, `URSA`,
  `chapter2-urban-forest-knowledge`, and `urbfo-agent-demo` are sibling
  checkouts.
- Research content 1 prototype/method: `../URSA/`
- Research content 2 execution: `../chapter2-urban-forest-knowledge/`
- Research content 2 product substrate, CV/homepage, and historical method
  repositories are optional satellites unless explicitly promoted.
- Research content 3 task/evaluation assets and mapping case:
  `../urbfo-agent-demo/`

## Git cloud-sync gate

GitHub backup is separate from academic upstream-proposal synchronization. Read
`process/repository_sync_policy.md` before cross-repository maintenance.

- Start non-trivial work with
  `python scripts/audit_repo_sync.py --repo <repo-path> --fetch`.
- Before a large run, push a recoverable checkpoint. At the end of a materially
  productive session, validate, commit, push, and verify `ahead=0`.
- A local commit is not a backup. Local-only commits must not persist longer
  than three days; network failures remain explicitly reported as not backed up.
- Commit and push downstream changes before recording their branch/SHA here.
- Record verified downstream chapter branch/SHA pairs in
  `registry/core_repo_checkpoints.json`; the control plane itself is gated by
  its configured branch/upstream divergence because a self-SHA checkpoint
  would be recursive. Use `--include-satellites` only when optional
  repositories are in scope.
- Never auto-commit research content, force-push thesis history, or delete a
  remote checkpoint/tag without a verified replacement.
