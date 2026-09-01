# Repository cloud-sync policy

> Applies to the Idea control plane and the three required thesis research
> repositories. Git cloud backup is distinct from academic upstream-proposal
> synchronization.

## Workspace contract

The canonical local layout is `sibling-v1`: `research-harness`, `URSA`,
`chapter2-urban-forest-knowledge`, and `urbfo-agent-demo` are sibling
checkouts. `config/repository_sync.json` is the structural registry; its four
`repositories` entries are the required core gate. Optional satellites (CV,
homepage, product substrate, or historical method repositories) belong in the
separate `satellites` list and do not block a default core audit.

The canonical GitHub identity is stored as `origin_repo` (`owner/repository`),
not as a transport-specific URL. SSH aliases such as `github-big` and
`github-small` are allowed as long as they resolve to that repository identity.
Use `scripts/bootstrap_workspace.py` in dry-run mode before creating a new
machine checkout; it never repurposes an existing directory.

## Invariants

1. A local commit is not a backup until its active branch exists on `origin` and
   the branch reports `ahead=0` after a fresh fetch.
2. Start non-trivial work with a repository sync audit. Before a large or remote
   experiment, push a recoverable checkpoint.
3. End every materially productive session by validating, committing, pushing,
   and verifying the remote SHA. An unfinished but safe checkpoint may use
   `wip/<topic>-YYYYMMDD`.
4. Do not commit credentials, `.env`, private notes, unreviewed large binaries,
   or generated outputs merely to make the tree clean.
5. If the network is unavailable, keep the local commit and report it as
   **not backed up**. Local-only commits must not persist for more than three
   days.
6. For cross-repository changes, commit and push the owning chapter repository
   first, then record its immutable branch/SHA in
   `registry/core_repo_checkpoints.json` in `research-harness`.
7. Never force-push thesis history or delete a remote checkpoint/tag without an
   explicitly verified replacement.

## Routine commands

From `research-harness`:

```powershell
python scripts/audit_thesis_workspace.py --fetch
python scripts/audit_repo_sync.py --all --fetch
python scripts/audit_repo_sync.py --repo ../URSA --fetch
python scripts/audit_repo_sync.py --all --no-fetch --json
python scripts/audit_repo_sync.py --all --include-satellites --fetch
python scripts/audit_repo_sync.py --all --strict-checkpoints --fetch
python scripts/bootstrap_workspace.py --workspace-root D:/Projects/phd-thesis
```

`audit_thesis_workspace.py` is the routine first command. It composes the
repository sync audit, sibling-workspace navigation audit, literature control
audit, Zotero/SeaDrive runtime-snapshot freshness, and the thesis-wide
`registry/human_gates.json` into one read-only result. The gate audit validates
the five current maintenance, Zotero, writing, Ch2 evidence, and Ch3 route
decisions without inferring their state from prose. Use the component commands only when the unified result
identifies a specific surface that needs diagnosis.

The audit never commits or pushes. Exit `0` is clean and synchronized; exit `2`
is a non-blocking warning such as a dirty tree, behind-only state, or temporary
network failure; exit `1` is a recovery risk such as a missing upstream,
deleted remote branch, local-only commits, divergence, or LFS integrity failure.
Checkpoint drift is a warning by default because it may be a just-pushed chapter
change awaiting a control-plane record; `--strict-checkpoints` makes it a gate.

## Repository-specific protections

- Chapter 1: preserve `prototype-notebook-v0-20250307` and
  `ch1-v053-closeout-20260819`; audit Git LFS separately from Git commits.
- Chapter 2: do not confuse `sync/upstream_proposals/` with GitHub backup.
- Chapter 3: use `backup/ch3-routeb-20260831` on the canonical
  `PandaBro666/urbfo-agent-demo` origin. It descends from that repository's
  `fix/audit-p0` history. Only the legacy, mistaken
  `zhelunSun/fewshot-rs-mapping` master has no common ancestor with this branch;
  keep that repository as a recovery source rather than merging or overwriting
  histories. Update the checkpoint only after the canonical remote branch has
  been verified.
