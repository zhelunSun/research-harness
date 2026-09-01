# Workspace navigation policy

## Contract

`D:/Projects/phd-thesis` is the canonical writable root for the long-running
thesis workspace. Its `sibling-v1` layout has four required repositories:
`research-harness`, `URSA`, `chapter2-urban-forest-knowledge`, and
`urbfo-agent-demo`. `REPO_MAP.md` is the human-readable authority for
cross-repository paths, ownership, and entry points.
`config/repository_sync.json` is its machine-readable mirror and provides each
repository's active `entry_docs` to automation.

The canonical root must contain `README.md`, `AGENTS.md`, and
`phd-thesis.code-workspace`. Both Markdown entries must route a fresh agent to
`research-harness/REPO_MAP.md`; the workspace file must include a
`research-harness` folder. A new session reads the repository map, thesis state,
current execution plan, and control-plane contract, then only the owning
chapter repository and active brief.

Repository sync has two inspection modes. Omitting `--fetch` checks only local
and already-known remote-tracking state. Adding `--fetch` refreshes Git refs but
does not edit repository files or the worktree; weekly gardening uses this
freshness mode and reports any network failure explicitly.

`D:/Projects/phd-research` is recovery-only. It is not a second writable
workspace and must not supply current thesis state. Historical mentions are
allowed in active entry surfaces only when the same line explicitly labels
the path as legacy, read-only, or recovery-only.

## Navigation audit

Run from `research-harness`:

```powershell
python scripts/audit_workspace_navigation.py
python scripts/audit_workspace_navigation.py --json
python scripts/audit_workspace_navigation.py --recovery-root D:/Projects/phd-research
```

The audit is read-only. It checks:

1. all three canonical root entry files and their `research-harness` pointer;
2. every configured `entry_docs` file in the four required repositories;
3. deprecated `thesis-harness` or `phd-research` routes in active entry
   surfaces, excluding explicit recovery/legacy notices;
4. every referenced `current_execution_plan*.md` path in those surfaces;
5. an optional recovery marker only when `--recovery-root` is supplied.

Exit codes are stable automation interfaces:

- `0`: the complete requested audit passed;
- `2`: the audit completed and found repairable navigation drift;
- `1`: configuration or an inspected file prevented a reliable audit.

Exit `2` is not permission to rewrite research content. Fix navigation in the
owning repository or record a separate maintenance task. Exit `1` blocks any
claim that the workspace route is healthy.

## Recovery marker

The optional marker is `<recovery-root>/.recovery-only.json`:

```json
{
  "schema_version": 1,
  "status": "recovery-only",
  "writable": false,
  "canonical_workspace": "D:/Projects/phd-thesis"
}
```

For compatibility with an existing recovery marker, the audit also accepts
`status: recovery_only`, `writes_allowed: false`, and `canonical_root` as
equivalent aliases. New markers should use the preferred form above.

The audit only reads this file. Bootstrap never creates it, and the navigation
tool must never edit, rename, or delete the recovery workspace. Marker creation
or retirement is a separate, explicit operator action.

## Bootstrap ownership

`scripts/bootstrap_workspace.py` is dry-run by default. Its plan now includes
the four checkouts and the three canonical root entry assets. With `--apply`,
it creates missing generated entries, refreshes entries previously generated
by the script, and preserves compatible hand-written root entries. It blocks
an incompatible unmanaged root file unless `--force-navigation` is supplied
after manual review.

Generated Markdown files carry a management comment; the generated workspace
file carries `researchHarness.navigationManaged=true`. Re-running bootstrap is
therefore idempotent. To add navigation assets to an already cloned canonical
workspace without recloning repositories, first review the dry-run and then
use:

```powershell
python scripts/bootstrap_workspace.py --workspace-root D:/Projects/phd-thesis --skip-existing
python scripts/bootstrap_workspace.py --workspace-root D:/Projects/phd-thesis --apply --skip-existing
```

The generated templates are intentionally compatible with the existing root
README, AGENTS contract, and four-folder VS Code workspace. Bootstrap does not
modify chapter content, thesis state, active-work locks, or recovery material.
