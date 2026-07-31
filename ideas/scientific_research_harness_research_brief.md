# Scientific Research Harness 中长期调研 Brief

> 建立日期：2026-07-30
> 状态：active study / first-pass research
> 优先级：中长期；不阻塞开题和三项研究的毕业基本盘

实际调研材料维护在
[`../studies/scientific-harness/`](../studies/scientific-harness/)。
本文件只保留立项动机、研究边界和停止条件。

## 1. 调研问题

> 面向 Agent 参与文献发现、科学问题形成、实验设计、代码执行、结果解释和论文
> 写作的长流程，怎样设计一个既能提高自主执行比例、又不让未经核验的 claim、
> 评分器漏洞和错误实验进入正式研究结论的 Scientific Research Harness？

本课题首先研究科研执行基础设施，不自动构成学位论文的第四项贡献。

## 2. 为什么值得单独调研

当前 `research-harness` 已经出现若干真实问题：

- Agent 能快速产生 idea，但科学 claim 的否决、收窄和晋级更昂贵；
- 文献摘要、源文定位、实验结果和人类判断具有不同证据等级；
- 长时间 Agent 运行容易把候选结论写成已验证事实；
- 研究代码、实验环境、评分器和论文叙事可能在不同仓库漂移；
- 同一个 Agent 同时生成结果和评价结果，存在循环验证；
- 负结果、失败分支和被拒绝的 idea 容易丢失，导致重复探索。

这些问题同时与个人的 Harness Engineering、Agent Evaluation、Memory/Tool
Learning 和 Agent Self-evolution 职业方向相关。

## 3. 初始参照系

| 系统/评测 | 主要启发 | 对本地 Harness 的问题 | Sources |
| --- | --- | --- | --- |
| AI Scientist-v2 | 假设—实验—分析—写作的端到端 Agentic tree search | 开放探索如何设置预算、分支淘汰、失败归因和人工责任 | SH-SRC-001, SH-SRC-002 |
| FutureHouse / Robin | 以专业 Agent 分工覆盖文献、推理和实验环节 | 专业工具、领域数据库和人类科学家如何形成稳定接口 | SH-SRC-003, SH-SRC-004 |
| PaperBench | 由论文作者参与构建分层 rubric，并单独校准自动 judge | 如何避免 Agent 自己定义成功和自己判分 | SH-SRC-007, SH-SRC-008 |
| ScienceAgentBench | 真实论文任务、专家验证、代码/结果/成本分离 | 如何先评价科学工作流的局部任务，而不是直接宣称端到端自主科研 | SH-SRC-010 |
| SciAgentArena | stepwise verification 和交互式、agent-agnostic 环境 | 如何评价长流程、异构科学任务和中间状态 | SH-SRC-012 |
| ResearchClawBench | 隐藏目标论文、专家多模态 rubric、实验/证据 mismatch 分析 | 如何评价 rediscovery，同时保留发现新结果的空间 | SH-SRC-015 |
| AutoResearchBench | Deep/Wide literature discovery 与开放结果集合 | 文献检索如何处理未知答案数、召回率和概念理解 | SH-SRC-018 |

来源标题、URL、版本和核验任务统一维护在
[`../studies/scientific-harness/sources.csv`](../studies/scientific-harness/sources.csv)。

## 4. 暂定研究轴线

1. **Research state**：问题、假设、证据、实验、结果和论断的显式状态机；
2. **Evidence provenance**：原始来源、定位、实验制品和 claim 之间可回溯；
3. **Environment isolation**：研究 Agent、执行环境与 evaluator 分离；
4. **Evaluation validity**：隐藏 gold、确定性检查、模型评分和人类评分分层；
5. **Branch governance**：idea 分支、失败、负结果、预算和停止规则；
6. **Human gates**：人类只在问题价值、科学正确性、风险和结论晋级处介入；
7. **Experience reuse**：历史轨迹可用于检索、错误分类和后续学习，但不能自动
   晋级为科学证据；
8. **Repository synchronization**：总控、执行层与代码仓保持弱耦合和版本化接口。

## 5. 与论文的两层关系

### Meta-level research harness

`research-harness` 管理论文 idea、claim、evidence、decision 和跨仓过程。它是科研
基础设施，不作为第一、二、三项研究的结果证据。

### Object-level agent harness

URSA/第三项研究中的 runtime、trace、repair、checkpoint、evaluation 和 experience
属于被研究的 Agent 系统，可形成论文方法或评测对象。

两层可以共享工程经验，但不得使用“meta harness 能工作”证明“论文方法有效”。

## 6. 调研序列

| Study | 内容 | 产出 | 人工参与 |
| --- | --- | --- | --- |
| Landscape | 术语、系统和 benchmark 边界调查 | [`01-landscape.md`](../studies/scientific-harness/01-landscape.md) | 无 |
| Lifecycle | 科研生命周期与状态比较 | [`02-lifecycle.md`](../studies/scientific-harness/02-lifecycle.md) | 批阅一次 |
| Risks | 评分器、证据和自主运行失效审计 | [`03-risks.md`](../studies/scientific-harness/03-risks.md) | 无 |
| Local Fit | 映射本地三层职责与 L0--L9 claim-audit loop | [`04-local-fit.md`](../studies/scientific-harness/04-local-fit.md) | 批阅一次 |
| Prototype | 最小可观测 Research Harness 原型 | trace + gate prototype | 另行授权 |

## 7. 当前停止边界

- 不在开题前重写整个 `research-harness`；
- 不把“全自动科研”作为论文 promise；
- 不为追求长时间自主运行取消来源核验和人类 claim 晋级；
- 不让该调研阻塞 Chapter 1 新机制 pilot、Chapter 2 contract 和 Chapter 3
  evaluation MVP。
