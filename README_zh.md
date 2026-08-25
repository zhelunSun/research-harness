# research-harness

> 版本说明：可复用 skill 当前为 `v1.3.2`；本地论文总控当前为
> `idea-v2026.08.02`（见 `IDEA_VERSION.md`）。

> 面向 AI-Native 科研实验的认知纪律框架
>
> [English Version](README.md)

## 本地论文材料导航

本仓同时保存可复用的 `research-harness` skill 与本地博士论文 Idea 总控；两者版本独立。
论文的当前权威入口依次为：

1. [`IDEA_VERSION.md`](IDEA_VERSION.md)：当前正式工作版本与发布清单；
2. [`THESIS_STATE.md`](THESIS_STATE.md)：慢更新的总体科学问题、章节边界与风险；
3. [`process/current_execution_plan_20260802.md`](process/current_execution_plan_20260802.md)：快更新的当前里程碑与单一下一动作；
4. [`thesis/outline_zh.md`](thesis/outline_zh.md)：可直接阅读的中文工作提纲。

`reports/` 保存历史汇报材料，`sync/upstream_proposals/` 保存待人工接受的跨仓提案；二者都不自动
改变当前论文版本。`process/` 中的职业材料是独立 sidecar，不属于论文研究内容或证据状态。

## 解决什么问题

用 LLM 跑实验很容易。但要让实验*可复现*、*可追踪*、*不夸大结论*，很难。Agent 做科研时经常犯这些错误：
- 还没验证最小闭环就开始规模化
- 把 "p < 0.05" 当作决定性证据
- 遇到反直觉结果就先怀疑方法，不检查执行链路
- 删除失败运行让进度看起来更干净
- 悄悄修改基线或评分标准

这个 skill 提供的是 **guardrails（护栏），不是 recipes（菜谱）** —— 一套由仓库结构和校验规则强制执行的认知纪律，独立于任何具体领域。

## 核心优势

- **教思考，不是教脚本** — 教 agent *如何推理*实验，而不只是跑哪些命令
- **领域无关** — 适用于 NLP、视觉、生物、社会科学等任何使用 LLM 评估的领域
- **来源追踪内置** — 每次运行都可追溯到 git commit、模型版本、prompt 版本
- **反夸大机制** — 证据状态分级、受保护表面、管道优先诊断，防止最常见的 agent 科研失误
- **Agent 安全交接** — 对齐文档替代聊天记录，实现跨 agent 连续性

## 如何使用

在搭建新实验时加载本 skill。Skill 提供：

1. **五条认知纪律** — agent 在实验推理中的护栏
2. **五条治理规则** — 人机边界与证据分级
3. **阶段工作流（0→4）** — 可定制的仓库骨架和验证框架
4. **参考知识** — 每个纪律的详细方法论在 `references/`

本 skill 不包含自动化脚本。它教 agent *如何思考*，而不是跑哪些命令。

## 来源

提炼自真实的博士研究执行经验 —— 运行 LLM agent 对照实验、构建双轨评分系统、并（通过踩坑）认识到：大多数"方法失败"实际上是**管道失败**。

## 许可

MIT
