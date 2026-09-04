# 原文负载段落复核与引文修复

2026-09-04 · reviewer: parent `/root` · writer: `task_difficulty_literature`

## Source-local V1

主agent独立于本包写作，重新核对下列五个原文负载位置，并报告其支持 TD-C1至TD-C5的局部事实：

| 来源 | 主agent复核位置 |
| --- | --- |
| ExpertsRS | 出版社indexed全文 §3.2.2 |
| GAIA | HTML §3.3 |
| ThinkGeo | v2 §3.3 |
| GeoPlan-bench | v1 §4.1及§8.2，HTML line 395的计划／执行边界 |
| ScienceAgentBench | v3 §2.3及§4.1 |

这项V1是原文支撑核对，不代表五篇逐页通读、论文结果复现、整个本地分类有效性验证或研究者接受。TD-C6和候选分类仍为needs_review；ExpertsRS附录A2等原有缺口不变。

## P2修复

主agent指出TD-C5的英文摘录中，动词写为`approximate`，但其检索到的当前原文为`estimate`。writer重新访问[ScienceAgentBench v3全文](https://arxiv.org/html/2410.05080v3)，确认§4.1 Figure 3之后的段落、HTML line 203当前使用后者。

早先检索返回的片段显示过前一种措辞；目前只能确认检索呈现差异，不能据此声称原论文或arXiv版本发生变更。本包以本次重新定位的v3原文为准，修正ledger中的一个词，并把位置说明改为实际段落位置。TD-C5中文释义、文献身份、关系及证据等级不变。

## 修复后V0

原命令重新运行：ledger为5来源、6主张、10关系，0错误／0警告；README中文写作审计0错误／0警告。审计输出已刷新至audit.json、writing-audit.json及writing-audit.md，writing-bridge.json重新生成。

本次仅修改同一包内文件；未扩检其他文献、未修改正式claim或registry、未提交或推送。
