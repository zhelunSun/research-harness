# Risks

> study: risks
> work_status: done
> basis: source
> evidence_status: candidate

## Question

哪些评分器、证据、自主运行和人工审查失效，可能让错误实验或未经核验的 claim
进入正式结论？哪些检查应由确定性机制、模型或人分别承担？

## Findings

| Risk | Level | Observable signal | Deterministic control | Model assistance | Human responsibility | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| self-evaluation loop | high；若是唯一晋级依据则 blocker | judge 分数提高但独立复算不变；换 judge 后排名反转 | 记录 generator/judge 版本；盲化与顺序交换；异构 judge 重复 | 定位分歧和风格偏置，不得单独放行 | 抽查原始证据和独立结果 | SH-SRC-007, SH-SRC-022, SH-SRC-023 |
| rubric or evaluator hacking | blocker | 评价文件被修改、访问隐藏标签、可信复算不一致 | evaluator hash/read-only；访问日志；clean replay | 标注可疑轨迹，不替代完整性检查 | 审计 mismatch 和 rubric 是否代表科学目标 | SH-SRC-007, SH-SRC-021 |
| judge calibration failure | high；高影响 claim 可为 blocker | 与专家 gold 一致率下降；顺序、seed 或版本不稳定 | 隐藏校准集；confusion matrix；版本化 prompt/model | 输出分项分数、置信度和升级请求 | 维护校准集并复核高影响节点 | SH-SRC-007, SH-SRC-023, SH-SRC-028 |
| hidden-gold leakage | blocker | 无合理轨迹却直接命中；与隐藏答案异常重合 | gold 与 agent 环境物理隔离；canary；访问审计与去重 | 相似性筛查，不能证明无泄漏 | 判断合法知识、检索与泄漏边界 | SH-SRC-007, SH-SRC-010, SH-SRC-021 |
| evidence/provenance mismatch | blocker | citation 无 locator；图表无法回到 run；claim 强于证据 | 强制 claim→evidence/source 或 run/artifact ID 链；hash 与重算 | 支持/反驳/无关分类并给 locator | 复核科学语境、协议和统计含义 | SH-SRC-015, SH-SRC-024, SH-SRC-028 |
| execution contamination | blocker | clean run 不复现；未知缓存或跨 run artifact | fresh environment；只读 evaluator；依赖、数据、网络和环境摘要 | 解释日志和聚类异常 | 审查 clean replay failure 和未知来源 artifact | SH-SRC-007, SH-SRC-012 |
| claim promotion error | blocker | candidate 跳到 accepted；无证据 ID 或审批记录 | 允许迁移表；append-only event；禁止生成器改正式状态 | 检查语气、状态和证据矛盾，只能建议降级 | `claim review` 决定接受、收窄或拒绝 | SH-SRC-015, SH-SRC-024 |
| negative-result loss | high；导致选择性结论时 blocker | run/预算账本缺口；只报告最佳 seed；失败被覆盖 | append-only branch/run ledger；计划、启动和终态数量守恒 | 失败分类与检索摘要 | 抽查 null、失败和被剪枝分支 | SH-SRC-027 |
| branch/budget pathology | high | 单分支吞噬预算；无限 debug；偶然正结果后停止 | 预设总预算、分支上限、debug depth、复现数和 stop rule | 评价分支新颖性与继续价值 | 在 checkpoint 决定扩预算、改假设或停止 | SH-SRC-001, SH-SRC-007 |
| repo/version drift | blocker | claim 找不到 commit；dirty diff 未记录；当前代码不复现 | 固化 commit、diff、lockfile、environment、data 和 evaluator version | 比较版本间接口和结果差异 | 判断漂移是否要求新 Run | local evidence; SH-SRC-020 |
| nominal human gate | blocker | 极短审批、连续全批准、同一主体产出并批准 | 不可绕过 gate；签名绑定 artifact manifest；记录理由与反证回应 | 生成审查包并突出分歧，不能代签 | 独立领域判断和高风险第二审查 | SH-SRC-025, SH-SRC-026 |

模型风险评分只允许输出：

```text
0 no signal | 1 weak | 2 clear | 3 blocking
```

同时必须给出 confidence、evidence locator 和 counterevidence。任何 `blocker`
都不能由模型单独解除。

## Evidence

核心 benchmark 证据来自 SH-SRC-007、SH-SRC-010、SH-SRC-012 和
SH-SRC-015。专门风险研究来自 SH-SRC-021, SH-SRC-022, SH-SRC-023,
SH-SRC-024, SH-SRC-025, SH-SRC-026, SH-SRC-027, SH-SRC-028。

这些来源证明相应风险在其研究范围内存在，不证明当前本地 repo 已经发生了每一种
故障。涉及新近预印本的数值和跨领域外推仍为 `needs-review` 或 `candidate`。

## Local implications

- `proposal`：claim status 必须由权限受控的状态迁移改变；自然语言报告和模型
  分数都不能直接晋级。
- `proposal`：evaluator、hidden gold 和 judge-only material 与 agent workspace
  应在文件系统和权限上隔离，而不只依赖 prompt。
- `proposal`：正式 claim 应绑定不可变的 source/run/artifact/version manifest。
- `proposal`：branch ledger 同时保存成功、失败、invalid、null、rejected 和
  pruned 分支。
- `proposal`：human gate 必须是绑定 artifact、记录理由和职责分离的决定。

## Open checks

- 对 Evidence 中列出的专门风险来源完成逐篇数值和适用范围核验。
- 将风险表映射到本地已有 validator，区分“已有检查”和“仅有文档约束”。
- 设计不依赖特定模型的 judge regression set 与版本变化触发条件。
- 明确哪些 `blocker` 需要第二位审查者，哪些只需要独立重放。
