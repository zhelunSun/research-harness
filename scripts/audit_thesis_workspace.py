#!/usr/bin/env python3
"""Audit thesis repositories, navigation, literature freshness, and human gates.

This is the portable read-only entry point for routine workspace maintenance.
Use ``--fetch`` when current remote state is required; otherwise local tracking
refs are used. The command never writes Zotero or tracked repository content.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_literature_control import (
    ControlError as LiteratureControlError,
    audit_literature_control,
)
from scripts.audit_human_gates import GateAuditError, audit_human_gates
from scripts.audit_repo_sync import (
    ConfigError as RepoConfigError,
    audit_repository,
    exit_code as repo_exit_code,
    load_targets,
)
from scripts.audit_workspace_navigation import (
    AuditError as NavigationAuditError,
    ConfigError as NavigationConfigError,
    audit_workspace,
)

DEFAULT_CONFIG = ROOT / "config" / "repository_sync.json"
DEFAULT_CHECKPOINTS = ROOT / "registry" / "core_repo_checkpoints.json"


def _combined_exit_code(*codes: int) -> int:
    if 1 in codes:
        return 1
    if 2 in codes:
        return 2
    return 0


def audit_thesis_control(
    root: Path = ROOT,
    *,
    config_path: Path | None = None,
    checkpoints_path: Path | None = None,
    workspace_root: Path | None = None,
    fetch: bool = False,
    strict_checkpoints: bool = False,
    as_of: date | None = None,
) -> dict[str, Any]:
    """Return one machine-readable view of workspace and literature health."""

    resolved_root = root.resolve()
    config = (config_path or resolved_root / "config" / "repository_sync.json").resolve()
    checkpoints = (
        checkpoints_path or resolved_root / "registry" / "core_repo_checkpoints.json"
    ).resolve()
    canonical_workspace = (workspace_root or resolved_root.parent).resolve()

    navigation = audit_workspace(config, canonical_workspace)
    targets = load_targets(config, checkpoints_path=checkpoints)
    repositories = [
        audit_repository(
            target["path"],
            target["name"],
            target.get("expected_branch"),
            fetch,
            repository_id=target["id"],
            kind=target["kind"],
            required=target["required"],
            expected_origin_repo=target.get("expected_origin_repo"),
            checkpoint=target.get("checkpoint"),
            strict_checkpoints=strict_checkpoints,
        )
        for target in targets
    ]
    repositories_code = repo_exit_code(repositories)
    literature = audit_literature_control(resolved_root, as_of=as_of or date.today())
    human_gates = audit_human_gates(resolved_root)
    overall_code = _combined_exit_code(
        int(navigation["exit_code"]),
        repositories_code,
        int(literature["exit_code"]),
        int(human_gates["exit_code"]),
    )
    readiness = "ready" if overall_code == 0 else "attention_required" if overall_code == 2 else "blocked"
    gates = list(human_gates.get("open_gates", []))
    return {
        "schema_version": "1.0",
        "audited_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "workspace_root": str(canonical_workspace),
        "readiness": readiness,
        "exit_code": overall_code,
        "components": {
            "navigation": navigation,
            "repositories": {
                "exit_code": repositories_code,
                "items": repositories,
            },
            "literature": literature,
            "human_gates": human_gates,
        },
        "pending_human_gates": gates,
    }


def render_text(result: dict[str, Any]) -> str:
    label = {0: "OK", 1: "CRITICAL", 2: "WARN"}[result["exit_code"]]
    components = result["components"]
    navigation = components["navigation"]
    repositories = components["repositories"]
    literature = components["literature"]
    human_gates = components["human_gates"]
    runtime = literature.get("runtime_scan", {})
    lines = [
        f"[{label}] thesis control: readiness={result['readiness']} root={result['workspace_root']}",
        f"  navigation: exit={navigation['exit_code']} issues={len(navigation['issues'])}",
        f"  repositories: exit={repositories['exit_code']} count={len(repositories['items'])}",
        f"  literature: exit={literature['exit_code']} packets={literature['packets_total']} "
        f"sources={literature['sources_total']} runtime_items={runtime.get('registered_zotero_items')}",
        f"  human gates: exit={human_gates['exit_code']} total={human_gates['gates_total']} "
        f"open={len(human_gates['open_gates'])}",
    ]
    for repository in repositories["items"]:
        repository_issues = repository.get("issues", [])
        if repository_issues:
            issue_codes = ",".join(issue["code"] for issue in repository_issues)
            lines.append(
                f"  - REPO {repository['id']}: behind={repository['behind']} "
                f"ahead={repository['ahead']} dirty={repository['dirty']} issues={issue_codes}"
            )
    for issue in navigation["issues"]:
        lines.append(f"  - NAV {issue['code']}: {issue['message']}")
    for issue in literature["issues"]:
        lines.append(f"  - LIT {issue['code']}: {issue['message']}")
    for issue in human_gates["issues"]:
        lines.append(f"  - GATE-REGISTRY {issue['code']}: {issue['message']}")
    for gate in result["pending_human_gates"]:
        lines.append(
            f"  - GATE {gate['gate_id']}: {gate['status']} "
            f"[{gate['category']}] ({gate['gate']})"
        )
    lines.append(
        f"summary: exit={result['exit_code']} pending_human_gates={len(result['pending_human_gates'])}"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--checkpoints", type=Path, default=None)
    parser.add_argument("--workspace-root", type=Path, default=None)
    parser.add_argument("--fetch", action="store_true", help="refresh remote-tracking metadata")
    parser.add_argument("--strict-checkpoints", action="store_true")
    parser.add_argument(
        "--as-of",
        type=lambda value: datetime.strptime(value, "%Y-%m-%d").date(),
        default=None,
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit_thesis_control(
            args.root,
            config_path=args.config,
            checkpoints_path=args.checkpoints,
            workspace_root=args.workspace_root,
            fetch=args.fetch,
            strict_checkpoints=args.strict_checkpoints,
            as_of=args.as_of,
        )
    except (
        RepoConfigError,
        NavigationConfigError,
        NavigationAuditError,
        LiteratureControlError,
        GateAuditError,
    ) as exc:
        payload = {"exit_code": 1, "configuration_error": str(exc)}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"[CRITICAL] thesis control: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
