# Scientific Harness Study

> study: scientific-harness
> work_status: active
> basis: source
> evidence_status: candidate

本模块研究面向 Agent 长流程科研的基础设施。它位于 idea 与稳定 reference
之间，不是学位论文的第四项研究内容，也不证明任何 object-level Agent 方法有效。

## Read first

默认读取顺序：

```text
README.md
→ 当前目标 study 文件
→ sources.csv 中被引用的 source_id 行
```

不要为了处理单个问题加载全部研究文件。来源标题、URL、版本和核验任务以
[`sources.csv`](sources.csv) 为准，其他文件只引用 `source_id`。

## Study index

| Study | File | work_status | Human action |
| --- | --- | --- | --- |
| Landscape | [`01-landscape.md`](01-landscape.md) | done | 无 |
| Lifecycle | [`02-lifecycle.md`](02-lifecycle.md) | review | 批阅状态模型与边界 |
| Risks | [`03-risks.md`](03-risks.md) | done | 无 |
| Local Fit | [`04-local-fit.md`](04-local-fit.md) | review | 批阅本地缺口与优先级 |
| Prototype | — | blocked | 需要单独授权 |

## Frozen v0.1 plan

本版本固定的是调研计划和初步结论，不是 prototype 设计或论文贡献。

1. **Landscape** 已完成首轮七系统比较；后续只补代码级和版本级核验。
2. **Lifecycle** 等待一次人工批阅，确认双轴状态模型及其不应覆盖的边界。
3. **Risks** 已完成首轮 taxonomy；后续将每类风险映射到本地已有检查或明确缺口。
4. **Local Fit** 等待一次人工批阅，确认五个 repo 的职责、接口优先级和不做事项。
5. 两次批阅完成后，才形成一个最小 prototype proposal；实施仍须单独授权。

不因新论文、模型或工具出现而重开全部调研。新材料先进入 `sources.csv`，只回到
它实际影响的单个 study；影响 thesis framing 或 stable skill 时另起 proposal。

## Model routing

本模块复用 Chapter 2 L0--L9 的“低成本广筛 → 结构化核验 → 高影响综合 → 人类决定”
经验，但不把该 claim-audit loop 当作通用科研生命周期。

| Work | Default executor | Permission boundary |
| --- | --- | --- |
| URL/版本对齐、去重、hash、schema、链接和 source ID 检查 | deterministic tools | 不消耗 LLM token；结果可直接作为过程记录 |
| 查询扩展、摘要/章节筛选、候选表、首轮结构化提取、缺失字段和拒绝理由草稿 | cheap model | 只能写 `candidate` 材料，不决定新颖性、证据状态或 canonical patch |
| 原文 locator 审计、support/limitation/contradiction 判定、direct-comparator matrix、cheap-model 分歧复核 | verifier model | 只能生成 evidence packet 和升级建议，不执行 claim promotion |
| 冻结问题与预算、最强竞争者比较、claim court、跨来源冲突收束、批阅包、已批准变更的复核 | Sol | 只接收小型、已核验的 evidence packet；不代替 human decision |
| claim 接受/收窄/拒绝、研究方向、资源升级、对外发布 | human | 唯一可改变 thesis-use 或 stable-reference 状态的责任方 |

对本 study 而言，优先把便宜模型用在 Landscape 的增量筛选、来源元数据整理、
Open checks 队列和表格规范化；把 Sol 留给 Lifecycle/Local Fit 的批阅前综合、
风险优先级冲突和任何可能改变论文边界的提案。若一项任务可由确定性检查完成，
不调用任何模型。

## Reusable operating lessons

- 把“生成候选”“验证来源”“评价执行”“接受 claim”拆成不同权限，不要让同一
  agent 定义成功并独自判定成功。
- 共享短入口、稳定 `source_id` 和固定章节，比让每个 agent 重新阅读整份调研
  更利于缓存复用，也更容易审计。
- 失败、invalid、null、retry、pruned 和 superseded 是可复用经验；它们必须有
  原因和 lineage，而不是从摘要中消失。
- 最值得优先实现的不是更复杂的自治，而是一条可重放的
  `claim → evidence/run → artifact → review decision` 链。
- meta-level harness 的可用性只能改善研究过程；它不能作为 object-level 方法
  有效性的实验结果。

## Current synthesis

### Supported findings

- `source`：执行型科研系统与评测型 benchmark 提供的是互补机制，不能把
  rubric 流程直接解释为科研生命周期。
- `source`：当前最可迁移的机制包括显式分支与预算、执行/评测环境分离、
  stepwise verification、judge calibration、可重放制品和具名人工决策。
- `source`：自动 judge、best-node score 或多轨迹 consensus 都不能单独完成
  scientific claim promotion。

### Design proposals

- `proposal`：科研对象状态使用 `phase` 与 `status` 两个正交字段；Run 另有
  独立终态，避免把“运行成功”与“科学结论接受”混为一谈。
- `proposal`：最小可信链为
  `research environment → immutable artifacts → independent evaluation → claim review`。
- `proposal`：跨仓同步首先采用稳定 ID、manifest 和 evidence pointer，不把
  总控、执行层和代码仓合并成一个强耦合产品。

### Open questions

- 新近 2026 preprint 的环境隔离、trace schema 和 judge calibration 仍需代码级审计。
- 当前本地仓库尚无统一的跨仓 claim、run、artifact 和 gate interface。
- human review 的实际负担、纠错率和职责分离尚未经过本地 pilot 测量。

## Prototype admission

只有以下条件同时满足，才可创建 `05-prototype.md` 或实现 trace/gate prototype：

1. Lifecycle 与 Local Fit 完成人工批阅；
2. prototype 问题、预算和成功标准通过 `scope review`；
3. 不阻塞论文三项研究的当前最低闭环；
4. 不修改受保护 rubric、raw results、论文 claim 或稳定 skill 规范；
5. 获得单独实现授权。

## Vocabulary

- `basis`: `source | inference | proposal`
- `evidence_status`: `candidate | needs-review | verified | rejected`
- `work_status`: `queued | active | review | done | blocked`
- 风险等级：`blocker | high | medium | low`
- 人工审查：`scope review | protocol review | claim review | release review`
