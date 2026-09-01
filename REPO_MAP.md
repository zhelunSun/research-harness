# 博士论文 canonical repository map

> Scope: this is the single human-readable authority for cross-repository paths,
> ownership, and entry points in `D:/Projects/phd-thesis`.
> Thesis framing belongs to `THESIS_STATE.md`; current action belongs to
> `process/current_execution_plan_20260802.md`.

## Start route

1. Use this file to identify the owning repository.
2. Read `THESIS_STATE.md` for the accepted thesis-wide framing.
3. Read `process/current_execution_plan_20260802.md`, starting at `## 0. Resume here`.
4. Read control-plane `AGENTS.md` for protected boundaries.
5. Check `registry/active_work.json` before writing.
6. Enter only the owning repository and read its `AGENTS.md` plus the active brief named there.

Do not scan every repository by default.

## Required repositories

| Research role | Canonical checkout | First local entry | Ownership boundary |
| --- | --- | --- | --- |
| Thesis Idea control plane | `research-harness/` | `AGENTS.md` | Thesis-wide framing, decisions, claims, evidence status, repository routing, and checkpoints |
| Chapter 1 system and workflow | `URSA/` | `AGENTS.md` | System implementation, workflow experiments, traces, and Chapter 1 evidence |
| Chapter 2 knowledge and reasoning | `chapter2-urban-forest-knowledge/` | `AGENTS.md` then `PLAN.md` | Knowledge/evidence assets, screening, reasoning experiments, and local decisions |
| Chapter 3 system evaluation | `urbfo-agent-demo/` | `AGENTS.md` then `PLAN.md` | Evaluation tasks, mapping substrates, replay fixtures, graders, and comparison runs |

All four checkouts are siblings under `D:/Projects/phd-thesis`. Chapter repositories may propose thesis-wide changes, but they do not redefine accepted framing or claims locally.

## Authority split

| Question | Source of truth |
| --- | --- |
| Which repository owns a task and where is it? | `REPO_MAP.md` |
| What is the accepted thesis framing and chapter relationship? | `THESIS_STATE.md` |
| What is the current milestone, next action, and human gate? | `process/current_execution_plan_20260802.md` |
| Which files are currently locked for parallel work? | `registry/active_work.json` |
| Which branch, remote, entry docs, and checkpoint should automation verify? | `config/repository_sync.json` and `registry/core_repo_checkpoints.json` |

`config/repository_sync.json` is the machine-readable mirror of this map. A path,
repository role, or required-entry change is incomplete until both surfaces agree
and `scripts/audit_workspace_navigation.py` passes.

Prose files may cite an older scientific or evidence baseline SHA. Current Git
freshness and recoverability are determined only by `audit_repo_sync.py` and
`registry/core_repo_checkpoints.json`. A prose label that says "current tip" but
disagrees with those machine surfaces is navigation drift, not a second tip.

## Recovery boundary

`D:/Projects/phd-research` is recovery-only and read-only. Its historical
directories, logs, and archives may be used for provenance-checked recovery,
but never as current navigation or thesis state.

## Maintenance rule

Keep this file short. Add detailed plans, methods, evidence, and run history to
their owning repositories. Do not turn this map into a roadmap or status log.
