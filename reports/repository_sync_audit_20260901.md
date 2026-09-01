# Thesis repository sync audit

> Date: 2026-09-01
>
> Status: historical verification snapshot. Current status must be obtained by
> running `python scripts/audit_repo_sync.py --all --strict-checkpoints --fetch`.

## Outcome

The canonical workspace is `D:/Projects/phd-thesis` with the `sibling-v1`
layout. The original `D:/Projects/phd-research` checkouts were not moved,
deleted, rewritten, or repurposed and remain a recovery fallback. The four
canonical working branches were clean and reported `ahead=0` and `behind=0`
after a fresh fetch and strict checkpoint audit.

| Role | Canonical GitHub repository | Active branch | Verified chapter SHA |
| --- | --- | --- | --- |
| Idea control plane | `zhelunSun/research-harness` | `codex/thesis-idea-v20260802` | verified directly against upstream; deliberately not self-checkpointed |
| Chapter 1 | `zhelunSun/URSA` | `codex/ch1-v2-e1-structured-planning` | `351adf137ef54fcbeb66def4c8d3c31e1ef0740d` |
| Chapter 2 | `zhelunSun/chapter2-urban-forest-knowledge` | `l2-task-distillation` | `807d5932d280d3500efe7fa5d786c8f2f90791fc` |
| Chapter 3 | `PandaBro666/urbfo-agent-demo` | `backup/ch3-routeb-20260831` | `4d841b7c10fe6a748610e98737db93db89f3990f` |

The control plane is verified by live upstream divergence rather than putting
its own SHA into the same commit, which would create an impossible
self-reference cycle.

## Recovery and remote corrections

- Chapter 3's recovery branch was copied without rewriting history to the
  canonical `PandaBro666/urbfo-agent-demo` origin. It descends from that
  repository's `fix/audit-p0` history.
- The no-common-ancestor boundary applies only to the mistaken historical
  `zhelunSun/fewshot-rs-mapping` master. That remote is retained as a read-only
  recovery source; its push URL is disabled in the canonical Chapter 3 clone.
- Canonical repository identity is stored as `owner/repository`; local SSH host
  aliases (`github-big` and `github-small` on this machine) are transport
  details and are not encoded as portable ownership.
- No force push, history rewrite, default-branch promotion, deletion, or legacy
  workspace migration was performed.

## Verification matrix

| Surface | Result |
| --- | --- |
| Four-repository strict cloud audit | 4 OK; all clean, `ahead=0`, `behind=0` |
| Control-plane sync tooling | 12 unit tests passed; Python compile and diff checks passed |
| Bootstrap | dry run blocked all four pre-existing canonical destinations and created nothing |
| Chapter 1 Git LFS | `git lfs fsck` passed; no object pending push |
| Chapter 2 repository validator | 41 PASS, 0 WARN, 0 FAIL |
| Chapter 3 test suite | all executed tests passed; 2 skipped |
| Line endings | explicit attributes added or repaired in the control plane, Chapter 2, and Chapter 3 |

Chapter 2's earlier JSONL checksum failures were working-tree CRLF conversion,
not changed research data. Normalizing the 45 tracked JSONL working copies to
their existing Git blob bytes restored every manifest check. Chapter 3's frozen
Python method blobs likewise remained unchanged while the checkout was restored
to LF.

## Environment and artifact boundaries

- Chapter 1's current base Python environment can run most tests but lacks the
  repository-pinned `autogen-agentchat==0.7.5` and
  `autogen-ext[openai]==0.7.5` dependencies: 115 tests passed and 6 failed for
  those unavailable imports. Do not repair this by installing into the global
  environment. Create a dedicated environment from `URSA/pyproject.toml` and
  rerun from `URSA/ExpertsRS` before treating 121/121 as reproduced on this
  machine.
- Chapter 3 tests pass in the existing `urban-forest-agent` conda environment.
  Earth Engine authentication remains an external, machine-specific gate.
- GitHub is not a complete backup for ignored raw/interim/processed datasets,
  Earth Engine assets, Drive exports, experiment outputs, secrets, or local
  environments. The external-data inventory in
  `repository_backup_inventory_20260831.md` remains in force.

## Satellite policy and remaining release decisions

`sheaf-ai`, `fewshot-rs-mapping`, and `zhelun-cv` are recorded as disabled,
optional satellites. Their expected cloud branches existed during this audit,
but they do not block the four-repository core gate. A future homepage should
enter the satellite registry first and become required only through an explicit
governance decision.

The active thesis branches were not promoted to `main` or made default branches,
and branch-protection settings were not changed. Those are release decisions,
not backup repairs. Retire the legacy workspace only after a later human review
confirms external-data recovery and the new-machine bootstrap path.
