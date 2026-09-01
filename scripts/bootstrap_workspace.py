#!/usr/bin/env python3
"""Bootstrap a sibling-v1 thesis workspace only after an explicit ``--apply``.

The default is a dry run.  It never repurposes an existing checkout, moves
files, deletes directories, or force-pushes.  Inspect the plan first, then use
``--apply --skip-existing`` only after independently checking every existing
directory.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

try:  # Supports both ``python scripts/...`` and ``python -m scripts...``.
    from scripts.audit_repo_sync import ConfigError, DEFAULT_CONFIG, load_targets
except ModuleNotFoundError:  # pragma: no cover - exercised by direct execution
    from audit_repo_sync import ConfigError, DEFAULT_CONFIG, load_targets


ROOT = Path(__file__).resolve().parents[1]
MANAGED_TEXT_MARKER = "<!-- managed by research-harness/scripts/bootstrap_workspace.py -->"
MANAGED_WORKSPACE_SETTING = "researchHarness.navigationManaged"


def clone_url(origin_repo: str) -> str:
    """Return a portable GitHub URL; authentication is delegated to Git."""

    return f"https://github.com/{origin_repo}.git"


def _workspace_navigation(config_path: Path) -> dict[str, Any]:
    """Read optional bootstrap navigation settings without breaking v1 callers."""

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read bootstrap configuration at {config_path}: {exc}") from exc
    workspace = data.get("workspace", {}) if isinstance(data, dict) else {}
    navigation = workspace.get("navigation", {}) if isinstance(workspace, dict) else {}
    if not isinstance(navigation, dict):
        raise ConfigError("workspace.navigation must be an object")
    return navigation


def _control_plane_dir(config_path: Path) -> str:
    navigation = _workspace_navigation(config_path)
    value = navigation.get("control_plane_dir", config_path.resolve().parents[1].name)
    if not isinstance(value, str) or not value or Path(value).name != value:
        raise ConfigError("workspace.navigation.control_plane_dir must be one directory name")
    return value


def build_plan(config_path: Path, workspace_root: Path) -> list[dict[str, Any]]:
    """Build a non-mutating clone plan for the four required core repositories."""

    targets = load_targets(config_path)
    destination_control_root = workspace_root.resolve() / _control_plane_dir(config_path)
    plan: list[dict[str, Any]] = []
    for target in targets:
        if not target["required"]:
            continue
        destination = (destination_control_root / target["relative_path"]).resolve()
        try:
            destination.relative_to(workspace_root.resolve())
        except ValueError as exc:
            raise ConfigError(f"target {target['id']} escapes workspace root: {destination}") from exc
        plan.append(
            {
                "id": target["id"],
                "destination": destination,
                "origin_repo": target.get("expected_origin_repo"),
                "branch": target.get("expected_branch"),
                "exists": destination.exists(),
            }
        )
    return plan


def _render_root_readme() -> str:
    return f"""{MANAGED_TEXT_MARKER}
# PhD Thesis Research Workspace

This is the canonical writable workspace for the long-running PhD research program.

## Start Here

1. Read `research-harness/REPO_MAP.md` to identify the owning repository.
2. Read `research-harness/THESIS_STATE.md`.
3. Resume from `research-harness/process/current_execution_plan_20260802.md`.
4. Read `research-harness/AGENTS.md` for protected boundaries.
5. Enter only the owning chapter repository and active brief named there.

Before non-trivial work, run:

```powershell
python research-harness/scripts/audit_repo_sync.py --all --strict-checkpoints --fetch
python research-harness/scripts/audit_workspace_navigation.py
```

`D:/Projects/phd-research` is recovery-only. It is not a writable source of current thesis state.
"""


def _render_root_agents() -> str:
    return f"""{MANAGED_TEXT_MARKER}
# Canonical Workspace Entry

This directory is the only writable local root for the current PhD thesis research program.

1. Run the audits listed in `README.md`.
2. Read `research-harness/REPO_MAP.md` and identify the owning repository.
3. Read `research-harness/THESIS_STATE.md` and resume through `research-harness/process/current_execution_plan_20260802.md`.
4. Read `research-harness/AGENTS.md` for protected boundaries.
5. Check `research-harness/registry/active_work.json` before editing.
6. Work only in the owning repository named by the current plan.

Do not scan all repositories by default. `D:/Projects/phd-research` is recovery-only and must not be edited.
"""


def _workspace_folder_name(identifier: str, fallback: str) -> str:
    labels = {
        "idea-control-plane": "Idea control plane",
        "chapter-1-ursa": "Chapter 1 - URSA",
        "chapter-2-knowledge": "Chapter 2 - Knowledge",
        "chapter-3-evaluation": "Chapter 3 - Evaluation",
    }
    return labels.get(identifier, fallback)


def _render_workspace_file(plan: list[dict[str, Any]], workspace_root: Path) -> str:
    folders = []
    for item in plan:
        relative = item["destination"].relative_to(workspace_root.resolve()).as_posix()
        folders.append({"name": _workspace_folder_name(item["id"], item["id"]), "path": relative})
    payload = {
        "folders": folders,
        "settings": {
            "files.eol": "\n",
            MANAGED_WORKSPACE_SETTING: True,
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _compatible_navigation_asset(path: Path, content: str, control_plane_dir: str) -> bool:
    if not path.is_file():
        return False
    try:
        existing = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    if existing == content:
        return True
    if path.name != "phd-thesis.code-workspace":
        normalized = existing.replace("\\", "/").casefold()
        return f"{control_plane_dir}/repo_map.md".casefold() in normalized
    try:
        payload = json.loads(existing)
    except json.JSONDecodeError:
        return False
    folders = payload.get("folders", []) if isinstance(payload, dict) else []
    paths = {
        str(item.get("path", "")).replace("\\", "/").rstrip("/").casefold()
        for item in folders
        if isinstance(item, dict)
    }
    return control_plane_dir.casefold() in paths


def _managed_navigation_asset(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        existing = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    if path.name != "phd-thesis.code-workspace":
        return MANAGED_TEXT_MARKER in existing
    try:
        payload = json.loads(existing)
    except json.JSONDecodeError:
        return False
    settings = payload.get("settings", {}) if isinstance(payload, dict) else {}
    return isinstance(settings, dict) and settings.get(MANAGED_WORKSPACE_SETTING) is True


def build_navigation_plan(config_path: Path, workspace_root: Path) -> list[dict[str, Any]]:
    """Build a deterministic plan for the three canonical root entry assets."""

    clone_plan = build_plan(config_path, workspace_root)
    control_plane_dir = _control_plane_dir(config_path)
    contents = {
        "README.md": _render_root_readme(),
        "AGENTS.md": _render_root_agents(),
        "phd-thesis.code-workspace": _render_workspace_file(clone_plan, workspace_root),
    }
    plan: list[dict[str, Any]] = []
    for name, content in contents.items():
        path = workspace_root.resolve() / name
        if not path.exists():
            status = "create"
        elif path.is_file() and path.read_text(encoding="utf-8") == content:
            status = "current"
        elif _managed_navigation_asset(path):
            status = "managed-update"
        elif _compatible_navigation_asset(path, content, control_plane_dir):
            status = "compatible"
        else:
            status = "conflict"
        plan.append({"name": name, "path": path, "content": content, "status": status})
    return plan


def render_plan(
    plan: list[dict[str, Any]],
    *,
    skip_existing: bool,
    navigation_plan: list[dict[str, Any]] | None = None,
) -> str:
    lines = ["Bootstrap plan (dry-run unless --apply is supplied):"]
    for item in plan:
        if item["exists"]:
            action = "SKIP existing checkout" if skip_existing else "BLOCK existing path"
        else:
            action = "CLONE"
        lines.append(
            f"- {action}: {item['id']} -> {item['destination']} "
            f"({item['origin_repo']} @ {item['branch']})"
        )
    if navigation_plan is not None:
        lines.append("Canonical root navigation assets:")
        for item in navigation_plan:
            action = {
                "create": "CREATE",
                "current": "KEEP current",
                "managed-update": "UPDATE managed",
                "compatible": "KEEP compatible",
                "conflict": "BLOCK unmanaged conflict",
            }[item["status"]]
            lines.append(f"- {action}: {item['path']}")
    return "\n".join(lines)


def apply_plan(plan: list[dict[str, Any]], *, skip_existing: bool) -> None:
    blocked = [item for item in plan if item["exists"] and not skip_existing]
    if blocked:
        names = ", ".join(item["id"] for item in blocked)
        raise ConfigError(f"refusing to touch existing path(s): {names}; re-run with --skip-existing after review")
    for item in plan:
        if item["exists"]:
            continue
        if not item["origin_repo"] or not item["branch"]:
            raise ConfigError(f"target {item['id']} lacks origin_repo or expected_branch")
        item["destination"].parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "git",
                "clone",
                "--branch",
                item["branch"],
                "--single-branch",
                clone_url(item["origin_repo"]),
                str(item["destination"]),
            ],
            check=True,
        )


def apply_navigation_plan(plan: list[dict[str, Any]], *, force: bool = False) -> None:
    """Create or refresh generated root entries without touching compatible hand-written files."""

    conflicts = [item for item in plan if item["status"] == "conflict" and not force]
    if conflicts:
        names = ", ".join(item["name"] for item in conflicts)
        raise ConfigError(
            f"refusing to overwrite unmanaged navigation asset(s): {names}; "
            "use --force-navigation only after review"
        )
    for item in plan:
        if item["status"] in {"current", "compatible"}:
            continue
        item["path"].parent.mkdir(parents=True, exist_ok=True)
        item["path"].write_text(item["content"], encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, required=True, help="parent directory for the sibling workspace")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--apply", action="store_true", help="perform the displayed clone plan")
    parser.add_argument("--skip-existing", action="store_true", help="leave pre-existing directories untouched")
    parser.add_argument(
        "--force-navigation",
        action="store_true",
        help="overwrite conflicting unmanaged root navigation assets after review",
    )
    args = parser.parse_args(argv)
    try:
        plan = build_plan(args.config, args.workspace_root)
        navigation_plan = build_navigation_plan(args.config, args.workspace_root)
        print(render_plan(plan, skip_existing=args.skip_existing, navigation_plan=navigation_plan))
        if not args.apply:
            return 0
        apply_plan(plan, skip_existing=args.skip_existing)
        apply_navigation_plan(navigation_plan, force=args.force_navigation)
        print("Bootstrap clone plan completed. Run audit_repo_sync.py --all --fetch before work.")
        return 0
    except (ConfigError, subprocess.CalledProcessError) as exc:
        print(f"[CRITICAL] bootstrap: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
