#!/usr/bin/env python3
"""Audit the thesis literature maintenance control plane.

Exit ``0`` means packet integrity, maintenance gates, and scan freshness pass.
Exit ``2`` means the audit completed and found repairable drift. Exit ``1``
means the registry or queue could not be interpreted safely. The command is
read-only and never calls or writes Zotero.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "evidence" / "literature" / "packet_registry.json"
DEFAULT_QUEUE = ROOT / "evidence" / "literature" / "maintenance_queue.json"
DEFAULT_ROUTES = ROOT / "evidence" / "literature" / "consumer_routes.json"
DEFAULT_WRITING_INTAKES = ROOT / "evidence" / "literature" / "writing_intakes.json"
DEFAULT_RUNTIME_SCAN = ROOT / "evidence" / "literature" / "runtime_scan.json"
DEFAULT_ACQUISITION_QUEUE = ROOT / "evidence" / "literature" / "acquisition_queue.json"
DEFAULT_HUMAN_GATES = ROOT / "registry" / "human_gates.json"
DEFAULT_REPO_CONFIG = ROOT / "config" / "repository_sync.json"
REQUIRED_PACKET_FILES = (
    "README.md",
    "references.bib",
    "ledger.json",
    "evidence_cards.md",
    "audit.json",
    "writing_bridge.json",
)
ALLOWED_PACKET_STATUSES = {
    "draft",
    "needs_review",
    "audited",
    "audited_pending_zotero_authorization",
    "archived",
}
ALLOWED_WRITING_ELIGIBILITY = {
    "not_merged_into_any_writing_contract",
    "blocked_on_zotero_identity_reconciliation_and_task_specific_review",
    "task_specific_review_required",
    "accepted_by_writing_contract",
}
ALLOWED_ACTION_STATUSES = {
    "pending_authorization",
    "pending_external_verification",
    "pending_task_specific_review",
    "authorized",
    "completed",
    "cancelled",
}
ALLOWED_ROUTE_STATUSES = {
    "candidate",
    "reconciliation_required",
    "reconciled_candidate",
    "accepted",
    "retired",
}
ALLOWED_INTAKE_STATUSES = {"draft", "reviewed_candidate", "accepted", "retired"}
ALLOWED_INTAKE_DECISIONS = {
    "candidate_support",
    "partial_split_required",
    "context_only",
    "insufficient_keep_marker",
    "defer",
}
ALLOWED_ACQUISITION_STATUSES = {
    "ready_for_search",
    "blocked_on_gate",
    "candidate_screening",
    "full_text_review",
    "packet_ready",
    "retired",
}
ALLOWED_ACQUISITION_PRIORITIES = {"P0", "P1", "P2"}
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.IGNORECASE)
BIB_FILE_FIELD_RE = re.compile(r"(?:^|[,\{\s])file\s*=", re.IGNORECASE | re.MULTILINE)
WINDOWS_ABSOLUTE_RE = re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/])")
UNC_PATH_RE = re.compile(r"(?<![A-Za-z0-9:])(?:\\\\|//)[^/\\\s]+[/\\]")


class ControlError(RuntimeError):
    """A control-plane input cannot be read or interpreted safely."""


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ControlError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ControlError(f"{label} must contain a JSON object")
    return value


def _read_text(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ControlError(f"cannot read {label} at {path}: {exc}") from exc


def _add_issue(
    result: dict[str, Any],
    code: str,
    message: str,
    *,
    path: Path | None = None,
) -> None:
    issue: dict[str, Any] = {"code": code, "message": message}
    if path is not None:
        issue["path"] = str(path)
    result["issues"].append(issue)


def _inside(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ControlError(f"{label} escapes control-plane root: {resolved}") from exc
    return resolved


def _parse_iso_date(value: Any, label: str) -> date:
    if not isinstance(value, str):
        raise ControlError(f"{label} must be an ISO date")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ControlError(f"{label} must be an ISO date: {value!r}") from exc


def _parse_iso_datetime(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise ControlError(f"{label} must be an ISO datetime")
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ControlError(f"{label} must be an ISO datetime: {value!r}") from exc


def _packet_path(root: Path, value: Any, packet_id: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ControlError(f"packet {packet_id} needs a non-empty path")
    candidate = Path(value.replace("\\", "/"))
    if candidate.is_absolute():
        raise ControlError(f"packet {packet_id} path must be repository-relative")
    return _inside(root / candidate, root, f"packet {packet_id}")


def _audit_packet(
    result: dict[str, Any],
    root: Path,
    packet: dict[str, Any],
    seen_packet_ids: set[str],
    seen_packet_paths: set[Path],
    global_zotero_keys: dict[str, str],
    packet_claim_ids: dict[str, set[str]],
    packet_claim_statuses: dict[str, dict[str, str]],
) -> None:
    packet_id = packet.get("packet_id")
    if not isinstance(packet_id, str) or not packet_id:
        raise ControlError("every packet needs a non-empty packet_id")
    if packet_id in seen_packet_ids:
        _add_issue(result, "duplicate_packet_id", f"duplicate packet_id {packet_id!r}")
    seen_packet_ids.add(packet_id)

    packet_path = _packet_path(root, packet.get("path"), packet_id)
    if packet_path in seen_packet_paths:
        _add_issue(result, "duplicate_packet_path", f"multiple packets use {packet_path}")
    seen_packet_paths.add(packet_path)
    if not packet_path.is_dir():
        _add_issue(result, "missing_packet_directory", f"packet directory is missing for {packet_id}", path=packet_path)
        return

    status = packet.get("status")
    if status not in ALLOWED_PACKET_STATUSES:
        _add_issue(result, "invalid_packet_status", f"packet {packet_id} has unsupported status {status!r}")
    writing_eligibility = packet.get("writing_eligibility")
    if writing_eligibility not in ALLOWED_WRITING_ELIGIBILITY:
        _add_issue(
            result,
            "invalid_writing_eligibility",
            f"packet {packet_id} has unsupported writing_eligibility {writing_eligibility!r}",
        )
    _parse_iso_date(packet.get("last_audited"), f"packet {packet_id} last_audited")

    missing = [name for name in REQUIRED_PACKET_FILES if not (packet_path / name).is_file()]
    for name in missing:
        _add_issue(result, "missing_packet_file", f"packet {packet_id} is missing {name}", path=packet_path / name)
    if missing:
        return

    pdfs = sorted(packet_path.rglob("*.pdf"))
    for pdf in pdfs:
        _add_issue(result, "committed_pdf_binary", f"packet {packet_id} contains a PDF binary", path=pdf)

    for candidate in packet_path.rglob("*"):
        if not candidate.is_file() or candidate.suffix.lower() == ".pdf":
            continue
        text = _read_text(candidate, f"packet file for {packet_id}")
        if WINDOWS_ABSOLUTE_RE.search(text) or UNC_PATH_RE.search(text):
            _add_issue(
                result,
                "workstation_path_in_packet",
                f"packet {packet_id} contains a workstation-specific path",
                path=candidate,
            )

    bib_path = packet_path / "references.bib"
    bib_text = _read_text(bib_path, f"bibliography for {packet_id}")
    if BIB_FILE_FIELD_RE.search(bib_text):
        _add_issue(result, "bibtex_file_field", f"packet {packet_id} bibliography contains a file field", path=bib_path)
    bib_keys = BIB_KEY_RE.findall(bib_text)
    duplicate_bib_keys = sorted(key for key, count in Counter(bib_keys).items() if count > 1)
    if duplicate_bib_keys:
        _add_issue(result, "duplicate_bibtex_key", f"packet {packet_id} repeats BibTeX keys: {duplicate_bib_keys}")

    ledger = _read_json(packet_path / "ledger.json", f"ledger for {packet_id}")
    audit = _read_json(packet_path / "audit.json", f"audit for {packet_id}")
    bridge = _read_json(packet_path / "writing_bridge.json", f"writing bridge for {packet_id}")
    if ledger.get("ledger_id") != packet_id:
        _add_issue(result, "ledger_id_mismatch", f"packet {packet_id} ledger_id does not match")
    if audit.get("ledger_id") != packet_id:
        _add_issue(result, "audit_ledger_id_mismatch", f"packet {packet_id} audit ledger_id does not match")
    if bridge.get("source_ledger_id") != packet_id:
        _add_issue(result, "bridge_ledger_id_mismatch", f"packet {packet_id} writing bridge does not match")

    sources = ledger.get("sources")
    claims = ledger.get("claims")
    links = ledger.get("links")
    if not isinstance(sources, list) or not isinstance(claims, list) or not isinstance(links, list):
        raise ControlError(f"packet {packet_id} ledger sources, claims, and links must be lists")
    claim_ids = {
        claim.get("claim_id")
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
    }
    packet_claim_ids[packet_id] = claim_ids
    packet_claim_statuses[packet_id] = {
        claim["claim_id"]: claim.get("evidence_status", "")
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
    }
    if len(claim_ids) != len(claims):
        _add_issue(result, "invalid_or_duplicate_claim_id", f"packet {packet_id} has invalid or duplicate claim IDs")
    declared_source_count = packet.get("source_count")
    if declared_source_count != len(sources):
        _add_issue(
            result,
            "source_count_mismatch",
            f"packet {packet_id} declares {declared_source_count!r} sources but ledger has {len(sources)}",
        )

    source_ids: list[str] = []
    source_bib_keys: list[str] = []
    source_zotero_keys: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            raise ControlError(f"packet {packet_id} contains a non-object source")
        source_id = source.get("source_id")
        bib_key = source.get("bibtex_key")
        zotero_key = source.get("zotero_item_key")
        if not isinstance(source_id, str) or not source_id:
            _add_issue(result, "missing_source_id", f"packet {packet_id} contains a source without source_id")
        else:
            source_ids.append(source_id)
        if not isinstance(bib_key, str) or not bib_key:
            _add_issue(result, "missing_bibtex_key", f"packet {packet_id} source {source_id!r} has no BibTeX key")
        else:
            source_bib_keys.append(bib_key)
            if bib_key not in bib_keys:
                _add_issue(
                    result,
                    "bibtex_key_missing_from_snapshot",
                    f"packet {packet_id} source {source_id!r} key {bib_key!r} is absent from references.bib",
                )
        if zotero_key is not None:
            if not isinstance(zotero_key, str) or not zotero_key:
                _add_issue(result, "invalid_zotero_item_key", f"packet {packet_id} source {source_id!r} has an invalid Zotero key")
            else:
                source_zotero_keys.append(zotero_key)
                owner = global_zotero_keys.get(zotero_key)
                if owner and owner != packet_id:
                    _add_issue(
                        result,
                        "zotero_key_reused_across_packets",
                        f"Zotero key {zotero_key} is used by packets {owner} and {packet_id}",
                    )
                global_zotero_keys[zotero_key] = packet_id
    if len(source_ids) != len(set(source_ids)):
        _add_issue(result, "duplicate_source_id", f"packet {packet_id} contains duplicate source IDs")
    if len(source_bib_keys) != len(set(source_bib_keys)):
        _add_issue(result, "source_bibtex_key_reuse", f"packet {packet_id} assigns one BibTeX key to multiple sources")

    registry_zotero_keys = packet.get("zotero_item_keys")
    if not isinstance(registry_zotero_keys, list) or not all(
        isinstance(item, str) and item for item in registry_zotero_keys
    ):
        _add_issue(result, "invalid_registry_zotero_keys", f"packet {packet_id} zotero_item_keys must be a string list")
    elif sorted(registry_zotero_keys) != sorted(source_zotero_keys):
        _add_issue(
            result,
            "zotero_key_mismatch",
            f"packet {packet_id} registry and ledger Zotero keys differ",
        )

    audit_summary = audit.get("summary")
    if audit.get("ok") is not True or not isinstance(audit_summary, dict):
        _add_issue(result, "packet_audit_not_ok", f"packet {packet_id} does not have a passing audit")
    else:
        expected_summary = {"sources": len(sources), "claims": len(claims), "links": len(links)}
        for field, expected in expected_summary.items():
            if audit_summary.get(field) != expected:
                _add_issue(
                    result,
                    "packet_audit_count_mismatch",
                    f"packet {packet_id} audit {field}={audit_summary.get(field)!r}, expected {expected}",
                )
        if audit_summary.get("errors") != 0 or audit_summary.get("warnings") != 0:
            _add_issue(result, "packet_audit_findings", f"packet {packet_id} audit reports errors or warnings")

    result["sources_total"] += len(sources)
    result["claims_total"] += len(claims)
    result["links_total"] += len(links)


def _audit_queue(
    result: dict[str, Any],
    queue: dict[str, Any],
    packet_ids: set[str],
    as_of: date,
) -> None:
    if queue.get("schema_version") != "1.0":
        raise ControlError("maintenance queue requires schema_version '1.0'")
    policy = queue.get("policy")
    if not isinstance(policy, dict):
        raise ControlError("maintenance queue policy must be an object")
    expected_policy = {
        "zotero_write_gate": "explicit_user_authorization",
        "writing_merge_gate": "task_specific_contract_review",
        "linked_attachment_transport": "SeaDrive",
    }
    for field, expected in expected_policy.items():
        if policy.get(field) != expected:
            _add_issue(result, "maintenance_policy_drift", f"policy {field} must remain {expected!r}")
    interval = policy.get("read_only_scan_interval_days")
    if not isinstance(interval, int) or interval < 1:
        raise ControlError("read_only_scan_interval_days must be a positive integer")

    scan = queue.get("read_only_scan")
    if not isinstance(scan, dict):
        raise ControlError("maintenance queue read_only_scan must be an object")
    last_completed = _parse_iso_date(scan.get("last_completed"), "read_only_scan.last_completed")
    required_checks = {
        "zotero_status",
        "selected_target",
        "doi_or_exact_title_dedup",
        "linked_pdf_resolution",
        "packet_audit",
    }
    checks = scan.get("checks")
    if not isinstance(checks, list) or not required_checks.issubset(set(checks)):
        _add_issue(result, "incomplete_read_only_scan", "weekly scan omits one or more required checks")
    age = (as_of - last_completed).days
    result["read_only_scan"] = {
        "last_completed": last_completed.isoformat(),
        "age_days": age,
        "interval_days": interval,
    }
    if age < 0:
        _add_issue(result, "future_read_only_scan", "last_completed is later than the audit date")
    elif age > interval:
        _add_issue(
            result,
            "read_only_scan_overdue",
            f"read-only Zotero/packet scan is {age} days old; interval is {interval} days",
        )

    actions = queue.get("actions")
    if not isinstance(actions, list):
        raise ControlError("maintenance queue actions must be a list")
    seen_ids: set[str] = set()
    for action in actions:
        if not isinstance(action, dict):
            raise ControlError("maintenance queue contains a non-object action")
        action_id = action.get("action_id")
        if not isinstance(action_id, str) or not action_id:
            raise ControlError("every maintenance action needs a non-empty action_id")
        if action_id in seen_ids:
            _add_issue(result, "duplicate_action_id", f"duplicate maintenance action {action_id!r}")
        seen_ids.add(action_id)
        status = action.get("status")
        if status not in ALLOWED_ACTION_STATUSES:
            _add_issue(result, "invalid_action_status", f"action {action_id} has unsupported status {status!r}")
        packet_id = action.get("packet_id")
        if packet_id is not None and packet_id not in packet_ids:
            _add_issue(result, "unknown_action_packet", f"action {action_id} references unknown packet {packet_id!r}")
        kind = action.get("kind")
        gate = action.get("gate")
        if not isinstance(kind, str) or not isinstance(gate, str) or not gate:
            _add_issue(result, "invalid_action_gate", f"action {action_id} needs kind and gate")
        if kind == "zotero_write":
            if gate != "explicit_user_authorization":
                _add_issue(result, "zotero_write_gate_drift", f"action {action_id} lacks the explicit Zotero write gate")
            if status in {"authorized", "completed"}:
                authorization = action.get("authorization")
                if not isinstance(authorization, dict) or not authorization.get("authorized_at"):
                    _add_issue(
                        result,
                        "missing_zotero_authorization_evidence",
                        f"action {action_id} is {status} without recorded authorization evidence",
                    )
        if kind == "external_verification":
            required = action.get("evidence_required")
            if not isinstance(required, list) or not required:
                _add_issue(
                    result,
                    "missing_external_verification_evidence",
                    f"action {action_id} has no explicit evidence requirements",
                )
        if kind == "route_reconciliation" and status == "completed":
            completed_at = action.get("completed_at")
            completion_evidence = action.get("completion_evidence")
            if not isinstance(completed_at, str) or not completed_at:
                _add_issue(
                    result,
                    "missing_reconciliation_completion_date",
                    f"completed reconciliation action {action_id} lacks completed_at",
                )
            if not isinstance(completion_evidence, list) or not completion_evidence:
                _add_issue(
                    result,
                    "missing_reconciliation_completion_evidence",
                    f"completed reconciliation action {action_id} lacks completion evidence",
                )
        if status not in {"completed", "cancelled"}:
            result["open_actions"].append(
                {
                    "action_id": action_id,
                    "kind": kind,
                    "status": status,
                    "gate": gate,
                }
            )


def _load_repository_roots(root: Path, config_path: Path) -> dict[str, Path]:
    config = _read_json(config_path, "repository sync configuration")
    if config.get("schema_version") != 2:
        raise ControlError("consumer route audit requires repository sync schema_version 2")
    repositories = config.get("repositories")
    if not isinstance(repositories, list):
        raise ControlError("repository sync configuration repositories must be a list")
    workspace_root = root.resolve().parent
    roots: dict[str, Path] = {}
    for repository in repositories:
        if not isinstance(repository, dict):
            raise ControlError("repository sync configuration contains a non-object repository")
        repository_id = repository.get("id")
        relative_path = repository.get("path")
        if not isinstance(repository_id, str) or not repository_id:
            raise ControlError("each repository needs a non-empty id")
        if repository_id in roots:
            raise ControlError(f"duplicate repository id {repository_id!r}")
        if not isinstance(relative_path, str) or not relative_path:
            raise ControlError(f"repository {repository_id} needs a non-empty path")
        roots[repository_id] = _inside(
            root / Path(relative_path.replace("\\", "/")),
            workspace_root,
            f"repository {repository_id}",
        )
    return roots


def _audit_consumer_routes(
    result: dict[str, Any],
    root: Path,
    routes: dict[str, Any],
    repository_roots: dict[str, Path],
    packet_claim_ids: dict[str, set[str]],
) -> None:
    if routes.get("schema_version") != "1.0":
        raise ControlError("consumer route registry requires schema_version '1.0'")
    policy = routes.get("policy")
    if not isinstance(policy, dict) or policy.get("accepted_route_gate") != "task_specific_contract_review":
        _add_issue(
            result,
            "consumer_route_policy_drift",
            "accepted routes must remain gated by task_specific_contract_review",
        )
    route_items = routes.get("routes")
    if not isinstance(route_items, list):
        raise ControlError("consumer route registry routes must be a list")
    result["routes_total"] = len(route_items)
    result["route_statuses"] = dict(
        Counter(item.get("status") for item in route_items if isinstance(item, dict))
    )
    seen_ids: set[str] = set()
    for route in route_items:
        if not isinstance(route, dict):
            raise ControlError("consumer route registry contains a non-object route")
        route_id = route.get("route_id")
        if not isinstance(route_id, str) or not route_id:
            raise ControlError("every consumer route needs a non-empty route_id")
        if route_id in seen_ids:
            _add_issue(result, "duplicate_consumer_route", f"duplicate consumer route {route_id!r}")
        seen_ids.add(route_id)
        status = route.get("status")
        if status not in ALLOWED_ROUTE_STATUSES:
            _add_issue(result, "invalid_consumer_route_status", f"route {route_id} has unsupported status {status!r}")
        packet_id = route.get("packet_id")
        if packet_id not in packet_claim_ids:
            _add_issue(result, "unknown_route_packet", f"route {route_id} references unknown packet {packet_id!r}")
            known_claim_ids: set[str] = set()
        else:
            known_claim_ids = packet_claim_ids[packet_id]
        claim_ids = route.get("claim_ids")
        if not isinstance(claim_ids, list) or not claim_ids or not all(isinstance(item, str) for item in claim_ids):
            _add_issue(result, "invalid_route_claims", f"route {route_id} needs a non-empty claim_ids list")
        else:
            unknown_claims = sorted(set(claim_ids) - known_claim_ids)
            if unknown_claims:
                _add_issue(
                    result,
                    "unknown_route_claim",
                    f"route {route_id} references unknown claims {unknown_claims}",
                )
        repository_id = route.get("repository_id")
        repository_root = repository_roots.get(repository_id)
        if repository_root is None:
            _add_issue(result, "unknown_route_repository", f"route {route_id} references unknown repository {repository_id!r}")
            continue
        artifact_value = route.get("artifact_path")
        if not isinstance(artifact_value, str) or not artifact_value:
            _add_issue(result, "invalid_route_artifact", f"route {route_id} needs artifact_path")
            continue
        artifact_relative = Path(artifact_value.replace("\\", "/"))
        if artifact_relative.is_absolute():
            _add_issue(result, "absolute_route_artifact", f"route {route_id} artifact_path must be repository-relative")
            continue
        artifact = _inside(repository_root / artifact_relative, repository_root, f"route {route_id} artifact")
        if not artifact.is_file():
            _add_issue(result, "missing_route_artifact", f"route {route_id} artifact is missing", path=artifact)
        if status == "accepted":
            acceptance = route.get("acceptance")
            if not isinstance(acceptance, dict) or not acceptance.get("accepted_at"):
                _add_issue(result, "missing_route_acceptance", f"accepted route {route_id} lacks acceptance evidence")
            contract_value = route.get("writing_contract_path")
            if not isinstance(contract_value, str) or not contract_value:
                _add_issue(result, "missing_route_writing_contract", f"accepted route {route_id} lacks writing_contract_path")
            else:
                contract = _inside(
                    repository_root / Path(contract_value.replace("\\", "/")),
                    repository_root,
                    f"route {route_id} writing contract",
                )
                if not contract.is_file():
                    _add_issue(result, "missing_route_writing_contract", f"route {route_id} writing contract is missing", path=contract)
        if status == "reconciled_candidate":
            _parse_iso_date(route.get("reconciled_at"), f"route {route_id} reconciled_at")
            reconciliation_value = route.get("reconciliation_artifact")
            if not isinstance(reconciliation_value, str) or not reconciliation_value:
                _add_issue(
                    result,
                    "missing_route_reconciliation_artifact",
                    f"reconciled route {route_id} lacks reconciliation_artifact",
                )
            else:
                reconciliation = _inside(
                    root / Path(reconciliation_value.replace("\\", "/")),
                    root,
                    f"route {route_id} reconciliation artifact",
                )
                if not reconciliation.is_file():
                    _add_issue(
                        result,
                        "missing_route_reconciliation_artifact",
                        f"route {route_id} reconciliation artifact is missing",
                        path=reconciliation,
                    )
        if status in {"candidate", "reconciliation_required"}:
            result["route_actions"].append(
                {
                    "route_id": route_id,
                    "packet_id": packet_id,
                    "repository_id": repository_id,
                    "status": status,
                    "artifact_path": artifact_value,
                }
            )


def _audit_writing_intakes(
    result: dict[str, Any],
    root: Path,
    intakes: dict[str, Any],
    repository_roots: dict[str, Path],
    packet_claim_statuses: dict[str, dict[str, str]],
) -> None:
    if intakes.get("schema_version") != "1.0":
        raise ControlError("writing intake registry requires schema_version '1.0'")
    policy = intakes.get("policy")
    if not isinstance(policy, dict) or policy.get("merge_gate") != "task_specific_contract_review":
        _add_issue(
            result,
            "writing_intake_policy_drift",
            "writing intakes must remain gated by task_specific_contract_review",
        )
    items = intakes.get("intakes")
    if not isinstance(items, list):
        raise ControlError("writing intake registry intakes must be a list")
    result["writing_intakes_total"] = len(items)
    result["writing_intake_statuses"] = dict(
        Counter(item.get("status") for item in items if isinstance(item, dict))
    )
    seen_ids: set[str] = set()
    for intake in items:
        if not isinstance(intake, dict):
            raise ControlError("writing intake registry contains a non-object intake")
        intake_id = intake.get("intake_id")
        if not isinstance(intake_id, str) or not intake_id:
            raise ControlError("every writing intake needs a non-empty intake_id")
        if intake_id in seen_ids:
            _add_issue(result, "duplicate_writing_intake", f"duplicate writing intake {intake_id!r}")
        seen_ids.add(intake_id)
        status = intake.get("status")
        if status not in ALLOWED_INTAKE_STATUSES:
            _add_issue(result, "invalid_writing_intake_status", f"intake {intake_id} has unsupported status {status!r}")
        _parse_iso_date(intake.get("reviewed_at"), f"intake {intake_id} reviewed_at")

        source_packets = intake.get("source_packets")
        if not isinstance(source_packets, list) or not source_packets or not all(
            isinstance(packet_id, str) for packet_id in source_packets
        ):
            _add_issue(result, "invalid_intake_packets", f"intake {intake_id} needs source_packets")
            source_packets = []
        for packet_id in source_packets:
            if packet_id not in packet_claim_statuses:
                _add_issue(result, "unknown_intake_packet", f"intake {intake_id} references unknown packet {packet_id!r}")

        repository_id = intake.get("target_repository_id")
        repository_root = repository_roots.get(repository_id)
        if repository_root is None:
            _add_issue(result, "unknown_intake_repository", f"intake {intake_id} references unknown repository {repository_id!r}")
            continue

        target_files: dict[str, Path] = {}
        for field in ("target_document", "target_contract"):
            value = intake.get(field)
            if not isinstance(value, str) or not value:
                _add_issue(result, "invalid_intake_target", f"intake {intake_id} needs {field}")
                continue
            relative = Path(value.replace("\\", "/"))
            if relative.is_absolute():
                _add_issue(result, "absolute_intake_target", f"intake {intake_id} {field} must be repository-relative")
                continue
            target = _inside(repository_root / relative, repository_root, f"intake {intake_id} {field}")
            target_files[field] = target
            if not target.is_file():
                _add_issue(result, "missing_intake_target", f"intake {intake_id} {field} is missing", path=target)

        control_files: dict[str, Path] = {}
        for field in ("decision_artifact", "contract_fragment"):
            value = intake.get(field)
            if not isinstance(value, str) or not value:
                _add_issue(result, "invalid_intake_artifact", f"intake {intake_id} needs {field}")
                continue
            relative = Path(value.replace("\\", "/"))
            if relative.is_absolute():
                _add_issue(result, "absolute_intake_artifact", f"intake {intake_id} {field} must be repository-relative")
                continue
            artifact = _inside(root / relative, root, f"intake {intake_id} {field}")
            control_files[field] = artifact
            if not artifact.is_file():
                _add_issue(result, "missing_intake_artifact", f"intake {intake_id} {field} is missing", path=artifact)

        target_document = target_files.get("target_document")
        observed_markers = intake.get("observed_ref_missing_occurrences")
        if target_document and target_document.is_file():
            actual_markers = _read_text(target_document, f"intake target for {intake_id}").count("[REF-MISSING]")
            if observed_markers != actual_markers:
                _add_issue(
                    result,
                    "intake_marker_count_drift",
                    f"intake {intake_id} records {observed_markers!r} REF-MISSING occurrences but target has {actual_markers}",
                    path=target_document,
                )

        merged = intake.get("writing_contract_merged")
        removable = intake.get("content_markers_removable_now")
        if not isinstance(merged, bool) or not isinstance(removable, int) or removable < 0:
            _add_issue(result, "invalid_intake_merge_state", f"intake {intake_id} needs boolean merge state and non-negative removable count")
        elif removable > 0 and not merged:
            _add_issue(result, "unmerged_marker_removal", f"intake {intake_id} cannot authorize marker removal before contract merge")
        if status == "reviewed_candidate" and merged is not False:
            _add_issue(result, "candidate_intake_marked_merged", f"reviewed candidate {intake_id} must remain unmerged")

        decision_path = control_files.get("decision_artifact")
        if not decision_path or not decision_path.is_file():
            continue
        decision_artifact = _read_json(decision_path, f"decision artifact for {intake_id}")
        if decision_artifact.get("intake_id") != intake_id:
            _add_issue(result, "intake_id_mismatch", f"decision artifact for {intake_id} has a different intake_id", path=decision_path)
        decisions = decision_artifact.get("decisions")
        if not isinstance(decisions, list) or not decisions:
            _add_issue(result, "missing_intake_decisions", f"intake {intake_id} has no decisions", path=decision_path)
            continue
        seen_decision_ids: set[str] = set()
        for decision in decisions:
            if not isinstance(decision, dict):
                raise ControlError(f"intake {intake_id} contains a non-object decision")
            decision_id = decision.get("decision_id")
            if not isinstance(decision_id, str) or not decision_id:
                _add_issue(result, "invalid_intake_decision_id", f"intake {intake_id} has a decision without an ID")
                continue
            if decision_id in seen_decision_ids:
                _add_issue(result, "duplicate_intake_decision", f"intake {intake_id} repeats decision {decision_id!r}")
            seen_decision_ids.add(decision_id)
            outcome = decision.get("outcome")
            if outcome not in ALLOWED_INTAKE_DECISIONS:
                _add_issue(result, "invalid_intake_decision", f"decision {decision_id} has unsupported outcome {outcome!r}")
            if outcome in {"partial_split_required", "insufficient_keep_marker"} and decision.get("marker_retained") is not True:
                _add_issue(result, "intake_marker_boundary_drift", f"decision {decision_id} must retain its unresolved marker")
            source_claims = decision.get("source_claims", [])
            if not isinstance(source_claims, list):
                raise ControlError(f"decision {decision_id} source_claims must be a list")
            for claim_ref in source_claims:
                if not isinstance(claim_ref, dict):
                    raise ControlError(f"decision {decision_id} has a non-object source claim")
                packet_id = claim_ref.get("packet_id")
                claim_id = claim_ref.get("claim_id")
                status_map = packet_claim_statuses.get(packet_id, {})
                if claim_id not in status_map:
                    _add_issue(result, "unknown_intake_claim", f"decision {decision_id} references unknown claim {packet_id}:{claim_id}")
                elif outcome == "candidate_support" and status_map[claim_id] != "verified":
                    _add_issue(
                        result,
                        "unverified_candidate_support",
                        f"decision {decision_id} treats {packet_id}:{claim_id} ({status_map[claim_id]}) as candidate support",
                    )


def _audit_runtime_scan(
    result: dict[str, Any],
    snapshot: dict[str, Any],
    snapshot_path: Path,
    queue: dict[str, Any],
    registered_zotero_keys: set[str],
) -> None:
    if snapshot.get("schema_version") != "1.0":
        raise ControlError("literature runtime scan requires schema_version '1.0'")
    if snapshot.get("scope") != "current_local_device":
        _add_issue(result, "runtime_scope_drift", "runtime scan scope must remain current_local_device")
    observed_at = _parse_iso_datetime(snapshot.get("observed_at"), "runtime_scan.observed_at")
    queue_scan = queue.get("read_only_scan")
    if not isinstance(queue_scan, dict):
        raise ControlError("maintenance queue read_only_scan must be an object")
    queue_date = _parse_iso_date(queue_scan.get("last_completed"), "read_only_scan.last_completed")
    if observed_at.date() != queue_date:
        _add_issue(
            result,
            "runtime_scan_date_drift",
            f"runtime snapshot date {observed_at.date()} differs from queue date {queue_date}",
            path=snapshot_path,
        )
    expected_snapshot = queue_scan.get("runtime_snapshot")
    if expected_snapshot != "evidence/literature/runtime_scan.json":
        _add_issue(
            result,
            "runtime_scan_pointer_drift",
            "maintenance queue must point to evidence/literature/runtime_scan.json",
        )

    zotero = snapshot.get("zotero")
    if not isinstance(zotero, dict):
        raise ControlError("runtime scan zotero must be an object")
    required_health = {
        "local_api_enabled_pref": True,
        "api_running": True,
        "connector_running": True,
    }
    for field, expected in required_health.items():
        if zotero.get(field) is not expected:
            _add_issue(result, "zotero_runtime_unhealthy", f"runtime scan zotero.{field} must be {expected}")
    if zotero.get("api_status") != 200:
        _add_issue(result, "zotero_runtime_unhealthy", "runtime scan api_status must be 200")

    selected_target = snapshot.get("selected_target")
    if not isinstance(selected_target, dict) or not all(
        selected_target.get(field) not in {None, ""}
        for field in ("library_id", "library_name", "collection_id", "collection_name")
    ):
        _add_issue(result, "invalid_runtime_target", "runtime scan needs a selected library and collection")
    elif selected_target.get("editable") is not True:
        _add_issue(result, "runtime_target_not_editable", "selected Zotero target is not editable")

    items = snapshot.get("items")
    if not isinstance(items, list):
        raise ControlError("runtime scan items must be a list")
    observed_keys: list[str] = []
    resolved = 0
    seadrive_resolved = 0
    for item in items:
        if not isinstance(item, dict):
            raise ControlError("runtime scan contains a non-object item")
        parent_key = item.get("parent_item_key")
        if not isinstance(parent_key, str) or not parent_key:
            _add_issue(result, "invalid_runtime_item_key", "runtime scan item lacks parent_item_key")
            continue
        observed_keys.append(parent_key)
        attachment_key = item.get("attachment_item_key")
        if not isinstance(attachment_key, str) or not attachment_key:
            _add_issue(result, "missing_runtime_attachment", f"runtime item {parent_key} has no attachment key")
        exists = item.get("linked_file_exists") is True
        if not exists:
            _add_issue(result, "unresolved_runtime_attachment", f"runtime item {parent_key} linked file is unavailable")
        else:
            resolved += 1
        if exists and item.get("transport") == "SeaDrive":
            seadrive_resolved += 1
        elif item.get("transport") != "SeaDrive":
            _add_issue(result, "runtime_transport_drift", f"runtime item {parent_key} is not resolved through SeaDrive")
    if len(observed_keys) != len(set(observed_keys)):
        _add_issue(result, "duplicate_runtime_item", "runtime scan repeats a Zotero parent key")
    if set(observed_keys) != registered_zotero_keys:
        _add_issue(
            result,
            "runtime_registry_identity_drift",
            "runtime parent keys differ from registered packet Zotero identities",
        )

    summary = snapshot.get("summary")
    expected_summary = {
        "registered_zotero_items": len(items),
        "linked_files_resolved": resolved,
        "seadrive_linked_files_resolved": seadrive_resolved,
        "all_registered_items_ready": bool(items)
        and resolved == len(items)
        and seadrive_resolved == len(items),
    }
    if not isinstance(summary, dict):
        raise ControlError("runtime scan summary must be an object")
    for field, expected in expected_summary.items():
        if summary.get(field) != expected:
            _add_issue(
                result,
                "runtime_summary_mismatch",
                f"runtime summary {field}={summary.get(field)!r}, expected {expected!r}",
            )

    if snapshot.get("path_disclosure") != "omitted":
        _add_issue(result, "runtime_path_disclosure", "runtime scan must omit workstation-specific paths")
    serialized = json.dumps(snapshot, ensure_ascii=False)
    if WINDOWS_ABSOLUTE_RE.search(serialized) or UNC_PATH_RE.search(serialized):
        _add_issue(result, "runtime_path_disclosure", "runtime scan contains a workstation-specific path")

    cross_device = snapshot.get("cross_device_equivalence_verified")
    if not isinstance(cross_device, bool):
        _add_issue(result, "invalid_cross_device_state", "cross-device equivalence must be boolean")
    external_actions = [
        action
        for action in queue.get("actions", [])
        if isinstance(action, dict) and action.get("action_id") == "lit-cross-device-seadrive-verification"
    ]
    external_completed = bool(external_actions and external_actions[0].get("status") == "completed")
    if cross_device is True and not external_completed:
        _add_issue(
            result,
            "unverified_cross_device_claim",
            "runtime scan claims cross-device equivalence before the external gate is completed",
        )
    if cross_device is False and external_completed:
        _add_issue(
            result,
            "cross_device_state_drift",
            "external cross-device gate is completed but runtime snapshot remains false",
        )
    result["runtime_scan"] = {
        "observed_at": snapshot.get("observed_at"),
        "registered_zotero_items": len(items),
        "linked_files_resolved": resolved,
        "seadrive_linked_files_resolved": seadrive_resolved,
        "cross_device_equivalence_verified": cross_device,
    }


def _audit_acquisition_queue(
    result: dict[str, Any],
    root: Path,
    acquisition: dict[str, Any],
    writing_intakes: dict[str, Any],
    human_gates: dict[str, Any],
    packet_ids: set[str],
) -> None:
    if acquisition.get("schema_version") != "1.0":
        raise ControlError("literature acquisition queue requires schema_version '1.0'")
    policy = acquisition.get("policy")
    if not isinstance(policy, dict):
        raise ControlError("literature acquisition queue policy must be an object")
    expected_policy = {
        "active_work_item_limit": 1,
        "minimum_sources_per_packet": 3,
        "maximum_sources_per_packet": 5,
        "metadata_is_not_evidence": True,
        "full_text_required_for_verified_entailment": True,
        "zotero_write_gate": "explicit_user_authorization",
        "writing_merge_gate": "task_specific_contract_review",
        "candidate_discovery_does_not_remove_ref_missing": True,
    }
    for field, expected in expected_policy.items():
        if policy.get(field) != expected:
            _add_issue(result, "acquisition_policy_drift", f"acquisition policy {field} must remain {expected!r}")

    intake_items = writing_intakes.get("intakes")
    if not isinstance(intake_items, list):
        raise ControlError("writing intake registry intakes must be a list")
    intake_decisions: dict[str, dict[str, dict[str, Any]]] = {}
    required_content_gaps: set[tuple[str, str]] = set()
    for intake in intake_items:
        if not isinstance(intake, dict):
            raise ControlError("writing intake registry contains a non-object intake")
        intake_id = intake.get("intake_id")
        artifact_value = intake.get("decision_artifact")
        if not isinstance(intake_id, str) or not isinstance(artifact_value, str):
            continue
        artifact = _inside(
            root / Path(artifact_value.replace("\\", "/")),
            root,
            f"writing intake {intake_id} decision artifact",
        )
        decision_artifact = _read_json(artifact, f"decision artifact for acquisition {intake_id}")
        decisions = decision_artifact.get("decisions")
        if not isinstance(decisions, list):
            raise ControlError(f"writing intake {intake_id} decisions must be a list")
        decision_map = {
            decision.get("decision_id"): decision
            for decision in decisions
            if isinstance(decision, dict) and isinstance(decision.get("decision_id"), str)
        }
        intake_decisions[intake_id] = decision_map
        required_content_gaps.update(
            (intake_id, decision_id)
            for decision_id, decision in decision_map.items()
            if decision.get("decision_scope") == "content_ref_missing_gap"
        )

    gate_items = human_gates.get("gates")
    if not isinstance(gate_items, list):
        raise ControlError("human-gate registry gates must be a list")
    gate_map = {
        gate.get("gate_id"): gate
        for gate in gate_items
        if isinstance(gate, dict) and isinstance(gate.get("gate_id"), str)
    }
    work_items = acquisition.get("work_items")
    if not isinstance(work_items, list):
        raise ControlError("literature acquisition queue work_items must be a list")
    result["acquisition_queue"] = {
        "work_items_total": len(work_items),
        "active_work_item_id": acquisition.get("active_work_item_id"),
        "status_counts": {},
        "ready_items": [],
    }
    seen_ids: set[str] = set()
    coverage: Counter[tuple[str, str]] = Counter()
    statuses: Counter[str] = Counter()
    item_map: dict[str, dict[str, Any]] = {}
    for item in work_items:
        if not isinstance(item, dict):
            raise ControlError("literature acquisition queue contains a non-object work item")
        work_item_id = item.get("work_item_id")
        if not isinstance(work_item_id, str) or not work_item_id:
            raise ControlError("every acquisition work item needs a non-empty work_item_id")
        if work_item_id in seen_ids:
            _add_issue(result, "duplicate_acquisition_work_item", f"duplicate acquisition item {work_item_id!r}")
        seen_ids.add(work_item_id)
        item_map[work_item_id] = item
        status = item.get("status")
        priority = item.get("priority")
        statuses[str(status)] += 1
        if status not in ALLOWED_ACQUISITION_STATUSES:
            _add_issue(result, "invalid_acquisition_status", f"item {work_item_id} has status {status!r}")
        if priority not in ALLOWED_ACQUISITION_PRIORITIES:
            _add_issue(result, "invalid_acquisition_priority", f"item {work_item_id} has priority {priority!r}")
        intake_id = item.get("target_intake_id")
        decision_map = intake_decisions.get(intake_id)
        if decision_map is None:
            _add_issue(result, "unknown_acquisition_intake", f"item {work_item_id} references intake {intake_id!r}")
            decision_map = {}
        decision_ids = item.get("target_decision_ids")
        if not isinstance(decision_ids, list) or not decision_ids or not all(
            isinstance(decision_id, str) for decision_id in decision_ids
        ):
            _add_issue(result, "invalid_acquisition_decisions", f"item {work_item_id} needs target_decision_ids")
            decision_ids = []
        for decision_id in decision_ids:
            if decision_id not in decision_map:
                _add_issue(result, "unknown_acquisition_decision", f"item {work_item_id} references {intake_id}:{decision_id}")
            else:
                coverage[(str(intake_id), decision_id)] += 1
        target_count = item.get("source_target_count")
        if not isinstance(target_count, int) or not (
            policy.get("minimum_sources_per_packet", 3)
            <= target_count
            <= policy.get("maximum_sources_per_packet", 5)
        ):
            _add_issue(result, "invalid_acquisition_source_cap", f"item {work_item_id} source_target_count must be 3--5")
        for field in ("research_question", "next_action"):
            if not isinstance(item.get(field), str) or not item.get(field):
                _add_issue(result, "incomplete_acquisition_item", f"item {work_item_id} lacks {field}")
        for field in ("target_sections", "source_requirements", "exclusions", "stop_conditions"):
            if not isinstance(item.get(field), list) or not item.get(field):
                _add_issue(result, "incomplete_acquisition_item", f"item {work_item_id} lacks {field}")
        queries = item.get("search_queries")
        if not isinstance(queries, list):
            _add_issue(result, "invalid_acquisition_queries", f"item {work_item_id} search_queries must be a list")
        elif status == "ready_for_search" and not queries:
            _add_issue(result, "missing_acquisition_queries", f"ready item {work_item_id} has no search queries")
        candidates = item.get("candidate_sources")
        if not isinstance(candidates, list):
            _add_issue(result, "invalid_acquisition_candidates", f"item {work_item_id} candidate_sources must be a list")
            candidates = []
        if len(candidates) > int(policy.get("maximum_sources_per_packet", 5)):
            _add_issue(result, "acquisition_candidate_cap_exceeded", f"item {work_item_id} exceeds the five-source cap")
        candidate_ids: set[str] = set()
        for candidate in candidates:
            if not isinstance(candidate, dict):
                raise ControlError(f"item {work_item_id} contains a non-object candidate")
            candidate_id = candidate.get("candidate_id")
            if not isinstance(candidate_id, str) or not candidate_id:
                _add_issue(result, "invalid_acquisition_candidate", f"item {work_item_id} candidate lacks candidate_id")
            elif candidate_id in candidate_ids:
                _add_issue(result, "duplicate_acquisition_candidate", f"item {work_item_id} repeats {candidate_id!r}")
            else:
                candidate_ids.add(candidate_id)
            for field in ("title", "stable_identity", "official_url"):
                if not isinstance(candidate.get(field), str) or not candidate.get(field):
                    _add_issue(result, "invalid_acquisition_candidate", f"item {work_item_id} candidate lacks {field}")
            read_state = candidate.get("read_state")
            entailment_status = candidate.get("entailment_status")
            if read_state not in {"metadata", "abstract", "full_text"}:
                _add_issue(result, "invalid_candidate_read_state", f"item {work_item_id} candidate has invalid read_state")
            if entailment_status not in {None, "unassessed", "abstract_consistent", "verified"}:
                _add_issue(result, "invalid_candidate_entailment", f"item {work_item_id} candidate has invalid entailment_status")
            elif entailment_status == "verified" and not (
                read_state == "full_text"
                and status == "packet_ready"
                and isinstance(item.get("downstream_packet_id"), str)
                and isinstance(candidate.get("packet_source_id"), str)
                and candidate.get("screening_decision") == "retain_for_packet"
            ):
                _add_issue(result, "candidate_evidence_promotion", f"item {work_item_id} candidate is prematurely promoted")
        downstream_packet_id = item.get("downstream_packet_id")
        if downstream_packet_id is not None and downstream_packet_id not in packet_ids:
            _add_issue(result, "unknown_acquisition_packet", f"item {work_item_id} references packet {downstream_packet_id!r}")
        blocking_gate_id = item.get("blocking_gate_id")
        if status == "blocked_on_gate":
            gate = gate_map.get(blocking_gate_id)
            if gate is None:
                _add_issue(result, "missing_acquisition_gate", f"blocked item {work_item_id} lacks a registered gate")
            elif not str(gate.get("status", "")).startswith("pending_"):
                _add_issue(result, "closed_acquisition_gate", f"blocked item {work_item_id} references a non-open gate")
        elif blocking_gate_id is not None:
            _add_issue(result, "unexpected_acquisition_gate", f"unblocked item {work_item_id} declares blocking_gate_id")
        if status == "packet_ready" and not downstream_packet_id:
            _add_issue(result, "missing_acquisition_packet", f"packet-ready item {work_item_id} lacks downstream_packet_id")
        if status == "packet_ready" and (
            len(candidates) != target_count
            or any(candidate.get("read_state") != "full_text" for candidate in candidates)
            or any(candidate.get("screening_decision") != "retain_for_packet" for candidate in candidates)
        ):
            _add_issue(
                result,
                "incomplete_packet_ready_acquisition",
                f"packet-ready item {work_item_id} must retain exactly its target count of full-text candidates",
            )
        if status in {"ready_for_search", "candidate_screening", "full_text_review"}:
            result["acquisition_queue"]["ready_items"].append(work_item_id)

    missing_coverage = sorted(required_content_gaps - set(coverage))
    duplicate_coverage = sorted(key for key, count in coverage.items() if count > 1)
    extra_coverage = sorted(set(coverage) - required_content_gaps)
    if missing_coverage:
        _add_issue(result, "unrouted_content_gap", f"acquisition queue omits content gaps {missing_coverage}")
    if duplicate_coverage:
        _add_issue(result, "duplicate_content_gap_route", f"content gaps have multiple acquisition routes {duplicate_coverage}")
    if extra_coverage:
        _add_issue(result, "non_content_gap_acquisition_route", f"acquisition queue routes non-content decisions {extra_coverage}")
    active_id = acquisition.get("active_work_item_id")
    active_item = item_map.get(active_id)
    if active_item is None:
        _add_issue(result, "missing_active_acquisition_item", f"active acquisition item {active_id!r} is missing")
    elif active_item.get("status") not in {"ready_for_search", "candidate_screening", "full_text_review"}:
        _add_issue(result, "inactive_acquisition_pointer", f"active acquisition item {active_id} is not actionable")
    active_count = sum(1 for item in work_items if item.get("work_item_id") == active_id)
    if active_count > int(policy.get("active_work_item_limit", 1)):
        _add_issue(result, "acquisition_active_limit_exceeded", "acquisition queue exceeds active work-item limit")
    result["acquisition_queue"]["status_counts"] = dict(statuses)


def audit_literature_control(
    root: Path = ROOT,
    registry_path: Path | None = None,
    queue_path: Path | None = None,
    routes_path: Path | None = None,
    repo_config_path: Path | None = None,
    writing_intakes_path: Path | None = None,
    runtime_scan_path: Path | None = None,
    acquisition_queue_path: Path | None = None,
    human_gates_path: Path | None = None,
    *,
    as_of: date | None = None,
) -> dict[str, Any]:
    """Return a machine-readable, non-mutating literature-control audit."""

    resolved_root = root.resolve()
    registry_file = (registry_path or resolved_root / "evidence" / "literature" / "packet_registry.json").resolve()
    queue_file = (queue_path or resolved_root / "evidence" / "literature" / "maintenance_queue.json").resolve()
    routes_file = (routes_path or resolved_root / "evidence" / "literature" / "consumer_routes.json").resolve()
    writing_intakes_file = (
        writing_intakes_path or resolved_root / "evidence" / "literature" / "writing_intakes.json"
    ).resolve()
    runtime_scan_file = (
        runtime_scan_path or resolved_root / "evidence" / "literature" / "runtime_scan.json"
    ).resolve()
    acquisition_queue_file = (
        acquisition_queue_path or resolved_root / "evidence" / "literature" / "acquisition_queue.json"
    ).resolve()
    human_gates_file = (human_gates_path or resolved_root / "registry" / "human_gates.json").resolve()
    repo_config_file = (repo_config_path or resolved_root / "config" / "repository_sync.json").resolve()
    _inside(registry_file, resolved_root, "packet registry")
    _inside(queue_file, resolved_root, "maintenance queue")
    _inside(routes_file, resolved_root, "consumer route registry")
    _inside(writing_intakes_file, resolved_root, "writing intake registry")
    _inside(runtime_scan_file, resolved_root, "literature runtime scan")
    _inside(acquisition_queue_file, resolved_root, "literature acquisition queue")
    _inside(human_gates_file, resolved_root, "human-gate registry")
    _inside(repo_config_file, resolved_root, "repository sync configuration")
    registry = _read_json(registry_file, "packet registry")
    queue = _read_json(queue_file, "maintenance queue")
    routes = _read_json(routes_file, "consumer route registry")
    writing_intakes = _read_json(writing_intakes_file, "writing intake registry")
    runtime_scan = _read_json(runtime_scan_file, "literature runtime scan")
    acquisition_queue = _read_json(acquisition_queue_file, "literature acquisition queue")
    human_gates = _read_json(human_gates_file, "human-gate registry")
    repository_roots = _load_repository_roots(resolved_root, repo_config_file)
    if registry.get("schema_version") != "1.0":
        raise ControlError("packet registry requires schema_version '1.0'")
    source_of_truth = registry.get("source_of_truth")
    expected_truth = {
        "bibliography": "local Zotero Desktop",
        "linked_attachments": "SeaDrive",
        "evidence_packets": "research-harness/evidence/literature/packets",
    }
    if not isinstance(source_of_truth, dict):
        raise ControlError("packet registry source_of_truth must be an object")

    result: dict[str, Any] = {
        "control_root": str(resolved_root),
        "registry": str(registry_file),
        "queue": str(queue_file),
        "consumer_routes": str(routes_file),
        "writing_intakes": str(writing_intakes_file),
        "runtime_scan_file": str(runtime_scan_file),
        "acquisition_queue_file": str(acquisition_queue_file),
        "human_gates_file": str(human_gates_file),
        "repository_config": str(repo_config_file),
        "packets_total": 0,
        "sources_total": 0,
        "claims_total": 0,
        "links_total": 0,
        "packet_statuses": {},
        "read_only_scan": {},
        "open_actions": [],
        "routes_total": 0,
        "route_statuses": {},
        "route_actions": [],
        "writing_intakes_total": 0,
        "writing_intake_statuses": {},
        "runtime_scan": {},
        "acquisition_queue": {},
        "issues": [],
    }
    for field, expected in expected_truth.items():
        if source_of_truth.get(field) != expected:
            _add_issue(result, "source_of_truth_drift", f"source_of_truth.{field} must remain {expected!r}")

    packets = registry.get("packets")
    if not isinstance(packets, list):
        raise ControlError("packet registry packets must be a list")
    result["packets_total"] = len(packets)
    result["packet_statuses"] = dict(Counter(packet.get("status") for packet in packets if isinstance(packet, dict)))
    seen_packet_ids: set[str] = set()
    seen_packet_paths: set[Path] = set()
    global_zotero_keys: dict[str, str] = {}
    packet_claim_ids: dict[str, set[str]] = {}
    packet_claim_statuses: dict[str, dict[str, str]] = {}
    for packet in packets:
        if not isinstance(packet, dict):
            raise ControlError("packet registry contains a non-object packet")
        _audit_packet(
            result,
            resolved_root,
            packet,
            seen_packet_ids,
            seen_packet_paths,
            global_zotero_keys,
            packet_claim_ids,
            packet_claim_statuses,
        )
    _audit_queue(result, queue, seen_packet_ids, as_of or date.today())
    _audit_consumer_routes(
        result,
        resolved_root,
        routes,
        repository_roots,
        packet_claim_ids,
    )
    _audit_writing_intakes(
        result,
        resolved_root,
        writing_intakes,
        repository_roots,
        packet_claim_statuses,
    )
    _audit_runtime_scan(
        result,
        runtime_scan,
        runtime_scan_file,
        queue,
        set(global_zotero_keys),
    )
    _audit_acquisition_queue(
        result,
        resolved_root,
        acquisition_queue,
        writing_intakes,
        human_gates,
        seen_packet_ids,
    )
    result["exit_code"] = 2 if result["issues"] else 0
    return result


def render_text(result: dict[str, Any]) -> str:
    label = "OK" if result["exit_code"] == 0 else "WARN"
    scan = result.get("read_only_scan", {})
    lines = [
        f"[{label}] literature control: packets={result['packets_total']} "
        f"sources={result['sources_total']} claims={result['claims_total']} links={result['links_total']} "
        f"routes={result['routes_total']} writing_intakes={result['writing_intakes_total']}",
        f"  read-only scan: last={scan.get('last_completed')} age={scan.get('age_days')}d "
        f"interval={scan.get('interval_days')}d",
    ]
    runtime = result.get("runtime_scan", {})
    lines.append(
        f"  runtime: items={runtime.get('registered_zotero_items')} "
        f"resolved={runtime.get('linked_files_resolved')} "
        f"seadrive={runtime.get('seadrive_linked_files_resolved')} "
        f"cross_device={runtime.get('cross_device_equivalence_verified')}"
    )
    acquisition = result.get("acquisition_queue", {})
    lines.append(
        f"  acquisition: items={acquisition.get('work_items_total')} "
        f"active={acquisition.get('active_work_item_id')} "
        f"actionable={len(acquisition.get('ready_items', []))}"
    )
    for action in result["open_actions"]:
        lines.append(
            f"  - WAIT {action['action_id']}: {action['status']} "
            f"(gate={action['gate']})"
        )
    for route in result["route_actions"]:
        lines.append(
            f"  - ROUTE {route['route_id']}: {route['status']} "
            f"({route['repository_id']}:{route['artifact_path']})"
        )
    for issue in result["issues"]:
        location = f" [{issue['path']}]" if issue.get("path") else ""
        lines.append(f"  - {issue['code']}: {issue['message']}{location}")
    lines.append(
        f"summary: exit={result['exit_code']} issues={len(result['issues'])} "
        f"open_actions={len(result['open_actions'])} route_actions={len(result['route_actions'])}"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--registry", type=Path, default=None)
    parser.add_argument("--queue", type=Path, default=None)
    parser.add_argument("--routes", type=Path, default=None)
    parser.add_argument("--repo-config", type=Path, default=None)
    parser.add_argument("--writing-intakes", type=Path, default=None)
    parser.add_argument("--runtime-scan", type=Path, default=None)
    parser.add_argument("--acquisition-queue", type=Path, default=None)
    parser.add_argument("--human-gates", type=Path, default=None)
    parser.add_argument("--as-of", type=lambda value: datetime.strptime(value, "%Y-%m-%d").date(), default=None)
    parser.add_argument("--json", action="store_true", help="write machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        result = audit_literature_control(
            args.root,
            args.registry,
            args.queue,
            args.routes,
            args.repo_config,
            args.writing_intakes,
            args.runtime_scan,
            args.acquisition_queue,
            args.human_gates,
            as_of=args.as_of,
        )
    except ControlError as exc:
        payload = {"exit_code": 1, "configuration_error": str(exc), "issues": []}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"[CRITICAL] literature control: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
