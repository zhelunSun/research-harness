# Proposal：接受第一章 v0.5.3 工程/live 集成收口并接入开题材料入口

> 状态：pending human decision  
> 来源仓库：`D:/projects/phd-thesis/URSA`  
> 不改变：总题目、三项研究角色、`idea-v2026.08.02`、Chapter 2 P0 / Chapter 1 P1 优先级

## Trigger

总控仓当前仍保留 2026-08-11 快照，其中第一章被描述为“D2 最小实现待完成、真实模型证据尚未
形成”。URSA 已在不修改冻结 v1 panel/gold 的前提下完成 v0.5.3：统一 `run()/resume()` runtime、
真实 Scientist 结构化计划、plan-bound action、真实工具 observation、Scientist revision、
planned/observed graph、运行内 checkpoint、原始需求交付义务、诚实终态和独立 v2 evaluator。

该变化是证据状态更新，不是新 Idea。按照总库治理规则，先提交本提案；未经人工接受，不直接
修改 `IDEA_VERSION.md`、`THESIS_STATE.md`、当前执行计划或开题证据矩阵。

## Proposed thesis-wide update

如获接受，建议同步：

1. `process/current_execution_plan_20260802.md`
   - M1 状态改为“v0.5.3 工程与小规模 live 集成收口；正式机制效果 open”；
   - 删除“当前唯一下一动作仍为 D2-A”的过期快照；
   - 第一章下一动作改为章节写作、图表和人工 claim review，不继续平台扩建。
2. `evidence/opening_evidence_matrix.md`
   - 将 schema、validator、定向停止/修订、trace/graph、交付闭合更新为 `VERIFIED-ASSET`；
   - 新增 v2 5×3 为 `DIAGNOSTIC / live integration evidence`；
   - 正式 baseline/ablation、科学准确性、用户效用继续为 `OPEN`。
3. `THESIS_STATE.md`
   - 只更新第一章证据指针与完成度说明；不改变章节问题、贡献边界或 Idea 版本。
4. `thesis/README.md`
   - 保留现有第一章最短访问路径；导航本身不晋级证据。

## Evidence proposed for acceptance

| 对象 | 指针 | 可支持 | 不支持 |
| --- | --- | --- | --- |
| 最终代码基线 | URSA commit `0efd090` | v0.5.3 runtime/evaluator 的可重建代码 | 当前材料工作树已提交或公开发布 |
| 验收与复现 | `URSA/docs/thesis/ch1_evidence_system/v053_evidence_index.md` | commit、run、checksum、命令和边界 | 科学精度或外部有效性 |
| 最终结果表 | `URSA/docs/thesis/ch1_evidence_system/v053_results_table.md` | 121/121；15/15 closure；5/7/3 终态；token/wall time | 成功率、规划提升、统计优越性 |
| claim 审核 | `URSA/docs/thesis/ch1_evidence_system/claim_registry.md` | 当前允许/禁止表述 | 未登记的新 claim |
| 方法与系统图 | `URSA/docs/thesis/ch1_evidence_system/module_continuity_map.md` | 三张稳定系统图的语义主源 | 图本身证明机制效果 |
| 写作与陈述 | `URSA/docs/thesis/ch1_evidence_system/ch1_v053_draft.md`、`narrative_cards.md` | 开题/论文/面试材料骨架 | 自动改变总论文 Idea |

## Proposed accepted wording

> 第一章已在冻结小面板中完成从对话式原型到统一领域运行时的工程与真实模型集成闭环：计划、
> 动作、反馈、过程证据和交付终态可以被独立检查。该证据支持系统机制在当前范围内可运行，
> 不支持规划优越性、checkpoint 独立效应、遥感专题精度或跨任务泛化。

## Claims that must remain prohibited

- “第一章已经完成正式效果实验”；
- “多智能体或自适应规划普遍优于基线”；
- “15/15 是任务成功率或科学准确率”；
- “task-11 生成了更优规划路径”；
- “绿地比例是东城区行政区绿地覆盖率”；
- “系统具备进程沙箱、durable recovery 或生产级通用 Harness”。

## Human decision needed

1. 是否接受 M1 状态为“工程与小规模 live 集成收口；正式效果 open”；
2. 是否允许把 v2 5×3 作为开题的 `DIAGNOSTIC / live integration evidence`；
3. 是否接受“工作流可靠性＝需求保持性、执行有效性、反馈适应性、结果可核验性”的第一章操作化；
4. 是否保持第一章停止平台扩建，下一阶段以写作、图表和人工审核为主；
5. 接受后是否由总库同步更新 execution plan、evidence matrix 和 THESIS_STATE 的证据指针。

## Cloud checkpoint

URSA 文档与可复现图件源已提交到分支
`codex/ch1-v2-e1-structured-planning`，当前材料 checkpoint 为 commit
`4a881a2`；冻结工程 closeout 由 tag `ch1-v053-closeout-20260819`
指向 `9e18532`，原始 notebook prototype 由 tag
`prototype-notebook-v0-20250307` 指向 `19db55b`。上述分支与两个 tag
均已推送到 `origin`。`build/` 与职业材料 sidecar 不属于本证据包。
