# Local Fit

> study: local-fit
> work_status: review
> basis: inference
> evidence_status: candidate

## Question

总控、科研执行和可运行代码三个职责层目前怎样分布在本地五个 repo？哪些接口
已经存在，哪些缺口阻止 claim、evidence、run、artifact 和 decision 形成连续审计链？

## Findings

### Three roles across five repositories

| Repository | Primary role | Existing surfaces | Main gap |
| --- | --- | --- | --- |
| `research-harness` | thesis-wide control plane + reusable governance skill | `THESIS_STATE.md`、ideas、claims、decisions、opening evidence matrix；稳定 `SKILL.md` 与 `references/` | claim/evidence/decision 主要是文档状态；缺少统一、机器可检查的跨仓 ID 和 promotion event |
| `chapter2-urban-forest-knowledge` | Chapter 2 scientific execution layer | L0–L9 claim-audit contract；claim/evidence CSV；experiment manifest；module contracts；validators；pilot run artifacts | 机制最完整但章节专用；已有 L0–L9 pilot 尚未生成完整 L0–L9 artifact set；跨仓 interface 未冻结 |
| `URSA` | Chapter 1 object-level workflow prototype | 四状态 ExpertsRS workflow、工具集；显式 `TaskSpec`/`WorkflowGraph`/trace 的 thesis plans | 当前运行状态仍主要由 conversation 隐式承载；durable trace、checkpoint、replay 和 manifest 仍属计划 |
| `sheaf-ai` | knowledge product/code substrate | KnowledgeCard 的 evidence、source IDs、provenance、confidence；strict validator | LLM confidence 不是 evidence status；缺少 `candidate → verified/rejected` 的科学晋级权限和 claim-level review |
| `urbfo-agent-demo` | Chapter 3 execution/evaluation and mapping code | workflow state YAML、experiment manifests、freeze manifests、最小 `AgentTrace`、trace 目录和治理规则 | trace 目录仍为空；最小 trace 仅有 event/payload/time，缺 run lineage、actor、environment、cost、artifact 和 gate refs |

以上是对当前文件表面的 `inference`，不是对代码正确性或实验有效性的正式审计。

### L0–L9 boundary

Chapter 2 的 L0–L9 处理一个 frozen claim：

```text
freeze
→ discover
→ screen
→ extract
→ verify
→ compare
→ challenge
→ package
→ human decision
→ approved patch
```

它是 literature/claim audit loop，不是 object-level scientific lifecycle。Local
Fit 只复用其 bounded autonomy、artifact contract、repair limit 和 human decision
模式，不把 L0–L9 复制成所有实验的状态机。

### Gap priorities

1. `blocker`：没有统一的 claim→evidence/source 或 run/artifact→decision 链，
   跨仓结论可能引用不同 commit、data、scorer 或叙事版本。
2. `high`：URSA 与 urbfo 的 trace-native observability 仍未形成可重放的共同最小面。
3. `high`：不同 repo 的 `candidate`、`needs-review`、`verified`、`rejected`
   语义与晋级权限尚未由共享 contract 约束。
4. `high`：generator、execution environment、evaluator 与 hidden material 的
   隔离强度不一致。
5. `medium`：失败、invalid、null、retry、pruned 和 superseded 的保存方式不统一。

## Evidence

本地证据来自以下已检查表面：

- `research-harness/AGENTS.md`、`SKILL.md`、`references/`、claims、decisions 和 evidence；
- Chapter 2 的 `WORKFLOW.md`、L0–L9 specification、claim/evidence registries、
  experiment manifest 和 pilot artifacts；
- URSA 的公开 prototype、upgrade freeze 和 parallel execution plan；
- Sheaf 的 KnowledgeCard schema、generator、validator 和 product documentation；
- urbfo 的 `AGENTS.md`、workflow state、manifests、trace helper 和 research governance。

外部 provenance 参照为 SH-SRC-020。这里的 `evidence_status` 保持 `candidate`，
直到逐 repo owner 批阅和机器检查完成。

## Local implications

- `proposal`：先定义轻量跨仓 pointer contract，不建立中央大数据库。
- `proposal`：最小 pointer 至少包含 stable ID、object type、status、repo、
  git commit、artifact path/hash、parent/retry、actor、timestamp 和 gate decision。
- `proposal`：总控只保存 claim、decision 和 evidence pointer；原始 run、rubric、
  trace 和结果继续留在下游 source-of-truth repo。
- `proposal`：Sheaf 可作为检索和来源组织工具，但其 card confidence 不得直接映射
  为 scientific evidence status。
- `proposal`：优先补齐一个完整 trace 和一个 claim promotion 回放，再决定是否
  需要更复杂的 orchestrator 或 provenance graph。

## Open checks

- 人工批阅五个 repo 的角色与优先级，确认没有把产品层或 object-level 方法误写成总控职责。
- 选择一个 Chapter 2 claim 和一个 URSA/urbfo Run，执行端到端纸面 lineage 回放。
- 核对各 repo 的 dirty state、manifest completeness、validator coverage 和
  protected surfaces，但不在本 study 中修复它们。
- 明确跨仓 stable ID 的命名和版本兼容策略。
- Prototype 仍为 `blocked`；本文件不得被解释为实现授权。
