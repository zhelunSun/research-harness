# 任务步数、复杂性与难度：有限文献决策包

2026-09-04 · 五篇原始来源 · 局部综合待复核 · 不冻结新 benchmark 分类

## 结论

**多步不必然复杂，复杂也不等于当前模型做不出来。** 已核对的文献分别使用请求标签、人工参考步骤、语义关键词、工具路径和程序长度，不能合并成一个跨领域标准。北京首轮可暂称“既有产品上的有界多步任务”；这比笼统贴上“简单任务”或“复杂科学任务”更准确。

## 原文到底如何区分

- [CLAIM:TD-C1] **ExpertsRS**：§3.2.2 明确将20条验证请求分成10条 single-step 和10条 multi-step，并固定同一 Sentinel-2 场景与研究范围；§4.3再次按这两组报告。已读设置段落未给出可复用的步数阈值。此处只确认历史标签，不补造定义。[@sun_llm-based_2026] [发表原文](https://www.tandfonline.com/doi/full/10.1080/20964471.2025.2600178)

- [CLAIM:TD-C2] **GAIA**：§3.3（PDF印刷页6–7）用人工标注者的步骤数和不同工具数作代理。Level 1通常无需工具或至多一种工具、最多5步；Level 2通常约5–10步并组合工具；Level 3允许更长行动序列和任意工具。作者明确说这不是硬约束，步骤和工具也没有唯一分法。[@mialon2023gaia] [原文](https://arxiv.org/pdf/2311.12983)

- [CLAIM:TD-C3] **ThinkGeo**：v2 §3.3的 Difficulty Annotation 按复杂关键词数与推理步骤数排序，前部标为 easy，其余为 hard。因此标签混合语义与程序性复杂性，不等于实际调用次数。该段没有交代数值切分点和同分处理，本轮未复建其分级代码。[@shabbir_thinkgeo_2026] [原文](https://arxiv.org/html/2505.23752v2#S3.SS3)

- [CLAIM:TD-C4] **GeoPlan-bench**：v1 §4.1、§8.1.2按标准工具路径的长度与复杂程度核查 Simple/Medium/Complex；已读定义段落没有可迁移的硬阈值。§8.2明确其指标评价生成计划，不依赖工具成功执行。因而规划复杂性与真实运行难度不能直接互换。[@li2025designing] [原文](https://arxiv.org/html/2511.17198v1#S4.SS1)

- [CLAIM:TD-C5] **ScienceAgentBench**：v3 §4.1以 gold 程序行数近似分析任务复杂性；§2.3的五阶段 rubric 是加载、处理、建模／可视化、格式化、保存，不是五个难度等级。其“单项科学任务”本身就包含多个阶段，不能读成单次调用。[@chen2024scienceagentbenchrigorousassessmentlanguage] [原文](https://arxiv.org/html/2410.05080v3#S2.SS3)

这里的 `full_text` 均表示**在全文中定向阅读并定位相关段落**，不是五篇逐页通读。来源与直接关系核对为 verified，只限上述原文事实；未复现论文实验。完整阅读范围和获取缺口见 [ledger.json](ledger.json)。

## ExpertsRS 历史定位与剩余缺口

原始清单：[20请求文件](../../../../URSA/ExpertsRS/evaluation/ch1/benchmark_20_original.json)。

该文件保留 ID 1–10 的单步、ID 11–20 的多步标签。单一指数制图属于前者，植被空间展示加覆盖率计算属于后者；这是原始任务清单的标签实例，不是重新制定定义。实际 canonical 路径、SHA256和仓库提交在 ledger 中记录。

发表原文 §4.3把实验设置回指到§3.1，但实际设置位于§3.2.2。附录 Table A2被正文引用，本轮未拿到其补充DOCX；也未在本次限定的 URSA 文件清单中找到论文PDF／TeX。不能以新 URSA 计划替代旧论文，更不能据这次缺口宣称论文任何位置都没有定义。若需要严格复现旧分组，应下一步只核查该附录及当时标注说明。

## 本地候选口径：先标结构，再报告难度

[CLAIM:TD-C6] 建议把“任务结构”“当前实施负担”“固定条件下的实测难度”分开记录；下列口径与北京映射均为 **needs_review**。[CRITICAL-CHECK:TD-C6] 文献只提供参照，不替我们接受这个本地方案。

| 候选结构标签 | 可操作判别 | 不自动意味着什么 |
| --- | --- | --- |
| 单项操作 | 在约定输入上完成一个主要分析目标，辅助读写不另算科学步骤 | 不等于一个API调用，也未必容易 |
| 有界多步 | 多个可检查操作围绕同一目标衔接，前一制品／判断影响后续输出 | 不因链长就成为高难度科学任务 |
| 耦合复合 | 多条分析链的结果必须按科学条件汇合或反馈，某链状态改变其他链的有效性／结论 | 不是把几项独立指标并排输出 |

“一步”暂按可命名、输入输出明确的语义操作标注。打开文件、重试、批处理切片与多次API调用另记为运行轨迹；一个大工具封装多项分析也不能抹掉语义依赖。先把输入、输出、依赖与验收写清楚，再判断是否需要更细等级，不先造加权总分。

当前实施负担只写“输入已就绪／尚缺什么、需不需要新增算法或数据、怎样验收”。实测难度必须绑定模型、工具粒度、数据、预算、环境和重复运行，之后才报告成功率、时间与典型失败。接口故障、环境缺失或当前模型失败，不能单独证明任务的内在结构更复杂。

**首轮北京案例**使用2025 strict500多类图＋BJuforebv4，交付空间图、有效像元组成和有依据的描述；不报告真实面积，不做连通性或生态功能推断。共同有效像元视图先约束统计与图面，再约束解释，暂归有界多步；相较重新制图，复用产品减少了新增数据与建模依赖，但尚无证据给它贴实测“低难度”标签。

**Wave2候选**中，土地覆被制图应拆开“复用冻结模型做分类推理”与“重新选样、训练、验证”：前者可能是有界流水线，后者新增训练与独立评价责任。连通性应拆开“给定对象和规则计算拓扑关系”与“证明物种移动或生态功能”：后者需要额外领域证据。二者都不能仅凭一次工具调用完成就称为简单；当前不启动这些候选。

## 验证与下一步

交付包括 ledger、BibTeX与[audit.json](audit.json)。候选写作接口见[writing-bridge.json](writing-bridge.json)。合同与变更记录分别见[writing-contract.json](writing-contract.json)、[section-brief.md](section-brief.md)。

确定性检查只能检出格式、身份和合同问题，不能证明科学真值、通用标准或本地分类有效性。主agent已独立完成五篇原文负载段落的 source-local V1核对；一处引文措辞已修复，见[verification.md](verification.md)。本地分类仍未获研究者接受，TD-C6保持needs_review；这不是 thesis-ready 文本。

下一步仅需以首轮实际制品与验收反查“有界多步”的标注是否清楚，并补 ExpertsRS 附录定义缺口；不扩大文献清单、不另建评分体系。当前用户已接受首轮范围，无需再审批同一方向。

从本目录运行：

```powershell
python C:/Users/zhelunStation/.codex/skills/literature-evidence-ledger/scripts/audit_ledger.py ledger.json --bib references.bib --output audit.json --bridge-out writing-bridge.json
python C:/Users/zhelunStation/.codex/skills/zh-scientific-writing/scripts/zh_scientific_audit.py audit --text README.md --contract writing-contract.json --bib references.bib --json-out writing-audit.json --md-out writing-audit.md
```

最初交付时本包仅本地新增，未提交／推送。随后研究者于 2026-09-04 授权本线程阶段提交与同步，本包一并纳入；具体同步身份以总控记录为准。该授权不接受候选难度分类或升级论文 claim。原并行任务没有修改总计划、registry、旧论文、其他仓库或 Zotero；入场同步审计四仓均 ahead=0／behind=0，导航审计 0 问题。变更说明见 section-brief 的 change ledger。
