# 开题证据矩阵

> 版本：v0.3，2026-08-02
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
- 研究内容一：**基于多智能体的城市森林遥感工作流构建**
- 研究内容二：**基于科学约束的城市森林遥感知识库构建**
- 研究内容三：**面向用户的城市森林遥感智能体系统验证**
- 内部科学主线：**规划机制 → 科学约束 → 可靠性评测**
- 长期设计原则：**轨迹原生、科学约束、评测驱动、经验可学习**

上述版本已向导师汇报且未收到新增修改意见，可作为当前执行基线；这不是方法 claim、
人体参与方案或最终送审题目的正式批准证据。

## 3. 研究内容一证据

| 证据对象 | 状态 | 当前能支持 | 当前不能支持 | 指针 |
| --- | --- | --- | --- | --- |
| ExpertsRS 已发表论文 | PUBLISHED | 多智能体完成遥感分析的初步可行性；Data--Tools--Brain；两项案例；20 条请求轻量比较 | 类型化工作流、图验证、定向修复、持久状态、轨迹可靠性 | DOI `10.1080/20964471.2025.2600178` |
| 18 个标准遥感工具和统一 schema | VERIFIED-ASSET | Tool 层已从 notebook 内零散函数升级为可注册、可调用工具集 | 完整 runtime、可靠规划或科学正确性 | `URSA/ExpertsRS/tools/registry.py` |
| 工具测试 | VERIFIED-ASSET | 当前工具接口和注册表具有可执行检查；本地检查 13/13 通过 | Agent 端到端任务成功率 | `URSA/ExpertsRS/test_tools.py` |
| 当前 notebook 调度 | VERIFIED-ASSET | 已有多角色编排和 tool-first 调用基础 | 显式运行状态、事件日志、检查点、图验证与重放 | `URSA/ExpertsRS/ExpertsRS_notebook.ipynb` |
| 新增方法边界 | FROZEN-DESIGN | `TaskSpec`、`OperatorSpec`、`WorkflowGraph`、验证、定向修复和 `WorkflowTrace` 已形成闭合假设 | C1 有效性 | `URSA/docs/thesis/ch1_upgrade_freeze_20260729.md` |
| P0--P3 匹配 pilot | OPEN | — | 新方法相对自由规划、结构化规划和图验证的增量 | 待 Chapter 1 执行计划创建 |

### 研究内容一开题门禁

1. 至少一组可版本化 schema 示例；
2. 一个可运行 validator；
3. 一个定向修复或正确停止路径；
4. 一次小型 P0--P3 匹配试跑；
5. 明确区分已发表结果与新增结果。

## 4. 研究内容二证据

| 证据对象 | 状态 | 当前能支持 | 当前不能支持 | 指针 |
| --- | --- | --- | --- | --- |
| 41 张 canonical knowledge cards 与 42 个 registry assets | VERIFIED-ASSET | 领域知识资产、schema、taxonomy、来源登记和可追溯表示已具有较大工作基础 | 每个 card claim 已获得论文级证据支持 | `chapter2-urban-forest-knowledge/assets/cards/` |
| 147 条 claim ledger（129 条为 2026-07-13 快照） | VERIFIED-ASSET | 已建立原子知识候选、来源、核验动作和状态的治理对象；当前 143 条 candidate、4 条 needs-review | 147 条科学约束、人工规则或 thesis-safe 知识；当前 147 条 evidence span 均为 TBD | `chapter2-urban-forest-knowledge/config/card_claims.csv` |
| 既有资产向科学约束的迁移解释 | FROZEN-DESIGN | cards/claims/evidence 被定位为知识与证据底座；模型按任务提出约束、治理准入、runtime 执行和结果评测的链条已定义 | 已完成自动约束学习、专家成本下降或错误更新防护 | `chapter2-urban-forest-knowledge/docs/20260731_ch2_asset_reinterpretation_and_harness_transition.md` |
| G1--G4 / Wave pilot | DIAGNOSTIC | 结构化知识和治理字段能够改变部分规划输出，值得进入匹配机制实验 | 一般规划质量提升；executed constraints 优于 RAG；工具正确性不变 | `chapter2-urban-forest-knowledge/PLAN.md` |
| 直接竞争与创新审计 | VERIFIED-ASSET | 已识别 AgentSpec、RNSP、KISS、KAG/WTS/OG-RAG 等威胁，禁止泛化创新语言 | 新颖性已经闭合 | `docs/20260713_ch2_innovation_and_evidence_audit.md` |
| Task-conditioned epistemic contract | FROZEN-DESIGN | 以最小科学边界改变行动的机制对象已经定义 | 约束确实降低科学风险 | `thinking-space/task-conditioned-epistemic-contract-spec.md` |
| B0--B5/A1/A2 匹配实验 | FROZEN-DESIGN | 已能区分任务、通用 self-check、文本内容、结构化内容、注入与执行 | 正式实验结果；人类校准 | `experiments/briefs/ch2-epistemic-contract-evaluation-v0.1.md` |
| WTS-informed 知识生命周期 | FROZEN-DESIGN | 经验触发 candidate update、证据准入和版本化 ledger 具有可执行候选设计 | 自主知识进化或维护成本下降 | `docs/20260724_ch2_wts_absorption_and_stability_gate.md` |

### 研究内容二开题门禁

1. 从直接竞争审计中选择最小、可防守的核心 claim；
2. 从 ledger 中只选择一个任务相关的 10--20 条候选切片，补齐证据原文和适用边界；
3. 冻结一个不泄露完整答案的最小 `ScientificContract`；
4. 完成至少一个 B0--B5 小型机制任务；
5. 用小规模 human-reference / model-proposed / governed 对照检验规则编写负担与错误准入；
6. 由领域人员确认约束本身正确，并校准自动评分；
7. 知识生命周期保持为可选扩展，不抢占基础机制。

## 5. 研究内容三证据

| 证据对象 | 状态 | 当前能支持 | 当前不能支持 | 指针 |
| --- | --- | --- | --- | --- |
| 北京 2025 Route B v1 方法与制图基线 | VERIFIED-ASSET | 多源弱标签、时序稳定性、空间纯度、分层抽样、RF 和制图流程已闭合并冻结 | 八类制图整体可靠；Agent 可靠性 | `urbfo-agent-demo/docs/reports/summary_routeb_v1_freeze_20260705.md` |
| 7,351 行训练表与方法冻结 | VERIFIED-ASSET | 当前场景已存在可复现任务、真实数据限制和专业制品 | 新第三项研究的任务/评分有效性 | `urbfo-agent-demo/experiments/results/routeb_v1_method_freeze_20260705.json` |
| 470 点历史回归诊断 | DIAGNOSTIC | Level 1 与八类结果的已知能力和错误类型 | 最终一次性未查看确认集；可靠性验证 gold | `urbfo-agent-demo/experiments/results/routeb_seasonal17_reused_v0_validation_20260705.json` |
| 北京项目过程资产 | VERIFIED-ASSET / 待结构化 | 当前可定位 107 条 GEE 运行记录、64 条结果 manifest 和 2,538 行弱标签决策日志，可作为任务、故障、恢复和经验 episode 候选来源 | 已经构成标准 Agent trace、可回放 episode 或可训练 RL trajectory 数据集 | `urbfo-agent-demo/metadata/runs/gee_routeb_runs.jsonl`; `experiments/results/manifest.csv`; `docs/method_notes/weak_label_decision_log_2026-06-15.md` |
| 第三项研究主线 | FROZEN-DESIGN | `EvalTask--TrialTrace--Outcome--Evaluation` 与任务/轨迹/用户三层验证边界已接受 | 可执行 benchmark、评分器有效性和跨方法结果 | `research-harness/decisions/DEC-2026-0729-eval-driven-experience-ready-storyline.md` |
| 制图资产到评测对象的映射 | FROZEN-DESIGN | 已将任务环境、弱样本方法、样本、制品、故障和过程历史分离；明确“trajectory candidate”边界 | 可执行任务集和已清洗 episode dataset | `urbfo-agent-demo/docs/plans/ch3_asset_to_eval_and_hitl_plan_20260731.md` |
| 面向生态学家和绿化管理者的用户验证 | FROZEN-DESIGN | 目标用户、遥感专家和评测审计角色已经区分；专家可达性不再是主要风险 | 真实任务、rubric 有效性、伦理/数据边界和正式样本设计 | `urbfo-agent-demo/docs/plans/ch3_asset_to_eval_and_hitl_plan_20260731.md` |
| 最小跨方法试跑 | OPEN | — | 第三项研究的独立实证闭环 | 待 Chapter 3 evaluation MVP |

### 研究内容三开题门禁

1. 定义目标用户可理解、可判断的任务协议和 intended-use 边界；
2. 冻结第一批真实任务族、成功条件和关键失败；
3. 建立一次 trial 的最小轨迹格式，并把历史日志明确标为 episode reservoir；
4. 实现至少一个确定性评分器和一份人工 rubric；
5. 先用两名目标用户、两名领域专家校准 6--10 个任务候选，按争议和风险扩展；
6. 确认人体参与/伦理审查与反馈数据使用边界；
7. 完成至少一次传统流程/通用 Agent/URSA 变体的跨方法试跑。

## 6. 对“已完成 50%”的当前解释

当前可以稳妥计算为已完成基础的内容：

- 一项已发表多智能体遥感论文及其案例和轻量 benchmark；
- URSA Tool 层升级；
- Chapter 2 知识资产、治理骨架、诊断 pilot 和正式实验设计；
- 北京 2025 制图方法、样本、结果与大量过程资产；
- 新总故事线、章节边界和第一项研究新增方法边界。

当前不能按已完成结果计算的内容：

- 第一项新增规划、验证与修复机制的正式 pilot；
- 第二项 B0--B5 的匹配结果及人类校准；
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
4. 决定第二项研究选择基础 contract，还是把生命周期扩展纳入正式承诺。

### H2：面向用户的验证构念与人工校准

Codex 负责生成任务模板、rubric、试验协议和分析代码；研究者本人负责：

1. 从 Codex 预填的任务包中确认哪些问题代表生态学家和绿化管理者的真实决策；
2. 批准目标用户、遥感专家和评测审计者的职责，不亲自设计完整 rubric；
3. 判断用户效用、科学正确性、关键失败和可接受风险；
4. 协调首批小型校准组，并批准真实项目数据、反馈和日志的使用边界；
5. 在正式收集研究数据前确认伦理/人体参与审查要求。

除 H1、H2 外，证据清点、文献候选筛选、schema、validator、pilot 实现、评测
harness、结果分析和文档维护可由 Codex 主导，在门禁处提交简短决策包。

## 8. 研究者精读清单

不建议广泛追逐 Agent 文献。第一轮只精读以下五组，并只读与决策有关的部分：

| 材料 | 精读部分 | 用来决定 |
| --- | --- | --- |
| 自己的 ExpertsRS 论文 | contributions、method、evaluation、limitations | 哪些证据已经发表，第一项新增边界在哪里 |
| Spatial-Agent | problem、GeoFlow Graph、constraints、ablation、limitations | 工作流图之外还必须增加什么 |
| GeoAgentBench 与 GeoDisaster | task construction、environment、grader、failure、baseline、limitations | 第三项如何避免重复现有地理 Agent benchmark |
| WTS 加一个最接近的约束方法（由 Ch2 comparator audit 选定） | update trigger、supervision、admission、evaluation | 第二项是稳定 contract，还是增加受控知识演化 |
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
