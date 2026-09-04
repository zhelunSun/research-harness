#!/usr/bin/env python3
"""Local, rebuildable bibliography/evidence retrieval. No Zotero writes or full-text reads."""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
import urllib.request

if __package__:
    from .refresh_literature_runtime import discover_zotero_helper, _helper_json, _atomic_write_json
else:
    from refresh_literature_runtime import discover_zotero_helper, _helper_json, _atomic_write_json

ROOT = Path(__file__).resolve().parents[1]
LIT = Path("evidence/literature")
CACHE = Path(".cache/literature/catalog.json")
CHILD_TYPES = {"attachment", "annotation", "note"}


def norm(value):
    return "".join(c for c in unicodedata.normalize("NFKC", value or "").casefold() if c.isalnum())


def doi(value):
    return re.sub(r"^https?://(?:dx\.)?doi.org/", "", (value or "").strip().casefold())


def arxiv(value):
    match = re.search(r"(?:arxiv[:./]|arxiv\.org/(?:abs|pdf)/)(\d{4}\.\d{4,5})(?:v\d+)?", value or "", re.I)
    return match.group(1) if match else ""


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_inputs(root):
    registry = load_json(root / LIT / "packet_registry.json")
    paths = [LIT / "packet_registry.json", LIT / "retrieval_facets.json"]
    paths += [Path(p["path"]) / "ledger.json" for p in registry["packets"]]
    return registry, paths


def fingerprints(root, paths):
    result = {}
    for path in paths:
        resolved = (root / path).resolve()
        resolved.relative_to(root.resolve())
        result[path.as_posix()] = hashlib.sha256(resolved.read_bytes()).hexdigest()
    return result


def read_pages(route, opener=urllib.request.urlopen):
    """Bounded pagination; failed/inconsistent reads must not become an empty-library snapshot."""
    rows, seen = [], set()
    total = None
    for start in range(0, 50000, 100):
        req = urllib.request.Request(
            "http://127.0.0.1:23119/api/users/0/" + route + f"?limit=100&start={start}",
            headers={"Zotero-API-Version": "3"},
        )
        with opener(req, timeout=30) as response:
            count = response.headers.get("Total-Results")
            if count is not None:
                count = int(count)
                if total is not None and total != count:
                    raise RuntimeError("library changed during pagination; retry the scan")
                total = count
            page = json.load(response)
        if not isinstance(page, list):
            raise RuntimeError("local API did not return an item list")
        for row in page:
            key = row["key"]
            if key in seen:
                raise RuntimeError("duplicate page key; do not publish this scan")
            seen.add(key)
        rows.extend(page)
        if len(page) < 100:
            if total is not None and len(rows) != total:
                raise RuntimeError("incomplete pagination")
            return rows
    raise RuntimeError("pagination safety limit reached")


def identity_matches(source, items):
    sd = doi(source.get("identifiers", {}).get("doi"))
    sa = source.get("identifiers", {}).get("arxiv", "")
    results = []
    for item in items:
        d = item["data"]
        idoi = doi(d.get("DOI"))
        ia = arxiv(" ".join(str(d.get(k) or "") for k in ("DOI", "url", "extra")))
        exact_title = bool(norm(source.get("title"))) and norm(source["title"]) == norm(d.get("title"))
        if sd and idoi == sd:
            status = "exact_identifier"
        elif sa and sa == ia:
            status = "same_arxiv_work_version_unchecked"
        elif exact_title:
            status = "title_candidate_version_review" if sd and idoi and sd != idoi else "title_candidate"
        else:
            continue
        results.append({"item_key": item["key"], "match": status, "item_doi": d.get("DOI"), "item_type": d["itemType"]})
    return results


def collection_paths(collections):
    rows = {c["key"]: c["data"] for c in collections}
    def trace(key, seen):
        if key in seen or key not in rows:
            return "[unresolved collection]"
        row = rows[key]
        parent = row.get("parentCollection")
        return (trace(parent, seen | {key}) + "/" if parent else "") + row["name"]
    return {key: trace(key, set()) for key in rows}


def build_catalog(root, items, collections, now=None):
    registry, paths = source_inputs(root)
    now = now or datetime.now(timezone.utc)
    parents = [x for x in items if x["data"]["itemType"] not in CHILD_TYPES]
    children = defaultdict(list)
    for item in items:
        if item["data"].get("parentItem"):
            children[item["data"]["parentItem"]].append(item["data"])
    cp = collection_paths(collections)
    entries, identity, grouped_sources = [], [], {}
    for packet in registry["packets"]:
        ledger = load_json(root / packet["path"] / "ledger.json")
        claims = {c["claim_id"]: c for c in ledger["claims"]}
        for source in ledger["sources"]:
            source_key = source["locator"]
            match = identity_matches(source, parents)
            if source.get("zotero_item_key") and source["zotero_item_key"] not in {m["item_key"] for m in match if m["match"] != "title_candidate_version_review"}:
                raise RuntimeError(f"registered identity mismatch: {packet['packet_id']}/{source['source_id']}")
            identity.append({"packet_id": packet["packet_id"], "source_id": source["source_id"], "title": source["title"], "registered_key": source.get("zotero_item_key"), "matches": match})
            if source_key not in grouped_sources:
                grouped_sources[source_key] = {
                    "id": "source:" + hashlib.sha256(source_key.encode()).hexdigest()[:16],
                    "title": source["title"], "locator": source_key, "bibtex_key": source["bibtex_key"],
                    "zotero_item_keys": [], "related_items": [], "evidence": [], "packets": [], "source_records": [],
                    "read_state": source["read_state"], "writing_eligibility": "not_accepted_by_this_catalog",
                    "bibliography": packet["path"] + "/references.bib",
                }
            entry = grouped_sources[source_key]
            entry["source_records"].append({"packet": packet["packet_id"], "source_id": source["source_id"], "read_state": source["read_state"], "bibtex_key": source["bibtex_key"], "bibliography": packet["path"] + "/references.bib"})
            if entry["read_state"] != source["read_state"]:
                entry["read_state"] = "mixed_see_source_records"
            if source.get("zotero_item_key") and source["zotero_item_key"] not in entry["zotero_item_keys"]:
                entry["zotero_item_keys"].append(source["zotero_item_key"])
            entry["related_items"].extend(source.get("zotero_related_items", []))
            entry["packets"].append(packet["packet_id"])
            for link in ledger["links"]:
                if link["source_id"] == source["source_id"]:
                    claim = claims[link["claim_id"]]
                    entry["evidence"].append({"packet": packet["packet_id"], "claim_id": claim["claim_id"], "claim": claim["text"], "status": claim["evidence_status"], "relation": link["relation"], "entailment_status": link["entailment_status"], "location": link.get("source_location"), "note": link.get("note"), "ledger": packet["path"] + "/ledger.json"})
    entries.extend(grouped_sources.values())
    by_key = {key: e for e in entries for key in e["zotero_item_keys"]}
    for item in parents:
        d, key = item["data"], item["key"]
        entry = by_key.get(key)
        if entry is None:
            entry = {"id": "zotero:users/0:" + key, "title": d.get("title"), "zotero_item_keys": [key], "bibtex_key": None, "read_state": "metadata", "writing_eligibility": "not_assessed", "evidence": [], "packets": [], "related_items": []}
            entries.append(entry)
        entry["zotero"] = {"library": "users/0", "item_key": key, "title": d.get("title"), "creators": d.get("creators", []), "date": d.get("date"), "date_added": d.get("dateAdded"), "date_modified": d.get("dateModified"), "doi": d.get("DOI"), "item_type": d["itemType"], "tags": [t["tag"] for t in d.get("tags", [])], "collections": [cp.get(c, c) for c in d.get("collections", [])], "pdf_attachment_count": sum(c.get("contentType") == "application/pdf" for c in children[key]), "note_count": sum(c.get("itemType") == "note" for c in children[key])}
    dg, tg = defaultdict(list), defaultdict(list)
    for item in parents:
        d = item["data"]
        if doi(d.get("DOI")):
            dg[doi(d["DOI"])].append(item["key"])
        if norm(d.get("title")):
            tg[norm(d["title"])].append(item["key"])
    recent = []
    for item in parents:
        value = item["data"].get("dateAdded")
        if value and datetime.fromisoformat(value.replace("Z", "+00:00")) >= now - timedelta(days=30):
            recent.append(item["key"])
    return {"schema_version": "1.0", "observed_at": now.isoformat(), "scope": "local_personal_library_and_registered_packets", "source_fingerprints": fingerprints(root, paths), "facets": load_json(root / LIT / "retrieval_facets.json")["facets"], "summary": {"bibliographic_items": len(parents), "collections": len(collections), "packet_source_entries": len(identity), "unique_packet_sources": len(grouped_sources), "catalog_entries": len(entries), "recent_30_day_keys": recent, "doi_duplicate_groups": [v for v in dg.values() if len(v) > 1], "title_duplicate_groups": [v for v in tg.values() if len(v) > 1]}, "identity_review": identity, "entries": entries, "limitations": ["Retrieval is lexical plus explicit bilingual hints, not semantic or exhaustive search.", "Tags and facets are retrieval hints, not accepted thesis roles.", "Reading/evidence states are copied from ledgers, not upgraded by indexing.", "Attachment counts do not prove local availability or cross-device synchronization.", "Group libraries, attachment paths, full text, annotations and private note bodies are excluded."]}


def search(catalog, query, limit=6, facet=None):
    q = query.casefold().strip()
    tokens = re.findall(r"[a-z0-9][a-z0-9-]*|[\u4e00-\u9fff]+", q)
    selected = [f for f in catalog["facets"] if f["id"] == facet or (q and any(t.casefold() in q for t in f["terms"]))]
    terms = set(tokens) | {t.casefold() for f in selected for t in f["terms"] if t.casefold() in q}
    # Modest Chinese recall without an embedding service or an external tokenizer.
    stops = {"如何", "怎么", "什么", "哪些", "是否", "可以", "以及", "一个", "我们", "我的", "怎样"}
    for chunk in re.findall(r"[\u4e00-\u9fff]{2,}", q):
        terms.update(chunk[i:i + 2] for i in range(len(chunk) - 1) if chunk[i:i + 2] not in stops)
    for original, alternatives in catalog.get("query_expansions", {}).items():
        if original in q:
            terms.update(a.casefold() for a in alternatives)
    ranked = []
    for entry in catalog["entries"]:
        specific = " ".join(e["claim"] for e in entry["evidence"] if e["status"] == "verified")
        unresolved = " ".join(e["claim"] for e in entry["evidence"] if e["status"] != "verified")
        fields = [entry.get("title") or "", specific, unresolved, entry.get("bibtex_key") or "", " ".join(entry.get("zotero_item_keys", [])), json.dumps(entry.get("zotero", {}), ensure_ascii=False)]
        fields = [x.casefold() for x in fields]
        reasons = [t for t in sorted(terms) if any(t in field for field in fields)]
        packet_hints = [f["id"] for f in selected if set(f["packets"]) & set(entry["packets"])]
        if facet and not packet_hints:
            continue
        score = sum((8 if t in fields[0] else 5 if t in fields[1] else 1 if t in fields[2] else 2) for t in reasons) + len(packet_hints) * 8
        if q and q in fields[0]:
            score += 20
        if score:
            ranked.append((score, entry["title"] or "", {**entry, "retrieval_score": score, "matched_terms": reasons, "retrieval_facets": packet_hints}))
    ranked.sort(key=lambda x: (-x[0], x[1]))
    return [e for _, _, e in ranked[:limit]]


def cache_delta(prior, current):
    old = {e["id"]: e for e in prior["entries"]} if prior else {}
    new = {e["id"]: e for e in current["entries"]}
    return {"baseline_available": prior is not None,
            "added_entry_ids": sorted(new.keys() - old.keys()) if prior else [],
            "removed_entry_ids": sorted(old.keys() - new.keys()) if prior else [],
            "changed_entry_ids": sorted(k for k in old.keys() & new.keys() if old[k] != new[k])}


def exact_lookup(catalog, query):
    """Known identity handles bypass lexical ranking; an absent DOI stays absent."""
    q = query.strip()
    identifier = doi(q)
    if re.fullmatch(r"10\.\d{4,9}/\S+", identifier):
        matches = [e for e in catalog["entries"] if identifier in {
            doi(e.get("zotero", {}).get("doi")), doi(e.get("locator"))}]
        return {"route": "exact_doi", "results": matches}
    matches = [e for e in catalog["entries"] if q.casefold() in {
        str(value).casefold() for value in [e.get("bibtex_key"), *e.get("zotero_item_keys", [])] if value}]
    if matches:
        return {"route": "exact_key", "results": matches}
    matches = [e for e in catalog["entries"] if q and norm(q) == norm(e.get("title"))]
    if matches:
        return {"route": "exact_title", "results": matches}
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan")
    scan.add_argument("--write", action="store_true", help="write ONLY the ignored local cache")
    query = sub.add_parser("query")
    query.add_argument("text", nargs="?", default="")
    query.add_argument("--facet")
    query.add_argument("--limit", type=int, default=6)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "scan":
            helper = discover_zotero_helper()
            status = _helper_json(helper, "status", "--json")
            if not isinstance(status, dict) or not status.get("api_running") or status.get("api_status") != 200:
                raise RuntimeError("Zotero local API is unavailable; no cache was updated")
            catalog = build_catalog(root, read_pages("items"), read_pages("collections"))
            catalog["query_expansions"] = load_json(root / LIT / "retrieval_facets.json").get("query_expansions", {})
            prior = load_json(root / CACHE) if (root / CACHE).exists() else None
            catalog["delta"] = cache_delta(prior, catalog)
            if args.write:
                _atomic_write_json(root / CACHE, catalog)
            output = {"written": args.write, "observed_at": catalog["observed_at"], "summary": catalog["summary"], "identity_review": catalog["identity_review"], "delta": catalog["delta"], "limitations": catalog["limitations"]}
        else:
            catalog = load_json(root / CACHE)
            _, paths = source_inputs(root)
            if fingerprints(root, paths) != catalog["source_fingerprints"]:
                raise RuntimeError("packet inputs changed; run scan --write before querying")
            if args.facet and args.facet not in {f["id"] for f in catalog["facets"]}:
                raise RuntimeError("unknown retrieval facet")
            if not args.text.strip() and not args.facet:
                raise RuntimeError("provide a query or --facet")
            age = datetime.now(timezone.utc) - datetime.fromisoformat(catalog["observed_at"])
            limit = max(1, min(args.limit, 30))
            exact = exact_lookup(catalog, args.text) if not args.facet else None
            results = exact["results"][:limit] if exact is not None else search(catalog, args.text, limit, args.facet)
            output = {"snapshot_at": catalog["observed_at"], "snapshot_age_hours": round(age.total_seconds() / 3600, 2), "zotero_metadata_may_have_changed": True, "refresh_recommended": age > timedelta(days=7), "retrieval_route": exact["route"] if exact is not None else "lexical_candidates", "results": results, "notice": "Candidate retrieval only; inspect linked evidence cards and exact source spans before making claims."}
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc), "cache_updated": False}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
