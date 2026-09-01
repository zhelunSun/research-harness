#!/usr/bin/env python3
"""Audit configured thesis repositories without changing tracked content.

``--fetch`` refreshes remote-tracking metadata only.  This command never
commits, pushes, merges, checks out, or rewrites repository content.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "repository_sync.json"
DEFAULT_CHECKPOINTS = ROOT / "registry" / "core_repo_checkpoints.json"
VALID_KINDS = {"control_plane", "chapter", "satellite"}


class ConfigError(ValueError):
    """A sync configuration cannot be interpreted safely."""


def run_git(repo: Path, *args: str, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(args, 124, "", f"{type(exc).__name__}: {exc}")


def redact_remote(url: str) -> str:
    return re.sub(r"(https?://)[^/@]+@", r"\1***@", url.strip())


def origin_repo_identity(url: str) -> str | None:
    """Return the GitHub-style ``owner/repository`` identity from a remote URL.

    The host and transport deliberately do not participate in the comparison:
    ``https://github.com``, a standard SSH URL, and local SSH aliases such as
    ``github-big`` all identify the same GitHub repository path.
    """

    cleaned = url.strip().rstrip("/")
    match = re.search(r"[/:]([^/:\s]+)/([^/\s]+?)(?:\.git)?$", cleaned)
    if not match:
        return None
    owner, repository = match.groups()
    if not owner or not repository or repository in {".", ".."}:
        return None
    return f"{owner}/{repository}"


def parse_lfs_pending(status_text: str) -> list[str]:
    pending: list[str] = []
    in_push = False
    for raw in status_text.splitlines():
        line = raw.strip()
        if line.startswith("Objects to be pushed"):
            in_push = True
            continue
        if line.startswith("Objects to be committed") or line.startswith("Objects not staged"):
            in_push = False
        elif in_push and line:
            pending.append(line)
    return pending


def lfs_findings(status_text: str, fsck_code: int, fsck_text: str) -> list[str]:
    findings = [f"LFS object pending push: {item}" for item in parse_lfs_pending(status_text)]
    if fsck_code:
        detail = next((line.strip() for line in fsck_text.splitlines() if line.strip()), "fsck failed")
        findings.append(f"LFS integrity failure: {detail}")
    return findings


def _issue(result: dict[str, Any], level: str, code: str, message: str) -> None:
    result["issues"].append({"level": level, "code": code, "message": message})


def _level(required: bool, strict: bool = False) -> str:
    return "critical" if required or strict else "warning"


def _remote_sha(repo: Path, branch: str) -> tuple[str | None, str | None]:
    probe = run_git(repo, "ls-remote", "--exit-code", "--heads", "origin", f"refs/heads/{branch}")
    if probe.returncode == 0:
        first_line = next((line for line in probe.stdout.splitlines() if line.strip()), "")
        return (first_line.split()[0] if first_line.split() else None), None
    if probe.returncode == 2 and not probe.stderr.strip():
        return None, "missing"
    detail = (probe.stderr or probe.stdout).strip().splitlines()
    return None, detail[-1] if detail else "ls-remote failed"


def audit_repository(
    repo: Path,
    name: str,
    expected_branch: str | None,
    fetch: bool,
    *,
    repository_id: str | None = None,
    kind: str = "chapter",
    required: bool = True,
    expected_origin_repo: str | None = None,
    checkpoint: dict[str, Any] | None = None,
    strict_checkpoints: bool = False,
) -> dict[str, Any]:
    """Audit one checkout.  The first four arguments remain v1-compatible."""

    repo = repo.resolve()
    result: dict[str, Any] = {
        "id": repository_id or name,
        "name": name,
        "kind": kind,
        "required": required,
        "path": str(repo),
        "branch": None,
        "expected_branch": expected_branch,
        "head": None,
        "upstream": None,
        "remote": None,
        "origin_repo": None,
        "expected_origin_repo": expected_origin_repo,
        "dirty": 0,
        "behind": None,
        "ahead": None,
        "checkpoint": checkpoint,
        "checkpoint_remote_sha": None,
        "issues": [],
    }

    inside = run_git(repo, "rev-parse", "--is-inside-work-tree")
    if inside.returncode or inside.stdout.strip() != "true":
        level = _level(required)
        code = "not_git_repository" if required else "optional_repository_unavailable"
        _issue(result, level, code, "path is not a Git work tree")
        return result

    branch = run_git(repo, "branch", "--show-current").stdout.strip()
    result["branch"] = branch or "<detached>"
    result["head"] = run_git(repo, "rev-parse", "HEAD").stdout.strip() or None
    if not branch:
        _issue(result, _level(required), "detached_head", "active checkout is detached")
    elif expected_branch and branch != expected_branch:
        _issue(result, "warning", "unexpected_branch", f"expected {expected_branch}, found {branch}")

    status = run_git(repo, "status", "--porcelain=v1")
    dirty_lines = [line for line in status.stdout.splitlines() if line.strip()]
    result["dirty"] = len(dirty_lines)
    if dirty_lines:
        _issue(result, "warning", "dirty_worktree", f"{len(dirty_lines)} uncommitted path(s)")

    origin = run_git(repo, "remote", "get-url", "origin")
    if origin.returncode:
        _issue(result, _level(required), "missing_origin", "origin remote is not configured")
        return result
    origin_url = origin.stdout.strip()
    result["remote"] = redact_remote(origin_url)
    result["origin_repo"] = origin_repo_identity(origin_url)
    if expected_origin_repo and (
        result["origin_repo"] is None
        or result["origin_repo"].casefold() != expected_origin_repo.casefold()
    ):
        observed = result["origin_repo"] or "unrecognised remote URL"
        _issue(
            result,
            _level(required),
            "unexpected_origin",
            f"expected {expected_origin_repo}, found {observed}",
        )

    upstream_proc = run_git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    upstream = upstream_proc.stdout.strip() if upstream_proc.returncode == 0 else ""
    result["upstream"] = upstream or None
    if not upstream:
        _issue(result, _level(required), "missing_upstream", "active branch has no upstream")
        return result

    fetch_ok = True
    if fetch:
        fetched = run_git(repo, "fetch", "--prune", "--tags", "origin", timeout=180)
        fetch_ok = fetched.returncode == 0
        if not fetch_ok:
            detail = (fetched.stderr or fetched.stdout).strip().splitlines()
            _issue(result, "warning", "fetch_failed", detail[-1] if detail else "origin fetch failed")

    remote_branch = upstream.split("/", 1)[1] if upstream.startswith("origin/") else upstream
    remote_sha, remote_problem = _remote_sha(repo, remote_branch)
    if remote_problem == "missing":
        _issue(result, _level(required), "remote_branch_deleted", f"origin/{remote_branch} does not exist")
    elif remote_problem:
        _issue(result, "warning", "remote_probe_failed", remote_problem)

    upstream_ref = run_git(repo, "show-ref", "--verify", f"refs/remotes/{upstream}")
    if upstream_ref.returncode:
        _issue(result, _level(required), "missing_tracking_ref", f"local tracking ref {upstream} is missing")
    else:
        divergence = run_git(repo, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
        if divergence.returncode == 0:
            parts = divergence.stdout.split()
            if len(parts) == 2:
                result["behind"], result["ahead"] = int(parts[0]), int(parts[1])
        if result["ahead"] and result["behind"]:
            _issue(result, _level(required), "diverged", f"behind {result['behind']}, ahead {result['ahead']}")
        elif result["ahead"]:
            _issue(result, _level(required), "local_only_commits", f"{result['ahead']} commit(s) not on upstream")
        elif result["behind"]:
            _issue(result, "warning", "behind_upstream", f"behind upstream by {result['behind']} commit(s)")
        elif not fetch_ok:
            result["behind"] = result["behind"] if result["behind"] is not None else 0
            result["ahead"] = result["ahead"] if result["ahead"] is not None else 0

    if checkpoint:
        checkpoint_branch = checkpoint["branch"]
        checkpoint_sha, checkpoint_problem = _remote_sha(repo, checkpoint_branch)
        result["checkpoint_remote_sha"] = checkpoint_sha
        if checkpoint_problem == "missing":
            _issue(
                result,
                _level(required, strict_checkpoints),
                "checkpoint_branch_missing",
                f"checkpoint branch origin/{checkpoint_branch} does not exist",
            )
        elif checkpoint_problem:
            _issue(result, "warning", "checkpoint_probe_failed", checkpoint_problem)
        elif checkpoint_sha != checkpoint["remote_sha"]:
            _issue(
                result,
                _level(False, strict_checkpoints),
                "checkpoint_stale",
                f"recorded {checkpoint['remote_sha']}, remote has {checkpoint_sha}",
            )

    lfs_files = run_git(repo, "lfs", "ls-files", "--all")
    if lfs_files.returncode == 0 and lfs_files.stdout.strip():
        lfs_status = run_git(repo, "lfs", "status")
        lfs_fsck = run_git(repo, "lfs", "fsck", timeout=180)
        for finding in lfs_findings(
            lfs_status.stdout + lfs_status.stderr,
            lfs_fsck.returncode,
            lfs_fsck.stdout + lfs_fsck.stderr,
        ):
            _issue(result, _level(required), "lfs_integrity", finding)

    return result


def exit_code(results: list[dict[str, Any]]) -> int:
    levels = {issue["level"] for result in results for issue in result["issues"]}
    if "critical" in levels:
        return 1
    if "warning" in levels:
        return 2
    return 0


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigError(f"{label} must contain a JSON object")
    return value


def _validate_item(item: Any, *, schema_version: int, section: str) -> None:
    if not isinstance(item, dict):
        raise ConfigError(f"{section} entries must be objects")
    required_fields = {"name", "path"}
    if schema_version >= 2:
        required_fields |= {"id", "kind", "required", "origin_repo"}
    missing = sorted(field for field in required_fields if field not in item)
    if missing:
        raise ConfigError(f"{section} entry is missing: {', '.join(missing)}")
    if schema_version >= 2:
        if item["kind"] not in VALID_KINDS:
            raise ConfigError(f"{section} entry {item['id']} has invalid kind {item['kind']!r}")
        if not isinstance(item["required"], bool):
            raise ConfigError(f"{section} entry {item['id']} required must be boolean")
        if not re.fullmatch(r"[^/\s]+/[^/\s]+", item["origin_repo"]):
            raise ConfigError(f"{section} entry {item['id']} origin_repo must be owner/repository")


def load_checkpoints(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = _read_json(path, "checkpoint registry")
    if data.get("schema_version") != 1 or not isinstance(data.get("checkpoints"), list):
        raise ConfigError("checkpoint registry must use schema_version 1 and a checkpoints list")
    checkpoints: dict[str, dict[str, Any]] = {}
    for item in data["checkpoints"]:
        if not isinstance(item, dict) or not all(field in item for field in ("id", "branch", "remote_sha")):
            raise ConfigError("each checkpoint needs id, branch, and remote_sha")
        if item["id"] in checkpoints:
            raise ConfigError(f"duplicate checkpoint id {item['id']}")
        checkpoints[item["id"]] = item
    return checkpoints


def load_targets(
    config_path: Path,
    *,
    include_satellites: bool = False,
    checkpoints_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Load v1 or v2 sync config and return audit targets.

    Version 1 has only core entries and remains accepted so existing external
    callers of the original script continue to work.
    """

    config = _read_json(config_path, "sync configuration")
    schema_version = config.get("schema_version", 1)
    if schema_version not in {1, 2}:
        raise ConfigError(f"unsupported repository sync schema_version {schema_version!r}")
    repositories = config.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        raise ConfigError("repositories must be a non-empty list")
    if schema_version == 2:
        workspace = config.get("workspace")
        if not isinstance(workspace, dict) or workspace.get("layout") != "sibling-v1":
            raise ConfigError("schema v2 requires workspace.layout = sibling-v1")
        if not isinstance(config.get("satellites", []), list):
            raise ConfigError("satellites must be a list")

    root = config_path.resolve().parents[1]
    checkpoint_file = checkpoints_path or root / "registry" / "core_repo_checkpoints.json"
    checkpoints = load_checkpoints(checkpoint_file)
    targets: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    sections: list[tuple[str, list[Any]]] = [("repositories", repositories)]
    if schema_version == 2 and include_satellites:
        enabled_satellites = [item for item in config.get("satellites", []) if item.get("enabled", True)]
        sections.append(("satellites", enabled_satellites))
    for section, items in sections:
        for item in items:
            _validate_item(item, schema_version=schema_version, section=section)
            identifier = item.get("id", item["name"])
            if identifier in seen_ids:
                raise ConfigError(f"duplicate repository id {identifier}")
            seen_ids.add(identifier)
            targets.append(
                {
                    "id": identifier,
                    "name": item["name"],
                    "kind": item.get("kind", "chapter"),
                    "required": item.get("required", True),
                    "relative_path": item["path"],
                    "path": (root / item["path"]).resolve(),
                    "expected_branch": item.get("expected_branch"),
                    "expected_origin_repo": item.get("origin_repo"),
                    "checkpoint": checkpoints.get(identifier),
                }
            )
    return targets


def render_text(results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for result in results:
        levels = {issue["level"] for issue in result["issues"]}
        label = "CRITICAL" if "critical" in levels else "WARN" if "warning" in levels else "OK"
        lines.append(
            f"[{label}] {result['name']} ({result['kind']}): branch={result['branch']} "
            f"behind={result['behind']} ahead={result['ahead']} dirty={result['dirty']}"
        )
        for issue in result["issues"]:
            lines.append(f"  - {issue['level'].upper()} {issue['code']}: {issue['message']}")
    lines.append(f"summary: exit={exit_code(results)} repos={len(results)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--all", action="store_true", help="audit every required core repository")
    target.add_argument("--repo", type=Path, help="audit one repository path")
    freshness = parser.add_mutually_exclusive_group()
    freshness.add_argument("--fetch", action="store_true", help="refresh origin metadata before comparing")
    freshness.add_argument("--no-fetch", action="store_true", help="use current tracking refs")
    parser.add_argument("--include-satellites", action="store_true", help="also audit enabled optional satellites")
    parser.add_argument("--strict-checkpoints", action="store_true", help="treat a changed checkpoint SHA as critical")
    parser.add_argument("--json", action="store_true", help="write machine-readable JSON to stdout")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--checkpoints", type=Path, default=None)
    args = parser.parse_args(argv)

    try:
        if args.repo:
            ad_hoc_path = args.repo.resolve()
            targets = [{
                "id": ad_hoc_path.name,
                "name": ad_hoc_path.name,
                "kind": "ad_hoc",
                "required": True,
                "relative_path": str(ad_hoc_path),
                "path": ad_hoc_path,
                "expected_branch": None,
                "expected_origin_repo": None,
                "checkpoint": None,
            }]
        else:
            targets = load_targets(
                args.config,
                include_satellites=args.include_satellites,
                checkpoints_path=args.checkpoints,
            )
    except ConfigError as exc:
        payload = {"exit_code": 1, "repositories": [], "configuration_error": str(exc)}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"[CRITICAL] config: {exc}")
        return 1

    results = [
        audit_repository(
            item["path"],
            item["name"],
            item.get("expected_branch"),
            args.fetch,
            repository_id=item["id"],
            kind=item["kind"],
            required=item["required"],
            expected_origin_repo=item.get("expected_origin_repo"),
            checkpoint=item.get("checkpoint"),
            strict_checkpoints=args.strict_checkpoints,
        )
        for item in targets
    ]
    if args.json:
        print(json.dumps({"exit_code": exit_code(results), "repositories": results}, ensure_ascii=False, indent=2))
    else:
        print(render_text(results))
    return exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main())
