# Agent 前沿对齐与论文吸收边界

> 版本：v2026.07.29
> 版本关系：作为前沿 context 原样沿用至 `idea-v2026.08.02`，不新增论文承诺。
> 用途：为论文 idea 检索、章节设计和新方向判断提供稳定 context。
> 状态：前沿研究会变化；本文件记录截至 2026-07-29 的设计含义，不替代
> 章节局部文献综述和原文核验。

## 1. 稳定设计原则

论文不以追逐单一 Agent 热点为目标，而采用四项可跨模型、跨框架保留的原则：

> **轨迹原生、科学约束、评测驱动、经验可学习。**

### 轨迹原生

任务状态、工具调用、观察、制品、错误、修复、成本和最终状态应成为一等研究
对象，而不是事后从聊天记录中推断。

### 科学约束

领域知识不直接替代模型决策。人类和证据系统提供适用条件、禁止推断、验证义务
和结论降级边界，模型在边界内完成开放规划和工具协同。

### 评测驱动

先定义真实任务、用户效用、环境最终状态和失败边界，再决定应增加什么方法。
最终答案指标、轨迹指标和人工判断必须分开。

### 经验可学习

执行轨迹应能够转换为 episode、transition、preference 或 update candidate，
为检索式经验复用、运行机制适应、SFT/RL 等后续方法提供接口。当前主线只承诺
experience-ready，不承诺大规模训练收益。

## 2. 前沿方向与吸收层级

| 方向 | 核心启发 | 论文吸收位置 | 层级 |
| --- | --- | --- | --- |
| AI Second Half / utility-first evaluation | 从刷既有 benchmark 转向定义真实效用、连续任务和人机交互 | 研究内容三的任务与评测方法 | 主线 |
| Experience-driven agents | Agent 通过环境行动和反馈积累可学习经验 | 统一轨迹接口；研究内容三的远期承诺 | 主线设计原则 |
| Operational geo-agent benchmarks | 以可执行工作流、确定性检查和执行契约评价工具型地理智能体 | 研究内容三的直接相关工作与竞争坐标 | 主线 |
| Human-in-the-loop geospatial systems | 以少量本地标签、交互验证、周转时间和真实部署衡量用户效用 | 研究内容三的外部效度和人工成本 | 支撑层 |
| Agentic RL | 将 Agent 执行与训练解耦，从 spans/trajectories 分配反馈 | 小规模 sidecar 或个人项目 | 可选上探 |
| Context engineering / memory | 管理每一步模型可见的状态、记忆、工具和知识 | 研究内容一状态管理；研究内容二动态约束选择 | 支撑层，不作核心创新 |
| Eval-driven development | 能力评测、回归评测、多次 trial、人工校准和轨迹审查 | 研究内容三核心方法 | 主线 |
| Safe self-improvement | 候选修改、隔离运行、版本谱系、回归门禁 | 研究内容三 3--5 个微型案例 | 可选上探 |
| Multi-agent networks | Agent 网络的身份、协议、群体失效和监督 | 讨论与个人项目 | 暂不进入主线 |
| World models / embodied agents | 通过交互环境学习动态和行动后果 | 展望 | 明确不硬接 |

## 3. 关键来源及其设计含义

### The Second Half

Shunyu Yao 认为 AI 研究重点正在从“训练模型解决给定问题”转向“定义有真实
效用的问题和评测”，并特别指出现有评测常假设无用户交互和任务独立同分布。

- Primary source:
  https://ysymyth.github.io/The-Second-Half/
- 对论文的含义：
  第三项研究应研究连续、交互、具有环境状态和专家效用的城市森林遥感任务，
  而不是只构造更多静态问答。

### Welcome to the Era of Experience

David Silver 与 Richard Sutton 提出未来 Agent 将更多从长期环境互动和基于
环境的反馈中学习，而不只依赖静态人类数据。

- Primary source:
  https://storage.googleapis.com/deepmind-media/Era-of-Experience%20/The%20Era%20of%20Experience%20Paper.pdf
- 对论文的含义：
  先使 URSA 的运行成为可记录、可评分、可复用的经验。论文无需先承诺训练模型。

### Agent Lightning

Agent Lightning 将执行轨迹表示为状态、动作和反馈，并将 Agent runner 与训练
算法解耦。

- Primary source:
  https://www.microsoft.com/en-us/research/blog/agent-lightning-adding-reinforcement-learning-to-ai-agents-without-code-rewrites/
- 对论文的含义：
  统一 trace schema 和可靠 outcome/reward 比立即选择 PPO、GRPO 或某个训练
  框架更优先；训练可作为读取相同轨迹的旁路。

### GeoDisaster

GeoDisaster 提出面向 operational geo-intelligence 的工具型多智能体 benchmark，
使用异构遥感与 GIS 证据、可执行工作流和确定性一致性检查，并以显式执行契约、
失败感知 SFT 和契约约束 RL 改进工具使用、证据 grounding 与状态一致性。

- Primary source:
  https://arxiv.org/abs/2606.17246
- 对论文的含义：
  它是第三项研究比传统 VLM benchmark 更直接的竞争坐标，也说明“工具调用 +
  结果问答”已经不足以构成新贡献。论文需要突出城市森林任务、真实用户效用、
  多次 trial、故障恢复和科学约束，而不是仅追求更大的实例数量。

### HASTE

HASTE 是灾后建筑损毁评估的无代码、人机协同平台。其两条方法分别是逐场景
分割，以及冻结视觉表征加少量本地标签的轻量分类；它报告标签效率、交互验证、
周转时间和三十余次真实响应。

- Primary sources:
  https://arxiv.org/abs/2607.11838
  https://github.com/microsoft/haste
- 对论文的含义：
  HASTE 并不是自然语言 Agent 与传统专家工作流的直接对照，不能用来证明
  Agent 方法优于专家方法。它真正可借鉴的是以真实分析人员、人工标注量、
  任务周转时间、现场分布偏移和部署记录定义外部效度，这正好补足第三项研究的
  用户级评测。

### 2026 年工具型地理 Agent 直接竞争

截至 2026-07-29，工具型 GIS/遥感 Agent 已经出现多条直接竞争路线：

| 工作 | 已覆盖内容 | 对论文的压力 |
| --- | --- | --- |
| Spatial-Agent | 以科学空间概念和 GeoFlow DAG 生成可解释、可执行工作流 | 第一项研究不能只以“工作流图”作为创新，必须证明类型语义、验证和定向修复的增量 |
| OpenEarthAgent | 以大规模已验证推理轨迹进行 SFT，覆盖遥感工具交互 | “有轨迹”不再新；论文应突出轨迹可靠性、科学约束和真实反馈 |
| GISclaw | 持久 Python 沙箱、Plan-Execute-Replan、错误记忆和三层评测 | 多 Agent 不天然更优；架构比较必须控制模型强度与任务复杂度 |
| GeoAgentBench | 117 个 GIS 工具、53 个动态任务、参数执行与视觉结果验证 | 第三项研究不能只做动态执行 benchmark，需增加领域科学性、用户效用和故障恢复 |
| GeoDisaster | 可执行遥感/GIS 证据链、确定性检查、执行契约和契约约束学习 | 与三项研究总体链条最接近，应作为直接 comparator 重点审计 |

- Primary sources:
  https://arxiv.org/abs/2601.16965
  https://arxiv.org/abs/2602.17665
  https://arxiv.org/abs/2603.26845
  https://arxiv.org/abs/2604.13888
  https://arxiv.org/abs/2606.17246
- 对论文的含义：
  当前差异化不能再停留在“自然语言、多智能体、工具调用、可执行 workflow”
  这些共性标签。稳妥且仍有领域价值的交点是：
  `scientific contracts + targeted repair + task/trace/user eval +
  real urban-forest experience`。

### AlphaEarth Foundations 的比较层级

AlphaEarth Foundations 提供多源地球观测年度 embedding，用于少标签制图和
地表属性估计；它不是自然语言 Agent 或工作流执行系统。

- Primary source:
  https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/
- 对论文的含义：
  AlphaEarth 可以作为制图表征、数据后端或专业模型能力基线，不能与 URSA
  直接做“整体框架谁更好”的单层比较。合理做法是固定上层任务与评测协议，
  比较不同感知/表征后端对结果的影响，或把它放入“专业模型/工具层”基线。
  传统专家流程、通用 Agent、专业模型后端和科学约束 Agent 必须分层报告，
  避免类别错误。

### Anthropic agent evaluation

Anthropic 区分 task、trial、grader、trace、outcome、agent harness 和 evaluation
harness，并强调能力评测、回归评测、多次运行以及代码/模型/人工评分组合。

- Primary source:
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 对论文的含义：
  第三项研究的独立贡献应是领域任务、评测器、故障与轨迹分析，而不是重复
  第一、二项研究的局部消融。

### Context engineering

Anthropic 将 context engineering 视为 prompt engineering 的延伸，核心是选择
模型当前应看到的状态、工具、知识和记忆。

- Primary source:
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 对论文的含义：
  context engineering 是运行框架的一项必要职责，但不是当前论文需要单独
  宣称的新方法。Harness 负责执行和生命周期，context engineering 负责模型
  每一步的可见信息，两者不是替代关系。

### Darwin Gödel Machine

DGM 展示了基于评测的 Agent 自我修改和开放式搜索，也暴露了伪造工具记录与
攻击奖励函数的风险。

- Primary source:
  https://sakana.ai/dgm/
- 对论文的含义：
  自我改进必须建立在沙箱、不可由 Agent 修改的评测器、版本谱系和回归门禁
  之上。当前只吸收受控 adaptation，不吸收开放式自进化承诺。

### Multi-agent safety

Google DeepMind 将多 Agent 网络的测试环境、交互协议、群体失效和监督列为
未来研究重点。

- Primary source:
  https://deepmind.google/blog/investing-in-multi-agent-ai-safety-research/
- 对论文的含义：
  URSA 当前是单一受控系统内的多角色协作，不应被包装成 Agent 网络研究。

## 4. 历史北京项目轨迹的研究价值

过去数月的代码、对话、导师反馈、方法分支和失败记录是 experience candidates，
但不能直接等同于 RL trajectories。进入学习或正式评测前至少需要转换为：

| 字段 | 含义 |
| --- | --- |
| episode_id | 一次可界定的任务或方法迭代 |
| task_intent | 当时真实目标和约束 |
| environment_version | 数据、代码、工具和配置快照 |
| action | Agent 或人类采取的操作 |
| observation | 工具输出、实验结果或错误 |
| artifact | 代码、地图、表格、报告等制品 |
| feedback | 用户、导师、验证器或环境反馈 |
| outcome | 任务最终状态及其证据 |
| evaluation | 可复现评分、人工判断与不确定性 |
| provenance | 时间、版本、来源与使用权限 |

历史日志的主要风险包括：

- 真实行动与事后总结混在一起；
- 导师意见是高价值反馈，但不天然是标量 reward；
- 方法分支同时改变多个变量，难以直接归因；
- 成功结果可能经过人工选择，存在幸存者偏差；
- 旧环境不一定可以完全重放。

因此优先顺序为：

1. 轨迹清点和 episode 化；
2. 建立可验证 outcome 和反馈类型；
3. 用于错误分类、案例检索和经验复用；
4. 在新受控任务上采集训练就绪轨迹；
5. 最后再尝试 SFT、preference learning 或 Agent RL。

## 5. 人类规则与 LLM 原生智能的边界

论文不应通过人为写完整答案来“约束”模型。推荐分工：

- 人类提供科学不变量、证据准入、风险边界和最终审核；
- 系统提供状态、工具语义、验证器和反馈通道；
- LLM 负责需求理解、开放规划、策略生成、冲突解释和候选更新；
- 评测决定候选行为或更新能否被接受。

这使第二项研究的科学约束与 experience-driven learning 相容：
约束定义可接受行为的边界，经验用于在边界内改进策略。

## 6. 当前禁止的叙事跳跃

- 有大量日志，不等于已经拥有可用于 RL 的高质量轨迹数据集；
- 使用模型反馈，不等于 Agent 已经自进化；
- 保存对话历史，不等于实现长期记忆；
- 多个角色协作，不等于研究 Agent 网络；
- 使用遥感多模态数据，不等于构建世界模型；
- 接入 RL 框架，不等于证明 RL 对研究问题有效；
- context engineering 或 harness 的术语流行，不自动构成论文创新。

## 7. 对个人品牌、求职与创业的可复用产物

在不增加学位论文核心风险的前提下，优先形成：

1. 可运行的 URSA typed workflow/runtime 最小实现；
2. 开放的城市森林遥感 Agent 任务与 trace schema；
3. 可靠性评测、故障库和回归套件；
4. 从历史日志到 experience dataset 的构建说明；
5. 一个读取同一轨迹的轻量 RL 或 adaptation proof-of-concept；
6. 系列技术文章：prototype → runtime → constraints → eval → experience。

这些产物同时支持研究岗位、Harness Engineering、个人品牌和垂直 Agent 创业
验证，但其中第 5 项不作为当前毕业基本盘。
