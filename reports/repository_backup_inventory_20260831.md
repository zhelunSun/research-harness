# Thesis repository backup inventory

> Repository-location, Chapter 3 lineage, and active-branch status in this
> snapshot are superseded by `repository_sync_audit_20260901.md`. Its
> large-data and external-asset inventory remains relevant.

> Date: 2026-08-31
>
> Scope: Git history, small tracked assets, LFS and external-data recovery
> surfaces. This report does not claim that large research data have been
> migrated or fully backed up.

## Git cloud checkpoints

| Repository | Active cloud ref | Content checkpoint | Recovery status |
| --- | --- | --- | --- |
| Idea control plane | `codex/thesis-idea-v20260802` | content `697da63`; governance `50bddf8` | Branch has an upstream and the control-plane content/tooling was pushed |
| Chapter 1 / URSA | `codex/ch1-v2-e1-structured-planning` | content `4a881a2`; LFS fix `351adf1` | Branch pushed; 121 unittests, figure rendering and clean-clone LFS recovery passed |
| Chapter 2 | `l2-task-distillation` | content `bc0ce42`; policy `e91bfef` | Branch pushed; G2, G3 and repository-state validators passed |
| Chapter 3 | `backup/ch3-routeb-20260831` | content `7b8e05d`; policy `4bdef41` | New remote branch created; clean clone and `git fsck` passed |

Protected Chapter 1 milestones:

- `prototype-notebook-v0-20250307` -> `19db55b`;
- `ch1-v053-closeout-20260819` -> `9e18532`.

## Large-data and LFS findings

### Chapter 1

- `ExpertsRS/data/Sentinel2_Dongcheng_20230718.tif` and the historical
  `ExpertsRS/data/Sentinel2_Xicheng_2023.tif` are represented by Git LFS.
- A clean clone with smudge disabled followed by `git lfs fetch --all origin`
  restored both objects (8,032,606 and 46,550,467 bytes); `git lfs fsck` passed.
- `assets/img/1Paradgim_trans_00.jpg` predates LFS adoption and is intentionally
  stored as a 339,986-byte normal Git object. Commit `351adf1` adds a precise
  attribute exception without rewriting history, after which `git lfs fsck`
  passes.
- `ExpertsRS/results/`, PNG render outputs, local environments and caches remain
  ignored. Reproducible Mermaid sources, theme, renderer and lightweight SVGs
  are tracked.

### Chapter 2

- No Git LFS pointers or untracked files above 20 MB were found.
- `.env`, local loop caches and `tmp/` remain ignored and are not cloud backup.

### Chapter 3

- No Git LFS pointers or untracked files above 20 MB were found in this audit.
- Raw/interim/processed data, labels, maps, figures, experiment outputs, private
  notes and literature PDFs are intentionally ignored by Git.
- GEE assets and Google Drive exports remain external dependencies. Their asset
  IDs, pull manifests and list/download entry point are preserved in the repo;
  GitHub alone is not a complete data backup.

## Recovery boundary and next actions

1. Use GitHub for code, documents, configuration, small reproducible assets,
   manifests and provenance.
2. Preserve the Chapter 1 LFS remote and repeat the clean-clone fetch when LFS
   rules or raster inputs change.
3. Build a separate checksum-indexed inventory for GEE/Drive/raw result assets;
   do not add them directly to Git merely to clear an audit warning.
4. Run `python scripts/audit_repo_sync.py --all --fetch` every three days and at
   the end of any materially productive session.
