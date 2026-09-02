# City-scale composite Agent evaluation study

> work_status: review
> evidence_status: candidate
> decision boundary: literature comparison and design hypothesis only

## Question

相邻 Agent 与科学评测工作是否已经覆盖“一个真实城市任务环境中，多条科学任务共享版本化数据与
中间制品，并评价跨任务依赖、故障和不确定性传播”的设计？

## Current answer

首轮五篇来源表明，相邻工作已经分别覆盖：

- 遥感工具调用、多步规划和步骤／结果评分；
- 从论文抽取的单项科学编程任务；
- 在虚拟环境中完成假设—实验—分析—结论循环；
- 连接真实 API、数据处理、分析和报告的端到端气候工作流；
- 在一个自包含数字组织环境中完成异构长程任务。

因此，“真实任务”“多步工作流”“环境式评测”或“城市级”均不能单独作为创新。当前尚可继续
检验的交叉点是：**以一个真实城市及其版本化遥感制品为共享环境，显式表示任务之间的科学依赖，
并评价上游状态如何传播到下游空间产品和结论。** 这是设计假设，不是新颖性结论。

## Closest comparator

ClimateAgent 是当前最需要正面比较的领域相邻工作：它已经把真实 API、异构气候数据、多步分析、
错误恢复和报告生成组织为端到端任务。我们的差异若成立，不能建立在“工作流更长”，而应落在
共享城市状态、跨任务制品复用、空间依赖、结果谱系和跨阶段错误传播的可操作定义及评价上。

ThinkGeo 是最直接的遥感 benchmark 对照。它已有数百个结构化遥感 Agent 任务和专家核验步骤；
第三章必须证明复合任务不是把这些任务串联，而是存在由数据版本、空间产品和科学用途决定的真实
依赖。

## Admission test

该方向只有同时满足以下条件，才值得升级为第三章方法主张：

1. 至少两条任务链消费同一版本化城市制品，而不是共享一个背景描述；
2. 下游正确性依赖上游制品身份、参数、适用条件或不确定性；
3. 可注入并定位跨阶段故障，且能观察其传播或被阻断；
4. grader 能区分制品正确、依赖保持、科学结论边界和系统过程；
5. 与 ThinkGeo、ClimateAgent 等最近工作形成可复核的构念差异。

若不能满足，应把北京工作降为真实综合案例，不把“城市级复合任务环境”作为独立创新。

## Contents

- `references.bib`: 五篇首轮来源的 intake BibTeX 身份；
- `ledger.json`: 仅依据官方摘要形成的 claim--source 关系；
- `evidence_cards.md`: 对每篇来源的可用信息和迁移边界；
- `audit.json`: 确定性账本审计；
- `writing_bridge.json`: 候选写作约束，不得直接并入开题合同。

## Evidence boundary

本轮没有下载或通读全部论文全文。所有来源最多为 `abstract`，所有直接关系最多为
`abstract_consistent`。ThinkGeo 已在本地 Zotero 找到父条目 `PUSEGPQQ`；其他四篇未找到。
本轮没有写入 Zotero、插入引用或改变论文 claim。
