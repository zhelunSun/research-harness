# 华为 Harness 实习申请—论文协同计划

> 版本：v2026.08.05
> 状态：active career–thesis sidecar；定向简历已形成固定面试基线
> 适用期：2026 年 8 月简历投递至 2026 年 9 月开题完成前
> 边界：本文件管理求职、开题和共用产物的协同，不是论文第四项研究内容，
> 不改变 `THESIS_STATE.md`、`ideas/chapter_ideas.md` 或下游实验的证据状态。
> 上游依据：`THESIS_STATE.md`、`process/current_execution_plan_20260802.md`、
> `ideas/agent_frontier_alignment.md`
> 执行依据：
> [`ch2-s0-validation-contract-sprint-v0.1.md`](../../chapter2-urban-forest-knowledge/experiments/briefs/ch2-s0-validation-contract-sprint-v0.1.md)
> 职业材料内容源：
> [`career_materials_master_content_20260802.md`](career_materials_master_content_20260802.md)
> 固定简历：
> `../../zhelun-cv/output/pdf/Sun_Zhelun_CV_Huawei_Harness_zh.pdf`
> （2026-08-05 12:40:29，SHA-256
> `9F983181B1B0D72CD87B5B8AD792811CB691EA2CA2E8F9AA8EA994B41E1464F1`）
> 面试与后续求职执行底稿：
> [`huawei-harness-interview-foundation-v1.md`](../../zhelun-cv/career/interviews/huawei-harness-interview-foundation-v1.md)

## 1. 当前核心决策

采用“先进入招聘池，再按明确信号逐级投入”的策略：

1. 以 2026-08-05 固定 PDF 作为当前投递与面试准备基线，不等待新的论文结果再进入招聘池；
2. 通过朋友将简历递交给 Harness 团队主管，并同步确认正式投递、机试和面试节奏；
3. 简历 v1.0 不等待新的论文结果、完整 Harness 原型或 RL 项目；
4. 在出现主管明确兴趣、面试安排或实习时间讨论前，不改变 9 月开题和当前论文执行优先级；
5. 出现实质信号后，再形成可向导师说明的开题、毕业、实习时间和成果边界方案；
6. 实习开始时间原则上放在开题之后。任何开题前立即全职到岗的要求，在获得具体条件
   且与导师沟通前不作承诺。

申请、面试和入职是三个不同决策点。当前只授权前两个步骤中的低成本探索，不以“已经
投递”推导“必须立即调整论文或入职”。

## 2. 求职项目的工作定位与术语边界

### 2.1 工作名称

对求职和跨项目技术沟通，采用：

> **Scientific Agent Harness for Observation-Intensive Science**
> **面向观测密集型科学任务的执行、科学约束与可靠性评测基础设施**

该名称承接当前论文的“轨迹原生、科学约束、评测驱动、经验可学习”原则，但不是新的
学位论文总题目或章节标题。

### 2.2 “观测密集型”与“知识密集型”的分工

- **观测密集型科学**用于定义 motivation 和任务类别：任务依赖开放世界观测、多源异构
  数据、长工具链，且通常缺少即时、干净的环境验证信号；
- **知识密集、工具密集**用于描述这些任务的结构特征：规划需要领域知识、方法适用条件、
  证据义务和异构工具协同；
- 对外一句话可表述为：

  > 面向缺乏即时验证信号、同时知识与工具密集的观测型科学任务，构建可执行、可约束、
  > 可追踪并可评测的 Agent Harness。

- 正式实验证据仍限定在 Earth Observation / 遥感 / 城市森林任务。气候、生态、水文等
  只作为 motivation 和 transfer hypothesis，在没有跨域实验前不声称已验证通用性。

用户提到的未发表“观测密集型科学”文章是 motivation 候选来源。进入简历、开题或技术
报告前，需要补齐文章标题、文件位置、作者贡献和当前投稿状态；未发表时不得把它写成
已发表成果，也不能用其替代论文原文或实验结果。

## 3. 论文主线与 Harness 岗位的共用结构

| 论文对象 | 当前论文职责 | 对 Harness 岗位的可迁移能力 | 状态边界 |
| --- | --- | --- | --- |
| 研究内容一 | 结构化工作流、验证、定向修复、`WorkflowTrace` | Agent Runtime、planning、tool orchestration、trace | typed workflow 与 ReAct routing 共 12 项回归测试已通过，scripted no-API 真工具 pilot 已运行；trace 计数缺陷、真实 LLM 规划和 P0--P3 匹配效果仍待处理 |
| 研究内容二 | evidence ledger、`ScientificContract`、约束行动效应 | Memory/knowledge、context、verifier、guardrail、action-changing evaluation | 当前 P0；只报告已完成闭环 |
| 研究内容三 | task/trial/trace/outcome/user evaluation | Benchmark、Evaluation Harness、failure/recovery analysis | 任务和评分器仍在建设 |
| 经验可学习接口 | episode/trajectory candidate 与反馈类型 | trajectory data、reward/verifier、post-training bridge | 只承诺 experience-ready，不承诺 Agent RL 收益 |

职业叙事使用同一批真实资产，但从系统问题、接口、实现和证据角度组织；论文叙事从科学
问题、因变量、实验控制和 claim 边界组织。两种表述共享一个证据源，不允许为了求职把
`FROZEN-DESIGN` 或 `OPEN` 改写为已验证结果。

## 4. 简历的滚动版本与证据语法

### 4.1 证据层

| 层级 | 当前代表成果 | 简历允许动词 |
| --- | --- | --- |
| Published | ExpertsRS 第一作者论文 | 发表、提出、完成案例/benchmark |
| Released | Sheaf、Skill Factory、PyPI/MCP/CLI | 独立开发、发布、维护、实现 |
| Delivered | 上海气象局 Qwen3-32B 专报项目 | 部署、交付、压缩耗时 |
| Verified asset | 18 个工具、测试、知识卡片、ledger、历史运行资产 | 建设、实现、测试通过、完成清点 |
| Ongoing research | ScientificContract、B0--B5、trace/eval 闭环 | 正在构建、已定义、当前推进、拟检验 |
| Research agenda | Self-evolution、Agent RL、SFT/GRPO、大规模 runtime | 研究兴趣、后续接口；不写作项目结果 |

### 4.2 版本节奏

- **v1.0（2026-08-05 固定）**：只依赖已有成果；作为朋友递交、主管预读、正式投递和面试准备的共同基线；
- **v1.1（S0-7/Gate A 后）**：加入 contract、trace、grader、行动变化和失败案例的
  第一批可检查结果；
- **v1.2（主管反馈后）**：按 Runtime / Evaluation / Tool-Memory / trajectory data 的
  实际需求重新排序，不凭 JD 猜测无限扩展。

v1.0 的目标岗位写为：

> **Harness 实习生｜Agent Runtime / Evaluation / Tool & Memory 方向**

进行中研究在 v1.0 中只占一个项目，不覆盖 Sheaf、ExpertsRS 和气象交付等更强的已完成
证据。

## 5. 开题与求职的唯一共用闭环产物

不另建一个纯求职 demo。2026-08-04 已完成的 Chapter 1 最小 workflow runtime
作为当前可演示的执行骨架；新增研究与求职共用产物继续采用 Chapter 2 P0：

> **ScientificContract × WorkflowTrace × Evaluation 最小闭环**

执行仍以下游
`ch2-s0-validation-contract-sprint-v0.1.md` 的 S0-1--S0-8 为准。本计划不修改其任务、
实验条件、证据准入或停止规则。

面试中必须把两类证据分开：现有 workflow pilot 证明接口、validator、局部修复、显式停止
和 trace 可以运行；Chapter 2 闭环用于检验科学约束能否正确改变行动。前者不替代后者，
两者都不提前证明真实用户效用。

### 5.1 论文侧最低产物

1. `UF-VAL-CLASS-01` 与 `UF-VAL-HAB-01` 两个冻结 fixture；
2. 8--12 条候选 claim 的 exact-span、适用性与准入记录；
3. human-reference 和 model-proposed contracts；
4. B0--B5 共 12 次 dry run；
5. `constraint selected -> violation detected -> action requested -> output changed`
   的可审计 trace；
6. add-validation、ask、reject、downgrade、科学正确性、成本和 repair count 的分离报告；
7. Gate A 的 retain / narrow / fallback 建议。

### 5.2 求职侧派生产物

只从已经完成的论文侧工件派生，不增加一套实验：

- 一页问题—架构—评测技术摘要；
- 一张 `task -> contract -> runtime -> trace -> grader -> update candidate` 架构图；
- 一条可阅读的成功 trace 与一条失败/错误约束 trace；
- 一张 B0--B5 行动变化、成本和失败类型表；
- 一个五分钟面试讲述：问题、设计取舍、失败、当前证据边界、下一步。

S0 dry run 只证明管线和信号可观测，不在简历中写成方法有效性定论。若 B2/B3 与 B4 等效、
B5 只增加成本或错误约束被机械执行，负结果仍作为 Harness 设计和评测能力的面试证据，
但论文 claim 按现有 fallback 收窄。

## 6. 招聘信号与投入门禁

### Gate R0：递交与流程发现（立即执行）

- 朋友将 CV v1.0 发给主管或指定邮箱；
- 确认目标岗位和内部投递入口；
- 确认正式提交是否立即触发限时机试、通常提前量、考试语言/题型、结果有效期或重试规则；
- 确认团队地点、最早到岗、期望时长、现场办公要求和当前 headcount 紧迫度。

### Gate R1：明确兴趣

以下任一项视为明确信号：

- 主管或技术人员提出针对经历的进一步问题；
- 收到机试、技术面试或简历沟通安排；
- 开始讨论实习起止时间、地点或具体工作方向。

只有进入 R1 后，才提高面试准备投入，并准备导师沟通包。泛泛的“可以内推”或系统自动
回执不构成 R1。

### Gate R2：导师沟通

在作出到岗承诺之前，向导师提交一个完整方案：

1. 9 月开题与按 2027 年 10 月毕业倒排的里程碑；
2. 实习工作与 Agent Harness / Evaluation 论文主线的对应关系；
3. 开题后到岗、实习期间论文保活和阶段汇报安排；
4. 华为内部知识产权、数据、代码和论文发表边界；
5. 学位论文不依赖企业内部成果也能完成的 fallback。

R0 阶段不需要因探索性投递立即改变导师预期；进入 R1 且时间安排开始具体化后，不应把
沟通拖延到已经签署或承诺到岗。

### Gate R3：接受与到岗

只有同时满足以下条件才进入：

- 9 月开题不被破坏，或导师明确同意另一安排；
- 团队方向与 Harness/Evaluation 主定位一致；
- 时间、地点、强度和期限可与毕业倒排兼容；
- 学术成果、企业 IP 和公开项目边界清楚；
- 论文具有不依赖实习产出的独立完成路径。

## 7. 开题前资源配置

### R0、尚无面试日期

- 70%：开题与 Chapter 2 共用闭环；
- 15%：机试基础训练；
- 10%：简历、项目讲述和证据核对；
- 5%：内推与流程协调。

### R1、7--10 天内有机试或面试

- 45%：开题与研究保活；
- 35%：机试和技术面试；
- 15%：项目材料与模拟讲述；
- 5%：协调。

### 开题前最后两周

- 原则上将开题恢复到约 80%；
- 机试保留最低稳定训练；
- 除已约定面试外，不新开大规模求职项目、RL 训练或通用 Runtime 开发。

## 8. 立即行动清单

### 未来 72 小时

- [x] 建立简历事实表：项目、个人贡献、代码/论文链接、技术栈、规模、结果、证据状态；
- [x] 完成并固定华为 Harness 定向中文 CV v1.0；
- [x] 以固定 PDF 建立逐项目的面试证据、风险与回退口径；
- [ ] 核实可实习时间、地点和持续月份的暂定答案；
- [ ] 请朋友完成主管预读/递交并回答 Gate R0 流程问题；
- [ ] 启动每日 60--90 分钟机试基础训练；
- [ ] 定位未发表的 observation-intensive science 文章并登记状态，暂不按发表成果使用。

### 接下来 1--3 周

- [ ] 按 Chapter 2 active sprint 推进 S0-1--S0-8，不为简历另建分支实验；
- [ ] 从已完成 workflow pilot 生成一页技术摘要、成功 trace 和受控终止 trace；
- [ ] 按面试底稿完成 90 秒主叙事、四个项目深挖和 claim-safe 追问演练；
- [ ] 收到 R1 信号后准备导师沟通包；
- [ ] S0-7/Gate A 后更新 CV v1.1，不等待更大规模正式实验。

## 9. 明确非目标

- 不把职业 sidecar 写成论文第四项研究内容；
- 不为贴合 JD 在开题前承诺大规模 Agent RL、SFT/GRPO 或开放式自进化；
- 不把未发表文章、候选 claim、dry run 或 frozen design 写成已验证成果；
- 不用“观测密集型科学”的宽叙事替代 EO/城市森林的正式证据；
- 不使毕业依赖华为内部代码、数据、模型、日志或发表许可；
- 不因滚动招聘无限等待完美成果，也不因探索性投递提前打乱开题。

## 10. 维护规则

- 招聘状态只在 R0--R3 发生变化或获得主管实质反馈时更新；
- 论文证据状态继续由 `evidence/opening_evidence_matrix.md` 与下游原始工件维护；
- 简历每条量化表述必须能指向公开链接、本地工件或人工确认；
- 求职反馈可以提出论文/工程候选方向，但必须经原有 thesis decision/proposal 流程才能进入
  canonical idea；
- 论文结果可以升级简历，简历语言不得反向升级论文 claim。

## 11. 云端优先的简历—网站工作模式

### 11.1 能力边界

当前 Codex 桌面任务依赖本机和当前会话；电脑关机后，不能继续进行新的阅读、判断、写作
或代码修改。GitHub Actions 可以在云端继续执行已经定义好的构建、测试和部署，但它不是
能够自行整理内容和作出研究判断的持续 Agent。

因此，目标不是假设本机永久在线，而是让状态、源文件、构建结果和待决策问题全部进入
云端仓库，使任何后续会话都能从稳定状态继续。

### 11.2 推荐架构

1. **私有 career-materials GitHub 仓库作为职业材料源**：保存事实表、证据状态、LaTeX
   简历源码、生成脚本和版本记录；手机号等不进入公开网站仓库；
2. **Overleaf 作为人工审阅与排版界面**：如果账户具有 Premium GitHub/Git 同步，则从
   GitHub 创建新的关联项目并手动 Pull/Push；Overleaf 的 GitHub 同步不是自动同步，且不能
   将一个既有 Overleaf 项目直接关联到一个既有 GitHub 仓库；
3. **GitHub Actions 作为云端构建器**：每次 push 编译 LaTeX、保存 PDF artifact、检查链接
   和可选 lint；即使本机关机，已触发的构建仍可完成；
4. **公开网站仓库保持独立**：`zhelunSun/zhelunsun.github.io` 继续使用现有 Next.js +
   GitHub Pages；只接收职业材料源中的公开子集；
5. **PR 作为人工门禁**：Codex 准备分支、内容差异和构建结果；研究者只确认定位、敏感边界、
   关键 claim 和最终 merge/publish。

初期不做带跨仓库 token 的全自动发布。先以一个主内容文件生成简历与网站候选 patch，
人工批准后分别合入，可减少泄密、错误覆盖和 Overleaf 冲突风险。

### 11.3 版本与发布流程

`facts/evidence -> shared narrative -> resume-cn -> website public subset -> build -> review -> publish`

- `draft`：Codex 可自主整理和改写，不公开；
- `candidate`：PDF 与网站 patch 均构建通过，等待研究者关键决策；
- `approved-resume`：允许发给朋友/主管，不自动更新网站；
- `approved-public`：允许合入网站 master，由现有 GitHub Actions 发布；
- `superseded`：保留历史，不继续传播旧 PDF 链接。

### 11.4 当前迁移顺序

1. 先用本仓的 `career_materials_master_content_20260802.md` 完成内容与证据核对；
2. 获取当前 Overleaf LaTeX 源码或 Git URL，不在网页编辑器里直接大段重写；
3. 获得授权后创建私有 career-materials 仓库和云端 PDF build；
4. CV v1.0 获批并递交后，再生成网站内容 patch；
5. 网站公开更新单独确认，不与简历递交绑定。

## 12. 固定简历驱动的面试与后续求职规划

2026-08-05 固定简历形成以下完整能力链，而不是四个互不相干的项目：

> **遥感 Agent 可行性与 benchmark（ExpertsRS） → Tool/Memory 与工程可靠性
> （Sheaf） → 可验证工作流、科学约束与分层评测（Scientific Agent Harness） →
> 真实行业部署和人工审核闭环（上海气象局）**

面试准备按照“已完成证据—当前原型—待验证研究”三层组织：

| 层级 | 固定简历中的主要内容 | 面试责任 |
| --- | --- | --- |
| 已完成证据 | ExpertsRS 论文与轻量 benchmark、Sheaf PyPI/CLI/MCP、气象局交付、三篇第一作者论文 | 给出问题、个人贡献、技术实现、数字口径和局限 |
| 当前原型 | 18 个工具、typed workflow、validator、targeted repair、stop、`WorkflowTrace` | 现场可定位代码/测试/trace，不把原型效果写成论文结论 |
| 待验证研究 | `ScientificContract`、B0--B5、任务—轨迹—用户分层评测 | 使用“提出、正在构建、拟检验”；清楚说明通过、失败和回退条件 |

固定 PDF 不因本规划自动修改。出现以下任一证据升级时，才打开下一版简历 copy review：

1. Chapter 2 形成 exact-span contract、错误约束控制和可审计 action-change trace；
2. 完成至少一次匹配的任务—轨迹—结果跨方法试跑；
3. 用户效用 rubric 获得伦理/数据边界确认并完成小型校准；
4. 招聘团队给出明确的 Runtime、Evaluation、Tool/Memory 或 trajectory 侧重点。

逐项目讲述、风险口径、问题库、证据包和后续岗位变体由
[`huawei-harness-interview-foundation-v1.md`](../../zhelun-cv/career/interviews/huawei-harness-interview-foundation-v1.md)
维护；本文件只维护它与论文优先级、招聘信号和版本门禁的关系。
