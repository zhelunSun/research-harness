# 开题报告 v0.5 文献写作准入审查

> 状态：`reviewed_candidate`，not merged。  
> 目标：`thesis/opening_report_draft_zh.md` v0.5。  
> 边界：本审查不修改开题正文、不删除 `[REF-MISSING]`、不写入 Zotero，也不提升论文 claim。

## 结论

[CLAIM:OI-C1] 当前开题稿共有 7 个字面 `[REF-MISSING]`：其中 1 个用于说明稿件状态，6 个是正文证据缺口。按照现有 O1 contract，现阶段可删除的正文标记数为 0。

[CLAIM:OI-C2] 第 1.2、2.2 和 2.4 节存在“部分可支持、综合判断仍缺证据”的情况，其中领域综合 `GAC-C6` 仍为 `needs_review`。第 1.2 与 2.2 节最适合在 V1 中拆成来源事实句与领域缺口句；第 2.4 节可拆出动态执行和过程评价实例，但用户校准有效性仍需独立来源。

[CLAIM:OI-C3] ExpertsRS 在第 32、212 和 340 行附近的三处历史可行性表述可由 `GAC-C1` 直接候选支持。不过，`sun_llm-based_2026` 仍是 provisional BibTeX key；只有完成明确授权的 Zotero 导入、身份核对及任务特定 contract 合并后，才可进入开题正文。

## 段落级决定

| 位置 | 当前决定 | 可用证据 | 保留边界 |
|---|---|---|---|
| 1.1 背景 | 证据不足 | `GAC-C1` 仅提供遥感工作流实例 | 保留 `[REF-MISSING]` |
| 1.2 问题提出 | 需要拆段 | `AFS-C2`、`GAC-C1/C2/C4/C5` 支持能力实例 | `GAC-C6` 为 `needs_review`，保留标记 |
| 2.1 科学智能体 | 证据不足 | `AFS-C1/C2` 仅为两个实例 | 保留 `[REF-MISSING]` |
| 2.2 地理空间智能体 | 需要拆段 | `GAC-C1` 至 `GAC-C5` 支持来源事实 | 领域综合依赖 `GAC-C6`，保留标记 |
| 2.3 知识表示 | 仅相邻背景 | `AFS-C5/C6/C7` 体现归属、复核和形式化 | 不能替代知识表示综述，保留标记 |
| 2.4 系统评测 | 需要拆段 | `GAC-C4/C5` 支持动态执行和过程评价实例 | 静态评测与用户效度判断仍缺来源，保留标记 |

稳定候选 key 只有已入库项目，例如 `ghareeb_multi-agent_2026`。`sun_llm-based_2026`、`bao_spatial-agent_2026`、`yu_geoagentbench_2026` 和 `hasan_geodisaster_2026` 在 Zotero 导入前均保持 provisional。

## 当前不进入开题主论证的材料

OpenAI 和 Anthropic 的数学报告分别由 `AFS-C5`、`AFS-C6` 和 `AFS-C7` 约束。它们适合进入第二章的 provenance、审计与 AI4Science 背景，不是开题 v0.5 的承重来源。

## 下一门禁

本准入片段不是 O1 contract 的修订。后续 V1 fresh-context 审阅可使用本矩阵提出拆段建议；若需要新增引文或移除标记，必须另行审阅并显式合并任务特定 writing contract。
