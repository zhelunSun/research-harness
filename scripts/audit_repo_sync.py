#!/usr/bin/env python3
"""Audit local thesis repositories against their configured Git remotes.

This command is deliberately read-only with respect to tracked files. With
``--fetch`` it refreshes Git remote-tracking metadata, but it never commits,
pushes, merges, checks out, or rewrites repository content.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "repository_sync.json"


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


def audit_repository(repo: Path, name: str, expected_branch: str | None, fetch: bool) -> dict[str, Any]:
    repo = repo.resolve()
    result: dict[str, Any] = {
        "name": name,
        "path": str(repo),
        "branch": None,
        "expected_branch": expected_branch,
        "head": None,
        "upstream": None,
        "remote": None,
        "dirty": 0,
        "behind": None,
        "ahead": None,
        "issues": [],
    }

    inside = run_git(repo, "rev-parse", "--is-inside-work-tree")
    if inside.returncode or inside.stdout.strip() != "true":
        _issue(result, "critical", "not_git_repository", "path is not a Git work tree")
        return result

    branch = run_git(repo, "branch", "--show-current").stdout.strip()
    result["branch"] = branch or "<detached>"
    result["head"] = run_git(repo, "rev-parse", "HEAD").stdout.strip() or None
    if not branch:
        _issue(result, "critical", "detached_head", "active checkout is detached")
    elif expected_branch and branch != expected_branch:
        _issue(result, "warning", "unexpected_branch", f"expected {expected_branch}, found {branch}")

    status = run_git(repo, "status", "--porcelain=v1")
    dirty_lines = [line for line in status.stdout.splitlines() if line.strip()]
    result["dirty"] = len(dirty_lines)
    if dirty_lines:
        _issue(result, "warning", "dirty_worktree", f"{len(dirty_lines)} uncommitted path(s)")

    origin = run_git(repo, "remote", "get-url", "origin")
    if origin.returncode:
        _issue(result, "critical", "missing_origin", "origin remote is not configured")
        return result
    result["remote"] = redact_remote(origin.stdout)

    upstream_proc = run_git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    upstream = upstream_proc.stdout.strip() if upstream_proc.returncode == 0 else ""
    result["upstream"] = upstream or None
    if not upstream:
        _issue(result, "critical", "missing_upstream", "active branch has no upstream")
        return result

    fetch_ok = True
    if fetch:
        fetched = run_git(repo, "fetch", "--prune", "--tags", "origin", timeout=180)
        fetch_ok = fetched.returncode == 0
        if not fetch_ok:
            detail = (fetched.stderr or fetched.stdout).strip().splitlines()
            _issue(
                result,
                "warning",
                "fetch_failed",
                detail[-1] if detail else "origin fetch failed",
            )

    remote_branch = upstream.split("/", 1)[1] if upstream.startswith("origin/") else upstream
    remote_probe = run_git(repo, "ls-remote", "--exit-code", "--heads", "origin", f"refs/heads/{remote_branch}")
    if remote_probe.returncode == 2 and not remote_probe.stderr.strip():
        _issue(result, "critical", "remote_branch_deleted", f"origin/{remote_branch} does not exist")
    elif remote_probe.returncode:
        detail = (remote_probe.stderr or remote_probe.stdout).strip().splitlines()
        _issue(result, "warning", "remote_probe_failed", detail[-1] if detail else "ls-remote failed")

    upstream_ref = run_git(repo, "show-ref", "--verify", f"refs/remotes/{upstream}")
    if upstream_ref.returncode:
        _issue(result, "critical", "missing_tracking_ref", f"local tracking ref {upstream} is missing")
    else:
        divergence = run_git(repo, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
        if divergence.returncode == 0:
            parts = divergence.stdout.split()
            if len(parts) == 2:
                result["behind"], result["ahead"] = int(parts[0]), int(parts[1])
        if result["ahead"] and result["behind"]:
            _issue(result, "critical", "diverged", f"behind {result['behind']}, ahead {result['ahead']}")
        elif result["ahead"]:
            _issue(result, "critical", "local_only_commits", f"{result['ahead']} commit(s) not on upstream")
        elif result["behind"]:
            _issue(result, "warning", "behind_upstream", f"behind upstream by {result['behind']} commit(s)")
        elif not fetch_ok:
            result["behind"] = result["behind"] if result["behind"] is not None else 0
            result["ahead"] = result["ahead"] if result["ahead"] is not None else 0

    lfs_files = run_git(repo, "lfs", "ls-files", "--all")
    if lfs_files.returncode == 0 and lfs_files.stdout.strip():
        lfs_status = run_git(repo, "lfs", "status")
        lfs_fsck = run_git(repo, "lfs", "fsck", timeout=180)
        for finding in lfs_findings(
            lfs_status.stdout + lfs_status.stderr,
            lfs_fsck.returncode,
            lfs_fsck.stdout + lfs_fsck.stderr,
        ):
            _issue(result, "critical", "lfs_integrity", finding)

    return result


def exit_code(results: list[dict[str, Any]]) -> int:
    levels = {issue["level"] for result in results for issue in result["issues"]}
    if "critical" in levels:
        return 1
    if "warning" in levels:
        return 2
    return 0


def load_targets(config_path: Path) -> list[dict[str, Any]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    root = config_path.resolve().parents[1]
    targets: list[dict[str, Any]] = []
    for item in config["repositories"]:
        targets.append(
            {
                "name": item["name"],
                "path": (root / item["path"]).resolve(),
                "expected_branch": item.get("expected_branch"),
            }
        )
    return targets


def render_text(results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for result in results:
        levels = {issue["level"] for issue in result["issues"]}
        label = "CRITICAL" if "critical" in levels else "WARN" if "warning" in levels else "OK"
        lines.append(
            f"[{label}] {result['name']}: branch={result['branch']} "
            f"behind={result['behind']} ahead={result['ahead']} dirty={result['dirty']}"
        )
        for issue in result["issues"]:
            lines.append(f"  - {issue['level'].upper()} {issue['code']}: {issue['message']}")
    lines.append(f"summary: exit={exit_code(results)} repos={len(results)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--all", action="store_true", help="audit every configured repository")
    target.add_argument("--repo", type=Path, help="audit one repository path")
    freshness = parser.add_mutually_exclusive_group()
    freshness.add_argument("--fetch", action="store_true", help="refresh origin metadata before comparing")
    freshness.add_argument("--no-fetch", action="store_true", help="use current tracking refs")
    parser.add_argument("--json", action="store_true", help="write machine-readable JSON to stdout")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args(argv)

    if args.repo:
        targets = [{"name": args.repo.name, "path": args.repo.resolve(), "expected_branch": None}]
    else:
        targets = load_targets(args.config)
    results = [
        audit_repository(item["path"], item["name"], item.get("expected_branch"), args.fetch)
        for item in targets
    ]
    if args.json:
        print(json.dumps({"exit_code": exit_code(results), "repositories": results}, ensure_ascii=False, indent=2))
    else:
        print(render_text(results))
    return exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main())
