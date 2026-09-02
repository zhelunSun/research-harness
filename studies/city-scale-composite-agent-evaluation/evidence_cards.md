# Evidence cards: city-scale composite Agent evaluation

## S-CSE-001 · ThinkGeo

- Read state: official abstract; Zotero parent item `PUSEGPQQ` found.
- Direct value: structured remote-sensing tool tasks, multi-step planning, expert-verified reasoning steps, and step/final metrics.
- Boundary: the abstract does not establish whether tasks share one city state or depend on one another's products.
- Use: closest remote-sensing task benchmark; full text and released task schema must be inspected before novelty comparison.

## S-CSE-002 · ScienceAgentBench

- Read state: official abstract; no local Zotero parent match.
- Direct value: explicitly decomposes scientific workflows into individual tasks and standardizes each output as a self-contained program.
- Boundary: scientific authenticity and expert validation do not make the tasks an interdependent workflow environment.
- Use: supports the contrast between validated atomic tasks and cross-task dependency evaluation.

## S-CSE-003 · DiscoveryWorld

- Read state: official abstract; no local Zotero parent match.
- Direct value: agents perform hypothesis formation, experiment design, execution, analysis and conclusion in a simulated environment.
- Boundary: the environment is text-based and simulated rather than a real geospatial data and artifact state.
- Use: shows that end-to-end scientific cycles and process metrics already exist as benchmark ideas.

## S-CSE-004 · ClimateAgent

- Read state: official abstract plus a located TMLR Section 4 search extract; conservatively recorded as abstract-level.
- Direct value: end-to-end climate workflows span real APIs, heterogeneous data, domain analysis, visualization, error recovery and reports.
- Boundary: the current pass has not established whether tasks reuse and transform a shared persistent scientific state across tasks.
- Use: closest scientific workflow comparator and the main challenge to any proposed Ch3 novelty claim.

## S-CSE-005 · TheAgentCompany

- Read state: official abstract; no local Zotero parent match.
- Direct value: a self-contained software-company environment supports heterogeneous professional tasks across multiple applications and actors.
- Boundary: it evaluates digital work rather than scientific validity, spatial products or ecological interpretation.
- Use: demonstrates that “one rich environment, many realistic tasks” is not by itself new.

## Cross-source boundary

The five sources motivate, but do not verify, the candidate gap `CSE-C6`. Full-text and released-environment inspection must test whether
ThinkGeo or ClimateAgent already encode persistent cross-task artifacts, dependency propagation, versioned environments and outcome
lineage comparable to the proposed Beijing setting.
