---
name: literature-library-bridge
description: Maintain the connection between a local Zotero library, existing research evidence packets, and evolving research questions. Use for library health, version-aware identity reconciliation, collection history, and finding already-collected literature when an outline is unsettled. Not for unbounded new-paper discovery or accepting thesis claims.
---

# Literature Library Bridge

Keep literature retrievable while research questions evolve. Do not require a final outline or a fixed acquisition list to organize existing material.

## Ownership and recall

- Zotero owns bibliography, item keys and parent/attachment relationships.
- The project's ledgers own located evidence, reading depth and claim boundaries.
- Git and explicit maintenance records preserve repairs and provenance. Chat/memory helps navigation but does not prove current state.
- A local catalog is disposable retrieval cache, not a second bibliography or a writing contract.
- Use the current workspace's AGENTS.md and navigation authority. Never treat a recovery checkout as writable. Keep project paths, item counts and current thesis decisions out of this reusable skill.

## Modes

**Scan/repair:** read the installed Zotero skill first, run its status check, and establish the exact scope. Prefer metadata-only diagnostics. Check identifiers, versions, collection membership, attachments, and packet identity links separately. Inspect PDF paths only when attachment checking is requested. Record before/after evidence for each repair.

**Find existing work:** accept rough questions such as “knowledge changes action”, “task success versus scientific validity”, or “failure recovery”. Search both the library and registered evidence packets. Use bilingual keywords, mechanism/task/evaluation facets, and source-specific claims; chapter assignments remain optional candidate views. Do not launch a new web search merely because a local query returns little.

**Prepare for writing:** use the evidence-ledger skill. Return a small shortlist with why each paper is relevant, reading depth, exact available evidence, limitations, Zotero identity and citation key. A search hit does not authorize a citation or settle novelty.

## Concrete implementation when available

In a research-harness control repository containing `scripts/literature_catalog.py`:

```powershell
python -X utf8 scripts/literature_catalog.py scan --write
python -X utf8 scripts/literature_catalog.py query "专家经验如何影响行动" --limit 5
python -X utf8 scripts/literature_catalog.py query --facet task-evaluation --limit 5
python -X utf8 scripts/audit_literature_control.py
```

`scan --write` reads Zotero and writes only the ignored local cache. It does not fetch PDFs, read private notes, import, tag, merge, or edit Zotero. Query output carries snapshot time and ledger pointers. Rebuild after source fingerprints change; refresh live before any external mutation. On another project, inspect its existing interfaces instead of assuming these scripts exist.

When attachment checking is authorized, use `scripts/refresh_literature_runtime.py`; `--write` updates repository scan metadata, not Zotero. Distinguish current-device file resolution, cloud metadata sync, and second-device equivalence.

## Fragile boundaries learned in use

- Scope item keys by library. Exclude attachment/note/annotation records from paper counts.
- A matching DOI is stronger than a title. Preprint and published versions can share a title and citation key while differing in text. Record related-version links; do not silently replace the edition supporting an evidence span.
- The same source can serve several packets. Deduplicate counts without merging distinct Zotero records.
- On Windows use UTF-8 for the helper process as well as captured output. The stock helper accepts a single `--item-key`; loop explicitly instead of repeating that flag.
- A selected library root is valid for reading. It is not an implicit destination approval for bulk import.
- Never report a failed or partial API read as an empty library. Preserve the last valid cache on failure.
- Cached attachment counts and metadata never prove that a PDF opens, a paper was read, or sync finished.
- Preserve existing writing gates and unresolved scientific judgments, even when the user authorizes technical maintenance.
- Broad repair authorization does not choose a destination for new imports, authorize destructive merges/deletions, or permit sync-account changes. Prepare exact source/destination choices if required.
- Do not edit vendor plugin caches. Keep additions in project code and a user-owned skill.
- Do not upload a whole personal-library cache, local attachment paths, private note bodies or annotations into Git.

## Completion

Report the actual repairs, checks, unresolved technical/scientific boundaries, cache timestamp, and one or two working natural-language retrieval examples. Do not present a reusable skill as an automatic monitor, an unlimited memory, or a cross-device installation.
