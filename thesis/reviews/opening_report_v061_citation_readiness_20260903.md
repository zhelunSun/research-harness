# 开题报告 v0.6.1 引文准入只读审计

> 日期：2026-09-03  
> 对象：`thesis/opening_report_draft_zh.md` v0.6.1  
> 范围：把当前稿中 `[REF-MISSING]` 槽位映射到既有 evidence packet、claim ID、读取状态、蕴含状态和仍需人工接受的动作。  
> 边界：本报告不插入引用、不删除标记、不合并 writing contract、不写 Zotero、不新增文献、不提升 claim 或 evidence status。

## 1. 总结论

当前稿共有 9 次字符串级 `[REF-MISSING]`：

1. 第 6 行是文件说明中的 drafting marker 定义，不是正文证据槽，不应进入 citation insertion；
2. 其余 8 处是正文证据槽，均可映射到已有审计过的 evidence packets；
3. 8 个正文槽位目前都不建议直接移除标记。主要原因不是没有来源，而是每个槽位都混合了至少一个已经全文验证的窄义事实和一个仍属 `needs_review` 的跨来源综合或领域迁移判断；
4. 因此，当前最稳妥的策略是：先保留全部正文 `[REF-MISSING]`，在下一轮 separate writer pass 中把可直接引用的窄义事实拆出来，再由研究者接受 task-specific writing contract 后插入 BibTeX key。

七个 evidence packet 的 ledger 审计均为 `0 errors / 0 warnings`；当前 opening report 的 writing contract 审计也为 `0 errors / 0 warnings`。本轮曾发现 1 个 `intake_marker_count_drift`：v0.6 intake 记录 8 次字符串级标记，而 v0.6.1 现在有 9 次。该 drift 的实际含义是：文件头部 marker 定义也被字符串计数捕获，且 v0.6.1 新增了 `2.1 城市森林遥感任务与方法基础` 的正文证据槽。它是 bookkeeping 问题，不是正文内容 P1；同轮后续 bookkeeping pass 已把 intake 更新为 9 次字符串级标记、8 个正文证据槽、0 个当前可移除槽位。

## 2. 准入矩阵

| 位置 | 槽位角色 | 邻接论断 | 候选证据 | 当前状态 | 准入判断 |
| --- | --- | --- | --- | --- | --- |
| line 6 | drafting infrastructure | 说明 `[REF-MISSING]` 的含义 | 无需来源 | 非正文证据槽 | `n/a`；不应插引用，不应作为内容缺口 |
| line 90 / 1.1 | 城市森林任务复杂性与数据约束 | 城市森林分析受定义、数据版本、分类体系、验证方式、多源多时相和跨尺度数据共同约束；当前年份高质量标注不足 | `urban_forest_remote_sensing_context_2026`: `UFR-C1`, `UFR-C2`, `UFR-C3`, `UFR-C5`; project evidence for current-year label limitation | `UFR-C1`--`UFR-C3` 为 full-text verified；`UFR-C5` 为 needs_review 综合；当前年份样本不足更接近 Ch3 项目证据而非通用文献 claim | `needs-task-review`；可拆出多源/尺度/用途条件引用，保留对任务链综合和样本限制的边界 |
| line 101 / 1.2 | 智能体路径背景 | LLM 能理解自然语言需求、生成计划、调用外部工具，为领域用户参与复杂遥感分析提供路径 | `geospatial_agent_comparators_2026`: `GAC-C1`, `GAC-C4`, `GAC-C5`; 可补充 `scientific_agent_workflow_boundaries_2026`: `SAW-C4` | 对遥感/地理 Agent 实例与工具调用能力有 verified claim；“为领域用户提供新路径”仍是写作综合 | `needs-task-review`；可引用实例，不能据此声称用户效用或普遍可用性 |
| line 113 / 1.3 | 现有遥感研究智能体不足 | 现有研究展示可行性，但在城市森林任务中的计划调整、科学知识使用、失败恢复和系统级验证方面证据不足 | `geospatial_agent_comparators_2026`: `GAC-C1`, `GAC-C4`, `GAC-C5`, `GAC-C6`; `scientific_agent_workflow_boundaries_2026`: `SAW-C5` | 能力事实有 verified claims；不足判断主要依赖 `GAC-C6` 和 `SAW-C5` 的 needs_review synthesis | `needs-task-review`；不能把 comparator synthesis 写成已验证 novelty，应保留标记或改写为“现有证据尚不足以直接支持……” |
| line 128 / 2.1 | 城市森林遥感方法基础 | 不同城市森林任务对数据、尺度、方法、验证和用途要求不同，上游定义与数据选择限定下游产品可比性和适用范围 | `urban_forest_remote_sensing_context_2026`: `UFR-C1`, `UFR-C2`, `UFR-C3`, `UFR-C4`, `UFR-C5` | `UFR-C1`--`UFR-C4` 均 full-text verified；`UFR-C5` 为 needs_review 综合 | `needs-task-review`；这是 v0.6.1 新增的正文证据槽，已补入 opening v0.6 intake 的当前登记 |
| line 137 / 2.2 | 科学 Agent 相关工作 | 科学 Agent 支持规划、工具、反馈和多智能体协作，但一次性规划、隐式状态和结果自评存在限制 | `scientific_agent_workflow_boundaries_2026`: `SAW-C1`, `SAW-C2`, `SAW-C3`, `SAW-C4`, `SAW-C5`; 可作背景参考 `ai4science_frontier_2026`: `AFS-C1`--`AFS-C4`, `AFS-C8` | 系统事实和局限事实有 verified claims；“共同表明”的一般化限制属于 `SAW-C5` needs_review | `needs-task-review`；可用 verified claims 支撑代表性系统与局限，不能说这些局限普遍成立 |
| line 143 / 2.3 | 遥感/地理空间 Agent 相关工作 | 现有工作验证工具使用和任务完成，但对动态工作流、科学充分性和复杂开放场景系统评价覆盖不足 | `geospatial_agent_comparators_2026`: `GAC-C1`--`GAC-C6` | `GAC-C1`--`GAC-C5` verified；`GAC-C6` needs_review | `needs-task-review`；可引用任务/工具/评价事实，保留关于科学充分性和复杂场景评价缺口的标记 |
| line 148 / 2.4 | 知识表示、检索与推理 | 来源、适用条件、证据状态、冲突和结论边界如何进入科学推理 | `knowledge_evidence_governance_2026`: `KEG-C1`--`KEG-C5`; `ch2_knowledge_action_interfaces_2026`: `KAI-C1`--`KAI-C5` | `KEG-C1`--`KEG-C4` 与 `KAI-C1`--`KAI-C4` verified；`KEG-C5` 与 `KAI-C5` needs_review | `needs-task-review`；可支撑表示原语和行动机制实例，不能直接证明 Ch2 方法效果 |
| line 158 / 2.5 | 系统评测与用户验证 | 静态题库、短任务、最终答案评分和单次演示难以覆盖依赖、环境变化和完整系统能力边界；人工/用户校准是补充 | `agent_evaluation_user_validity_2026`: `AEV-C1`--`AEV-C5` | `AEV-C1`--`AEV-C4` verified；`AEV-C5` needs_review | `needs-task-review`；可引用过程评价、状态依赖、重复可靠性和真实用户评价实例，不能直接推出城市森林领域评价构念已成立 |

## 3. 可准入与不可准入边界

### 可在下一轮拆句后候选准入

- 城市森林遥感的多源、多尺度、用途条件、方法选择与局限：`UFR-C1`--`UFR-C4`。
- 遥感/地理空间 Agent 的代表性能力与评价对象：`GAC-C1`--`GAC-C5`。
- 科学 Agent 的阶段化流程、工具反馈、人工反馈和自评局限实例：`SAW-C1`--`SAW-C4`。
- 知识治理与知识行动接口的来源、限定词、证据状态、动作约束、工具约束和经验复用实例：`KEG-C1`--`KEG-C4`, `KAI-C1`--`KAI-C4`。
- Agent 评价中的过程进展、状态依赖、重复可靠性和真实用户评分实例：`AEV-C1`--`AEV-C4`。

这些项目的前提是：使用各 packet 的 BibTeX key，不使用 Zotero item key；插入前由研究者接受 task-specific writing contract；句子表达需收窄到 claim 本身。

### 仍不可直接准入

- `UFR-C5`, `GAC-C6`, `SAW-C5`, `KEG-C5`, `KAI-C5`, `AEV-C5`, `AFS-C8` 这类跨来源综合仍是 `needs_review`，不能作为已验证 thesis claim。
- 不能把 metadata、Zotero 命中、abstract 或 packet 存在本身当作支持。当前涉及的候选来源大多已有 full-text verified claim，但 synthesis claim 的蕴含关系仍没有逐段评估。
- 不能把“城市级”“多步”“真实任务”单独写成创新；只能把跨任务依赖、故障传播、可观察试验记录和分层评价作为待证明的候选贡献。
- 不能把 Route B 只读离线治理链描述成 GEE 专业流程已经迁移为本地算法；它是首个评测任务，不是 Ch3 全部任务族。

## 4. 对当前审阅版本的影响

对研究者现在的低带宽审阅，建议先看：

1. `thesis/advisor_discussion_packet_20260907_v0.1.md` 的一句话主线、三章最低闭环和五个导师问题；
2. `thesis/opening_report_draft_zh.md` 的 0、1、2.6、3、4 节；
3. 本报告的第 1 节和第 2 节中 `needs-task-review` 的位置。

不建议研究者现在逐篇检查全部候选文献；当前更重要的是确认三章逻辑和导师讨论问题是否符合自己的真实想法。

## 5. 最小下一动作

1. 先保留正文全部 8 个内容 `[REF-MISSING]`，不在本轮移除；
2. Bookkeeping pass 已完成：opening v0.6 intake 现在记录 v0.6.1 的 9 次字符串级标记、8 个正文证据槽，并登记 line 128 的城市森林方法基础槽位；
3. 若研究者认可当前主线，再做 citation insertion pass：只给已经 verified 的窄义 claim 插入 BibTeX key；跨来源 synthesis 继续保留缺引或改写为待验证判断。

## 6. 需要研究者判断的问题

1. 是否接受默认策略：导师讨论前保留全部正文 `[REF-MISSING]`，只把引用准入准备好，不追求形式上的“满引文”？
2. 是否接受把第 2.1 节“城市森林遥感任务与方法基础”作为国内外研究动态的第一小节，并将其作为后续 Agent 相关工作的专业问题入口？
3. 是否允许下一轮只做拆句级 citation insertion，而不再扩写正文？

默认建议均为“是”。这样能最大限度保持当前版本轻、稳、可解释。
