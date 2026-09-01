# Intake decision: knowledge and evidence governance

## Read-only checks completed on 2026-09-01

- Zotero Desktop 9.0.5: local API enabled and healthy; connector healthy.
- Selected target at scan time: `我的文库 / AI_for_Science` (collection `19`).
- DOI and exact-title searches returned zero parent-item matches for all four retained sources:
  - `10.1109/eScience65000.2025.00016`
  - `10.1186/2041-1480-5-28`
  - `10.18653/v1/2021.emnlp-main.381`
  - `Actionable Understanding: Action Units for Bridging the Knowledge-Action Gap in Post-FAIR Knowledge Infrastructures`

## Screening decision

Retain four sources and stop. They form the smallest complementary packet found: openEO covers EO workflow provenance, Micropublications covers evidence and explicit challenge, SciClaim covers epistemic and scope qualifiers, and Action Units covers context-dependent applicability, empirical validation state, and auditability for human or machine action.

`SciGraph-LLM: Automatic Knowledge Graph Construction from Scientific Papers` was not admitted. Its publisher abstract was relevant, but the full text was not accessible through the available official route during this scan, so it could not satisfy the packet's full-text entailment rule. A fifth source is not needed to close the bounded packet.

## Future Zotero decision gate

No write is authorized by this packet. If the researcher later authorizes import, confirm the destination first; the current selected target is `AI_for_Science`, while the existing thesis-oriented candidate is `我的文库 / Phd_thesis_new / C2_knowledge / representation`. Recommended tags are `Knowledge Governance`, `Evidence Representation`, `Scientific Knowledge Graph`, `Provenance`, `Applicability`, and `Chapter 2`; add `Remote Sensing` only to the openEO record and `Biodiversity` only to the Action Units record. The import must then verify four parent item keys, four stable BibTeX keys, and four official PDFs linked through SeaDrive before registry reconciliation.
