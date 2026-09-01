# Literature evidence control plane

This directory connects the local Zotero library to thesis writing without turning Git into a second reference manager.

## Source-of-truth split

```text
Zotero metadata + item keys                 SeaDrive linked PDF files
                 \                           /
                  question-bounded evidence packet
                    - references.bib snapshot
                    - ledger.json
                    - evidence cards
                    - audit + writing bridge
                                  |
          research-harness claim/evidence pointers
                /                 |                \
             Chapter 1         Chapter 2         Chapter 3
```

- Zotero owns bibliographic identity, collection membership, tags, notes, and the link between a parent item and its attachment.
- SeaDrive owns cross-device transport of linked PDF files. PDF binaries and workstation-specific paths must not be committed to Git.
- `research-harness` owns thesis-wide evidence packets, claim boundaries, writing-contract bridges, and cross-repository routing.
- Chapter repositories consume only the source IDs or claims needed by their current method, experiment, or writing task. They do not copy the master packet.

## Maintenance states

Every source moves through the following states; no later state is implied by an earlier one:

1. `discovered`: found in search, another device, or an external alert.
2. `deduplicated`: DOI or exact title checked in Zotero.
3. `imported`: parent item, stable Zotero item key, and tags exist.
4. `full_text_ready`: the linked PDF opens locally and its source is known.
5. `evidence_carded`: a narrow research question, exact source location, read state, and evidence boundary are recorded.
6. `audited`: `ledger.json` passes the evidence-ledger audit against its packet-local BibTeX snapshot.
7. `routed`: the packet registry identifies possible chapter consumers.
8. `writing_eligible`: a task-specific writing contract explicitly accepts the relevant claim and citation key.

`imported` never means `verified`, and `routed` never means that a thesis claim has been accepted.

## Update loop

1. Run the Zotero skill's read-only checks: `status --json`, `selected-target --json`, then DOI/exact-title searches.
2. Prepare a decision packet before any Zotero import, merge, bulk tag, attachment change, or delete. The researcher authorizes writes explicitly.
3. After an authorized import, verify the parent item, BibTeX key, child attachment, and the resolved SeaDrive file.
4. Create or update one packet for one narrow research question. Export only the cited items. Remove workstation-specific `file` fields from the committed BibTeX snapshot.
5. Preserve the evidence ladder: `metadata < abstract < full_text`; preserve the entailment ladder: `unassessed < abstract_consistent < verified`.
6. Run the audit and generate a writing bridge. Do not merge the bridge into a writing contract until that writing task accepts it.
7. Update `packet_registry.json`; add only a pointer to the current thesis evidence matrix or chapter asset that actually consumes the packet.

## Verification command

For routine thesis-workspace maintenance, run the unified read-only audit:

```powershell
python scripts/audit_thesis_workspace.py --fetch
```

It combines Git/upstream state, workspace navigation, the literature control
audit, the current path-redacted Zotero/SeaDrive snapshot, and pending human
gates. For literature-only diagnosis, run the repository-level control audit.
It validates every registered packet,
the Zotero/SeaDrive source-of-truth split, identity reconciliation, forbidden local
paths/PDF binaries, the weekly scan age, every pending human gate, and the existence
of every exact cross-repository consumer route without writing to Zotero or a chapter
repository:

```powershell
python scripts/audit_literature_control.py
```

Use `--json` for a machine-readable result and `--as-of YYYY-MM-DD` for deterministic
freshness checks. Open actions are reported as `WAIT` but do not fail the audit; a
missing authorization record, stale weekly scan, broken packet, or identity mismatch
returns exit `2`.

Refresh the current-device runtime snapshot with the installed Zotero skill
helper. The command is read-only against Zotero; `--write` updates only the
path-redacted repository snapshot and scan date after every registered linked
file resolves through SeaDrive:

```powershell
python scripts/refresh_literature_runtime.py --write
```

`runtime_scan.json` never stores local PDF paths. It proves only current-device
resolution. Second-device equivalence remains a separate external gate.

For an individual evidence ledger, run the installed skill audit from
`research-harness`:

```powershell
python C:\Users\zhelunStation\.codex\skills\literature-evidence-ledger\scripts\audit_ledger.py evidence\literature\packets\ai4science_frontier_2026\ledger.json --bib evidence\literature\packets\ai4science_frontier_2026\references.bib --output evidence\literature\packets\ai4science_frontier_2026\audit.json --bridge-out evidence\literature\packets\ai4science_frontier_2026\writing_bridge.json
```

The absolute skill path is machine-specific; packet paths and the packet format are repository-stable.

## Cadence

- Event-driven: run the loop whenever a paper is imported, a thesis claim changes, or a chapter begins a new evidence review.
- Weekly read-only scan: inspect new Zotero items, missing PDFs, duplicate DOI/title candidates, and packets whose source metadata changed.
- Before writing milestones: audit only the packets routed to that writing contract; do not refresh the whole library blindly.

`packet_registry.json` is the packet identity surface. `maintenance_queue.json` is the
only literature-specific action queue; it records read-only scan freshness, external
verification gates, explicit Zotero write gates, and task-specific writing review.
`consumer_routes.json` maps packet claim IDs to exact artifacts in the repository that
owns them. A `candidate`, `reconciliation_required`, or `reconciled_candidate` route is
a pointer, not a write authorization or evidence upgrade. The last state means only
that source identity and use boundaries were repaired. None of these files upgrades a
thesis claim by itself.

`writing_intakes.json` registers task-specific, read-only reviews of packet claims
against a particular draft and writing contract. Its decision artifacts distinguish
direct candidate support, paragraph splitting, context-only use, retained evidence
gaps, and deferral. An intake marked `reviewed_candidate` is not a merged writing
contract and cannot authorize citation insertion or marker removal.
