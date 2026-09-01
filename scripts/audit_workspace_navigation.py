#!/usr/bin/env python3
"""Audit the portable navigation contract of a sibling-v1 thesis workspace.

Exit ``0`` means the navigation contract passes. Exit ``2`` means the audit
completed and found repairable navigation drift. Exit ``1`` means the audit
could not complete because its configuration or an inspected file was invalid.
The command is read-only, including when a recovery workspace is supplied.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "repository_sync.json"
ROOT_ENTRY_FILES = ("README.md", "AGENTS.md", "phd-thesis.code-workspace")
CURRENT_PLAN_RE = re.compile(
    r"(?P<path>(?:[A-Za-z]:[\\/])?[^`\"'<>\s]*current_execution_plan[^`\"'<>\s]*\.md)",
    re.IGNORECASE,
)
LEGACY_NOTICE_TERMS = (
    "recovery-only",
    "recovery only",
    "read-only",
    "do not write",
    "not a writable",
    "legacy",
    "历史",
    "只读",
    "恢复",
)


class ConfigError(ValueError):
    """The navigation configuration cannot be interpreted safely."""


class AuditError(RuntimeError):
    """The audit could not read an inspected surface reliably."""


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigError(f"{label} must contain a JSON object")
    return value


def _safe_name(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or Path(value).name != value:
        raise ConfigError(f"{label} must be one directory or file name")
    return value


def load_navigation_config(config_path: Path) -> dict[str, Any]:
    """Load the sibling-v1 navigation contract from the sync registry."""

    data = _read_json(config_path, "repository sync configuration")
    if data.get("schema_version") != 2:
        raise ConfigError("navigation audit requires repository sync schema_version 2")
    workspace = data.get("workspace")
    if not isinstance(workspace, dict) or workspace.get("layout") != "sibling-v1":
        raise ConfigError("navigation audit requires workspace.layout = sibling-v1")

    navigation = workspace.get("navigation", {})
    if not isinstance(navigation, dict):
        raise ConfigError("workspace.navigation must be an object")
    control_plane_dir = _safe_name(
        navigation.get("control_plane_dir", "research-harness"),
        "workspace.navigation.control_plane_dir",
    )
    root_entries = navigation.get("root_entry_files", list(ROOT_ENTRY_FILES))
    if not isinstance(root_entries, list) or set(root_entries) != set(ROOT_ENTRY_FILES):
        raise ConfigError(
            "workspace.navigation.root_entry_files must contain README.md, AGENTS.md, "
            "and phd-thesis.code-workspace"
        )
    deprecated_markers = navigation.get("deprecated_markers", ["thesis-harness", "phd-research"])
    if not isinstance(deprecated_markers, list) or not deprecated_markers or not all(
        isinstance(item, str) and item for item in deprecated_markers
    ):
        raise ConfigError("workspace.navigation.deprecated_markers must be a non-empty string list")
    recovery_marker = _safe_name(
        navigation.get("recovery_marker", ".recovery-only.json"),
        "workspace.navigation.recovery_marker",
    )

    repositories = data.get("repositories")
    if not isinstance(repositories, list):
        raise ConfigError("repositories must be a list")
    required = [item for item in repositories if isinstance(item, dict) and item.get("required") is True]
    if len(required) != 4:
        raise ConfigError(f"sibling-v1 navigation requires four required repositories, found {len(required)}")
    controls = [item for item in required if item.get("kind") == "control_plane"]
    if len(controls) != 1:
        raise ConfigError("sibling-v1 navigation requires exactly one required control_plane")

    seen_ids: set[str] = set()
    for item in required:
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in seen_ids:
            raise ConfigError("each required repository needs a unique non-empty id")
        seen_ids.add(identifier)
        if not isinstance(item.get("name"), str) or not item["name"]:
            raise ConfigError(f"required repository {identifier} needs a name")
        if not isinstance(item.get("path"), str) or not item["path"]:
            raise ConfigError(f"required repository {identifier} needs a path")
        entry_docs = item.get("entry_docs")
        if not isinstance(entry_docs, list) or not entry_docs or not all(
            isinstance(entry, str) and entry for entry in entry_docs
        ):
            raise ConfigError(f"required repository {identifier} needs a non-empty entry_docs list")

    return {
        "layout": "sibling-v1",
        "control_plane_dir": control_plane_dir,
        "root_entry_files": tuple(root_entries),
        "deprecated_markers": tuple(deprecated_markers),
        "recovery_marker": recovery_marker,
        "repositories": required,
    }


def default_workspace_root(config_path: Path) -> Path:
    """Infer the canonical root from ``<root>/<control-plane>/config``."""

    return config_path.resolve().parents[2]


def _add_issue(
    result: dict[str, Any],
    code: str,
    message: str,
    *,
    path: Path | None = None,
    line: int | None = None,
) -> None:
    issue: dict[str, Any] = {"code": code, "message": message}
    if path is not None:
        issue["path"] = str(path)
    if line is not None:
        issue["line"] = line
    result["issues"].append(issue)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise AuditError(f"cannot read active entry surface {path}: {exc}") from exc


def _inside(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ConfigError(f"{label} escapes canonical workspace root: {resolved}") from exc
    return resolved


def _repository_path(workspace_root: Path, control_plane_dir: str, relative_path: str) -> Path:
    control_plane = workspace_root / control_plane_dir
    return _inside(control_plane / relative_path, workspace_root, f"repository path {relative_path!r}")


def _is_legacy_notice(line: str) -> bool:
    folded = line.casefold()
    return any(term.casefold() in folded for term in LEGACY_NOTICE_TERMS)


def _resolve_plan_reference(token: str, *, surface_root: Path, workspace_root: Path) -> Path:
    cleaned = token.rstrip(".,;:")
    candidate = Path(cleaned.replace("\\", "/"))
    if candidate.is_absolute():
        return candidate.resolve()
    if candidate.parts and candidate.parts[0].casefold() == "research-harness":
        return (workspace_root / candidate).resolve()
    return (surface_root / candidate).resolve()


def _scan_active_surface(
    result: dict[str, Any],
    path: Path,
    *,
    surface_root: Path,
    workspace_root: Path,
    deprecated_markers: tuple[str, ...],
) -> None:
    text = _read_text(path)
    for line_number, line in enumerate(text.splitlines(), start=1):
        folded = line.casefold()
        if not _is_legacy_notice(line):
            for marker in deprecated_markers:
                if marker.casefold() in folded:
                    _add_issue(
                        result,
                        "deprecated_workspace_route",
                        f"active entry surface contains deprecated marker {marker!r}",
                        path=path,
                        line=line_number,
                    )
        for match in CURRENT_PLAN_RE.finditer(line):
            token = match.group("path")
            target = _resolve_plan_reference(
                token,
                surface_root=surface_root,
                workspace_root=workspace_root,
            )
            if not target.is_file():
                _add_issue(
                    result,
                    "missing_current_execution_plan",
                    f"current execution plan reference does not exist: {token}",
                    path=path,
                    line=line_number,
                )


def _audit_root_entries(
    result: dict[str, Any],
    workspace_root: Path,
    config: dict[str, Any],
) -> None:
    control_plane_dir = config["control_plane_dir"]
    expected_map_pointer = f"{control_plane_dir}/REPO_MAP.md".casefold()
    for name in config["root_entry_files"]:
        path = workspace_root / name
        if not path.is_file():
            _add_issue(result, "missing_root_entry", f"canonical root is missing {name}", path=path)
            continue
        if name == "phd-thesis.code-workspace":
            try:
                payload = json.loads(_read_text(path))
            except json.JSONDecodeError as exc:
                _add_issue(result, "invalid_workspace_file", f"workspace JSON is invalid: {exc}", path=path)
                continue
            folders = payload.get("folders", []) if isinstance(payload, dict) else []
            paths = {
                str(item.get("path", "")).replace("\\", "/").rstrip("/").casefold()
                for item in folders
                if isinstance(item, dict)
            }
            if control_plane_dir.casefold() not in paths:
                _add_issue(
                    result,
                    "root_entry_missing_control_plane_pointer",
                    f"workspace file does not include {control_plane_dir}",
                    path=path,
                )
            continue

        text = _read_text(path)
        normalized = text.replace("\\", "/").casefold()
        if expected_map_pointer not in normalized:
            _add_issue(
                result,
                "root_entry_missing_control_plane_pointer",
                f"{name} does not point to {control_plane_dir}/REPO_MAP.md",
                path=path,
            )
        _scan_active_surface(
            result,
            path,
            surface_root=workspace_root,
            workspace_root=workspace_root,
            deprecated_markers=config["deprecated_markers"],
        )


def _audit_required_repositories(
    result: dict[str, Any],
    workspace_root: Path,
    config: dict[str, Any],
) -> None:
    for repository in config["repositories"]:
        repo_path = _repository_path(
            workspace_root,
            config["control_plane_dir"],
            repository["path"],
        )
        if not repo_path.is_dir():
            _add_issue(
                result,
                "missing_required_repository",
                f"required repository {repository['id']} is unavailable",
                path=repo_path,
            )
            continue
        for relative_entry in repository["entry_docs"]:
            entry = _inside(repo_path / relative_entry, repo_path, f"entry doc {relative_entry!r}")
            if not entry.is_file():
                _add_issue(
                    result,
                    "missing_entry_doc",
                    f"required entry doc for {repository['id']} is missing: {relative_entry}",
                    path=entry,
                )
                continue
            _scan_active_surface(
                result,
                entry,
                surface_root=repo_path,
                workspace_root=workspace_root,
                deprecated_markers=config["deprecated_markers"],
            )


def _audit_repo_map_registrations(
    result: dict[str, Any],
    workspace_root: Path,
    config: dict[str, Any],
) -> None:
    map_path = workspace_root / config["control_plane_dir"] / "REPO_MAP.md"
    if not map_path.is_file():
        return
    normalized = _read_text(map_path).replace("\\", "/").casefold()
    for repository in config["repositories"]:
        repo_path = _repository_path(
            workspace_root,
            config["control_plane_dir"],
            repository["path"],
        )
        checkout = f"{repo_path.name}/".casefold()
        if checkout not in normalized:
            _add_issue(
                result,
                "missing_repo_map_registration",
                f"REPO_MAP.md does not register required checkout {repo_path.name}/",
                path=map_path,
            )


def _audit_recovery_marker(
    result: dict[str, Any],
    recovery_root: Path,
    *,
    canonical_root: Path,
    marker_name: str,
) -> None:
    marker = recovery_root.resolve() / marker_name
    if not marker.is_file():
        _add_issue(
            result,
            "missing_recovery_marker",
            f"recovery workspace has no {marker_name}",
            path=marker,
        )
        return
    try:
        payload = json.loads(_read_text(marker))
    except json.JSONDecodeError as exc:
        _add_issue(result, "invalid_recovery_marker", f"recovery marker JSON is invalid: {exc}", path=marker)
        return
    expected = canonical_root.resolve()
    canonical_value = None
    if isinstance(payload, dict):
        canonical_value = payload.get("canonical_workspace", payload.get("canonical_root"))
    canonical_matches = False
    if isinstance(canonical_value, str) and canonical_value:
        canonical_matches = Path(canonical_value).resolve() == expected
    status = payload.get("status") if isinstance(payload, dict) else None
    writable = None
    if isinstance(payload, dict):
        writable = payload.get("writable", payload.get("writes_allowed"))
    if not isinstance(payload, dict) or (
        payload.get("schema_version") != 1
        or status not in {"recovery-only", "recovery_only"}
        or writable is not False
        or not canonical_matches
    ):
        _add_issue(
            result,
            "invalid_recovery_marker",
            "marker must declare schema_version=1, recovery-only status, writes disabled, "
            "and the audited canonical root",
            path=marker,
        )


def audit_workspace(
    config_path: Path,
    workspace_root: Path | None = None,
    *,
    recovery_roots: list[Path] | None = None,
) -> dict[str, Any]:
    """Return a machine-readable, non-mutating navigation audit."""

    config = load_navigation_config(config_path)
    canonical_root = (workspace_root or default_workspace_root(config_path)).resolve()
    result: dict[str, Any] = {
        "workspace_root": str(canonical_root),
        "layout": config["layout"],
        "required_repositories": len(config["repositories"]),
        "recovery_roots_checked": [],
        "issues": [],
    }
    _audit_root_entries(result, canonical_root, config)
    _audit_required_repositories(result, canonical_root, config)
    _audit_repo_map_registrations(result, canonical_root, config)
    for recovery_root in recovery_roots or []:
        resolved = recovery_root.resolve()
        result["recovery_roots_checked"].append(str(resolved))
        _audit_recovery_marker(
            result,
            resolved,
            canonical_root=canonical_root,
            marker_name=config["recovery_marker"],
        )
    result["exit_code"] = 2 if result["issues"] else 0
    return result


def render_text(result: dict[str, Any]) -> str:
    label = "OK" if result["exit_code"] == 0 else "WARN"
    lines = [
        f"[{label}] sibling-v1 navigation: root={result['workspace_root']} "
        f"required_repositories={result['required_repositories']}",
    ]
    for issue in result["issues"]:
        location = issue.get("path", "")
        if issue.get("line"):
            location = f"{location}:{issue['line']}"
        lines.append(f"  - {issue['code']}: {issue['message']} [{location}]")
    lines.append(f"summary: exit={result['exit_code']} issues={len(result['issues'])}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--workspace-root", type=Path, default=None)
    parser.add_argument(
        "--recovery-root",
        type=Path,
        action="append",
        default=[],
        help="optionally verify a read-only .recovery-only.json marker; may be repeated",
    )
    parser.add_argument("--json", action="store_true", help="write machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        result = audit_workspace(
            args.config,
            args.workspace_root,
            recovery_roots=args.recovery_root,
        )
    except (ConfigError, AuditError) as exc:
        payload = {"exit_code": 1, "configuration_error": str(exc), "issues": []}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"[CRITICAL] navigation audit: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
