# 大纲冻结阶段并行协作协议

> 日期：2026-07-30
> 状态：active coordination protocol
> 当前对齐：`idea-v2026.08.02`
> 目标：把研究者参与压缩到两个高价值门禁，其余工作由 Codex 并行推进并记录。

## 1. 仓库职责

| 仓库 | 当前职责 | 本轮允许的修改 |
| --- | --- | --- |
| `research-harness` | 总题目、三项关系、claim、decision、证据指针、人工门禁 | 控制面、决策包、跨仓证据和过程记录 |
| `URSA` | 第一项研究的可运行工作流、runtime、validator、repair、trace 和 pilot | 方法代码、测试、实验 brief、结果 manifest |
| `chapter2-urban-forest-knowledge` | 第二项研究的文献、知识资产、contract 和匹配实验 | comparator、contract fixture、实验与日志 |
| `urbfo-agent-demo` | 北京制图任务资产和第三项可靠性评测执行 | 任务协议、trace、grader、用户验证与比较 |
| `sheaf-ai` | 潜在知识产品与界面载体 | 仅在 Chapter 2 明确需要产品化接口时调用 |

下游结果通过 proposal 或 evidence pointer 返回总控；总控不复制原始实验。

## 2. 仅保留两个研究者门禁

### Gate A：方法与 claim 批阅

Codex 提交一个合并决策包，研究者一次性决定：

1. 第二、三项研究的正式术语；
2. 第一项研究新增贡献的最小组合；
3. 第二项研究采用基础 contract，还是把知识生命周期列为正式上探；
4. 哪些 claim 允许进入开题。

输入必须是推荐方案、备选方案、直接竞争、证据状态、工作量和失败条件。不得向
研究者提出开放式“你想怎么做”。

### Gate B：真实用户与科学校准

Codex 提交任务、角色和 rubric 包；研究者只需：

1. 确认任务是否代表生态学家和绿化管理者的真实问题；
2. 从已有关系网络中协调小型目标用户与遥感专家校准组；
3. 批准目标用户、领域评审和评测审计的责任边界；
4. 批准人工评分、反馈数据使用和可能的人体参与/伦理审查路径。

专家“能否找到”不再作为主要门禁。Gate B 的核心是任务真实性、角色分工、
专家劳动预算、争议裁决和数据合规。

## 3. 不作为高强度门禁的事项

- 证据矩阵中的路径、状态和仓库内事实由 Codex 维护；
- 文献搜索、候选去重、source locator 和竞争矩阵由 Codex 完成；
- schema、validator、trace、grader、运行脚本和分析由 Codex 实现；
- 工程选择只要可逆、不改变科学 claim，可自主推进；
- 研究者只需异步纠正仓库外事实，无需为此专门开会。

## 4. 并行工作流

### Track A：总控与证据

- 完成开题证据矩阵；
- 完成术语决策包；
- 把所有工作映射到 E1/C1/C2/C3/C4；
- 保持“设计已冻结”和“结果已验证”分离。

### Track B：URSA 第一项研究

- 在 URSA 内建立 schema、validator、targeted repair 和 trace；
- 保留现有 notebook 作为 published baseline；
- 先运行小型 P0--P3 pilot，不扩展 UI、Agent 角色或分布式 runtime。

### Track C：Chapter 2

- 按现有 L0--L9 loop 完成直接竞争和 claim contraction；
- 将 claim ledger 解释为候选知识治理面，不批量转换为人工 runtime 规则；
- 只对一个任务相关的 10--20 条候选切片补齐证据原文和适用边界；
- 准备 human-reference、model-proposed 与 governed-proposal 的小型构建来源对照；
- 准备最小 contract fixture；
- 人类 Gate A 前不扩展正式实验和知识生命周期。

### Track D：Chapter 3

- 保留北京制图冻结结果；
- 将任务环境、弱样本方法、样本、结果制品、故障和过程日志分层登记；
- 历史日志只标记为 episode reservoir，未结构化前不得写成 RL trajectory dataset；
- 设计目标用户任务、TEVV 指标、故障注入和跨方法比较；
- Gate B 前只做不会依赖真实用户判断的 deterministic MVP。

### Track E：Scientific Research Harness

- 仅做文献矩阵、失效模式和本地 gap analysis；
- 不阻塞 A--D，不要求研究者立即参与。

## 5. WIP 限制

- 每项研究同时最多一个毕业核心 claim；
- 全论文同时最多一个 RL/self-evolution 上探；
- 每次提交给研究者的决策包最多三个实质选项；
- 未通过 human gate 的 candidate 不进入正式中文大纲；
- 下游仓库存在未提交工作时，优先新增文件，避免覆盖活动状态。

## 6. 汇报节奏

Codex 持续执行并记录；只有出现以下情况才打断研究者：

1. 直接竞争使核心 claim 无法成立；
2. 结果与科学假设方向相反且无法通过一次修复解释；
3. 需要真实用户、数据权限或不可逆资源投入；
4. 准备把 candidate 晋级为开题/论文正式论断。

正常情况下，研究者只接收 Gate A 和 Gate B 两个批阅包。

## 7. 当前顺序

1. 总题目和三项标题：已按 2026-07-31 汇报版本更新，作为当前工作基线；
2. Chapter 2：当前 P0，先完成验证设计任务的证据切片、contract 和 B0--B5 dry run；
3. URSA：当前 P1，只完成 workflow graph/validator/repair/trace 最小 pilot；
4. Chapter 3：当前 P2，整理任务环境和评分接口，真实用户运行等待 Gate B；
5. 开题证据矩阵 v0.3：随三个最小闭环更新；
6. 中文节级工作提纲 v0.1：已建立，方法名和实验规模仍按证据门禁迭代。
