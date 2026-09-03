# Intake decision: critical inheritance for Chapter 2

## Read-only checks completed on 2026-09-02

- Zotero Desktop 9.0.5 local API and connector were healthy.
- Current selected target: root `我的文库`, with no named collection selected.
- Stable-identifier and exact-title searches returned zero parent-item matches for:
  - arXiv `2512.15231` — CangLing-KnowFlow;
  - DOI `10.18653/v1/2025.findings-naacl.205` — KnowAgent;
  - arXiv `2602.03439` — ontology-to-tools compilation;
  - DOI `10.1609/aaai.v38i17.29936` — ExpeL.
- The records were added to the thesis literature evidence system. Zotero import was not attempted because collection placement was ambiguous; `references.bib` is a ready, exact four-record import set after a named destination is selected.

## Critical reading of the five-category proposal

The five categories are useful as an elicitation checklist but not as a formal taxonomy. They mix different analytical dimensions:

- declarative and procedural knowledge describe representational form;
- conditional knowledge is an applicability or trigger property that can qualify either form;
- negative knowledge is the polarity of a constraint and can also qualify either form;
- research taste is a preference or value judgment, not the same kind of knowledge object.

A rule such as “when ecological-zone shift is large, do not trust random splitting; require spatial validation” is simultaneously procedural, conditional, and negative. Treating the five labels as mutually exclusive ontology classes would therefore create annotation ambiguity and a new validation burden.

## Retain inside the current Chapter 2 loop

### 1. Task-conditioned knowledge-to-action projection

Retain the narrow mechanism, not a new architecture:

`knowledge item + current task state -> trigger + required action + prohibited action + verification obligation + conclusion boundary`

This is a conceptual reading of fields already present in the current Chapter 2 assets: applicability, common errors, trigger condition, constraint scope, verification basis, evidence status, and governed outputs. It does not require a new schema or a new data-collection stream.

### 2. Separate knowledge carrier from behavioural effect

Use two axes when analysing the six future scientific cases:

| Axis | Minimal values |
| --- | --- |
| knowledge carrier | claim, procedure, constraint, preference, experience |
| behavioural effect | expose, require, permit, prohibit, rank, verify, downgrade, stop/escalate |

The first axis says what the knowledge is; the second says how it changes the Agent. Provenance, scope, evidence status, confidence, and review state remain governance metadata rather than additional “experience types”.

### 3. Strengthen matched evaluation, not system breadth

For the existing matched conditions, ask whether the same task causes the Agent to supplement evidence, check applicability, reject a method, avoid an unnecessary step, downgrade a conclusion, or stop/request clarification. This sharpens action-change and scientific-appropriateness measures already required by the Chapter 2 plan.

## Narrow or rename

- Use “knowledge-to-action interface” or “task-conditioned action obligation” as analytic language.
- Keep “knowledge-to-policy compilation” only as an analogy. The current Chapter 2 representation is not a formal compiler and should not inherit that guarantee from ontology-to-tools work.
- Keep ERA's outer scientific operationalization versus inner executable search as a comparator for who defines data, objective, constraints, budget, and stopping rules; do not make it the Chapter 2 architecture.
- Treat CangLing-KnowFlow as a direct procedural-workflow competitor. Chapter 2 must not claim novelty for expert workflow templates, dynamic repair, or experience-derived repair memory.

## Defer to the idea library

- research taste via pairwise preference learning;
- automatic experience-to-knowledge updates or lifelong memory;
- a separate critic/value model for scientific quality;
- Pareto optimization across validity, cost, reproducibility, and novelty;
- a general human-escalation policy beyond the stopping/clarification actions already available.

These directions are scientifically interesting but would require new expert-label protocols, negative-update safeguards, additional baselines, and longer-term evaluation.

## Reject for the dissertation chapter

- a full Scientific Cognitive Environment as a new system contribution;
- the five labels as an exhaustive or novel ontology of scientific experience;
- a six-channel `prior/action/constraint/value/memory/escalation` implementation claim;
- “first to inject fragmented expert knowledge into a remote-sensing Agent”;
- treating execution success, reflection, or expert preference as scientific evidence.

## Lowest-risk next use

Do not interrupt G4 Batch A. After the researcher approves the current low/boundary records and the six case set begins to stabilize, add only an analysis-side `behavioural_effect` coding sheet derived from existing outputs. It should not become a required schema field unless the matched pilot shows that it improves interpretability without increasing annotation disagreement or leaking an expert answer.

