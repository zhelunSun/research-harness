# 中文论文材料

本目录保存面向读者的中文论文结构材料。它是**写作入口**，不是新的论文总控面：题目、
章节角色、核心 claim 和证据状态仍以仓库根目录的当前 Idea 发布为准。

## 开始写作时的最短阅读路径

1. [`../IDEA_VERSION.md`](../IDEA_VERSION.md)：确认正在使用的正式工作版本；
2. [`../THESIS_STATE.md`](../THESIS_STATE.md)：确认总科学问题、三项研究的边界和禁止夸大的表述；
3. [`outline_zh.md`](outline_zh.md)：把当前版本翻译为中文论文结构；
4. [`opening_report_outline_zh.md`](opening_report_outline_zh.md)：接近既有 V1.1 篇幅的导师汇报大纲；
5. [`opening_report_draft_zh.md`](opening_report_draft_zh.md)：为大纲提供详细论证和证据边界的后台工作稿；
6. [`opening_three_chapter_route_matrix_zh.md`](opening_three_chapter_route_matrix_zh.md)：导师讨论前按同构字段核对三章技术路线、评价责任和边界；
7. 按所写章节进入下方对应的“章节材料包”，不要先扫描历史计划或聊天记录。

两份选题材料采用同一套“背景意义—研究动态—科学问题与研究内容—方法与技术路线—前期基础—
特色创新—后续安排”结构。`opening_report_outline_zh.md` 是汇报和人工润色入口；
`opening_report_draft_zh.md` 第 0 节是三项研究唯一的章级源定义，正文由该节向研究不足、科学
问题、目标、内容、技术路线、创新与计划传播。章节仓继续维护事实、证据和实验，不另建三份
重复的 thesis-wide 研究设计卡。
当前 `opening_report_draft_zh.md` v0.6 已完成城市森林问题牵引的 argument-edit writer pass 和 V0
确定性审计，写作合同、变更账和待闭合的 V1/V2 门见
[`writing_contracts/opening_report_o1_v0.6.brief.md`](writing_contracts/opening_report_o1_v0.6.brief.md)；
完成 v0.6 fresh-context V1 审阅前不标记为 thesis-ready。

## 当前结构与章节材料包

| 写作对象 | 当前定位 | 首选材料 | 证据与边界 |
| --- | --- | --- | --- |
| 总题目、研究问题、三项研究关系 | 当前正式工作框架 | [`outline_zh.md`](outline_zh.md)、[`../ideas/chapter_ideas.md`](../ideas/chapter_ideas.md) | [`../claims/key_claims.md`](../claims/key_claims.md)、[`../evidence/opening_evidence_matrix.md`](../evidence/opening_evidence_matrix.md) |
| 研究内容一：面向开放需求的多智能体遥感科学分析系统 | 完整系统为核心，工作流贯通为载体，动态规划、过程图和错误调节为增量 | [`../../URSA/docs/thesis/ch1_evidence_system/README.md`](../../URSA/docs/thesis/ch1_evidence_system/README.md)、[`../../URSA/docs/thesis/ch1_evidence_system/ch1_v053_draft.md`](../../URSA/docs/thesis/ch1_evidence_system/ch1_v053_draft.md) | [`../../URSA/docs/thesis/ch1_evidence_system/v053_evidence_index.md`](../../URSA/docs/thesis/ch1_evidence_system/v053_evidence_index.md)、[`../../URSA/docs/thesis/ch1_evidence_system/claim_registry.md`](../../URSA/docs/thesis/ch1_evidence_system/claim_registry.md) |
| 研究内容二：面向智能体的遥感科学知识表示与推理 | 章级主术语已统一；具体表示、运行界面和作用效果仍待最小闭环 | [`../../chapter2-urban-forest-knowledge/sync/upstream_proposals/20260829_ch2_c0_idea_and_opening_handoff.md`](../../chapter2-urban-forest-knowledge/sync/upstream_proposals/20260829_ch2_c0_idea_and_opening_handoff.md) | [`../../chapter2-urban-forest-knowledge/docs/20260829_ch2_academic_terminology_alignment_decision_v0.1.md`](../../chapter2-urban-forest-knowledge/docs/20260829_ch2_academic_terminology_alignment_decision_v0.1.md) 是方法输入；当前总控边界见 [`../decisions/DEC-2026-0831-opening-consensus-and-working-titles.md`](../decisions/DEC-2026-0831-opening-consensus-and-working-titles.md) |
| 研究内容三：面向城市森林遥感任务的智能体系统评测 | 多阶段依赖、任务链组织和分层系统评测；静态资产—评测—结论审计已完成，首轮路线待研究者确认 | [`../../urbfo-agent-demo/docs/reports/ch3_asset_eval_claim_audit_20260831.md`](../../urbfo-agent-demo/docs/reports/ch3_asset_eval_claim_audit_20260831.md) | [`../../urbfo-agent-demo/docs/plans/ch3_asset_to_eval_and_hitl_plan_20260731.md`](../../urbfo-agent-demo/docs/plans/ch3_asset_to_eval_and_hitl_plan_20260731.md)、[`../decisions/DEC-2026-0831-opening-consensus-and-working-titles.md`](../decisions/DEC-2026-0831-opening-consensus-and-working-titles.md) |

### 第一章开题材料的最短访问路径

第一章的章内导航以
[`../../URSA/docs/thesis/ch1_evidence_system/README.md`](../../URSA/docs/thesis/ch1_evidence_system/README.md)
为准。常用材料不需要扫描整个 URSA 仓库：

1. 写大论文提纲：[`ch1_v053_draft.md`](../../URSA/docs/thesis/ch1_evidence_system/ch1_v053_draft.md)；
2. 取系统三图：[`module_continuity_map.md`](../../URSA/docs/thesis/ch1_evidence_system/module_continuity_map.md)
   与 [`figures/`](../../URSA/docs/thesis/ch1_evidence_system/figures/)；
3. 准备开题/PPT/面试：[`narrative_cards.md`](../../URSA/docs/thesis/ch1_evidence_system/narrative_cards.md)；
4. 引用结果数字：[`v053_results_table.md`](../../URSA/docs/thesis/ch1_evidence_system/v053_results_table.md)；
5. 核对运行、hash 与证据边界：[`v053_evidence_index.md`](../../URSA/docs/thesis/ch1_evidence_system/v053_evidence_index.md)；
6. 审核可说/不可说：[`claim_registry.md`](../../URSA/docs/thesis/ch1_evidence_system/claim_registry.md)。

以上链接只提供访问入口。v0.5.3 的开题证据状态已由
[`DEC-2026-0829`](../decisions/DEC-2026-0829-ch1-v053-opening-evidence-admission.md) 接受；
正式机制效果仍为 open，导航和证据接收均不等于效果结论成立。

当前 `outline_zh.md` 只定义三项研究内容的工作提纲；绪论、相关研究、结论与展望等完整
学位论文章节编排，待开题写作时在不改变已接受 Idea 的前提下补全。

## 版本与历史材料规则

- 当前版本与发布关系只看 [`../IDEA_VERSION.md`](../IDEA_VERSION.md)；章节仓库的 plan、brief、
  run 和 proposal 不会自动提升为论文事实。
- 需要知道下一项执行动作时看
  [`../process/current_execution_plan_20260802.md`](../process/current_execution_plan_20260802.md)，
  不另建平行总计划。
- 历史决策从 [`../decisions/README.md`](../decisions/README.md) 进入；历史汇报在
  [`../reports/`](../reports/)；待接受跨仓建议在 [`../sync/`](../sync/)。
- 提纲节级调整若改变章节方法对象或边界，应先经 decision 与 thesis-wide 文件同步；纯表述
  整理可在保持 Idea 对齐的前提下更新本目录文件。
