#!/usr/bin/env python3
"""Audit the thesis-wide machine-readable human-gate registry.

The registry reports existing researcher decisions and external checks. This
audit never resolves a gate or infers status from prose.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATES = ROOT / "registry" / "human_gates.json"
DEFAULT_QUEUE = ROOT / "evidence" / "literature" / "maintenance_queue.json"
DEFAULT_REPO_CONFIG = ROOT / "config" / "repository_sync.json"
OPEN_STATUSES = {
    "pending_external_verification",
    "pending_authorization",
    "pending_task_specific_review",
    "pending_researcher_review",
    "pending_researcher_decision",
}
TERMINAL_STATUSES = {"completed", "cancelled"}
ALLOWED_CATEGORIES = {
    "maintenance_external",
    "zotero_write",
    "writing_acceptance",
    "scientific_evidence",
    "scientific_route",
}
REQUIRED_CURRENT_GATE_IDS = {
    "lit-cross-device-seadrive-verification",
    "lit-geospatial-agent-zotero-import",
    "lit-agent-evaluation-zotero-import",
    "lit-knowledge-governance-zotero-import",
    "lit-opening-v05-contract-merge",
    "ch2-g4-batch-a-researcher-review",
    "ch3-first-evaluation-route-selection",
}
BOUND_LITERATURE_ACTION_KINDS = {"external_verification", "zotero_write", "writing_merge"}


class GateAuditError(RuntimeError):
    """Human-gate inputs cannot be interpreted safely."""


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GateAuditError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GateAuditError(f"{label} must contain a JSON object")
    return value


def _issue(result: dict[str, Any], code: str, message: str, path: Path | None = None) -> None:
    issue: dict[str, Any] = {"code": code, "message": message}
    if path is not None:
        issue["path"] = str(path)
    result["issues"].append(issue)


def _inside(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise GateAuditError(f"{label} escapes repository root: {resolved}") from exc
    return resolved


def _repository_roots(root: Path, config: dict[str, Any]) -> dict[str, Path]:
    if config.get("schema_version") != 2:
        raise GateAuditError("human-gate audit requires repository sync schema_version 2")
    repositories = config.get("repositories")
    if not isinstance(repositories, list):
        raise GateAuditError("repository configuration repositories must be a list")
    workspace_root = root.resolve().parent
    roots: dict[str, Path] = {}
    for repository in repositories:
        if not isinstance(repository, dict):
            raise GateAuditError("repository configuration contains a non-object repository")
        repository_id = repository.get("id")
        relative_path = repository.get("path")
        if not isinstance(repository_id, str) or not isinstance(relative_path, str):
            raise GateAuditError("each repository needs id and path")
        if repository_id in roots:
            raise GateAuditError(f"duplicate repository id {repository_id!r}")
        roots[repository_id] = _inside(
            root / Path(relative_path.replace("\\", "/")),
            workspace_root,
            f"repository {repository_id}",
        )
    return roots


def audit_human_gates(
    root: Path = ROOT,
    gates_path: Path | None = None,
    queue_path: Path | None = None,
    repo_config_path: Path | None = None,
) -> dict[str, Any]:
    """Return a non-mutating audit of all current thesis human gates."""

    resolved_root = root.resolve()
    gates_file = (gates_path or resolved_root / "registry" / "human_gates.json").resolve()
    queue_file = (queue_path or resolved_root / "evidence" / "literature" / "maintenance_queue.json").resolve()
    config_file = (repo_config_path or resolved_root / "config" / "repository_sync.json").resolve()
    _inside(gates_file, resolved_root, "human-gate registry")
    _inside(queue_file, resolved_root, "literature maintenance queue")
    _inside(config_file, resolved_root, "repository configuration")
    registry = _read_json(gates_file, "human-gate registry")
    queue = _read_json(queue_file, "literature maintenance queue")
    config = _read_json(config_file, "repository configuration")
    repository_roots = _repository_roots(resolved_root, config)

    if registry.get("schema_version") != "1.0":
        raise GateAuditError("human-gate registry requires schema_version '1.0'")
    policy = registry.get("policy")
    if not isinstance(policy, dict):
        raise GateAuditError("human-gate registry policy must be an object")
    expected_policy = {
        "source_of_truth": "registry/human_gates.json",
        "decision_owner": "researcher",
        "automatic_resolution_forbidden": True,
        "literature_queue_binding_required": True,
    }
    result: dict[str, Any] = {
        "registry": str(gates_file),
        "gates_total": 0,
        "open_gates": [],
        "category_counts": {},
        "status_counts": {},
        "issues": [],
    }
    for field, expected in expected_policy.items():
        if policy.get(field) != expected:
            _issue(result, "human_gate_policy_drift", f"policy {field} must remain {expected!r}")
    if set(policy.get("open_statuses", [])) != OPEN_STATUSES:
        _issue(result, "human_gate_policy_drift", "policy open_statuses differs from the audited state set")

    gates = registry.get("gates")
    if not isinstance(gates, list):
        raise GateAuditError("human-gate registry gates must be a list")
    result["gates_total"] = len(gates)
    seen_ids: set[str] = set()
    gate_by_source_action: dict[str, dict[str, Any]] = {}
    categories: Counter[str] = Counter()
    statuses: Counter[str] = Counter()
    for gate in gates:
        if not isinstance(gate, dict):
            raise GateAuditError("human-gate registry contains a non-object gate")
        gate_id = gate.get("gate_id")
        if not isinstance(gate_id, str) or not gate_id:
            raise GateAuditError("every human gate needs a non-empty gate_id")
        if gate_id in seen_ids:
            _issue(result, "duplicate_human_gate", f"duplicate human gate {gate_id!r}")
        seen_ids.add(gate_id)
        category = gate.get("category")
        status = gate.get("status")
        categories[str(category)] += 1
        statuses[str(status)] += 1
        if category not in ALLOWED_CATEGORIES:
            _issue(result, "invalid_human_gate_category", f"gate {gate_id} has category {category!r}")
        if status not in OPEN_STATUSES | TERMINAL_STATUSES:
            _issue(result, "invalid_human_gate_status", f"gate {gate_id} has status {status!r}")
        if gate.get("decision_owner") != "researcher":
            _issue(result, "human_gate_owner_drift", f"gate {gate_id} must remain researcher-owned")
        if not isinstance(gate.get("gate"), str) or not gate.get("gate"):
            _issue(result, "missing_human_gate_condition", f"gate {gate_id} lacks a gate condition")
        if not isinstance(gate.get("required_evidence"), list) or not gate.get("required_evidence"):
            _issue(result, "missing_human_gate_evidence", f"gate {gate_id} lacks required evidence")
        if not isinstance(gate.get("blocks"), list) or not gate.get("blocks"):
            _issue(result, "missing_human_gate_block", f"gate {gate_id} lacks an explicit blocked outcome")
        if not isinstance(gate.get("next_action"), str) or not gate.get("next_action"):
            _issue(result, "missing_human_gate_next_action", f"gate {gate_id} lacks next_action")

        repository_id = gate.get("repository_id")
        repository_root = repository_roots.get(repository_id)
        if repository_root is None:
            _issue(result, "unknown_human_gate_repository", f"gate {gate_id} references {repository_id!r}")
        else:
            artifact_value = gate.get("artifact_path")
            if not isinstance(artifact_value, str) or not artifact_value:
                _issue(result, "missing_human_gate_artifact", f"gate {gate_id} lacks artifact_path")
            else:
                relative = Path(artifact_value.replace("\\", "/"))
                if relative.is_absolute():
                    _issue(result, "absolute_human_gate_artifact", f"gate {gate_id} artifact must be relative")
                else:
                    artifact = _inside(repository_root / relative, repository_root, f"gate {gate_id} artifact")
                    if not artifact.is_file():
                        _issue(result, "missing_human_gate_artifact", f"gate {gate_id} artifact is missing", artifact)

        source_action_id = gate.get("source_action_id")
        if source_action_id is not None:
            if not isinstance(source_action_id, str) or not source_action_id:
                _issue(result, "invalid_gate_source_action", f"gate {gate_id} has invalid source_action_id")
            elif source_action_id in gate_by_source_action:
                _issue(result, "duplicate_gate_source_action", f"multiple gates bind {source_action_id!r}")
            else:
                gate_by_source_action[source_action_id] = gate
        if status in OPEN_STATUSES:
            result["open_gates"].append(
                {
                    "gate_id": gate_id,
                    "category": category,
                    "status": status,
                    "gate": gate.get("gate"),
                    "repository_id": repository_id,
                    "next_action": gate.get("next_action"),
                }
            )
        elif status == "completed":
            resolution = gate.get("resolution")
            if not isinstance(resolution, dict) or not all(
                resolution.get(field) for field in ("decided_at", "decided_by", "evidence")
            ):
                _issue(result, "missing_human_gate_resolution", f"completed gate {gate_id} lacks resolution evidence")

    missing_required = sorted(REQUIRED_CURRENT_GATE_IDS - seen_ids)
    if missing_required:
        _issue(result, "missing_current_human_gate", f"registry omits current gates {missing_required}")

    actions = queue.get("actions")
    if not isinstance(actions, list):
        raise GateAuditError("literature maintenance queue actions must be a list")
    action_map = {
        action.get("action_id"): action
        for action in actions
        if isinstance(action, dict) and isinstance(action.get("action_id"), str)
    }
    for source_action_id, gate in gate_by_source_action.items():
        action = action_map.get(source_action_id)
        if action is None:
            _issue(result, "missing_bound_literature_action", f"gate {gate['gate_id']} binds missing action {source_action_id!r}")
            continue
        if action.get("status") != gate.get("status"):
            _issue(result, "human_gate_status_drift", f"gate {gate['gate_id']} status differs from literature action")
        if action.get("gate") != gate.get("gate"):
            _issue(result, "human_gate_condition_drift", f"gate {gate['gate_id']} condition differs from literature action")
    for action in actions:
        if not isinstance(action, dict):
            continue
        if action.get("kind") in BOUND_LITERATURE_ACTION_KINDS and action.get("status") in OPEN_STATUSES:
            action_id = action.get("action_id")
            if action_id not in gate_by_source_action:
                _issue(result, "unregistered_literature_gate", f"open literature action {action_id!r} is absent from human-gate registry")

    result["category_counts"] = dict(categories)
    result["status_counts"] = dict(statuses)
    result["exit_code"] = 2 if result["issues"] else 0
    return result


def render_text(result: dict[str, Any]) -> str:
    label = "OK" if result["exit_code"] == 0 else "WARN"
    lines = [
        f"[{label}] human gates: total={result['gates_total']} open={len(result['open_gates'])} "
        f"categories={len(result['category_counts'])}"
    ]
    for gate in result["open_gates"]:
        lines.append(
            f"  - GATE {gate['gate_id']}: {gate['status']} "
            f"[{gate['category']}] ({gate['repository_id']})"
        )
    for issue in result["issues"]:
        location = f" [{issue['path']}]" if issue.get("path") else ""
        lines.append(f"  - {issue['code']}: {issue['message']}{location}")
    lines.append(f"summary: exit={result['exit_code']} issues={len(result['issues'])}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--gates", type=Path, default=None)
    parser.add_argument("--queue", type=Path, default=None)
    parser.add_argument("--repo-config", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit_human_gates(args.root, args.gates, args.queue, args.repo_config)
    except GateAuditError as exc:
        payload = {"exit_code": 1, "configuration_error": str(exc), "issues": []}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"[CRITICAL] human gates: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
