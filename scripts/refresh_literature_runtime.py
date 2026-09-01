#!/usr/bin/env python3
"""Refresh a path-redacted Zotero/SeaDrive runtime snapshot.

The command reads Zotero through the installed Zotero skill helper. It never
imports, edits, tags, moves, or deletes Zotero items. Repository files are only
updated when ``--write`` is supplied.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "evidence" / "literature" / "packet_registry.json"
DEFAULT_QUEUE = ROOT / "evidence" / "literature" / "maintenance_queue.json"
DEFAULT_SNAPSHOT = ROOT / "evidence" / "literature" / "runtime_scan.json"


class RefreshError(RuntimeError):
    """The read-only refresh could not be completed safely."""


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RefreshError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RefreshError(f"{label} must contain a JSON object")
    return value


def discover_zotero_helper(codex_home: Path | None = None) -> Path:
    """Return the newest installed Zotero plugin helper without persisting its path."""

    base = codex_home
    if base is None:
        configured = os.environ.get("CODEX_HOME")
        base = Path(configured) if configured else Path.home() / ".codex"
    pattern = "plugins/cache/openai-curated-remote/zotero/*/skills/zotero/scripts/zotero.py"
    candidates = sorted(base.glob(pattern), reverse=True)
    if not candidates:
        raise RefreshError(
            "installed Zotero skill helper was not found; pass --zotero-helper explicitly"
        )
    return candidates[0].resolve()


def _run_helper(helper: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            [os.fspath(Path(sys.executable)), os.fspath(helper), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RefreshError(f"Zotero helper failed for {' '.join(args)}: {exc}") from exc
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise RefreshError(f"Zotero helper failed for {' '.join(args)}: {detail}")
    return completed.stdout.strip()


def _helper_json(helper: Path, *args: str) -> Any:
    raw = _run_helper(helper, *args)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RefreshError(f"Zotero helper returned invalid JSON for {' '.join(args)}") from exc


def _registered_zotero_keys(registry: dict[str, Any]) -> list[str]:
    packets = registry.get("packets")
    if not isinstance(packets, list):
        raise RefreshError("packet registry packets must be a list")
    keys: list[str] = []
    for packet in packets:
        if not isinstance(packet, dict):
            raise RefreshError("packet registry contains a non-object packet")
        packet_keys = packet.get("zotero_item_keys")
        if not isinstance(packet_keys, list) or not all(
            isinstance(key, str) and key for key in packet_keys
        ):
            raise RefreshError("packet zotero_item_keys must be a string list")
        keys.extend(packet_keys)
    if len(keys) != len(set(keys)):
        raise RefreshError("registered Zotero item keys are not unique")
    return sorted(keys)


def _local_file_state(file_url: str) -> tuple[bool, str]:
    parsed = urlparse(file_url)
    if parsed.scheme.casefold() != "file":
        return False, "non_file_url"
    local_value = unquote(parsed.path)
    if os.name == "nt" and len(local_value) >= 3 and local_value[0] == "/" and local_value[2] == ":":
        local_value = local_value[1:]
    local_path = Path(local_value)
    transport = "SeaDrive" if any(part.casefold() == "seadrive" for part in local_path.parts) else "other"
    return local_path.is_file(), transport


def build_runtime_scan(
    helper: Path,
    registry_path: Path = DEFAULT_REGISTRY,
    *,
    observed_at: datetime | None = None,
    json_runner: Callable[..., Any] = _helper_json,
    text_runner: Callable[..., str] = _run_helper,
) -> dict[str, Any]:
    """Read Zotero and linked files, returning a path-redacted snapshot."""

    registry = _read_json(registry_path, "packet registry")
    item_keys = _registered_zotero_keys(registry)
    status = json_runner(helper, "status", "--json")
    target = json_runner(helper, "selected-target", "--json")
    if not isinstance(status, dict) or not isinstance(target, dict):
        raise RefreshError("Zotero status and selected target must be JSON objects")

    item_states: list[dict[str, Any]] = []
    for parent_key in item_keys:
        children = json_runner(helper, "children", parent_key, "--json")
        if not isinstance(children, list):
            raise RefreshError(f"children for {parent_key} must be a JSON list")
        attachments = [
            child
            for child in children
            if isinstance(child, dict)
            and child.get("itemType") == "attachment"
            and isinstance(child.get("key"), str)
        ]
        if not attachments:
            item_states.append(
                {
                    "parent_item_key": parent_key,
                    "attachment_item_key": None,
                    "linked_file_exists": False,
                    "transport": "missing",
                }
            )
            continue
        attachment_key = attachments[0]["key"]
        file_url = text_runner(helper, "file-url", attachment_key).strip()
        exists, transport = _local_file_state(file_url)
        item_states.append(
            {
                "parent_item_key": parent_key,
                "attachment_item_key": attachment_key,
                "linked_file_exists": exists,
                "transport": transport,
            }
        )

    resolved = sum(bool(item["linked_file_exists"]) for item in item_states)
    seadrive = sum(
        bool(item["linked_file_exists"] and item["transport"] == "SeaDrive")
        for item in item_states
    )
    timestamp = observed_at or datetime.now().astimezone()
    return {
        "schema_version": "1.0",
        "observed_at": timestamp.isoformat(timespec="seconds"),
        "scope": "current_local_device",
        "zotero": {
            "version": status.get("zotero_version"),
            "local_api_enabled_pref": status.get("local_api_enabled_pref"),
            "api_running": status.get("api_running"),
            "api_status": status.get("api_status"),
            "connector_running": status.get("connector_running"),
        },
        "selected_target": {
            "library_id": target.get("libraryID"),
            "library_name": target.get("libraryName"),
            "collection_id": target.get("id"),
            "collection_name": target.get("name"),
            "editable": target.get("editable"),
        },
        "items": item_states,
        "summary": {
            "registered_zotero_items": len(item_states),
            "linked_files_resolved": resolved,
            "seadrive_linked_files_resolved": seadrive,
            "all_registered_items_ready": bool(item_states)
            and resolved == len(item_states) == seadrive,
        },
        "path_disclosure": "omitted",
        "cross_device_equivalence_verified": False,
        "limitations": [
            "This snapshot verifies only the current local device.",
            "Zotero local API health does not prove account-level cloud sync completion.",
            "Second-device SeaDrive path resolution remains an external verification gate.",
        ],
    }


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def write_runtime_scan(
    snapshot: dict[str, Any],
    snapshot_path: Path = DEFAULT_SNAPSHOT,
    queue_path: Path = DEFAULT_QUEUE,
) -> None:
    """Write the redacted snapshot and advance the read-only scan date together."""

    if snapshot.get("summary", {}).get("all_registered_items_ready") is not True:
        raise RefreshError("runtime scan is incomplete; maintenance freshness was not advanced")
    queue = _read_json(queue_path, "maintenance queue")
    read_only_scan = queue.get("read_only_scan")
    if not isinstance(read_only_scan, dict):
        raise RefreshError("maintenance queue read_only_scan must be an object")
    observed_date = str(snapshot.get("observed_at", ""))[:10]
    read_only_scan["last_completed"] = observed_date
    control_root = queue_path.resolve().parents[2]
    try:
        runtime_pointer = snapshot_path.resolve().relative_to(control_root).as_posix()
    except ValueError as exc:
        raise RefreshError("runtime snapshot must remain inside the control-plane root") from exc
    read_only_scan["runtime_snapshot"] = runtime_pointer
    read_only_scan["result"] = (
        f"Zotero Desktop/local API healthy; {snapshot['summary']['registered_zotero_items']} "
        "registered parent items have current-device SeaDrive linked files; "
        "cross-device equivalence remains unverified"
    )
    queue["updated_at"] = snapshot["observed_at"]
    _atomic_write_json(snapshot_path, snapshot)
    _atomic_write_json(queue_path, queue)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zotero-helper", type=Path, default=None)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--write", action="store_true", help="write the redacted snapshot and queue freshness")
    parser.add_argument("--json", action="store_true", help="write machine-readable output")
    args = parser.parse_args(argv)
    try:
        helper = (args.zotero_helper or discover_zotero_helper()).resolve()
        snapshot = build_runtime_scan(helper, args.registry)
        if args.write:
            write_runtime_scan(snapshot, args.snapshot, args.queue)
    except RefreshError as exc:
        payload = {"exit_code": 1, "error": str(exc)}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"[CRITICAL] literature runtime refresh: {exc}")
        return 1
    payload = {"exit_code": 0, "written": bool(args.write), "snapshot": snapshot}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        summary = snapshot["summary"]
        print(
            "[OK] literature runtime: "
            f"items={summary['registered_zotero_items']} "
            f"resolved={summary['linked_files_resolved']} "
            f"seadrive={summary['seadrive_linked_files_resolved']} "
            f"written={bool(args.write)}"
        )
        print("  cross-device equivalence: unverified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
