# O1 v0.6.1 P1 writer pass 变更台账

> 日期：2026-09-03
>
> 模式：argument edit；仅处理 `opening_report_o1_v0.6_v1_review_20260903.md` 的两项 P1。

## 结果

两项 P1 均已按已有原子论述图和研究者接受的 Route B 顺序完成最小修复。主稿版本更新为
`v0.6.1`。本 pass 未插入引用、未删除任何 `[REF-MISSING]`、未处理 P2/P3，也未改变论文题目、
章级源定义、方法版本、证据状态或效果结论。

## Before / after

| 位置 | 原职责或状态 | 问题 | 本轮修改 | 论断／证据变化 |
| --- | --- | --- | --- | --- |
| 第 2 节入口 | 由通用大语言模型智能体综述开始 | 与原子图的“先问题域、后智能体”顺序不一致 | 新增 `2.1 城市森林遥感任务与方法基础`，原 2.1–2.5 顺延为 2.2–2.6 | 将已登记的原子论述传播到正文；新增内容保留 `[REF-MISSING]`，未准入引用 |
| 3.5 与 4.4 | “首轮仍推荐”“研究者确认前” | 与 2026-09-02 已接受 Route B-first 决策冲突 | 改为“首轮采用／实施顺序已确认”，并紧邻保留“不等于第三章完整方法冻结” | 只同步决策状态；未把首任务顺序升级为方法或系统效果 |

## 保持不变的边界

- Route B 仍只是首个只读评测实现，不是第三章全部路线或已完成 benchmark。
- `manual 301` 仍是人工校准／训练数据，不是独立验证。
- “城市级”“真实任务”和“多步流程”仍不单独构成创新。
- 第一章正式机制效果、第二章 scientific gold／方法效果和第三章系统效果均保持 open。
- V1 中关于第一章术语、“科学意图”定义和第三章信息密度的 P2/P3 留给后续独立 pass。

## 确定性检查

```powershell
python C:\Users\zhelunStation\.codex\skills\zh-scientific-writing\scripts\zh_scientific_audit.py audit --text thesis\opening_report_draft_zh.md --contract thesis\writing_contracts\opening_report_o1_v0.6.contract.json
python C:\Users\zhelunStation\.codex\skills\zh-scientific-writing\scripts\zh_scientific_audit.py audit --text thesis\opening_three_chapter_route_matrix_zh.md --contract thesis\writing_contracts\opening_three_chapter_route_matrix_v0.2.contract.json
git diff --check
```

两份 writing audit 均为 `errors=0 warnings=0`，`git diff --check` 通过。正文中的
`[REF-MISSING]` 由 8 个增加为 9 个，原因是新增问题域小节显式保留了一个待准入证据槽位；没有
旧标记被移除。脚本结果只证明合同覆盖的确定性约束未被破坏，不替代引文蕴含、新颖性或科学有效性
判断。

## 独立差异复核

原 V1 reviewer 在未编辑文件的条件下复核 HEAD v0.6 与工作稿 v0.6.1 的差异，确认两项 P1 均已
关闭、无新 P1、无 claim／evidence state 越界；Route B、只读离线、GEE 流程非迁移、manual 301、
strict500、rare250、Wave2 和完整方法未冻结等边界均保留。P2/P3 未被顺带处理。复核再次得到两份
writing audit `errors=0 warnings=0`，`git diff --check` 无错误。
