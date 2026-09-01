# 开题证据矩阵

> 版本：v0.8，2026-09-01
> 对齐 Idea：`idea-v2026.08.02`
> 用途：回答“已经完成了什么、能支持什么、不能支持什么、开题 50% 还缺什么”。
> 边界：本文件只维护跨仓库证据指针和状态，不复制或改写下游原始实验。

## 1. 状态定义

| 状态 | 含义 | 开题使用方式 |
| --- | --- | --- |
| PUBLISHED | 已发表并可定位到论文原文 | 可作为既有工作和已验证基础 |
| VERIFIED-ASSET | 本地资产、代码或结果可检查 | 可证明完成度；能否支持科学结论另行判断 |
| DIAGNOSTIC | 已运行但存在构念、公平性、人类校准或样本边界 | 只作方向性证据 |
| FROZEN-DESIGN | 问题、方法对象和实验边界已冻结 | 可证明研究可执行，不能计作结果 |
| OPEN | 尚无匹配证据或尚未完成 | 开题前门禁或开题后计划 |

## 2. 总体题目与三项研究

- 工作总题目：**面向城市森林遥感制图的智能方法研究**
- 研究内容一：**面向开放需求的多智能体遥感科学分析系统**
- 研究内容二：**面向智能体的遥感科学知识表示与推理**
- 研究内容三：**面向城市森林遥感任务的智能体系统评测**
- 内部科学主线：**城市森林遥感任务 → 多智能体科学分析工作流 → 知识支持的产品与结论 → 智能体系统评测**
- 长期设计原则：**轨迹原生、科学约束、评测驱动、经验可学习**

上述版本已向导师汇报且未收到新增修改意见，可作为当前执行基线；这不是方法 claim、
人体参与方案或最终送审题目的正式批准证据。

## 3. 研究内容一证据

| 证据对象 | 状态 | 当前能支持 | 当前不能支持 | 指针 |
| --- | --- | --- | --- | --- |
| ExpertsRS 已发表论文 | PUBLISHED | 面向用户的多智能体遥感分析、角色分工和基本工作流具有初步可行性；Data--Tools--Brain；两项案例；20 条请求轻量比较 | 动态规划、过程图、错误调节、检查点恢复或一般可靠性 | DOI `10.1080/20964471.2025.2600178` |
| v0.5.3 统一运行与证据系统 | VERIFIED-ASSET | 代码基线 `0efd090`；主／clean 环境 121/121；统一 run/resume、结构化计划、plan-bound action、真实工具反馈、计划修订、planned/observed graph、运行内 checkpoint 和交付闭合可检查 | 规划优越性、检查点独立效应、科学精度、跨任务泛化和生产级持久恢复 | `URSA/docs/thesis/ch1_evidence_system/v053_evidence_index.md` |
| 冻结 v2 5×3 live 集成试验 | DIAGNOSTIC | 15/15 evaluator closure；支持冻结任务面板内的协议贯通和真实模型集成可运行性 | 任务成功率、统计优越性、一般可靠性或用户效用 | `URSA/docs/thesis/ch1_evidence_system/v053_results_table.md` |
| 第一章论断登记与稳定叙事入口 | VERIFIED-ASSET | 当前允许／禁止表述、方法图语义和写作入口已统一 | 未登记的新 claim 或正式效果结论 | `URSA/docs/thesis/ch1_evidence_system/README.md` |
| 正式匹配机制实验 | OPEN | — | 自适应规划、过程图与检查点恢复相对基线的增量效果 | 第一章后续章节实验 |

### 研究内容一开题门禁

1. 已完成：可版本化表示、运行与证据结构；
2. 已完成：可运行的验证、受控停止和计划修订路径；
3. 已完成：planned/observed graph、运行内 checkpoint 与交付检查；
4. 已完成：冻结 5×3 live 集成诊断，但不得替代正式匹配效果实验；
5. 已完成：已发表 ExpertsRS 与新增方法的 claim 边界登记；
6. 待完成：必要的同任务匹配机制实验与人工 claim 签字。

## 4. 研究内容二证据

| 证据对象 | 状态 | 当前能支持 | 当前不能支持 | 指针 |
| --- | --- | --- | --- | --- |
| 41 张 canonical knowledge cards 与 42 个 registry assets | VERIFIED-ASSET | 领域知识资产、schema、taxonomy、来源登记和可追溯表示已具有较大工作基础 | 每个 card claim 已获得论文级证据支持 | `chapter2-urban-forest-knowledge/assets/cards/` |
| 147 条 claim ledger（129 条为 2026-07-13 快照） | VERIFIED-ASSET | 已建立原子知识候选、来源、核验动作和状态的治理对象；当前 143 条 candidate、4 条 needs-review | 147 条科学约束、人工规则或 thesis-safe 知识；当前 147 条 evidence span 均为 TBD | `chapter2-urban-forest-knowledge/config/card_claims.csv` |
| 既有资产的任务条件化使用设计 | FROZEN-DESIGN | cards/claims/evidence 被定位为离线知识与证据底座；来源、适用条件、证据状态和有效性边界可按任务组织并进入运行界面 | 已形成完整推理方法、自动知识学习、专家成本下降或错误更新防护 | `chapter2-urban-forest-knowledge/docs/20260731_ch2_asset_reinterpretation_and_harness_transition.md` |
| G1--G4 / Wave pilot | DIAGNOSTIC | 结构化知识和治理字段能够改变部分规划输出，值得进入匹配机制实验 | 一般规划质量提升；executed constraints 优于 RAG；工具正确性不变 | `chapter2-urban-forest-knowledge/PLAN.md` |
| 直接竞争与创新审计 | VERIFIED-ASSET | 已识别 AgentSpec、RNSP、KISS、KAG/WTS/OG-RAG 等威胁，禁止泛化创新语言 | 新颖性已经闭合 | `docs/20260713_ch2_innovation_and_evidence_audit.md` |
| 任务条件化知识—证据运行界面 | FROZEN-DESIGN | 可查询的候选接口能够暴露来源、适用条件、证据状态、冲突、验证义务和结论边界；`ScientificContract` 仅为一种紧凑投影形式 | 该界面已经支持稳定的知识推理、确实降低科学风险，或是唯一／最优实现 | `thinking-space/task-conditioned-epistemic-contract-spec.md` |
| 等知识内容的分层匹配实验 | FROZEN-DESIGN | 现有 B0--B5/A1/A2 brief 可复用来区分普通任务、通用 self-check、检索文本、结构化表示和运行时作用条件 | 正式实验结果；流程、产品、科学意图和严重科学错误的有效评价；人类校准 | `experiments/briefs/ch2-epistemic-contract-evaluation-v0.1.md` |
| WTS-informed 知识生命周期 | FROZEN-DESIGN | 经验触发 candidate update、证据准入和版本化 ledger 具有可执行候选设计 | 自主知识进化或维护成本下降 | `docs/20260724_ch2_wts_absorption_and_stability_gate.md` |

### 研究内容二开题门禁

1. 从直接竞争审计中选择最小、可防守的核心 claim，并明确它落在知识表示、运行界面还是知识推理；
2. 从完整遥感任务中选择少量锚点，只补齐任务相关知识的证据原文、适用条件和有效性边界；
3. 冻结不泄露完整答案的任务条件化知识表示，以及智能体可查询、可检查的最小知识—证据运行界面；
4. 在等知识内容下完成至少一个普通任务／检索文本／结构化表示／基于证据状态的知识推理匹配实验；
5. 同时设置证据充分、不足、冲突、不适用和无需干预条件，分别评价流程执行、产品正确性、科学意图满足、严重科学错误和不必要干预；
6. 由领域人员确认任务、知识和判断边界，并校准依赖科学判断的评分；
7. 知识生命周期、自动更新和特定 contract 形式保持为可选扩展，不抢占基础方法。

## 5. 研究内容三证据

| 证据对象 | 状态 | 当前能支持 | 当前不能支持 | 指针 |
| --- | --- | --- | --- | --- |
| 北京 2025 Route B v1 方法与制图基线 | VERIFIED-ASSET | 多源弱标签、时序稳定性、空间纯度、分层抽样、RF 和制图流程已闭合并冻结 | 八类制图整体可靠；Agent 可靠性 | `urbfo-agent-demo/docs/reports/summary_routeb_v1_freeze_20260705.md` |
| 7,351 行训练表与方法冻结 | VERIFIED-ASSET | 当前场景已存在可复现任务、真实数据限制和专业制品 | 新第三项研究的任务/评分有效性 | `urbfo-agent-demo/experiments/results/routeb_v1_method_freeze_20260705.json` |
| 470 点历史回归诊断 | DIAGNOSTIC | Level 1 与八类结果的已知能力和错误类型 | 最终一次性未查看确认集；可靠性验证 gold | `urbfo-agent-demo/experiments/results/routeb_seasonal17_reused_v0_validation_20260705.json` |
| 北京项目过程资产 | VERIFIED-ASSET / 待结构化 | 当前可定位 107 条 GEE 运行记录、63 条结果 manifest 记录和持续更新的弱标签决策日志，可作为任务、故障、恢复和经验 episode 候选来源 | 已经构成标准 Agent trace、可回放 episode 或可训练 RL trajectory 数据集 | `urbfo-agent-demo/metadata/runs/gee_routeb_runs.jsonl`; `experiments/results/manifest.csv`; `docs/method_notes/weak_label_decision_log_2026-06-15.md` |
| 第三项研究主线 | FROZEN-DESIGN | 城市森林遥感任务中的多阶段依赖、任务链组织与完整系统评测的核心边界及最低可执行路径已接受 | 可执行任务链、评价有效性和跨方法结果 | `research-harness/decisions/DEC-2026-0831-opening-consensus-and-working-titles.md` |
| 制图资产到评测对象的映射 | FROZEN-DESIGN | 已将任务环境、弱样本方法、样本、制品、故障和过程历史分离；明确“trajectory candidate”边界 | 可执行任务集和已清洗 episode dataset | `urbfo-agent-demo/docs/plans/ch3_asset_to_eval_and_hitl_plan_20260731.md` |
| 用户／专家校准候选增量 | FROZEN-DESIGN | 目标用户、领域专家和评测审计角色已经区分，可用于检查任务和评价构念 | 用户效用提升、正式样本设计、伦理／数据边界或人体参与结论 | `urbfo-agent-demo/docs/plans/ch3_asset_to_eval_and_hitl_plan_20260731.md` |
| 最小跨方法试跑 | OPEN | — | 第三项研究的独立实证闭环 | 待 Chapter 3 evaluation MVP |

### 研究内容三开题门禁

1. 冻结一组城市森林遥感任务的范围、共同特征与 intended-use 边界；
2. 把遥感制图、植物生态、景观格局、生态系统服务和管理解释中的首组指标组织为复合任务依赖；
3. 冻结版本化环境、成功条件、关键失败和可观察试验记录；
4. 实现至少一个确定性检查器，并建立跨步骤一致性、运行适应性和结果可追溯性评价；
5. 完成至少一次传统流程／通用 Agent／结构化遥感智能体的跨方法试跑；
6. 仅在主线需要时开展小规模领域或用户校准；正式收集研究数据前确认伦理与数据使用边界；
7. 历史日志保持 episode reservoir；经验适应或自演进不进入当前开题门禁。

## 6. 对“已完成 50%”的当前解释

当前可以稳妥计算为已完成基础的内容：

- 一项已发表多智能体遥感论文及其案例和轻量 benchmark；
- URSA v0.5.3 工程与小规模真实模型集成闭环；
- Chapter 2 知识资产、治理骨架、诊断 pilot 和正式实验设计；
- 北京 2025 制图方法、样本、结果与大量过程资产；
- 新总故事线、章节边界和第一项研究新增方法边界。

当前不能按已完成结果计算的内容：

- 第一项新增规划、过程图与检查点机制的正式匹配效果证据；
- 第二项等知识内容的分层匹配结果及领域校准；
- 第三项用户系统验证的任务、评分器和跨方法结果；
- 历史日志转化后的 experience dataset；
- Agent RL、自适应或自进化收益。

因此，当前“工作资产完成度”接近或超过开题所需的量级，但“新故事线下
thesis-safe 证据完成度”尚需前三个最小闭环补齐。开题汇报应同时展示已有完成量
和新增门禁，不能把冻结设计写成已验证结论。

## 7. 需要研究者本人高强度参与的两个门禁

### H1：核心 claim 选择与证据签字

Codex 负责生成竞争矩阵、证据定位和可选 claim；研究者本人负责：

1. 判断哪一个科学问题确实值得作为自己的博士贡献；
2. 确认论文、代码和实验中的实际个人工作边界；
3. 对“允许写入开题/禁止写入开题”的 claim 做最终签字；
4. 决定第二项研究中知识表示、运行界面和知识推理的最小成立范围，以及哪些实现形式只作候选。

### H2：复杂场景与评价构念校准

Codex 负责生成任务模板、rubric、试验协议和分析代码；研究者本人负责：

1. 确认大型城市复杂场景中哪些指标与依赖代表真实的城市森林研究或管理问题；
2. 判断复合任务的科学一致性、关键失败、可接受风险和结果使用边界；
3. 批准领域专家、目标用户和评测审计者在必要校准中的职责，不亲自设计完整 rubric；
4. 批准真实项目数据、反馈和日志的使用边界；
5. 若进入正式用户数据收集，再确认伦理／人体参与审查要求。

除 H1、H2 外，证据清点、文献候选筛选、schema、validator、pilot 实现、评测
harness、结果分析和文档维护可由 Codex 主导，在门禁处提交简短决策包。

## 8. 研究者精读清单

不建议广泛追逐 Agent 文献。第一轮只精读以下五组，并只读与决策有关的部分：

| 材料 | 精读部分 | 用来决定 |
| --- | --- | --- |
| 自己的 ExpertsRS 论文 | contributions、method、evaluation、limitations | 哪些证据已经发表，第一项新增边界在哪里 |
| Spatial-Agent | problem、GeoFlow Graph、constraints、ablation、limitations | 工作流图之外还必须增加什么 |
| GeoAgentBench 与 GeoDisaster | task construction、environment、grader、failure、baseline、limitations | 第三项如何避免重复现有地理 Agent benchmark |
| WTS 加一个最接近的知识约束方法（由 Ch2 comparator audit 选定） | representation、runtime use、evidence state、evaluation | 第二项最小贡献落在何种知识表示与推理机制；知识演化是否仅作扩展 |
| HASTE 与 Anthropic Agent Evals | real users、human effort、trial/trace/outcome/grader、limitations | 面向用户的可靠性验证测什么 |

每篇不需要从头逐句阅读。优先阅读摘要/引言、方法总图、核心定义、实验变量、
失败分析和局限；训练超参数、全部相关工作和工程部署细节先跳过。Codex 应先为每组
生成一页 decision brief，研究者再读原文定位，避免无目的精读。

## 9. 仍需本人确认的两个信息包

Codex 先根据仓库和现有对话预填，研究者只作纠错和确认：

1. **开题证据包**：仓库外正式成果、个人工作边界、导师的 50% 口径，以及学校
   开题/预答辩/送审时间节点；
2. **真实研究环境包**：未入仓的北京项目日志与反馈、首批适合承担目标用户/领域
   校准/评测审计角色的人选，以及数据、记录和人体参与研究的使用边界。

不要求研究者先整理完整档案；缺失项可标为 unknown，由 Codex 后续逐项定位。
