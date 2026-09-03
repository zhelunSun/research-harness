# 当前执行计划：开题源定义收口与三章最小闭环

> 版本：v2026.09.03
> 对齐 Idea：`idea-v2026.08.02`
> 状态：active；保留原文件名作为稳定入口，不再按日期新建论文总执行计划
> 触发：固定简历与面试路径已形成；研究内容一已有最小原型；研究内容二核心机制仍待验证

## 0. Resume here：每次新会话先读这里

### 0.1 只维护两个论文级人类入口和一个机器登记

1. `THESIS_STATE.md`：慢更新，维护总科学问题、三项研究角色、贡献边界和正式风险；
2. 本文件：快更新，维护当前里程碑、下一动作、人工门禁的人类可读摘要、证据状态和会话恢复点；
3. `registry/human_gates.json`：机器可读的当前人工门禁全集，统一记录 maintenance/external、Zotero、writing、Ch2 scientific evidence 与 Ch3 scientific route 状态。

下游 `PLAN.md`、experiment brief、chapter plan 和报告仍是所属仓库的执行/证据文件，
但不再与本文件竞争“当前总计划”。职业材料只由
`huawei_harness_internship_thesis_alignment_20260802.md` 作为 sidecar 维护，不反向升级论文状态。

除非总题目、章节角色或核心 claim 发生变化，不再新建 thesis-wide roadmap、handoff 或
“最新版计划”。新会话通过本节恢复，不依赖翻找历史 chat。

### 0.2 2026-09-03 当前快照

| 里程碑 | 状态 | 已有证据 | 当前缺口 |
| --- | --- | --- | --- |
| M0 固定简历与证据边界 | completed | 固定华为 PDF、claims、面试风险口径 | 不作为论文结果升级 |
| M1 面向用户的多智能体科学分析系统 | opening evidence accepted；formal effect open | ExpertsRS 提供角色分工与基本工作流的已发表基础；URSA v0.5.3、代码基线 `0efd090`、冻结 5×3 live 集成闭环支持新增运行机制；当前电脑的 repo-local `.venv`、121 项测试、两个 no-API closeout 和 LFS 已复核，canonical tip 为 `codex/ch1-v2-e1-structured-planning@0ccc3fc` | 完整系统叙事需与增量机制分层；正式匹配效果、科学精度和跨任务泛化仍为 open |
| M2 遥感科学知识表示与推理 | core method accepted；formal effect open | Chapter 2 已形成知识／证据资产，章级主术语统一为面向智能体的遥感科学知识表示与推理；G3 已完成 150 条高召回筛选和 60 条 G4 队列；低／边界优先、来源平衡的六个十条浅审批次已形成，G4 evidence baseline 为 `l2-task-distillation@9dc0e01`，仓库验证为 41 PASS；当前远端 tip 由 checkpoint registry 判定 | 先由研究者完成批次 A 的 10 条低／边界抽查，再决定是否继续五个核心批次；scientific gold、最小表示与运行界面、知识推理闭环和分层匹配效果均未完成 |
| M3 城市森林遥感任务系统评测 | first implementation order accepted；MVP brief ready | 静态资产审计和 Route B-first 决策已落到 Ch3；`routeb_readonly_evaluation_mvp_v0.1.md` 固定 strict500 正常闭合、manual 301 角色误置、variant lineage 混淆三个只读案例，并分开 protocol closure 与 scientific validity；canonical checkpoint 为 `PandaBro666/urbfo-agent-demo:backup/ch3-routeb-20260831@c16f1ff` | 下一步只实现本地 schema、provenance 和确定性 grader smoke tests；不运行 GEE／Drive／重训／外部模型；跨任务依赖和故障传播的候选创新仍需近邻全文比较与可执行评测共同检验 |
| M4 用户／专家校准与经验驱动适应 | deferred increment | 目标用户／专家角色与 episode reservoir 已界定 | 二者均不进入第三章最低承诺；伦理／数据门禁、rubric 校准、episode 化和学习实验均未启动 |
| L0 文献证据控制面 | seven packets audited; acquisition queue exhausted | 本地 Zotero 维护书目身份，SeaDrive 承载 linked PDF；统一审计覆盖仓库、导航、文献 freshness、runtime snapshot 与人工门；七包合计 29 source / 39 claim / 61 link，8 条 exact consumer routes 与开题 writing intake 均纳入确定性审计；新增 Ch2 knowledge-action packet 分开记录工作流模板、动作转移、ontology-to-tools 约束与经验复用，跨来源定位 `KAI-C5` 仍为 `needs_review`；`acquisition_queue.json` 当前 actionable=0、`active_work_item_id=null` | 跨设备同构、五个 prepared packet 的 Zotero 授权、开题 writing acceptance 与 Ch2 G4 Batch A 浅审保持 researcher-owned；所有跨来源综合与原 OI-D1“总体门槛下降”判断仍不得因检索完成而晋级或移除缺口标记 |
| O0 选题材料 | urban-forest-first v0.6.1；V1 P1 closed；advisor packet ready | 独立 V1 后的 separate writer pass 已补齐城市森林遥感方法入口并同步 Route B-first 状态；导师讨论包 v0.1 已压缩为修改版大纲、三章最低闭环与五个问题，专用 writing contract 为 0 error / 0 warning | P2/P3、正式引文准入、图件和写作合同接受仍待后续；当前稿和讨论包可供快速检查，但不能称为引用完成或正式定稿 |

### 0.3 当前唯一下一动作

独立 fresh-context V1、两项 P1 separate writer pass、只读差异复核和导师讨论包 v0.1 均已完成。
当前唯一自动推进动作是对 v0.6.1 的 9 个 `[REF-MISSING]` 做一次 citation-readiness 审计：只把每个
槽位映射到现有 evidence packet、claim ID、read state、entailment 状态和仍缺的研究者接受动作，
不插入引用、不删除标记、不新搜无明确 writing gap 的文献。该审计与研究者快速查看
`thesis/advisor_discussion_packet_20260907_v0.1.md` 并行；研究者当前无需逐句润色。

V1 可把 `evidence/literature/packets/ai4science_frontier_2026/` 作为 AI4Science 相邻背景与比较维度的候选输入；
其 writing bridge 当前不得直接并入 O1 contract。只有任务特定审阅接受 AFS claim 与引用键后，才允许替换对应
`[REF-MISSING]`；AFS-C8 自身仍保留 `[REF-MISSING:AFS-C8]`。

`evidence/literature/packets/geospatial_agent_comparators_2026/` 已补齐 ExpertsRS、Spatial-Agent、GeoAgentBench 与
GeoDisaster 的第一轮对照证据；当前 BibTeX 键为临时 intake 身份，Zotero 去重未发现既有条目，但导入与 PDF 关联须等
研究者明确授权后执行。其 GAC-C6 仍保留 `[REF-MISSING:GAC-C6]`，不得据此提前宣称 Ch1 或 Ch3 的新颖性。

`AQ-OI-D6-EVALUATION` 已按4篇目标完成全文筛选并形成
`evidence/literature/packets/agent_evaluation_user_validity_2026/`：四个窄义 claim 可定位，跨来源领域迁移
`AEV-C5` 仍为 `needs_review`。`AQ-OI-D5-KNOWLEDGE` 也已按4篇目标形成
`evidence/literature/packets/knowledge_evidence_governance_2026/`：四个窄义 claim 分别覆盖 EO 工作流来历、
支持／挑战论证图、epistemic／scope qualifiers 与情境适用性／验证状态；跨来源的 Agent 效果转移
`KEG-C5` 仍为 `needs_review`。`AQ-OI-D3-SCIENTIFIC-AGENTS` 已按4篇目标形成
`evidence/literature/packets/scientific_agent_workflow_boundaries_2026/`：能力事实与局限事实分栏，分别覆盖
树搜索与节点状态、角色协作与人工反馈、跨轮观测、实验工具调用及原文自评／模拟／半自主边界；跨来源综合
`SAW-C5` 仍为 `needs_review`。`AQ-OI-D1-BACKGROUND` 已按4篇目标形成
`evidence/literature/packets/urban_forest_remote_sensing_context_2026/`：分别定位多源／多时相／多尺度输入、
用途—尺度—分辨率方法选择、多阶段 LiDAR--高光谱分类链，以及生态服务的地方／社会解释边界；跨来源综合
`UFR-C5` 仍为 `needs_review`，原 OI-D1 的“总体门槛下降”判断也未被这些来源修复。当前 acquisition queue
已无 actionable item，`active_work_item_id=null`。这些包均不修改 O1 正文，也不取代上述 thesis-wide 唯一下一动作；候选发现、
Zotero 入库和 writing contract 接受仍分别受 full-text、明确授权和任务特定审阅门约束。

与该动作并行只保留 Ch2 批次 A 的 10 条低／边界浅审这一低带宽科学门；它不阻塞 O1 正文与
导师讨论包。Route B 首轮实施顺序已由研究者确认并登记，后续实现仍须进入 Ch3 所属仓库。
其余外部、Zotero、写作和 Ch2 门统一登记在 `registry/human_gates.json`；自动化只能报告和校验，
不能替研究者关闭。

本动作只做写作和证据映射，不启动新实验，也不发布新 Idea。当前决定状态为：

1. 第一章以完整的面向用户多智能体科学分析系统为核心，动态规划和错误调节为增量；工程与
   小规模 live 集成证据已接受，正式效果仍为 open；
2. 第二章章级主术语统一为“面向智能体的遥感科学知识表示与推理”；证据状态是方法属性，具体
   表示、运行界面和方法效果仍待最小闭环；
3. 第三章以同一城市版本化制品上的多阶段依赖、任务链组织和系统评测为核心；Route B 已确认为
   首个评测任务，本地核心栖息地与 RSS 是后续候选任务族；城市级本身不是创新，跨任务依赖与故障
   传播的差异化仍需全文比较和可执行评测共同检验。

三项开题阶段标题、共同对象链、用户定义和城市森林问题牵引已由
`DEC-2026-0902-opening-urban-forest-problem-framing.md` 接受并同步；最终送审题目仍待后续人工
确认。`idea-v2026.08.02` 不变。

### 0.4 2026-08-29 定时任务未创建记录

- 原计划：北京时间 2026-08-29 15:30 使用 `gpt-5.6-sol`、高推理执行开题源定义整理；
- 实际结果：只生成了 `suggested_create` 确认卡，未获得自动化 ID、可查看配置或运行记录，因此
  任务没有被正式创建，也没有在预定时间运行；
- 沟通错误：助手把“已渲染自动化卡片”误报为“定时任务已创建”；
- 复核结果：预定时间后未发现对应自动化配置、运行任务或由该任务产生的仓库改动；
- 后续规则：只有返回真实自动化 ID，且能够再次查看其状态时，才报告“已创建”；若只返回建议
  卡片，明确写为“等待用户确认”。到期后应检查运行状态或结果任务，不能以卡片展示代替执行。

## 1. 总执行逻辑

当前节奏不是平均推进三章，而是：

> **第一章设计冻结与最小资产盘点 → 第一章实现确认 → 第二章无悔资产漏斗 → 人工 Idea Gate → 第二章最小机制实验 →
> 第三章 Evaluation MVP**

第一章构建从用户开放需求、多智能体协作、工作流生成与工具执行到可解释结果交付的完整系统，
并将动态规划、过程图和错误调节作为增量；第二章研究如何对具有来源、适用条件和证据状态的
遥感科学知识进行任务条件化表示，并通过知识—证据运行界面支持面向任务的知识推理；第三章消费前
两章的冻结接口，在具有多阶段依赖、环境变化和可观察过程的城市森林遥感任务中组织任务链并评测
完整系统。

第三章在接口和实验环境上会因前两章完成而明显降本，但不会自动“水到渠成”。复杂场景和
复合任务的构造有效性、grader validity、跨方法公平比较与故障条件仍是第三章自己的研究贡献；
用户／专家校准仅用于必要的评价有效性检查。

## 2. 当前优先级与时间节奏

| 顺序 | 研究内容 | 当前任务 | 停止扩张 |
| --- | --- | --- | --- |
| 1 | 研究内容一 / M1 | v0.5.3 工程与 live 集成收口；当前做章节写作、稳定图件、人工 claim 审核和必要匹配机制实验 | 常驻审核 Agent、MCTS、界面、工具/任务说明扩张、完整企业权限/隔离、分布式运行时、通用平台化 |
| 2 | 研究内容二 / M2 | 先审核少量完整任务和证据，冻结任务条件化表示、运行界面与分层评价 | 全量 147 claims、完整知识库、生命周期、自进化 |
| 3 | 研究内容二机制实验 | 只在方法对象与任务成立后开展等知识内容的小型匹配实验 | 60--80 任务扩量、无门禁 multi-seed 大跑、预设 contract 优越性 |
| 4 | 研究内容三 / M3 | 前两章接口冻结后完成复杂场景表示、复合任务、grader、故障和跨方法试跑 | 正式用户研究、自演进、大规模比较、RL |

若没有明确面试日期，论文研究内容二保持约 70% 投入；M1 和面试证据包是短时收口任务。
若未来 7--10 天出现明确技术面试，则按 career sidecar 临时提高项目讲述和机试投入，不改变
M2 的科学门禁。

### 2.1 2026-09-01 至 2026-09-14 开题双节点推进窗口

本窗口有两个时间节点：

1. **2026-09-07（周一）导师讨论**：交付以城市森林遥感问题为牵引的修改版开题大纲，三项研究
   的科学问题、方法对象、最低技术路线、已有证据与缺口能够逐项对应；
2. **2026-09-14（周一）组会试讲**：交付可连续阅读的选题报告 O1 草稿和一套试讲材料，能够在
   有限时间内说明问题牵引、三章递进关系、技术路线、现有基础、待验证创新和近期实验门禁。

执行采用“证据核对与文本同步写入”，不等三章全部实验完成后再写：

| 截止 | 主任务 | 最小交付物 | 停止条件 |
| --- | --- | --- | --- |
| 09-02（09-01 已提前完成） | Ch3 P2 资产—评测—结论审计 | 资产—任务—评价器—结论矩阵已提交；Route B 首轮顺序已于 09-02 获研究者确认 | 不运行新实验、不晋级证据 |
| 09-03（09-02 已更新） | 三章技术路线与逐节论述对照 | v0.2 路线矩阵和原子论述图已传播城市森林问题牵引，并将 Route B 收窄为首个最小评测实现 | 不预设未冻结算法或效果 |
| 09-04 | Ch2 G4 第一门 | 10 条低／边界项人工复核记录；确定是否继续 50 条核心浅审 | 不把机器筛选当 scientific gold |
| 09-05（09-03 已提前完成） | 开题正文 O1 首轮 | v0.6.1 已从城市森林任务依赖重构问题提出；原子论述图固定逐节职责与证据槽位；独立 V1 的两项 P1 已关闭且差异复核无新 P1；全部 `[REF-MISSING]` 保留 | 不用占位引用制造完成感 |
| 09-06（09-03 已提前形成 v0.1） | 导师讨论包 | 修改版大纲、三章路线矩阵、证据缺口和 5 个待导师判断问题已压缩成低带宽包 | 不制作大而全答辩稿；研究者快速检查后再冻结会前版本 |
| 09-07 | 导师讨论 checkpoint | 记录反馈、未决问题和 retain/narrow/reject 决策候选 | 未经研究者确认不发布新 Idea |
| 09-08 至 09-10 | 反馈吸收与 Ch2 主线 | 形成 decision 或保持原版本的记录；推进 G4 核心浅审和 12--20 candidate list | 不提前冻结六个 gold cases |
| 09-11 | 三章路线冻结候选 | 三章技术路线、共享接口和局部／系统评价边界一致 | 仍有核心冲突则标 open，不强行冻结 |
| 09-12 至 09-13 | 组会试讲材料 | O1 草稿、总体路线图、三章各一页、证据／风险页和讲述提纲 | 只用可定位证据与拟议语气 |
| 09-14 | 组会试讲 checkpoint | 记录问题、反馈和下一轮修改优先级 | 试讲不自动等同于开题通过 |

动态调整规则：

- 每天只保留一个跨仓最高优先动作；章节内可并行做只读证据核对与文字整理，但不并行改变同一
  claim、gold 或方法版本；
- 若前置证据不足，优先收窄表述、记录缺口和准备导师问题，不为了赶日期伪造结果或降低验证门；
- 若某日任务提前完成，优先补正文、引用定位和图表来源，不提前启动大规模实验；
- 若遇到外部认证、研究者判断、伦理、Zotero 写入、付费模型或正式实验门，自动任务必须停在
  decision packet，等待明确授权；
- 每次产生实质进展后更新本文件的 `0.2`、`0.3` 和本窗口完成状态；下游结果先在 owning repo
  验证、提交和推送，再更新控制面 checkpoint；
- 09-07 导师反馈可改变 09-08 至 09-14 的任务顺序，但题目、章节角色、核心 claim 或证据状态的
  实质变化仍必须经过 decision，不在日常自动推进中静默接受。

## 3. 研究内容一：M1 收口门槛

M1 当前有两层必须分开：工程与小规模真实模型集成闭环已经可检查；正式匹配机制效果尚未证明。

### 已完成

- `TaskSpec`、`OperatorSpec`、`WorkflowGraph`、`WorkflowTrace`；
- 18 个遥感工具到 operator contract 的 adapter；
- unknown tool/artifact、missing input/output、type mismatch、invalid order、文件前置条件检查；
- 唯一安全缺失输出的 targeted repair，以及歧义/不支持情况下的显式停止；
- ReAct selector/executor 分离、每 Agent 工具预算和 decision/tool/observation/handoff trace；
- 2026-08-07 20:10 CST 本地复核：10 scientific、4 benchmark、11 workflow、8 ReAct tests 与 13 tool checks 通过；
- scripted no-API pilot 使用真实 ExpertsRS 工具生成 NDVI、mask 和 trace，B8/B4 由 metadata 解析到栈内 7/3，nodata 不进入类别计数；
- band/nodata/grid/area/reflectance-scale/LST 科学前置条件已按 ADR-002 写入工具、contract、validator、prompt 与 fixture；
- repair trace 与 Sentinel-2 缺 B10 的 controlled-stop trace 已重新生成；
- 第一章一页摘要、claim registry、evolution ledger、独立审计处置记录和 benchmark-20 admission gold draft 已形成。

### 当前允许的表述

> 已实现并测试面向遥感工作流的 typed representation、执行前验证、有限局部修复、受控停止
> 与可检查 trace 最小原型。

> 在保留面向用户自然语言遥感分析与 Manager–Scientist–Engineer/Executor 分工的基础上，
> 已形成由可调整的分层规划、随执行更新的过程图和基于检查点的局部恢复组成的统一运行闭环，
> 并完成冻结小面板的真实模型集成检查；正式效果证据尚待完成。

仍禁止写作：三个自适应对象已经贯通、真实 LLM 规划可靠性已经提高、一般工作流均可修复、完整 durable runtime、
多智能体普遍优于单智能体。

### 后续正式研究接口

第一章后续使用同任务对照实验比较 B0 原始对话、B1 静态预先规划、B2 根据真实反馈调整计划并更新过程图、B3 从检查点局部恢复。主指标限于任务是否执行闭合、工具反馈后是否正确改道、系统是否错误地报告成功、恢复范围、过程记录完整性与成本；遥感科学约束质量和最终结果精度分别属于第二、三章。该实验不要求现在扩展运行时平台功能。

当前已达到 M1“最小方法原型闭环”：足以冻结三张架构图、完成方法初稿和工程证据包，但
仍不能声称真实模型可靠性提高。第一章后续只追加必要的少量同任务匹配对照，不做
完整用户研究、主题精度或知识消融；后者分别由第二章科学约束实验和第三章独立系统评测承担。

### Validation、权限与生产控制面的边界

- 检查是一项系统责任，不自动对应新 Agent：原有角色负责判断，运行时执行固定规则，临时
  只读审核器只提供建议，系统外独立评测与标准答案保持隔离；
- 第一章只检查可执行性、完整性、权限、停止和任何正确工具执行都必须满足的底线不变量；
  第二章判断方法适用性、证据充分性、验证义务、冲突与结论降级，并输出修改/补验证/询问/
  拒绝/降级；检查点、产出复用和替代路径仍由第一章实现；
- 权限属于运行支撑：D1 冻结最小权限检查原则，D2 只实现本地允许、拒绝或要求确认，不能
  写成权限管理创新；
- D1 只记录 OpenTelemetry、STAC/OGC 等未来映射；D2/D3 只补 run/plan/event/artifact IDs、
  version、授权检查、逻辑 checkpoint 和必要指标；
- OTel exporter、STAC/OGC API Processes、container sandbox、durable queue/state、企业 IAM、
  online monitoring、MCP/A2A 均进入章节后的生产/求职/创业 backlog，不形成五条并行开发线。

## 4. 研究内容二：冻结最小方法闭环，再验证作用边界

### 4.1 当前判断

第二项研究的章级主术语已经统一为“面向智能体的遥感科学知识表示与推理”，但这不等于方法
形式和效果已经成立。后续需要结合完整任务、直接竞争论文和领域方法原文，确定最小贡献范围：

1. 如何表示来源、适用条件、证据状态、冲突、验证义务和结论边界；
2. 如何根据原始科学问题形成任务条件化的知识—证据状态；
3. 如何通过可查询运行界面支持面向任务的知识推理，而不规定唯一专家流程；
4. 如何区分流程执行、产品正确性、科学意图满足、严重科学错误和不必要干预。

`ScientificContract` 只是可能的紧凑投影或序列化形式，“认知环境”只是设计隐喻；二者均不
替代上述方法对象。在人工完成关键精读和任务深审前，不冻结更强 novelty claim，也不以跑完
旧 B0--B5 条件代替学术判断。

### 4.2 Idea Gate 前的无悔工作包

以下产物在具体表示或运行界面最终成立、收窄或失败时都可复用，因此可以先做：

1. **任务资产**：冻结 `UF-VAL-CLASS-01` 与 `UF-VAL-HAB-01` 的 task-visible 字段、成功/失败
   条件和 gold 隔离；
2. **证据资产**：只处理 8--12 条 atomic claims，补 exact source spans、适用范围、冲突、
   不确定性和禁止过强表述；
3. **证据状态资产**：形成 sufficient、insufficient、conflicting、inapplicable 和 no-intervention
   的最小正负条件；
4. **行动语义**：统一 `pass/revise/add-validation/ask/reject/downgrade/escalate`，不绑定某个
   特定表示或接口实现；
5. **可观测接口**：冻结 before/after、violation、affected step、action、artifact 和 cost 的
   trace 字段；
6. **评测资产**：固定 task/gold separation、matched context budget、leakage check 和
   scientific-correctness review 字段；
7. **claim-safe memo**：分别记录 supported asset、positive signal、failed idea、remaining
   uncertainty 和下一证据。

这些资产即使不能证明基于证据状态的知识推理优于普通检索，仍能支持第二章的知识与证据表示、方法适用性、
错误知识防护，也能直接成为第三章的任务、故障和 grader 输入。

### 4.3 人工 Idea Gate

Codex 只提交一个压缩包，不要求研究者通读 147 条 ledger。研究者确认：

1. 两个验证任务是否代表博士论文中的真实科学风险；
2. 精读直接竞争后，最小方法 claim 在 knowledge representation、runtime interface 和
   evidence-constrained reasoning 三者中如何划界；
3. 自动提出知识状态或约束是核心贡献还是可选上探；
4. 哪些 evidence spans/适用边界需要研究者本人签字。

在该 Gate 前，允许证据定位、task/gold 分离、schema、validator 和 fixture 工作；不允许把
候选知识或机器判断晋级为 thesis-safe 结论，也不启动正式扩量。

### 4.4 Idea Gate 后的最小机制实验

旧 B0--B5 编号只作为可复用实验资产，正式实验按下列方法条件重新解释：

| 条件 | 作用 |
| --- | --- |
| B0 | task 与共同输出 schema |
| B1 | 通用 self-check |
| B2 | 等预算 plain evidence text |
| B3 | 结构化知识表示，但无任务条件化状态或运行时作用 |
| B4 | 任务条件化知识—证据表示与可查询运行界面 |
| B5 | 基于当前证据状态的推理、行动或结论调整及其 trace |

最低通过条件：

- admitted claim 均能定位原文且不泄露 gold；
- B4/B5 在需要干预时产生与证据相称的推理、行动或结论变化；
- 在证据充分、不适用或无需干预时避免机械停止和不必要改变；
- 流程执行、产品正确性、科学意图、严重错误、不必要干预、额外成本和失败分别报告。

### 4.5 失败也必须留下的方法资产

| 结果 | 论文收窄 | 保留资产 |
| --- | --- | --- |
| B2/B3 与 B4 等效 | 不宣称运行界面增量；收窄到 evidence-governed representation | exact-span ledger、task-conditioned projection、matched evaluation |
| B4 有效、B5 无增益 | 保留任务条件化表示，删除不必要运行时机制 | query schema、状态 trace、成本分析 |
| 自动提出知识状态不稳定 | 以人工校准的任务条件化表示为基本盘 | proposal/review 分离、错误知识 controls |
| 全部信号弱或任务不成立 | 不强写机制；转为任务与评测方法/负结果分析 | task fixtures、failure taxonomy、grader、claim-safe memo |

因此，第二章每个阶段的完成条件不是“得到正结果”，而是“形成可追踪工件并作出可防守的
retain/narrow/reject 决策”。

## 5. 研究内容三：前两章之后的最小进入路径

M2 Gate A 后才正式启动 M3：

1. 冻结大型城市中遥感制图、植物生态、景观格局、生态系统服务和管理解释之间的指标依赖图；
2. 从依赖图中组织 2--3 条跨层复合任务链，并定义共同输入、前置条件、中间产物和结论边界；
3. 冻结 `ComplexScenario -> CompositeTask -> TrialTrace -> Outcome -> Evaluation` 与版本化运行环境；
4. 将已有环境变化和已知失败转成可重放 fixture；
5. 先实现 deterministic outcome/provenance/dependency graders；
6. 比较传统脚本、通用 tool-using Agent、structured URSA，必要时增加第二章知识—证据界面
   variant；
7. 分开报告结果、依赖保持、过程、恢复、成本和人工介入；
8. 只有复合任务和 grader 稳定后，才进入用户 rubric、伦理边界和小型校准。

第三章不重复证明第一、二章机制，也不靠北京地图精度或综合 demo 代替独立评测贡献。

第三章首先把大型城市中的多层指标及其跨学科依赖组织成复合任务族，而不是简单增加独立短任务
数量。最小验证覆盖任务分解与依赖保持、科学一致性、环境变化与故障处理、结果可追溯性和跨系统
比较；用户／专家校准和基于历史经验的受控适应只在主线闭合后作为可选增量。

## 6. 职业协同边界

华为 Harness 实习申请、面试材料和招聘投入门禁由
[`huawei_harness_internship_thesis_alignment_20260802.md`](huawei_harness_internship_thesis_alignment_20260802.md)
维护。本计划只接受以下职业侧影响：

- M1 现有工件可压缩为一页摘要和两条 trace，不另建求职 demo；
- M2 的无悔资产和负结果均可作为研究判断与 Evaluation 能力证据；
- 只有明确面试/到岗信号才临时调整时间比例；
- 简历语言不得反向升级 thesis claim；
- Agent RL、自进化和大规模后训练不进入开题前门禁。

## 7. 跨会话恢复与过程记录协议

### 会话开始

任何 thesis-wide 或跨仓任务先读取：

1. `THESIS_STATE.md`；
2. 本文件的 `## 0. Resume here`；
3. 仅当“当前唯一下一动作”指向某章时，再读取该章 `AGENTS.md`、`PLAN.md` 和唯一 active brief。

不默认扫描全部历史 plans、reports 或 chats。

### 会话进行中

- 原始代码、run、trace、rubric 和结果写在 owning repo；
- 本文件只记录状态、证据指针、下一动作和人工门禁；
- 实质性题目/章节角色/claim 变化走 decision，不在聊天里静默接受；
- 诊断失败保留原始 artifact，不覆盖成成功记录；
- 同一里程碑不新建并行总计划，只更新 active brief 或本文件。

### 会话结束

每个产生实质进展的会话必须更新本文件 `0.2` 和 `0.3`，至少记录：

1. 最后完成的工件及路径；
2. 证据状态：completed / diagnostic / frozen-design / open；
3. 仍存在的失败、缺口或 dirty-state 风险；
4. 下一次只执行的一步；
5. 需要研究者决定的问题；
6. 若有运行，记录 owning repo、配置/版本、输出路径和是否可复现。

聊天记录不是 source of truth。若聊天与仓库状态冲突，以原始工件和本文件最后一次经过检查的
checkpoint 为恢复起点。

### 7.1 2026-08-09 M1 架构冻结 checkpoint

- owning repo：`D:/projects/phd-thesis/URSA`，branch `main`；
- command：在 `ExpertsRS/` 运行 `python run_m1_closeout.py`；
- completed：33 tests、13 tool checks、repair/controlled-stop 与 scripted real-tool pilot；
- readable sources：`docs/thesis/ch1_m1_closeout_20260807.md`、
  `docs/evidence/ch1_m1/README.md`、`docs/thesis/ch1_evidence_system/`；
- raw outputs：`ExpertsRS/results/react_pilot_20260807201058.json` 与
  `ExpertsRS/results/ch1_m1_closeout/`，为 ignored/generated local evidence；
- diagnostic boundary：语义 B8/B4 与 nodata invariant 已通过单 fixture；0.3 threshold
  未校准、无 thematic gold、非 live LLM、非 P0--P3 effect；
- reproducibility risk：workflow/ReAct/tests/docs 仍有 untracked/dirty source，当前 HEAD
  不能单独重建本次结果；需研究者决定 commit/archive；
- accepted design：规划是可以根据真实反馈修改的未来意图，执行是真实动作、观测和产出；过程图在运行中逐步整理，用于检查和查询。当时冻结的三个增量研究对象为可调整的分层规划、随执行更新的过程图和基于检查点的局部恢复；章节核心已由 `DEC-2026-0830` 校准为面向用户的完整多智能体科学分析系统；
- implementation boundary：静态工作流、规则检查、有限修补和停止为已实现基线；计划版本、由运行记录自动整理过程图、检查点替代路径和基于过程图的反思尚未实现；
- benchmark correction：20 条 admission gold 草案已降级，rich scientific-risk labels 不再作为第一章指标；
- 2026-08-10 clarification：不默认新增审核 Agent；采用角色责任、运行时固定规则、按需只读
  审核器、独立评测与最小权限检查，完整生产控制面分期延后；
- D1 result：主线资产为权威；旁支只选择性借用编号、清单、来源与闭合检查；拒绝固定六节点、
  常驻审核/报告角色和旧数字波段约定；真实运行记录按时间保留，过程图由记录逐步整理；
- 术语修正：人工审批和论文主线不再使用 `EventLedger`、`RunGraph`、
  `materializer` 等项目内部代称；类名与字段只留技术附录；
- 2026-08-10 researcher decision：三条 D2 原则获认可；进一步冻结“分层规划不等于搜索树、
  过程图可由事实确定性重建、检查点只位于已验证安全边界”；
- 2026-08-11 figure/boundary freeze：第一章只维护系统模块、角色责任、运行闭环三张稳定架构图；
  运行闭环在叙事上承接 StateFlow，代码上仍保留 StateFlow 为历史基线。第一章管运行与恢复，
  第二章管科学依据与行动义务，第三章管独立系统/用户评测；
- next：进入 0.3 的 D2-A 无 API 最小机制与测试；不花模型 API，不实现 MCTS。

## 8. 旧计划与专项文件的处理规则

- 历史 plan/brief 不删除，保留研究演进和实验 provenance；
- `THESIS_STATE.md` 与本文件之外的 thesis-wide plan 默认视为 historical/context；
- 下游每章只能由其 `PLAN.md` 指向一个 active brief；旧 brief 不因存在于目录中自动生效；
- career sidecar、outline freeze protocol 和各章计划只在本文件显式指向时进入当前执行；
- 新的任务细节写入 owning repo 的 active brief，不把本文件膨胀成代码级 runbook；
- 当前文件名虽含 `20260802`，为避免继续产生“新版计划”而保留为稳定入口；版本和快照日期
  由文件正文维护。
