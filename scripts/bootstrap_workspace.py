#!/usr/bin/env python3
"""Bootstrap a sibling-v1 thesis workspace only after an explicit ``--apply``.

The default is a dry run.  It never repurposes an existing checkout, moves
files, deletes directories, or force-pushes.  Inspect the plan first, then use
``--apply --skip-existing`` only after independently checking every existing
directory.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any

try:  # Supports both ``python scripts/...`` and ``python -m scripts...``.
    from scripts.audit_repo_sync import ConfigError, DEFAULT_CONFIG, load_targets
except ModuleNotFoundError:  # pragma: no cover - exercised by direct execution
    from audit_repo_sync import ConfigError, DEFAULT_CONFIG, load_targets


ROOT = Path(__file__).resolve().parents[1]


def clone_url(origin_repo: str) -> str:
    """Return a portable GitHub URL; authentication is delegated to Git."""

    return f"https://github.com/{origin_repo}.git"


def build_plan(config_path: Path, workspace_root: Path) -> list[dict[str, Any]]:
    """Build a non-mutating clone plan for the four required core repositories."""

    targets = load_targets(config_path)
    source_control_root = config_path.resolve().parents[1]
    destination_control_root = workspace_root.resolve() / source_control_root.name
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


def render_plan(plan: list[dict[str, Any]], *, skip_existing: bool) -> str:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, required=True, help="parent directory for the sibling workspace")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--apply", action="store_true", help="perform the displayed clone plan")
    parser.add_argument("--skip-existing", action="store_true", help="leave pre-existing directories untouched")
    args = parser.parse_args(argv)
    try:
        plan = build_plan(args.config, args.workspace_root)
        print(render_plan(plan, skip_existing=args.skip_existing))
        if not args.apply:
            return 0
        apply_plan(plan, skip_existing=args.skip_existing)
        print("Bootstrap clone plan completed. Run audit_repo_sync.py --all --fetch before work.")
        return 0
    except (ConfigError, subprocess.CalledProcessError) as exc:
        print(f"[CRITICAL] bootstrap: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
