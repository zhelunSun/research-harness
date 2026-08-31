# Repository cloud-sync policy

> Applies to the Idea control plane and the three thesis research repositories.
> Git cloud backup is distinct from academic upstream-proposal synchronization.

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
   first, then record its immutable branch/SHA in `research-harness`.
7. Never force-push thesis history or delete a remote checkpoint/tag without an
   explicitly verified replacement.

## Routine commands

From `research-harness`:

```powershell
python scripts/audit_repo_sync.py --all --fetch
python scripts/audit_repo_sync.py --repo ../URSA --fetch
python scripts/audit_repo_sync.py --all --no-fetch --json
```

The audit never commits or pushes. Exit `0` is clean and synchronized; exit `2`
is a non-blocking warning such as a dirty tree, behind-only state, or temporary
network failure; exit `1` is a recovery risk such as a missing upstream,
deleted remote branch, local-only commits, divergence, or LFS integrity failure.

## Repository-specific protections

- Chapter 1: preserve `prototype-notebook-v0-20250307` and
  `ch1-v053-closeout-20260819`; audit Git LFS separately from Git commits.
- Chapter 2: do not confuse `sync/upstream_proposals/` with GitHub backup.
- Chapter 3: use `backup/ch3-routeb-20260831`; it has no common ancestor with
  `origin/master`, so the two histories must not be directly merged or used to
  overwrite each other.
