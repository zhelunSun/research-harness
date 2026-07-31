# Lifecycle

> study: lifecycle
> work_status: review
> basis: source
> evidence_status: candidate

## Question

怎样把问题、假设、证据、实验、结果、claim 和决定表示为可审计生命周期，同时
避免把 benchmark 评分流程误当成科研状态机？

## Findings

### Two lifecycle classes

- `source`：AI Scientist-v2 和 Robin 属于执行型科研循环，实际推进 idea 或
  hypothesis、实验、结果、后续分析和写作。
- `inference`：PaperBench、ScienceAgentBench、SciAgentArena、
  ResearchClawBench 和 AutoResearchBench 主要提供任务包装、环境隔离、
  intermediate verification 或 final evaluation；其 rubric 层级不是 Agent 的
  科研状态。

### Common research entities

`inference`：跨系统可归纳出以下最小实体：

```text
ResearchQuestion
Hypothesis
EvidenceItem
ExperimentPlan
Run
Artifact
Result
Claim
Decision
Branch
GateReview
Actor
EnvironmentSnapshot
```

`source`：W3C PROV 的 `Entity`、`Activity`、`Agent` 以及 `used`、
`wasGeneratedBy`、`wasDerivedFrom`、`wasAttributedTo` 可作为 provenance
关系参照，但不直接规定科学 claim 的晋级语义（SH-SRC-020）。

### Candidate state model

以下全部为 `proposal`，不是文献共识。

`phase` 表示工作走到哪里：

```text
draft
→ scoped
→ evidence-ready
→ hypothesis-ready
→ experiment-ready
→ running
→ result-ready
→ claim-review
→ closed
```

`status` 表示该对象当前如何处置：

```text
active | revise | blocked | rejected
inconclusive | accepted | abandoned | superseded
```

Run 使用独立终态：

```text
succeeded | failed | invalid | cancelled
```

关键不变量：

- `scope review` 接受问题价值、范围、预算和责任人后，才能进入 `scoped`。
- `evidence-ready` 需要 source locator 和仍未知的 coverage；它不代表假设受到支持。
- `experiment-ready` 需要 baseline、falsification criterion、资源与风险说明；
  高成本或高风险工作触发 `protocol review`。
- Run 失败、无效或取消都必须保留 artifact 与原因；retry 创建新 Run 并
  `wasDerivedFrom` 旧 Run。
- Result 不能自动升级为 Claim；`claim review` 必须检查支持证据、反证、替代解释和适用边界。
- 任意阶段都可以 `blocked` 或 `abandoned`，但必须记录 actor、reason 和 timestamp。
- experience 或 memory 默认不是 scientific evidence，只能作为检索和错误分类上下文。

### Named human reviews

| Review | Decision |
| --- | --- |
| `scope review` | 问题价值、范围、预算和责任 |
| `protocol review` | 高风险/高成本协议、关键偏离和资源 |
| `claim review` | claim 接受、收窄、拒绝或保持 inconclusive |
| `release review` | 对外发布、跨仓同步和稳定规范晋级 |

## Evidence

- AI Scientist-v2 的阶段树、debug 与 checkpoint：SH-SRC-001, SH-SRC-002。
- Robin 的 lab-in-the-loop 循环与人工停止：SH-SRC-003, SH-SRC-004,
  SH-SRC-005, SH-SRC-006。
- benchmark 的隔离、stepwise verification 和局部状态：
  SH-SRC-007, SH-SRC-010, SH-SRC-012, SH-SRC-015, SH-SRC-018。
- provenance 底座：SH-SRC-020。

## Local implications

- `proposal`：不要使用一个 enum 同时表示 workflow progress、run outcome 和
  scientific disposition。
- `proposal`：每次状态迁移最少记录 `from`、`to`、actor、reason、input IDs、
  generated artifact IDs、environment/version 和 timestamp。
- `proposal`：Claim 必须连接 EvidenceItem 或 Result；Decision 必须连接 Claim
  和 GateReview。
- `inference`：Chapter 2 的 L0–L9 是一个 frozen claim 的 literature/claim
  audit loop。它可以为本状态模型提供审计经验，但不是通用科研生命周期。

## Open checks

- 人工批阅 `phase` 与 `status` 是否足够表达本地科研对象，而不引入多余复杂度。
- 判断 evidence、result 和 claim 是否需要独立 revision 号或统一 revision event。
- 检查 W3C PROV 最小映射，避免为了标准兼容引入不需要的本体复杂度。
- 用一个既有失败实验和一个被收窄 claim 做纸面回放，验证无历史覆盖和无状态跳级。
