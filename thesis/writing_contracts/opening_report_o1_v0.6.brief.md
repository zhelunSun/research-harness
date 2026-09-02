# Section brief

- Document / section: `thesis/opening_report_draft_zh.md` v0.6，全稿重点为第 0、1、2.5、3、4 和 6 节。
- Writing mode: argument edit, followed by terminology and sentence-level language edit.
- Reader question answered: 为什么城市森林遥感问题需要工作流、知识表示与推理、系统评测三项研究，而不是为什么通用 Agent 还缺三个模块？
- One-sentence section job: 从城市森林研究与管理问题中的任务依赖出发，引出三个方法缺口，并保持第一、二项的遥感可迁移边界和第三项的候选状态。
- Authoritative sources: researcher feedback on 2026-09-02; `DEC-2026-0902-opening-urban-forest-problem-framing.md`; `THESIS_STATE.md`; accepted 2026-08-30/31 opening decisions; O1 v0.5 V1 review; current Ch3 static audit.
- Approved claims: 城市森林问题是共同出发点；第一、二项方法可在其他遥感任务检验可迁移性；Route B 是首个评测任务而非第三章全部路线；本地核心栖息地与 RSS 可作为后续任务族；城市级本身不是创新。
- Evidence route for each claim: human decision and canonical Idea for framing; Chapter 3 static audit for asset/task boundary; literature study only motivates later novelty review and is not writing eligible.
- Method/data/evaluation state: Ch1 formal effect open; Ch2 scientific gold and method effect open; Ch3 system effect open and first route pending researcher confirmation.
- Required limitations: no citation insertion; no `[REF-MISSING]` removal; no new experimental result; no full RSS/quick baseline collapse; no GEE-to-local migration claim.
- Canonical terms and English anchors: three accepted chapter titles; 城市森林遥感任务；复合任务；版本化环境；Route B 只读离线治理链；RSS；quick corridor baseline；scientific gold.
- Protected numbers and literals: `2,228 / 150 / 60 / 107 / 63 / 2–3`; `manual 301`; `idea-v2026.08.02`.
- Required citations: none added in this pass.
- Unresolved markers: all existing `[REF-MISSING]` and `[待确认]`; literature-study markers remain outside the draft.
- Explicit non-goals: final thesis-title freeze; novelty acceptance; Chapter 3 implementation; Zotero import; reference-marker resolution.
- Paragraph function map: 城市森林任务需求与依赖 → Agent 提供的新路径及其不足 → 三项研究不足 → 三个方法对象 → 局部验证与系统评测 → 证据与创新边界。

## Change ledger

| ID | Type: argument/language | Before | After | Evidence or authorization |
| --- | --- | --- | --- | --- |
| U1 | argument | 背景先讲 AI 与通用遥感 Agent，城市森林随后作为场景 | 先讲城市森林研究任务、制品依赖和领域用户，再引出 Agent 方法 | researcher feedback; canonical Idea Section 1 |
| U2 | argument | 第一、二项研究不足从通用遥感 Agent 出发 | 从城市森林开放需求和领域知识作用出发，同时保留其他遥感任务的可迁移验证 | researcher feedback; `DEC-2026-0902` |
| U3 | argument | Route B 与 RSS 容易被读成互斥章级路线 | Route B 明确为首个只读评测任务；核心栖息地与 RSS 是接口稳定后的候选任务族 | Ch3 static audit; researcher question |
| U4 | argument | “城市级综合案例”可能暗示规模即创新 | 候选贡献收窄到共享版本化制品、跨任务依赖、故障传播和分层评价；城市级本身不构成创新 | five-source candidate study; no novelty promotion |
| U5 | status fix | 第一章创新点缺少局部 `[待验证]`，使用效果性“增强” | 增加 `[待验证]`，改为检验是否改善 | O1 v0.5 V1 P1-01 |
| U6 | terminology | 附录使用“科学知识表示与证据约束推理” | 恢复“面向智能体的遥感科学知识表示与推理”，证据状态作为方法属性 | O1 v0.5 V1 P1-02 |
| U7 | language | “错误成功报告”语义不明 | 统一为“失败误报为成功” | O1 v0.5 V1 P2-01 |
| U8 | scope | “科学适用性”笼统交给第二、三项 | 分别写明 Ch2 的知识／证据机制责任与 Ch3 的固定任务系统结果责任 | O1 v0.5 V1 P2-02 |
| U9 | provenance | 关键词比较了 recovery-only 旧材料 | 仅在决策中记录路径和未采用状态，不作为当前论证权威 | Recovery Workspace Guard |
