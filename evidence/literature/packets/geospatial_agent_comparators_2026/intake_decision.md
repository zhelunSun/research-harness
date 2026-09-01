# Zotero intake decision: geospatial agent comparators

> Scan date: 2026-09-01  
> Zotero status: local API enabled and running; connector running  
> Current selected target: `AI_for_Science`  
> Recommended target before import: existing `AI_for_Science/scientific agent` collection

## Deduplication result

| Source | Search identifiers | Zotero result |
| --- | --- | --- |
| An LLM-based multi-agent system for remote sensing analysis | DOI `10.1080/20964471.2025.2600178`; exact title; `ExpertsRS` | no matching parent item |
| Spatial-Agent: Agentic Geo-spatial Reasoning with Scientific Core Concepts | arXiv `2601.16965`; exact title | no matching parent item |
| GeoAgentBench: A Dynamic Execution Benchmark for Tool-Augmented Agents in Spatial Analysis | arXiv `2604.13888`; exact title | no matching parent item |
| GeoDisaster: Benchmarking Orchestrated Agents for Operational Disaster Geo-Intelligence | arXiv `2606.17246`; exact title | no matching parent item |

The absence of a search hit is sufficient to prepare intake, but it is not authorization to write.

## Recommended write

After explicit researcher authorization:

1. Select the existing `AI_for_Science/scientific agent` collection in Zotero.
2. Run `selected-target --json` again and confirm that exact destination.
3. Re-run DOI/exact-title deduplication immediately before import.
4. Import `references.bib`.
5. Attach the official open-access publisher PDF for ExpertsRS and official arXiv PDFs for the three preprints as linked files under the SeaDrive attachment base.
6. Add common tags: `PhD Thesis`, `Remote Sensing Agents`, `Geospatial Agents`, `Agent Evaluation`, `2026 Frontier`.
7. Add source-specific tags:
   - ExpertsRS: `ExpertsRS`, `Multi-Agent Systems`, `User-Centric Remote Sensing`
   - Spatial-Agent: `GeoFlow Graph`, `Scientific Core Concepts`, `Workflow Constraints`
   - GeoAgentBench: `Dynamic Execution`, `GIS Benchmark`, `VLM Grader`
   - GeoDisaster: `Disaster Geo-Intelligence`, `Execution Contracts`, `Deterministic Checks`
8. Export each new Zotero item and replace the provisional citation keys and `null` Zotero keys in this packet.
9. Re-run the ledger audit and only then reconsider the writing bridge.

## Official attachment sources

- ExpertsRS publisher page: https://www.tandfonline.com/doi/full/10.1080/20964471.2025.2600178
- Spatial-Agent PDF: https://arxiv.org/pdf/2601.16965
- GeoAgentBench PDF: https://arxiv.org/pdf/2604.13888
- GeoDisaster PDF: https://arxiv.org/pdf/2606.17246

## Decision gate

No Zotero import or attachment write has been made. Required researcher decision:

> Authorize importing these four records into the currently selected target, or first select `AI_for_Science/scientific agent` and authorize that destination.
