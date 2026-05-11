# Repo Architecture & Governance

> Distilled from real-world AI-native research execution practice

## Three-Layer Repo Positioning

Research work naturally splits into three layers with different ownership and lifecycles:

| Layer | Role | Source of Truth | Should NOT Contain |
|-------|------|-----------------|-------------------|
| `thinking-space/` | Research direction | claims, decisions, hypotheses | raw logs, routine code |
| `execution-layer/` | Experiment execution | briefs, logs, results, drafts | claim reframing, unverified claims as facts |
| `code-workshop/` | Runnable artifacts | code, packages, reproducible tools | research governance, long prose |

**Information flow**: thinking-space defines direction → execution-layer generates evidence → code-workshop provides tools → insights flow back as proposals.

## Phase + Module Contract Dual Governance

Phase controls **time progress** (Phase 0→4). Module controls **asset quality**.

```text
Phase       controls progress over time
Module      controls asset correctness
Manifest    controls experiment facts
Validator   controls local correctness
Checkpoint  controls phase summary
```

### Seven Stable Modules

These modules appear in most research execution repos, regardless of domain:

| Module | Typical Assets | Local Checks |
|--------|---------------|-------------|
| Literature | survey, paper notes, research intake | citation status, source verification |
| Assets | schema, taxonomy, knowledge artifacts | schema compliance, ID validity, evidence status |
| Tasks | test tasks, gold checklist, rubric | task schema, coverage, checklist completeness |
| Runner | prompts, LLM client, run config | output schema, group settings, prompt version |
| Scoring | scorer, metrics, exports | metric definitions, score range, version metadata |
| Results | raw outputs, scores, manifest | run coverage, status, retry records |
| Writing | method, experiment, results drafts | claim evidence, missing refs, critical checks |

## Module CONTRACT.md Template

Every core module gets a contract with 9 fixed sections:

```markdown
# Module Contract: <Name>

## Purpose
## Inputs
## Outputs
## Canonical Files
## Allowed Changes
## Forbidden Changes
## Invariants
## Local Validator
## Downstream Consumers
```

Example invariants for the Assets module:
- Every artifact passes schema validation
- Every taxonomy ID exists in the canonical taxonomy file
- Every artifact has an evidence_registry entry
- Artifacts marked "verified" must have a source citation

## Experiment Manifest

`experiments/results/manifest.csv` is the canonical run ledger.

Key columns: run_id, wave, task_id, group, model, prompt_version, runner_version, scorer_version, schema_version, raw_output_path, score_path, status, retry_of, git_commit

**Rules**:
- Raw outputs only append, never overwrite
- Retries get new run_id + retry_of pointer
- Successful rows must have both raw_output_path and score_path
- wave/task_id/group combo must not repeat unless retry

## Local Validators

```text
scripts/validate_assets.py
scripts/validate_tasks.py
scripts/validate_runner.py
scripts/validate_scoring.py
scripts/validate_results_manifest.py
scripts/validate_repo_state.py  ← aggregator
```

Phase gate rule: `python scripts/validate_repo_state.py` must report 0 FAIL before any formal execution.

## Protected Surfaces

These require version bump + proposal, never silent change:
- **claims** — writing claims must point to evidence
- **rubric** — versioned; old scores never rescored silently
- **raw results** — append-only
- **scoring config** — metric definitions
- **schema/taxonomy** — canonical data structures

## Four Checkpoint Levels

1. **Run checkpoint** — per-run, in manifest.csv
2. **Module checkpoint** — after major module change
3. **Wave checkpoint** — after each experiment wave
4. **Phase checkpoint** — after phase gate (summarizes module checkpoints)

## Agent Onboarding

New agent reads short alignment doc, not long chat history:

```text
AGENTS.md → PLAN.md current phase → target module CONTRACT.md → target module manifest → local validator
```

Minimum file set for external AI review:
1. AGENTS.md — workspace map
2. PLAN.md — current status
3. WORKFLOW.md — execution procedure
4. config/schema.json — core data types
5. config/schema.yaml — canonical taxonomy and classification
6. experiments/briefs/*.md — experiment design
