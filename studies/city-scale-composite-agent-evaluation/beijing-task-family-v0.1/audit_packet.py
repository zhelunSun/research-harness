"""Read-only integrity audit for a candidate proposal, never a scientific grader."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


PACKET = Path(__file__).resolve().parent
CH3 = PACKET.parents[3] / "urbfo-agent-demo"


def audit(spec: dict, chapter_root: Path, *, verify_assets: bool = True) -> dict:
    errors = []
    if spec.get("status") != "candidate":
        errors.append("This audit only accepts a candidate specification.")
    approvals = spec.get("approvals", {})
    required_approvals = {"scope_accepted", "scientific_gold_accepted", "rubric_accepted", "experiment_authorized"}
    if set(approvals) != required_approvals or any(v is not False for v in approvals.values()):
        errors.append("Candidate document must not imply scope, gold, rubric or experiment approval.")
    runtime = spec.get("runtime_boundary", {})
    if runtime.get("solver_runs") != 0 or runtime.get("geospatial_runs") != 0:
        errors.append("Specification preparation must not be reported as experiment execution.")
    if runtime.get("external_writes") is not False or runtime.get("public_task_package_ready") is not False:
        errors.append("Candidate packet is not a solver-visible package or external-write authorization.")
    if spec.get("readiness", {}).get("scientific_validity") != "not-assessed":
        errors.append("Mechanical checks cannot promote scientific validity.")
    if spec.get("scope", {}).get("approval_status") != "pending_researcher_review":
        errors.append("Scope review must remain pending.")
    if set(spec.get("solver_visible_inputs", [])) & set(spec.get("evaluation_only_inputs", [])):
        errors.append("Evaluation-only information leaks into solver-visible inputs.")

    tasks = spec.get("tasks", [])
    ids = [t["task_id"] for t in tasks]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate task ID.")
    task_by_id = {t["task_id"]: t for t in tasks}
    asset_ids = [a["asset_id"] for a in spec.get("assets", [])]
    if len(asset_ids) != len(set(asset_ids)):
        errors.append("Duplicate asset ID.")
    producers = {}
    for task in tasks:
        if task.get("scientific_reference") != "pending_researcher_review":
            errors.append(f"{task['task_id']}: scientific reference is not admitted.")
        for output in task.get("produces", []):
            if output in producers:
                errors.append(f"Multiple producers for {output}.")
            producers[output] = task["task_id"]
        if not task.get("knowledge_support") or not task.get("required_output_candidate"):
            errors.append(f"{task['task_id']}: missing constructive knowledge/output mapping.")
        for dependency in task.get("depends_on", []):
            if dependency not in task_by_id:
                errors.append(f"{task['task_id']}: unknown dependency {dependency}.")
        for asset in task.get("asset_refs", []):
            if asset not in asset_ids:
                errors.append(f"{task['task_id']}: unknown asset {asset}.")

    def ancestors(task_id: str, visiting: frozenset = frozenset()) -> set:
        if task_id in visiting:
            raise ValueError("Task dependency cycle.")
        result = set()
        for dependency in task_by_id[task_id].get("depends_on", []):
            if dependency not in task_by_id:
                continue
            result.add(dependency)
            result.update(ancestors(dependency, visiting | {task_id}))
        return result

    external = set(spec.get("external_inputs", []))
    consumers = Counter()
    for task in tasks:
        try:
            inherited = ancestors(task["task_id"])
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for item in task.get("consumes", []):
            if item in external:
                continue
            if item not in producers or producers[item] not in inherited:
                errors.append(f"{task['task_id']}: input {item} lacks a dependency-linked producer.")
            consumers[item] += 1
    shared = sorted(k for k, v in consumers.items() if v > 1)
    if not shared:
        errors.append("No actual shared intermediate product is declared.")

    gaps = []
    for asset in spec.get("assets", []):
        relative = Path(asset["path"])
        target = (chapter_root / relative).resolve()
        try:
            target.relative_to(chapter_root.resolve())
        except ValueError:
            errors.append(f"{asset['asset_id']}: source path escapes Chapter 3.")
            continue
        if not asset["exists"]:
            gaps.append(asset["path"])
        if not verify_assets:
            continue
        present = target.is_file()
        if present != asset["exists"]:
            errors.append(f"{asset['asset_id']}: source availability changed; re-audit, do not auto-promote.")
        elif present:
            sha = hashlib.sha256(target.read_bytes()).hexdigest()
            if sha != asset["sha256"]:
                errors.append(f"{asset['asset_id']}: source hash drift.")
        elif asset.get("sha256") is not None:
            errors.append(f"{asset['asset_id']}: absent file has a fabricated hash.")
    return {
        "ok": not errors,
        "scope": "proposal integrity only; no scientific validation",
        "tasks": len(tasks),
        "assets_checked": len(asset_ids),
        "shared_intermediate_products": shared,
        "known_missing_asset_paths": gaps,
        "scientific_validity": spec.get("readiness", {}).get("scientific_validity"),
        "benchmark_release": spec.get("readiness", {}).get("benchmark_release"),
        "errors": errors,
    }


def audit_links() -> list[str]:
    errors = []
    for name in ("README.md", "design.md", "verification.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", (PACKET / name).read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            if not (PACKET / target.split("#", 1)[0]).exists():
                errors.append(f"{name}: missing link {target}")
    contract = json.loads((PACKET / "writing_contract.json").read_text(encoding="utf-8"))
    for target in contract["document"]["authority"]:
        if not (PACKET / target).is_file():
            errors.append(f"Missing contract authority: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter-root", type=Path, default=CH3)
    args = parser.parse_args()
    spec = json.loads((PACKET / "specification.json").read_text(encoding="utf-8"))
    result = audit(spec, args.chapter_root)
    result["errors"].extend(audit_links())
    result["ok"] = not result["errors"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
