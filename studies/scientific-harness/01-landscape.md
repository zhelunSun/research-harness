# Landscape

> study: landscape
> work_status: done
> basis: source
> evidence_status: candidate

## Question

现有 autonomous science 系统和 scientific-agent benchmark 分别怎样组织任务、
环境、轨迹、评测、预算与人工责任？哪些机制可以安全迁移到本地 Scientific
Harness？

## Findings

### System matrix

| System | Research unit and workflow | State, isolation, and evaluation | Human role and limits | Sources |
| --- | --- | --- | --- | --- |
| AI Scientist-v2 | 从高层主题生成 idea，经 preliminary investigation、hyperparameter tuning、research agenda execution、ablation 和 writeup 形成论文 | agentic tree search 保存节点、错误、脚本、图和 checkpoint；LLM evaluator 选 best node；官方建议隔离 LLM-written code | 人选择研究主题和最终稿并承担学术责任；tree score 和 workshop acceptance 不能替代 scientific claim validation | SH-SRC-001, SH-SRC-002 |
| Robin | 疾病问题经文献、机制、assay、候选药物、湿实验、Finch 多轨迹分析和 follow-up experiment 循环 | 专业 agent 分工；Finch 使用受控 notebook 环境；八条分析轨迹形成 consensus | 人审查候选、改变不可行协议、执行物理实验并决定停止；它是 semi-autonomous、lab-in-the-loop 单案例 | SH-SRC-003, SH-SRC-004, SH-SRC-005, SH-SRC-006 |
| PaperBench | 复现论文并提交 repository 与 `reproduce.sh` | agent 环境结束后在 fresh VM 独立执行；hidden hierarchical rubric；JudgeEval 单独校准自动 judge | 原作者参与 rubric/addendum 并 sign-off；违规和部分评分需要人工复核；不是在线科研 human gate | SH-SRC-007, SH-SRC-008, SH-SRC-009 |
| ScienceAgentBench | 针对真实论文派生的局部数据科学任务生成独立 Python 程序 | 分开报告执行成功、结果、代码相似度和成本；self-debug 使用执行反馈；专家构建和复核任务 | 专家验证任务、参考程序和 rubric；它评估局部 scientific workflow，不代表完整科研生命周期 | SH-SRC-010, SH-SRC-011 |
| SciAgentArena | 跨领域异构任务在统一接口下运行 generalist 和 specialist agents | running framework 与 evaluation framework 分离；对中间步骤做 task-specific verification | 专家定义任务和指标；高风险 validity task 需要人类监督，但没有统一在线 gate | SH-SRC-012, SH-SRC-013, SH-SRC-014 |
| ResearchClawBench | 给定问题、相关文献、原始数据和环境，隐藏目标论文，要求端到端 report 与 artifacts | 以 artifact-aware final evaluation 和 RADS 为主；主要评价最终报告，不是成熟的细粒度轨迹评测 | 专家构建任务与 rubric；高于 reference 的分数只表示 discovery potential，仍需独立验证 | SH-SRC-015, SH-SRC-016, SH-SRC-017 |
| AutoResearchBench | Deep 任务查找唯一文献或 no-answer；Wide 任务查找未知数量的完整集合 | 显式状态包含 query、history、observed documents；受控检索环境；Deep accuracy 与 Wide IoU/precision/recall | 人机协同构建和审计 gold；它覆盖文献发现，不覆盖实验和 claim promotion | SH-SRC-018, SH-SRC-019 |

### Cross-system patterns

- `source`：探索系统需要显式 parent/child、预算、debug depth、停止原因和失败
  终态；AI Scientist-v2 提供了最直接的 tree-search 参照。
- `source`：执行真实性需要独立环境重放，而不是读取 agent 自报结果；
  PaperBench 和 SciAgentArena 提供了最清晰的分离模式。
- `source`：结果至少应区分 code exists、execution succeeded、result matched 和
  scientific claim approved；PaperBench 与 ScienceAgentBench 共同支持这种分层。
- `source`：长轨迹需要保存中间状态和可定位证据，不能只保留压缩 memory 或
  final report。
- `source`：human involvement 必须指明发生在问题、协议、物理实验、证据核验、
  claim 或停止决策中的哪一处，不能仅标注“human-in-the-loop”。

## Evidence

本文件只使用 `SH-SRC-001` 至 `SH-SRC-019`。来源的完整标题、版本、URL、
核验状态和下一检查见 [`sources.csv`](sources.csv)。

所有系统级陈述当前最高为 `needs-review`。特别是 2026 年 preprint，不能仅因
有开放代码或较高 benchmark score 就升级为通用设计事实。

## Local implications

- `inference`：本地最小可信路径应为
  `research environment → immutable artifact snapshot → independent evaluation → claim review`。
- `inference`：best-node、judge score、多轨迹 consensus 和人类点击批准均只能
  提供不同类型的信号，不能共享一个“成功”状态。
- `proposal`：Landscape 的模式先进入 Lifecycle、Risks 和 Local Fit，只有人工
  接受的通用部分才可提议更新稳定 `references/`。

## Open checks

- 审计 AI Scientist-v2 的节点 schema、checkpoint 恢复和阶段默认预算。
- 审计 Robin trajectory、ranking、consensus 与 wet-lab handoff 的稳定 ID。
- 审计 SciAgentArena 是否存在跨领域统一的 intermediate-state schema。
- 审计 ResearchClawBench 的环境权限、终止字段和 judge 对 artifact lineage 的使用。
- 审计 AutoResearchBench 输出是否包含 supporting spans，而不只是 paper IDs。
