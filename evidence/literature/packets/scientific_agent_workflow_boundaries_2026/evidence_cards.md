# Evidence cards: scientific-agent workflows and boundaries

> Packet: `scientific-agent-workflow-boundaries-2026`
>
> Full-text state: four official PDFs inspected
>
> Zotero state: absent by exact title and DOI/arXiv identifier; import not authorized
>
> Writing state: provisional keys; no contract merge

## Evidence-grade convention

- `G1`: peer-reviewed full text; the claim is limited to the reported system, task, and evaluation.
- `G2`: official primary-system preprint; the mechanism and reported limitations are locatable, while peer review and independent replication are not upgraded.

## S-SAW-001: AI Scientist-v2

### Capability fact

- Intake key: `yamada_ai-scientist-v2_2025`; evidence grade: `G2`.
- Four research stages use parallel agentic tree search. Each experimental node retains a plan, script, error trace, runtime, metrics, LLM/VLM feedback, figure paths, and buggy/non-buggy status; dedicated replication and aggregation nodes preserve repeated-run statistics.
- Decision value: this is a direct counterexample to treating automated research as one immutable plan followed by one terminal answer.

### Limitation fact

- An LLM selects or prioritizes nodes from performance metrics and plots; this is an internal search heuristic, not independent scientific approval.
- Only one of three generated manuscripts was accepted at workshop level. The authors identify genuinely novel hypotheses, innovative experimental methods, and deep domain justification as continuing difficulties.
- Official source: https://arxiv.org/abs/2504.08066

## S-SAW-002: Agent Laboratory

### Capability fact

- Intake key: `schmidgall_agent-laboratory_2025`; evidence grade: `G2`.
- PhD, Postdoc, ML/SW Engineer, Professor, and reviewer roles connect iterative literature search, collaborative plan formation, code execution, result interpretation, report generation, review, and possible return to earlier stages. Co-pilot mode exposes a human feedback point after each subtask.
- Decision value: the paper separates research roles and explicitly tests autonomous versus human-guided operation rather than merely labeling the system multi-agent.

### Limitation fact

- Automated reviewer scores overestimated human assessments, and the authors warn that LLM self-evaluation may rely on superficial patterns.
- The paper documents hallucinated experimental results, zero-accuracy runs not corrected before the step budget expired, manual removal of generated `exit()` calls, and absent repository-level management.
- Official source: https://arxiv.org/abs/2501.04227

## S-SAW-003: BioDiscoveryAgent

### Capability fact

- Intake key: `roohani_biodiscoveryagent_2025`; evidence grade: `G1` (ICLR 2025).
- Each round conditions the next gene-selection decision on the task and observations from earlier rounds. Optional tools provide PubMed search, biological-database lookup, code/data access, and an LLM critic that can revise the proposed batch.
- Decision value: it supplies a narrow, measurable example of a scientific agent revising decisions from accumulated observations rather than relying only on a static initial prompt.

### Limitation fact

- The evaluation simulates each perturbation by retrieving its outcome from past datasets; it is not prospective autonomous wet-lab execution.
- Tool effects are model- and dataset-dependent. In the reported comparisons, literature search or the full tool suite sometimes reduced hit ratio, and most benefits were concentrated in early rounds.
- Official source: https://arxiv.org/abs/2405.17631

## S-SAW-004: Coscientist

### Capability fact

- Intake key: `boiko_autonomous_2023`; evidence grade: `G1` (Nature 2023).
- A Planner selects web search, documentation search, isolated Python execution, and experiment-automation commands. In the integrated liquid-handler case, documentation feedback was used to correct an invalid heater-shaker method before successful execution.
- Decision value: this is the packet's strongest peer-reviewed example of tool-grounded planning and error correction reaching physical laboratory execution.

### Limitation fact

- The paper calls the system a semi-autonomous proof of concept. Plates were moved manually, synthesis grading included acknowledged subjectivity, and complete data, code, and prompts were withheld for safety reasons.
- The demonstrated task set therefore does not establish unrestricted end-to-end autonomy, complete reproducibility, or a general scientific-discovery evaluator.
- Official source: https://doi.org/10.1038/s41586-023-06792-0

## Decision synthesis

| Mechanism | Direct source | Source-level boundary |
| --- | --- | --- |
| explicit branching, node state, debug and replication | AI Scientist-v2 | internal LLM selection; inconsistent workshop-level outcome |
| named roles, stage feedback and revision | Agent Laboratory | self-evaluation disagreement, hallucination and runtime failures |
| cross-round observation conditioning and critic/tool calls | BioDiscoveryAgent | retrospective dataset simulation; tool gains are not monotonic |
| web/docs/code/hardware execution and correction | Coscientist | semi-autonomous proof of concept with partial manual work and restricted release |

The packet meets the four-source stop condition. `SAW-C5` remains `needs_review`: the four systems motivate explicit state, feedback, tool, and oversight dimensions, but they do not establish a universal defect of one-shot planning or implicit state and do not validate those mechanisms for the thesis's urban-forest remote-sensing workflow.
