# Identity and retrieval maintenance — 2026-09-04

## Scope and authority

The researcher requested technical repairs to existing literature connections and
preparation for fast retrieval while the proposal outline remains unsettled.
This permits local indexing, mechanical identity repair and attachment checks;
it does not accept a thesis question, claim, citation insertion, destructive merge,
new import destination, plugin installation, or cloud-sync setting change.

## Observed repairs

| Surface | Before | After / evidence |
| --- | --- | --- |
| ExpertsRS `S-GAC-001` | Ledger key null; old intake reported no match | DOI and exact title match `QRJ9MQ9N`; added 2026-04-23; exported `sun_llm-based_2026`; key bound in ledger/registry; removed from new-import list |
| KnowAgent `S-KAI-002` | Old intake reported no match | Existing preprint `DGHR7CFL`, added 2026-04-28; related-version link recorded, conference DOI retained; no PDF on the preprint; equivalence not verified |
| Runtime snapshot | Five registered keys; did not cover EarthVerse | Seven keys including EarthVerse and ExpertsRS; seven current-device SeaDrive files resolve; no cross-device claim |
| Runtime audit | Required selected collection for a read-only scan | A valid library-root selection passes; missing library identity remains an error; no effect on import approval |
| Helper process | Windows output encoding depended on locale | Child Python runs with `-X utf8` as well as UTF-8 decoding |
| Cross-packet reuse | Repeated item keys rejected | Same source reused across packets counted once in runtime scan |
| Retrieval | Repeated ad hoc inventory commands | Rebuildable local catalog joins personal-library metadata and registered evidence, with bilingual problem/mechanism/task facets and explicit version candidates |

No Zotero item, tag, collection, note, attachment, or synchronization preference
was written. Existing PDFs were checked in place, not copied, moved or uploaded.
No new external scientific search or paper reading was performed.

## Preparation without a frozen outline

Use `retrieval_facets.json` as candidate retrieval hints, not chapter assignments:
knowledge-to-action; evidence/conditions/conflicts; workflow feedback/recovery;
task evaluation; urban-forest interpretation; scientific discovery.

`scripts/literature_catalog.py scan --write` reads 573 personal-library records
and 33 registered source entries (32 distinct source locators). Its 598 catalog
entries are **not 598 distinct papers**: separate unaligned publication versions
and unregistered packet sources remain separate. Group libraries are outside this
cache. The ignored cache never includes private note text, annotations, PDF paths
or full-text payloads. It is not a bibliography or a scientific evidence authority.

Exact/source identifiers, candidate title matches, source spans, publication
version, reading depth and writing eligibility remain separately visible. A
changed ledger invalidates the cache; a failed API read cannot overwrite it with
an empty library. Local scans can expose additions, removals and changed records
relative to the previous cache, but do not reconstruct unobserved historical edits.

## Open boundaries

- Twenty-four distinct packet sources remain unmatched in the personal library;
  KnowAgent has a related preprint requiring version review. Do not conflate these.
- Existing DOI/title duplicate groups remain candidates; no destructive merges.
- Import placement still requires an exact target; selecting the library root is
  not permission to scatter new records there.
- Two-device/cloud equivalence remains an external check.
- All unresolved synthesis claims and opening-report citation markers remain.
- The current execution plan and active-work registry were locked by another
  ongoing task; this maintenance did not overwrite those shared surfaces.

## Verification

```powershell
python -X utf8 -m unittest discover -s tests
python -X utf8 scripts/audit_literature_control.py
python -X utf8 scripts/literature_catalog.py scan --write
python -X utf8 scripts/literature_catalog.py query "专家经验如何影响行动" --limit 5
python -X utf8 scripts/literature_catalog.py query "任务成功不等于科学结论成立" --limit 5
```

Query examples are smoke checks, not a measured semantic-search recall benchmark.
The reusable skill is versioned under `.agents/skills/literature-library-bridge/`;
a matching personal skill is installed on this computer only.

On 2026-09-04 the complete repository suite passed 73 tests and the literature
control audit reported zero issues (pending human gates remain pending). Four
Chinese-question smoke queries returned existing candidates. The whole-library
cache is not uploaded or committed.

## Concurrent-work checkpoint boundary

Only standalone tool, test, skill, retrieval-hint and this maintenance-record
changes belong in this task's technical checkpoint. Identity ledgers, registry,
runtime/maintenance metadata and the literature README remain local working-tree
changes: the current seven-item snapshot also depends on another task's uncommitted
Chapter 2 evaluation packet. They must not be described as backed up by the
technical checkpoint or swept together with unrelated research decisions.
