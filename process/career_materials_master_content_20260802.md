# 职业材料主内容：Harness 定向简历与个人网站

> 版本：v2026.08.02-draft
> 状态：working content source；待研究者核实关键事实
> 用途：为华为 Harness 中文简历、个人网站和技术面试提供共同事实与分层叙事
> 边界：本文件不是公开网页，不替代论文 evidence matrix，也不授权对外发布。
> 关联计划：`huawei_harness_internship_thesis_alignment_20260802.md`

## 1. 内容模型

所有职业材料从同一事实层派生，但按受众使用不同表达：

| 层 | 作用 | 简历 | 网站 |
| --- | --- | --- | --- |
| Fact | 学校、项目、链接、技术栈、数量、结果 | 只放最强证据 | 可完整展示 |
| Evidence status | published/released/delivered/verified/ongoing/proposed | 必须显式区分 | ongoing/research agenda 可展开 |
| Narrative | 为什么这些工作属于同一条路线 | 针对 Harness 岗位 | 面向长期个人身份 |
| Public boundary | 是否可公开、是否涉及合作方/IP | 默认保守 | 公开前逐项确认 |

简历和网站不得各自维护互相冲突的学位名称、项目日期、版本号和成果状态。

## 2. 统一职业定位

### 2.1 中文定位

> **清华大学博士研究生｜Agent Harness、Evaluation 与科学工作流｜LLM 多智能体与
> Tool/Memory 基础设施**

### 2.2 English positioning

> **Ph.D. Candidate at Tsinghua University | Agent Harness, Evaluation, and
> Scientific Workflows**

### 2.3 核心叙事

> 面向缺乏即时验证信号、同时知识与工具密集的观测型科学任务，研究并开发可执行、
> 可约束、可追踪和可评测的 Agent 系统。以遥感和城市森林为主要验证场景，工作覆盖
> 多智能体工作流、Tool/Skill/Memory 基础设施、科学约束、运行轨迹和可靠性评测。

该叙事把遥感解释为高价值验证环境，而不是把个人限定为 GIS 应用开发者。

## 3. 简历顶部摘要草案

> 清华大学地球系统科学系博士研究生，聚焦 Agent Harness、可执行科学工作流与可靠性
> 评测。第一作者发表 LLM 多智能体系统论文；独立开发并维护 PyPI 开源项目 Sheaf
> （MCP/CLI，1024 项测试）；具备本地大模型部署和真实行业场景交付经验。希望参与
> Agent Runtime、Evaluation、Tool/Skill/Memory 与轨迹学习基础设施研发。

目标岗位：

> **Harness 实习生｜Agent Runtime / Evaluation / Tool & Memory 方向**

## 4. 定向简历内容草案

### 4.1 Sheaf — Agent 知识与上下文基础设施

**状态：Released / maintained**
**链接：** `https://github.com/zhelunSun/sheaf-ai`

- 独立设计并开发 Local-First 的 Agent 知识基础设施，发布至 PyPI v0.7.0；构建多源内容
  采集、结构化摘要、证据溯源知识卡片和全文/语义检索的端到端管线。
- 开发 CLI、MCP Server 与 MCP Resources，支持 Codex、Claude Code、Cursor 等 Agent
  搜索和消费个人知识；将高频能力收敛为 4 个核心 MCP Tools，降低工具描述的上下文开销。
- 建立语义化退出码、可迁移 Markdown/JSON 数据存储和多提供商配置，使用 1024 项自动化
  测试覆盖核心管线与接口。

**待核实后可增加：** PyPI 下载量、真实用户数、外部 issue/discussion、跨平台安装成功率。

### 4.2 Scientific Agent Harness for Observation-Intensive Science

**状态：Ongoing research；不得写作已验证通用方法**

- 面向缺乏即时验证信号、知识与工具密集的遥感研究任务，正在构建评测驱动的 Scientific
  Agent Harness，统一表示任务、工具、工作流、运行轨迹、科学约束与最终结果。
- 定义 `TaskSpec`、`OperatorSpec`、`WorkflowGraph` 和 `WorkflowTrace`，将工具调用、
  观察、制品、错误、修复、成本与 outcome 组织为可审计轨迹。
- 建立 41 张结构化知识卡片与 147 条候选 claim ledger；当前以城市森林制图验证任务推进
  B0--B5 对照，检验最小 `ScientificContract` 能否触发 add-validation、ask、reject、
  repair 或 downgrade 等行动变化。
- 完成 107 次历史 GEE 运行和 64 份结果 manifest 的资产清点，按 episode/trajectory
  candidate 管理，为失败诊断、经验检索和后续训练数据构建提供接口。

**升级条件：** 只有 S0-7/Gate A 产生可检查结果后，才在 v1.1 中增加 trace、grader、成本、
行动变化和失败案例数据。

### 4.3 ExpertsRS / URSA — LLM 多智能体遥感分析

**状态：Published + verified assets**
**论文：** `https://doi.org/10.1080/20964471.2025.2600178`
**代码：** `https://github.com/zhelunSun/URSA`

- 基于 AutoGen 构建多智能体遥感分析系统，实现需求澄清、任务定义、工具执行和结果报告
  工作流；完成两项案例研究与 20 条请求的轻量 benchmark，以第一作者发表于
  *Big Earth Data*。
- 将原型工具层升级为 18 个可注册遥感工具及 OpenAI 风格 Tool Schema，覆盖数据读取、
  指数计算、空间分析和可视化；当前本地工具接口检查 13/13 通过。

### 4.4 上海市气象局气象专报生成智能体

**状态：Industry delivery；公开边界待核实**

- 面向中心气象台专报业务，部署本地 Qwen3-32B 驱动的生成智能体，融合气象观测、业务
  规则和历史案例，生成符合业务规范的专报初稿。
- 将平均约 4 小时的人工撰写流程压缩至分钟级，并部署定时生成脚本，降低预报员重复性
  工作负担。

**待核实：** 正式项目/实习名称、个人负责范围、部署栈、数据规模、验收方式、是否允许在
公开网站写出合作单位和模型名称。

### 4.5 Skill Factory — Agent Skill 生命周期工具

**状态：Released**
**链接：** `https://github.com/zhelunSun/skill-factory`

- 开源 Agent Skill meta-skill，将 Skill 开发抽象为需求锁定、资料收集、知识蒸馏和版本发布
  四阶段 SOP，支持 Skill 的可复用、可检查、可发布和持续迭代。

### 4.6 Agent OS

**状态：需核实后决定是否保留**
**网站当前链接：** `https://github.com/zhelunSun/agent-os`

网站当前将其描述为 file-based multi-agent coordination layer，并声称用于 daily production
coordination。该项目未出现在当前工业简历和本地核心证据矩阵中。更新前需要核实：

- 仓库是否公开、当前可运行状态和个人贡献；
- “used in production”是否准确且适合公开；
- 与 Scientific Agent Harness / research-harness 是否重复或造成概念混乱。

在核实前不进入华为定向简历；网站可暂时降级或移至 Other Projects。

## 5. 教育与论文

### 5.1 教育

- 清华大学，地球系统科学系，博士研究生，2023.09--预计 2028.06；
- 中国农业大学，地理信息科学，理学学士，2019.09--2023.06，GPA 3.85/4.00。

**必须人工确认：** 正式学籍专业/学位名称。个人网站目前同时出现
“Ph.D. Candidate in Ecology”和“Ph.D. Candidate in AI & Remote Sensing”，与现有中文简历
不一致。未确认前，英文网站优先使用不虚构专业的：

> Ph.D. Candidate at Tsinghua University

### 5.2 精选论文排序

1. **Sun, Z.**, Zhou, Y., & Yang, J. (2026). An LLM-based multi-agent system for
   remote sensing analysis. *Big Earth Data*.
2. **Sun, Z.**, Li, X., Wei, H., Feng, Z., & Yang, J. (2024). Landsat image
   classification using a deep learning model and multiple-source training samples.
3. **Sun, Z.**, Xiao, B., Zhao, Z., et al. (2023). Loading and service implementation
   of GF-1 satellite data based on Open Data Cube.
4. Zhang, Y., **Sun, Z.**, et al. (2026). Measuring perceived green volume for
   quantifying urban green exposure.

华为简历展开第 1 篇；其余压缩。个人网站保留完整列表。

### 5.3 未发表 observation-intensive science 文章

当前只在本地找到由其派生的 `KC-OBSERVATION-SCIENCE-ANCHOR.md`，未找到原稿。需要登记：

- 正式标题和语言；
- 原稿文件/Overleaf 项目位置；
- 作者及个人贡献；
- 当前状态：draft / internal review / submitted / rejected / dormant；
- 哪些段落可以作为 motivation，哪些 claim 已有外部来源支持。

在完成登记前，它只支撑研究动机整理，不进入 Publications。

## 6. 技术能力草案

- **Agent Systems：** multi-agent workflow、tool/function calling、MCP、RAG/knowledge
  layer、context engineering、trace/evaluation design；
- **Engineering：** Python、pytest、CLI/package development、FastAPI、Git、Linux、SQL、
  LaTeX；
- **Machine Learning：** PyTorch、scikit-learn、pandas、NumPy、SciPy；
- **Scientific/Geospatial：** Google Earth Engine、GDAL、rasterio、ArcGIS、ENVI。

暂不写入：分布式训练、DPO/GRPO/RL、Reward Model、Verifier training，除非补充真实项目证据。

## 7. 个人网站英文内容草案

### 7.1 Hero

**Title**

> Ph.D. Candidate at Tsinghua University
> Agent Harness · Evaluation · Scientific Workflows

**Short introduction**

> I build agent systems for observation-intensive scientific tasks—open-ended,
> knowledge- and tool-intensive workflows where the environment rarely provides an
> immediate verification signal. Using remote sensing and urban-forest analysis as my
> primary testbed, I work on agent runtime, scientific constraints, tool and memory
> infrastructure, execution traces, and reliability evaluation.

### 7.2 Longer bio

> I am a Ph.D. candidate at Tsinghua University working at the intersection of agent
> systems and remote sensing. My research asks how an open scientific request can be
> transformed into an executable, traceable, scientifically constrained, and evaluable
> workflow. I developed ExpertsRS, an LLM-based multi-agent system published in
> *Big Earth Data*, and I maintain Sheaf, a local-first MCP-native knowledge layer for
> coding agents. My ongoing work explores a Scientific Agent Harness for
> observation-intensive science, with Earth observation and urban-forest mapping as the
> current formal evidence boundary.

### 7.3 网站项目顺序草案

1. **Scientific Agent Harness for Observation-Intensive Science** — 标注 Ongoing Research；
2. **Sheaf — Local-First Knowledge Layer for Agents**；
3. **ExpertsRS / URSA — LLM Multi-Agent Remote Sensing Analysis**；
4. **Weather Bulletin Generation Agent** — 仅在公开许可确认后加入；
5. **Skill Factory — Reusable Skill Lifecycle for Agents**；
6. **Agent OS / GF-1 ODC** — 经核实后进入 Other Projects。

网站允许展示长期 research agenda，但每个卡片必须显示 Ongoing / Published / Released /
Delivered 等状态，避免与已验证结果混淆。

## 8. 需要研究者作出的关键决策

只请求以下高杠杆决策，其余内容整理、版本同步和格式化可由 Codex 继续完成：

1. 正式博士专业/学位英文名称；
2. 可实习起始时间、时长和地点的暂定口径；
3. 气象局项目允许公开到什么程度；
4. 未发表 observation-intensive science 原稿的位置与状态；
5. Agent OS 是否是当前个人品牌的一部分；
6. Overleaf 是否具有 Premium Git/GitHub 同步，以及当前简历项目能否导出源码。

## 9. 更新纪律

- 新增数字先进入事实表并附证据位置，再进入简历/网站；
- 简历强调岗位相关的已完成证据；网站展示更完整的研究演进；
- 个人网站公开更新需要独立发布确认，不因简历投递自动上线；
- 网站或简历对正在进行研究的描述，不得反向升级论文 claim；
- 每次版本更新同时检查简历 PDF、网站 profile/projects/publications 和下载链接是否一致。
