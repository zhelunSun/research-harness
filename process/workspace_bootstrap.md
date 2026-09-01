# Thesis workspace bootstrap

## Purpose

This repository defines a portable, non-submodule workspace with one Idea
control plane and three required chapter repositories. The layout is named
`sibling-v1`:

```text
<workspace-root>/
  research-harness/
  URSA/
  chapter2-urban-forest-knowledge/
  urbfo-agent-demo/
  satellites/                 # optional; not part of the default gate
```

`config/repository_sync.json` lists only the four required core repositories.
It records each canonical GitHub `origin_repo`, expected working branch, and
relative path. `REPO_MAP.md` is the human-readable authority for repository
ownership and entry points; the registry is its machine-readable mirror.
`registry/core_repo_checkpoints.json` records the immutable
downstream chapter SHA last verified by the control plane. The control plane's
own branch is checked directly against its upstream because recording its own
commit SHA in the same commit would create a self-reference cycle. These files
have different jobs: structure changes rarely; downstream checkpoints change
after a verified cross-repository handoff.

## Safe bootstrap

Run the plan first from an existing, trusted `research-harness` checkout:

```powershell
python scripts/bootstrap_workspace.py --workspace-root D:/Projects/phd-thesis
```

The default is dry-run only. Review every destination, remote/branch, and root
navigation asset. The script creates no directories or files until `--apply`
is supplied. It refuses any pre-existing destination; `--skip-existing`
merely leaves that directory untouched after the operator has checked it. It
preserves compatible hand-written root entries and blocks incompatible
unmanaged ones. It never moves a legacy checkout, merges histories, rewrites
branches, or pushes data. See `workspace_navigation_policy.md` for generated
asset ownership and conflict handling.

```powershell
python scripts/bootstrap_workspace.py --workspace-root D:/Projects/phd-thesis --apply
python scripts/audit_repo_sync.py --all --fetch
python scripts/audit_workspace_navigation.py
```

For an already cloned workspace, review and then apply only missing navigation
assets with `--skip-existing` as documented in
`workspace_navigation_policy.md`.

If a private GitHub repository requires authentication, configure Git access
before `--apply`; do not embed credentials in the registry or command line.

## Existing workspaces and recovery material

Existing directories such as `thesis-harness`, `ch1-agent-workflow`,
`ch1-ursa`, `ch2-knowledge-enhancement`, `urbfo-mapping`, and
`exp-fewshot-mapping` are legacy or recovery checkouts, not bootstrap targets.
Preserve them until the new sibling workspace has passed the core audit and its
required checkpoints have been verified.

For Chapter 3, `backup/ch3-routeb-20260831` is now backed up on the canonical
`PandaBro666/urbfo-agent-demo` origin and descends from that repository's
`fix/audit-p0` history. The no-common-ancestor warning applies only when
comparing it with the legacy, mistaken `zhelunSun/fewshot-rs-mapping` master.
Keep that legacy history as a recovery source; do not merge, rebase, or
force-push it merely to make repository names look tidy. The current canonical
checkpoint is recorded in the registry rather than copied into this procedure.

## Satellites

Add a satellite only when it has a stable ownership and backup need. Put it in
`satellites` with `kind: satellite`, `required: false`, an `origin_repo`, and a
relative path. It is skipped by default; audit enabled satellites only with:

```powershell
python scripts/audit_repo_sync.py --all --include-satellites --fetch
```

An unavailable optional satellite reports a warning, not a core failure. A
satellite must never become a hidden dependency of a thesis chapter without
being promoted deliberately into the required registry.

## Daily use

Open `D:/Projects/phd-thesis/phd-thesis.code-workspace` for the canonical
four-repository editor view. The control-plane-local
`research-harness/phd-thesis.code-workspace` remains a portable fallback. At
the start of substantive work, run the core audit with `--fetch`. At the end,
validate in the owning repository, commit and push there, verify `ahead=0`, and
then update the downstream SHA registry here. Keep the old
`D:/Projects/phd-research` workspace read-only as a recovery fallback until a
later, explicit retirement decision.

## Unified command routing

The four directory names deliberately match their canonical GitHub repository
names. A local directory rename would not rename a GitHub repository, but it
would invalidate the relative paths in the sync registry, editor workspace,
documentation, and automation prompts. Keep the physical names stable and use
the friendly labels already defined in `phd-thesis.code-workspace`.

The user may start a Codex task from `D:/Projects/phd-thesis` or its saved
parent project and name only the research role. Resolve it as follows:

| User shorthand | Owning checkout |
| --- | --- |
| Idea / thesis / opening report | `research-harness` |
| Ch1 / URSA / workflow | `URSA` |
| Ch2 / knowledge | `chapter2-urban-forest-knowledge` |
| Ch3 / evaluation / Beijing assets | `urbfo-agent-demo` |

Before editing, enter the owning checkout and run its sync gate. Keep code,
experiments, and raw evidence in that repository; update the control-plane
checkpoint only after the downstream commit is validated and pushed. A task
must not require the user to switch the app manually between the four folders.
