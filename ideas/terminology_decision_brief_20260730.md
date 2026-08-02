# 第二、三项研究术语决策简报

> 日期：2026-07-30
> 状态：历史 decision brief；当前命名已由 `DEC-2026-0802-advisor-reported-frame-and-ch2-priority.md` 决定
> 目标：先由 Codex 完成术语证据和方案比较，再由研究者一次性批阅。

## 1. 决策标准

候选术语同时满足：

1. 在相关学术共同体中有可定位用法，而不是仅由本项目创造；
2. 与章节真正操纵和测量的变量一致；
3. 不把一个局部机制扩大为“可信 AI”“自主科学家”等过强命题；
4. 符合中文学位论文标题的简洁和可读性；
5. 能与导师给出的“知识库构建”“面向用户验证”框架兼容。

## 2. 第二项研究

当前工作标题：

> **基于科学约束的城市森林遥感知识库构建**

### 初步术语判断

| 表述 | 优点 | 风险 | 当前判断 |
| --- | --- | --- | --- |
| 科学约束 | 能覆盖适用性、证据、验证和结论降级；中文直观 | 不是当前 Agent 文献中高度稳定的单一标准术语 | 保留为工作总称 |
| 知识约束 | AI/规划领域更常见 | 过宽，且与“知识库构建”重复；不能突出证据状态 | 不优先用于章标题 |
| 证据约束 | 可操作、可测量，直接对应来源、充分性和禁止推断 | 可能无法覆盖全部方法适用性和人工检查义务 | 若正式实验聚焦 evidence obligations，优先候选 |
| 认识论约束 | 对应 epistemic constraints，理论上精确 | 中文遥感论文中生硬；相关 Agent 用法仍分散 | 适合理论阐释，不优先用于章标题 |
| 面向科学推理 | 学术表达稳妥，不声称自创标准术语 | 表达目标而非核心机制，方法辨识度较弱 | 安全候选 |

### 候选标题

1. **基于科学约束的城市森林遥感知识库构建**
   继续作为工作标题，直到 B0--B5 的主要处理变量确定。
2. **基于证据约束的城市森林遥感知识库构建**
   适用于正式方法主要围绕 evidence status、applicability、validation
   obligation 和 conclusion downgrade 展开。
3. **面向科学推理的城市森林遥感知识库构建**
   适用于希望避免术语争议、把 ScientificContract 放入节级标题的方案。

### 暂定建议

现在不改标题。由 Chapter 2 的直接竞争审计回答两个问题后再决定：

1. 最可防守的独立变量究竟是“证据约束”还是更广的“科学约束”；
2. `ScientificContract` 是核心方法名，还是知识库到 Agent 的运行接口。

研究者不需要自行搜索全部文献。Codex 应提交一份不超过两页的 L7 决策包，只给出
“保留 / 改为证据约束 / 改为面向科学推理”三个选项及证据。

## 3. 第三项研究

当前工作标题：

> **面向用户的城市森林遥感智能体可靠性验证**

### 初步术语判断

NIST 将 AI 的 testing、evaluation、validation、verification 作为 TEVV 组合过程，
并把 valid and reliable 视为 trustworthy AI 的基础特征。其定义中：

- validation 强调以客观证据确认特定预期用途的要求是否满足；
- reliability 强调系统在给定条件和时间范围内无故障地按要求运行；
- evaluation 负责建立任务、测试床、数据、指标和测量方法。

因此，“可靠性验证”语义上成立，但容易被理解为对一个已有系统作一次验收；当前
第三项研究实际要提出任务协议、轨迹评分、故障注入、多次 trial 和用户效用测量，
研究对象更接近 reliability evaluation。

| 表述 | 优点 | 风险 | 当前判断 |
| --- | --- | --- | --- |
| 可靠性验证 | 与导师的“验证章”直觉一致；强调预期用途 | 容易显得只是综合应用验收 | 可作工作标题 |
| 可靠性评测 | 与 benchmark、testbed、grader、多次 trial 匹配 | 需要在正文说明不仅是排行榜 | 当前首选 |
| 可信性评测 | 可覆盖安全、透明、公平、隐私等 | 范围过大，当前证据无法覆盖全部 trustworthiness | 不建议 |
| 有效性验证 | 直接面向用户目标 | 弱化失败恢复、鲁棒性与长期运行 | 可作指标，不作总标题 |

### 候选标题

1. **面向用户的城市森林遥感智能体可靠性验证**
2. **面向用户的城市森林遥感智能体可靠性评测**

### 暂定建议

优先将正式标题调整为：

> **面向用户的城市森林遥感智能体可靠性评测**

正文中再使用 TEVV 结构说明：

`测试任务 → 系统评价 → 预期用途验证 → 关键行为核验`

这样既保留导师提出的应用和对比要求，又把第三项研究从一次性验证升级为独立的
测量方法。

## 4. 初始共识来源

- NIST AI TEVV:
  https://www.nist.gov/ai-test-evaluation-validation-and-verification-tevv
- NIST AI RMF, Valid and Reliable:
  https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/
- ISO/IEC TR 24028:2020, Trustworthiness in AI:
  https://www.iso.org/standard/77608.html
- ISO/IEC TS 5723:2022, Trustworthiness vocabulary:
  https://www.iso.org/standard/81608.html
- Anthropic, Demystifying evals for AI agents:
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

以上来源能够支持“可靠性评测/验证”的术语区分。第二项研究的术语仍需完成
AgentSpec、RNSP、KISS、WTS 等直接竞争全文审计后再定。

## 5. 唯一人工门禁

Codex 完成 Chapter 2 comparator 包和 Chapter 3 evaluation construct 包后，研究者
一次性选择：

1. 第二项标题三个候选中的一个；
2. 第三项使用“可靠性验证”还是“可靠性评测”；
3. 允许进入开题的对应核心 claim。

在此之前，不要求研究者额外检索术语文献。
