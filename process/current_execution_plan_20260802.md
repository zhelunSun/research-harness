# 当前执行计划：M1 收口与研究内容二无悔推进

> 版本：v2026.08.11
> 对齐 Idea：`idea-v2026.08.02`
> 状态：active；保留原文件名作为稳定入口，不再按日期新建论文总执行计划
> 触发：固定简历与面试路径已形成；研究内容一已有最小原型；研究内容二核心机制仍待验证

## 0. Resume here：每次新会话先读这里

### 0.1 只维护两个论文级入口

1. `THESIS_STATE.md`：慢更新，维护总科学问题、三项研究角色、贡献边界和正式风险；
2. 本文件：快更新，维护当前里程碑、下一动作、人工门禁、证据状态和会话恢复点。

下游 `PLAN.md`、experiment brief、chapter plan 和报告仍是所属仓库的执行/证据文件，
但不再与本文件竞争“当前总计划”。职业材料只由
`huawei_harness_internship_thesis_alignment_20260802.md` 作为 sidecar 维护，不反向升级论文状态。

除非总题目、章节角色或核心 claim 发生变化，不再新建 thesis-wide roadmap、handoff 或
“最新版计划”。新会话通过本节恢复，不依赖翻找历史 chat。

### 0.2 2026-08-11 当前快照

| 里程碑 | 状态 | 已有证据 | 当前缺口 |
| --- | --- | --- | --- |
| M0 固定简历与证据边界 | completed | 固定华为 PDF、claims、面试风险口径 | 不作为论文结果升级 |
| M1 面向用户的自适应运行方法 | D1 已完成 / D2 原则已认可 | 静态工程基线与三个研究对象已冻结；D1 已盘点主线和旧旁支、检查/权限职责、18 个工具的动作类型以及 D2 验收条件；研究者认可 D2 三条原则 | 尚无计划版本、由记录自动整理的过程图、检查点替代路径、统一权限检查或正式对照效果；源码/结果仍有未提交本地状态 |
| M2 ScientificContract 行动闭环 | preparation | active sprint、两任务设想、contract interface、B0--B5 设计 | 新任务 fixture、exact evidence spans、admitted contract、dry run 和 action-change trace 尚未形成 |
| M3 Evaluation MVP | pending | 北京制图资产、任务/轨迹/用户分层设计 | 可执行任务、grader 和跨方法试跑未完成 |
| M4 用户效用与经验复用 | deferred | 目标用户/专家角色与 episode reservoir 已界定 | 伦理/数据门禁、rubric 校准、episode 化和任何学习实验均未启动 |

### 0.3 当前唯一下一动作

研究者已于 2026-08-10 认可 D2 三条原则。当前唯一下一动作改为 **D2-A：无 API 最小机制实现
与测试**，不再等待概念审批，也不启动真实模型或 MCTS。

编码前关系已冻结：分层规划面向未来，只表达总体目标、当前阶段和下一动作；过程图面向已经
发生的事实，并可由运行记录确定性重建；检查点只建立在工具动作完成、执行后检查通过、有效
产出已登记的安全边界。过程图可以把当前相关信息反馈给 Scientist，但不替代规划。

D2 预计 2--3 个工作会话：

1. **D2-A，约 1 个会话**：增加计划版本、稳定运行记录、过程图重建、最小权限决定和安全
   检查点；完成纯函数和单元测试；
2. **D2-B，约 1 个会话**：运行一个无 API、真实遥感工具小样，展示元数据反馈引起计划修改、
   一次注入故障从检查点换路、一次越界写入被拦截；
3. **D2-C，约半个到 1 个会话**：重跑既有测试，独立检查可读轨迹与过程图，更新一页摘要和
   证据状态。

停止条件：D2 只证明三个对象能够贯通和失败路径可检查；不实现搜索树、图数据库、任意回滚、
云服务或真实模型效果比较。总题目、三章角色与 `idea-v2026.08.02` 仍不发布新版本。

## 1. 总执行逻辑

当前节奏不是平均推进三章，而是：

> **第一章设计冻结与最小资产盘点 → 第一章实现确认 → 第二章无悔资产漏斗 → 人工 Idea Gate → 第二章最小机制实验 →
> 第三章 Evaluation MVP**

第一章研究开放式用户请求如何在真实观测下调整计划、物化为可审计执行图并局部恢复；第二章判断知识和证据是否能形成真正改变行动的
科学边界；第三章消费前两章的冻结接口，研究如何在真实任务中比较结果、轨迹、恢复和
用户效用。

第三章在接口和实验环境上会因前两章完成而明显降本，但不会自动“水到渠成”。任务真实性、
grader validity、跨方法公平比较、故障注入、用户角色和伦理边界仍是第三章自己的研究贡献。

## 2. 当前优先级与时间节奏

| 顺序 | 研究内容 | 当前任务 | 停止扩张 |
| --- | --- | --- | --- |
| 1 | 研究内容一 / M1 | D1 已完成、D2 原则已认可；当前只做 D2-A 无 API 最小机制与测试 | 常驻审核 Agent、MCTS、界面、工具/任务说明扩张、完整企业权限/隔离、分布式运行时、通用平台化 |
| 2 | 研究内容二 / M2 | 先做不依赖最终 ScientificContract claim 的证据与任务资产，再过人工 Idea Gate | 全量 147 claims、完整知识库、生命周期、自进化 |
| 3 | 研究内容二机制实验 | 只有 Idea Gate 后才冻结最小 contract 并运行两任务 B0--B5 | 60--80 任务扩量、无门禁 multi-seed 大跑 |
| 4 | 研究内容三 / M3 | 前两章接口冻结后完成最小任务、grader、故障和跨方法试跑 | 正式用户研究、大规模比较、RL |

若没有明确面试日期，论文研究内容二保持约 70% 投入；M1 和面试证据包是短时收口任务。
若未来 7--10 天出现明确技术面试，则按 career sidecar 临时提高项目讲述和机试投入，不改变
M2 的科学门禁。

## 3. 研究内容一：M1 收口门槛

M1 当前有两层必须分开：静态软件基线已经可检查；自适应方法设计已经冻结但尚未实现，更未证明有效性。

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
> 已冻结由可调整的分层规划、随执行更新的过程图和基于检查点的局部恢复组成的
> 第一章方法设计；其统一实现和效果证据尚待完成。

仍禁止写作：三个自适应对象已经贯通、真实 LLM 规划可靠性已经提高、一般工作流均可修复、完整 durable runtime、
多智能体普遍优于单智能体。

### 后续正式研究接口

第一章后续使用同任务对照实验比较 B0 原始对话、B1 静态预先规划、B2 根据真实反馈调整计划并更新过程图、B3 从检查点局部恢复。主指标限于任务是否执行闭合、工具反馈后是否正确改道、系统是否错误地报告成功、恢复范围、过程记录完整性与成本；遥感科学约束质量和最终结果精度分别属于第二、三章。该实验不要求现在扩展运行时平台功能。

D2 完成即达到 M1“最小方法原型闭环”：足以冻结三张架构图、完成方法初稿和工程证据包，但
仍不能声称真实模型可靠性提高。第一章最终只追加一个 D3-light 少量同任务真实模型对照，不做
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

## 4. 研究内容二：先积累无悔资产，再决定最终 Idea

### 4.1 当前判断

`ScientificContract` 是可检验的候选方法对象，不是必须捍卫到底的预定结论。研究者尚需结合
直接竞争论文和领域方法原文精读，判断最终贡献应落在：

1. evidence-governed representation；
2. task-conditioned minimal contract；
3. admission/enforcement 与 action change；
4. 或上述对象的更窄组合。

在人工完成关键精读前，不冻结更强 novelty claim，也不以自动跑完 B0--B5 代替学术判断。

### 4.2 Idea Gate 前的无悔工作包

以下产物在 ScientificContract 最终成立、收窄或失败时都可复用，因此可以先做：

1. **任务资产**：冻结 `UF-VAL-CLASS-01` 与 `UF-VAL-HAB-01` 的 task-visible 字段、成功/失败
   条件和 gold 隔离；
2. **证据资产**：只处理 8--12 条 atomic claims，补 exact source spans、适用范围、冲突、
   不确定性和禁止过强表述；
3. **风险资产**：形成 invalid、irrelevant、missing、conflicting constraint 的最小 fixture；
4. **行动语义**：统一 `pass/revise/add-validation/ask/reject/downgrade/escalate`，不绑定某个
   contract 实现；
5. **可观测接口**：冻结 before/after、violation、affected step、action、artifact 和 cost 的
   trace 字段；
6. **评测资产**：固定 task/gold separation、matched context budget、leakage check 和
   scientific-correctness review 字段；
7. **claim-safe memo**：分别记录 supported asset、positive signal、failed idea、remaining
   uncertainty 和下一证据。

这些资产即使不能证明“约束执行优于 RAG”，仍能支持第二章的知识与证据治理、方法适用性、
错误知识防护，也能直接成为第三章的任务、故障和 grader 输入。

### 4.3 人工 Idea Gate

Codex 只提交一个压缩包，不要求研究者通读 147 条 ledger。研究者确认：

1. 两个验证任务是否代表博士论文中的真实科学风险；
2. 精读直接竞争后，最小方法 claim 选 representation、contract 还是 enforcement；
3. model-proposed constraints 是核心贡献还是可选上探；
4. 哪些 evidence spans/适用边界需要研究者本人签字。

在该 Gate 前，允许证据定位、task/gold 分离、schema、validator 和 fixture 工作；不允许把
候选约束晋级为 thesis-safe 结论或启动正式扩量。

### 4.4 Idea Gate 后的最小机制实验

保留两任务 B0--B5，但把它视为可证伪实验：

| 条件 | 作用 |
| --- | --- |
| B0 | task 与共同输出 schema |
| B1 | 通用 self-check |
| B2 | 等预算 plain evidence text |
| B3 | 结构化知识但无行动义务 |
| B4 | 最小可读 contract |
| B5 | violation detection、repair/reject 和 enforcement trace |

最低通过条件：

- admitted claim 均能定位原文且不泄露 gold；
- B4/B5 至少在正确情形触发可观测行动变化；
- 错误、无关或缺失约束不会被机械服从；
- 行动变化、科学正确性、额外成本和失败分别报告。

### 4.5 失败也必须留下的方法资产

| 结果 | 论文收窄 | 保留资产 |
| --- | --- | --- |
| B2/B3 与 B4 等效 | 不宣称 contract 增量；转向 evidence-governed representation | exact-span ledger、task-conditioned projection、matched evaluation |
| B4 有效、B5 无增益 | 保留软约束，删除不必要 enforcement | action vocabulary、violation trace、成本分析 |
| model-proposed 不稳定 | 静态/人工校准 contract 作为基本盘 | proposal/admission 分离、错误约束 controls |
| 全部信号弱或任务不成立 | 不强写机制；转为任务与评测方法/负结果分析 | task fixtures、failure taxonomy、grader、claim-safe memo |

因此，第二章每个阶段的完成条件不是“得到正结果”，而是“形成可追踪工件并作出可防守的
retain/narrow/reject 决策”。

## 5. 研究内容三：前两章之后的最小进入路径

M2 Gate A 后才正式启动 M3：

1. 选择前两章已经暴露真实失败的 2 个任务族；
2. 冻结 `EvalTask -> TrialTrace -> Outcome -> Evaluation`；
3. 将 2--3 个已知失败转成可重放 fixture；
4. 先实现 deterministic outcome/provenance graders；
5. 比较传统脚本、通用 tool-using Agent、structured URSA，必要时增加 scientific-contract
   variant；
6. 分开报告结果、过程、恢复、成本和人工介入；
7. 只有任务和 grader 稳定后，才进入用户 rubric、伦理边界和小型校准。

第三章不重复证明第一、二章机制，也不靠北京地图精度或综合 demo 代替独立评测贡献。

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
- accepted design：规划是可以根据真实反馈修改的未来意图，执行是真实动作、观测和产出；过程图在运行中逐步整理，用于检查和查询。第一章只保留可调整的分层规划、随执行更新的过程图和基于检查点的局部恢复三个研究对象；
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
