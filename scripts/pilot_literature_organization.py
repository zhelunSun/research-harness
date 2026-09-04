#!/usr/bin/env python3
"""Read-only, same-corpus retrieval ablation; writes only an ignored local result."""
from __future__ import annotations

import argparse
import copy
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time

if __package__:
    from .literature_catalog import ROOT, CACHE, load_json, search, source_inputs, fingerprints
    from .refresh_literature_runtime import _atomic_write_json
else:
    from literature_catalog import ROOT, CACHE, load_json, search, source_inputs, fingerprints
    from refresh_literature_runtime import _atomic_write_json

CASES = Path("evidence/literature/pilots/organization_20260904/cases.json")
OUTPUT = Path(".cache/literature/organization-pilot.json")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def metadata_view(catalog):
    view = copy.deepcopy(catalog)
    view["facets"] = []
    for entry in view["entries"]:
        entry["evidence"] = []
        entry["packets"] = []
    return view


def fuse(first, second, limit=5):
    scores, entries = defaultdict(float), {}
    for results in (first, second):
        seen = set()
        for rank, entry in enumerate(results, 1):
            if entry["id"] not in seen:
                scores[entry["id"]] += 1 / (60 + rank)
                entries[entry["id"]] = entry
                seen.add(entry["id"])
    ids = sorted(scores, key=lambda key: (-scores[key], entries[key].get("title") or "", key))
    return [entries[key] for key in ids[:limit]]


def anchor_keys(entry):
    # Do not equate related preprints with the edition supporting a packet.
    return {entry.get("bibtex_key")} | {x["bibtex_key"] for x in entry.get("source_records", [])}


def measure(results, anchors):
    found = set().union(*(anchor_keys(e) for e in results)) & set(anchors)
    return {"found": sorted(found), "missed": sorted(set(anchors) - found),
            "coverage_at_5": len(found) / len(set(anchors)),
            "hit_at_5": bool(found), "returned": len(results)}


def archived_view_check(catalog, members):
    # The view holds pointers, never the only copy of literature records.
    before = digest(catalog)
    view = {"id": "provisional-question", "label": "旧问题", "status": "active", "members": list(members)}
    view["label"] = "旧问题（已放弃，保留历史）"
    view["status"] = "archived"
    return {"catalog_unchanged": before == digest(catalog), "records_retained": len(catalog["entries"]),
            "archived_view_members_retained": len(view["members"]),
            "interpretation": "By-construction non-destructive view check, not a measured advantage over Zotero collections."}


def run(catalog, protocol):
    before = digest(catalog)
    metadata = metadata_view(catalog)
    by_bib = {key: e for e in catalog["entries"] for key in anchor_keys(e) if key}
    cases = protocol["cases"]
    if not cases or len({c["id"] for c in cases}) != len(cases):
        raise ValueError("cases must be non-empty with unique IDs")
    for case in cases:
        if not case["anchors"] or len(set(case["anchors"])) != len(case["anchors"]):
            raise ValueError("case anchors must be non-empty and unique")
        if set(case["anchors"]) - by_bib.keys():
            raise ValueError(f"unknown anchor in {case['id']}")
    trials, timing = [], defaultdict(list)
    for case in cases:
        started = time.perf_counter()
        first = search(metadata, case["query"], 30)
        timing["metadata"].append((time.perf_counter() - started) * 1000)
        started = time.perf_counter()
        keywords = search(metadata, protocol.get("keyword_queries", {}).get(case["id"], case["query"]), 30)
        timing["metadata_keywords"].append((time.perf_counter() - started) * 1000)
        started = time.perf_counter()
        second = search(catalog, case["query"], 30)
        timing["question"].append((time.perf_counter() - started) * 1000)
        started = time.perf_counter()
        hybrid = fuse(keywords, second)
        timing["hybrid"].append(timing["metadata_keywords"][-1] + timing["question"][-1] + (time.perf_counter() - started) * 1000)
        for strategy, results in (("metadata", first[:5]), ("metadata_keywords", keywords[:5]), ("question", second[:5]), ("hybrid", hybrid)):
            trials.append({"case": case["id"], "group": case["group"], "query": case["query"],
                           "strategy": strategy, **measure(results, case["anchors"]),
                           "results": [{"id": e["id"], "title": e["title"], "bibtex_key": e.get("bibtex_key"),
                                        "matched_terms": e.get("matched_terms", [])} for e in results]})
    summary = []
    for group in sorted({c["group"] for c in cases}):
        for strategy in ("metadata", "metadata_keywords", "question", "hybrid"):
            subset = [t for t in trials if t["group"] == group and t["strategy"] == strategy]
            summary.append({"group": group, "strategy": strategy, "queries": len(subset),
                            "macro_anchor_coverage_at_5": statistics.mean(t["coverage_at_5"] for t in subset),
                            "queries_with_anchor_at_5": sum(t["hit_at_5"] for t in subset)})
    probe = protocol["stale_view_probe"]
    changed = next(c for c in cases if c["id"] == probe["case_id"])
    scope = next(f for f in catalog["facets"] if f["id"] == probe["old_facet"])
    restricted = {**catalog, "entries": [e for e in catalog["entries"] if set(e["packets"]) & set(scope["packets"])]}
    stale_result = measure(search(restricted, changed["query"], 5), changed["anchors"])
    parents = [e for e in catalog["entries"] if e.get("zotero")]
    handles = next(c["anchors"] for c in cases if c["id"] == "K4")
    tag_results = [e for e in parents if "AI4Science" in e["zotero"]["tags"]]
    collection_results = [e for e in parents if "AI_basis/AI_for_Science" in e["zotero"]["collections"]]
    keys = set().union(*(set(c["anchors"]) for c in cases))
    result = {"snapshot_at": catalog["observed_at"], "catalog_digest": before,
              "case_digest": digest(protocol), "source_fingerprints": catalog["source_fingerprints"],
              "scope": {"catalog_entries_not_unique_papers": len(catalog["entries"]), "zotero_parent_records": len(parents),
                        "unique_anchors": len(keys), "anchors_with_primary_zotero_binding": sum(bool(by_bib[k].get("zotero")) for k in keys),
                        "tagged_parent_records": sum(bool(e["zotero"]["tags"]) for e in parents),
                        "filed_parent_records": sum(bool(e["zotero"]["collections"]) for e in parents)},
              "summary": summary, "trials": trials,
              "median_local_query_ms": {k: statistics.median(v) for k, v in timing.items()},
              "exact_navigation": {"tag": {"total_results": len(tag_results), "known_intake_records_found": len(measure(tag_results, handles)["found"])},
                                   "collection": {"total_results": len(collection_results), "known_intake_records_found": len(measure(collection_results, handles)["found"])},
                                   "note": "Exact filtering without top-5 ranking. Non-anchor records are unjudged, not false positives."},
              "stale_view": {"case": changed["id"], "old_scope": scope["id"], "remaining_candidates": len(restricted["entries"]), **stale_result},
              "archive_check": archived_view_check(catalog, [by_bib[k]["id"] for k in changed["anchors"]]),
              "input_catalog_unchanged": before == digest(catalog)}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        catalog = load_json(root / CACHE)
        _, paths = source_inputs(root)
        if fingerprints(root, paths) != catalog["source_fingerprints"]:
            raise ValueError("catalog source inputs changed; refresh scan before running")
        result = run(catalog, load_json(root / CASES))
        if args.write:
            _atomic_write_json(root / OUTPUT, result)
        print(json.dumps({k: v for k, v in result.items() if k not in {"trials", "source_fingerprints"}}, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, StopIteration) as exc:
        print(json.dumps({"error": str(exc), "results_updated": False}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
