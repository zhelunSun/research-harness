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

1. Start from a current writing gap in `acquisition_queue.json`, not from an unbounded topic search. Keep one active work item and a target packet of 3--5 primary sources.
2. Run the Zotero skill's read-only checks: `status --json`, `selected-target --json`, then DOI/exact-title searches.
3. Prepare a decision packet before any Zotero import, merge, bulk tag, attachment change, or delete. The researcher authorizes writes explicitly.
4. After an authorized import, verify the parent item, BibTeX key, child attachment, and the resolved SeaDrive file.
5. Create or update one packet for one narrow research question. Export only the cited items. Remove workstation-specific `file` fields from the committed BibTeX snapshot.
6. Preserve the evidence ladder: `metadata < abstract < full_text`; preserve the entailment ladder: `unassessed < abstract_consistent < verified`. Discovery alone never removes a `[REF-MISSING]` marker.
7. Run the audit and generate a writing bridge. Do not merge the bridge into a writing contract until that writing task accepts it.
8. Update `packet_registry.json`; add only a pointer to the current thesis evidence matrix or chapter asset that actually consumes the packet.

## Verification command

For routine thesis-workspace maintenance, run the unified read-only audit:

```powershell
python scripts/audit_thesis_workspace.py --fetch
```

It combines Git/upstream state, workspace navigation, the literature control
audit, the current path-redacted Zotero/SeaDrive snapshot, and pending human
gates. Its literature line also reports the active acquisition work item or an
explicit null pointer when the actionable queue is exhausted.
For literature-only diagnosis, run the repository-level control audit.
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

`packet_registry.json` is the packet identity surface. `maintenance_queue.json` records
read-only scan freshness, external verification gates, explicit Zotero write gates,
and task-specific writing review. `acquisition_queue.json` is the separate,
writing-gap-driven literature search queue: each content-level intake gap must have
exactly one route, only one route is active, and each source packet remains bounded to
3--5 papers.
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

The completed `AQ-OI-D6-EVALUATION` acquisition is preserved as
`packets/agent_evaluation_user_validity_2026/`. Its four-source ledger separates
process progress, mutable-state trajectory grading, repeated-run reliability, and
actual-user satisfaction. The cross-domain transfer claim remains `needs_review`;
the packet creates neither a Chapter 3 method decision nor a Zotero write approval.

The completed `AQ-OI-D5-KNOWLEDGE` acquisition is preserved as
`packets/knowledge_evidence_governance_2026/`. Its four-source ledger separates EO
workflow provenance, claim-evidence challenge graphs, epistemic/scope qualifiers,
and context-sensitive applicability plus validation state. `KEG-C5` remains
`needs_review`: the packet does not prove that combining these representation
primitives improves a remote-sensing Agent, and it creates neither a Chapter 2
method decision nor a Zotero write approval.

The completed `AQ-OI-D3-SCIENTIFIC-AGENTS` acquisition is preserved as
`packets/scientific_agent_workflow_boundaries_2026/`. Its four-source ledger keeps
capability facts separate from limitation facts across explicit tree state, staged
multi-agent collaboration, cross-round experimental observations, and real laboratory
tool execution. `SAW-C5` remains `needs_review`: the packet does not turn these
examples into a universal defect claim about one-shot planning, implicit state, or
self-evaluation, and it creates neither a thesis novelty claim nor a Zotero write
approval.

The completed `AQ-OI-D1-BACKGROUND` acquisition is preserved as
`packets/urban_forest_remote_sensing_context_2026/`. Its four-source ledger
separates multi-source/time/scale conditions, purpose-scale-resolution method
selection, a staged LiDAR--hyperspectral classification workflow, and locally
conditioned ecosystem-service interpretation. `UFR-C5` remains `needs_review`:
the packet establishes neither a universal urban-forest workflow nor an Agent,
knowledge-representation, or planning effect. The original OI-D1 claim that a
natural-language interface lowers the overall analysis barrier remains
unsupported. All actionable acquisition items are now exhausted;
`active_work_item_id` is intentionally null until a new writing gap is routed.

The researcher-requested Chapter 2 critical intake is preserved as
`packets/ch2_knowledge_action_interfaces_2026/`. Its four-source ledger separates
remote-sensing workflow templates and repair memory, generic action-transition
knowledge, ontology-compiled tool constraints, and cross-task experiential insights.
The cross-source positioning inference `KAI-C5` remains `needs_review`: the packet
supports narrowing Chapter 2 toward auditable scientific action obligations, but does
not establish a new taxonomy, a knowledge-to-policy compiler, or a thesis novelty
claim. All four records were absent from Zotero; they were added to the evidence system
rather than imported into an ambiguous root-library target.
