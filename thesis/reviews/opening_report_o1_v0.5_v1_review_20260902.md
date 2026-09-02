# 开题报告 O1 v0.5 fresh-context V1 审阅

> 审阅日期：2026-09-02  
> 审阅模式：只读 `fresh-context review`；本轮未参与 v0.5 生成，也不在同一遍审阅中改写正文  
> 结论：**at-risk；2 个 P1、2 个 P2。当前不进入导师讨论包生成。**

## 1. 审阅范围与权威输入

本轮只读以下输入：

- `thesis/writing_contracts/opening_report_o1_v0.5.brief.md`；
- `thesis/writing_contracts/opening_report_o1_v0.5.contract.json`；
- `thesis/writing_contracts/opening_three_chapter_route_matrix_v0.1.brief.md`；
- `thesis/writing_contracts/opening_three_chapter_route_matrix_v0.1.contract.json`；
- `thesis/opening_report_draft_zh.md` v0.5；
- `thesis/opening_three_chapter_route_matrix_zh.md` v0.1；
- `evidence/opening_evidence_matrix.md` v0.8。

审阅维度为 claim--evidence、章节衔接、范围漂移、限定语附着和三章评价责任。没有核验外部文献
原文，因此本报告不能证明引用 entailment 或科学真实性。

## 2. Findings

### P1-01 第一章预期创新的待验证状态没有局部附着

- 位置：`thesis/opening_report_draft_zh.md:377-384`。
- 现象：预期创新点 2、3 显式带有 `[待验证]`，创新点 1 没有同等级标记，并使用“通过动态规划、
  过程图与检查点恢复增强真实反馈下的运行调节”这一效果性表述。第 384 行虽对三项创新作统一
  限定，但限定语与第 1 项不相邻。
- 风险：局部阅读会把第一章的工程与小规模集成闭环误读为增量机制效果已经成立；这与合同中的
  “正式机制效果仍待匹配实验”以及证据矩阵中正式匹配机制实验为 `OPEN` 不一致。
- 建议修复：在独立 writer pass 中给第 1 项附加与第 2、3 项同等级的 `[待验证]`，并把“增强”
  改为待检验关系；不改变第一章方法对象或新增 claim。

### P1-02 附录中的第二章主术语发生未授权漂移

- 位置：`thesis/opening_report_draft_zh.md:423-424`。
- 现象：附录称“科学知识表示与证据约束推理”为“当前方法主术语”，而第 0 节、相邻合同和路线
  矩阵的 canonical term 均为“面向智能体的遥感科学知识表示与推理”。
- 风险：前者把“证据状态是方法属性”压缩成新的章级主术语，可能被误读为已经接受的方法命名或
  贡献收窄，违反第 0 节唯一源定义和合同的术语保护。
- 建议修复：在独立 writer pass 中恢复 canonical term；把来源、适用条件和证据状态另写为表示
  与推理需要处理的属性，不新增标题或方法版本。

### P2-01 “错误成功报告”语义不清

- 位置：`thesis/opening_report_draft_zh.md:208-210`；
  `thesis/opening_three_chapter_route_matrix_zh.md:53-56`。
- 现象：“错误成功报告”可能被理解为“错误但成功的报告”，也可能指系统把失败误报为成功。
- 影响：不改变 claim，但会降低第一章评价指标的可解释性。
- 建议修复：writer pass 统一为能明确表达 false-success reporting 的中文短语，并保持两份文件一致。

### P2-02 第一、二、三章的“科学适用性”责任仍可再收窄

- 位置：`thesis/opening_report_draft_zh.md:313-315`；
  `thesis/opening_three_chapter_route_matrix_zh.md:53-56`。
- 现象：文本把“科学适用性”整体交给研究内容二、三，范围大于路线矩阵第 155-164 行已经给出的
  分工。第二章实际负责知识与证据机制的科学意图、严重错误和不必要干预；第三章负责固定任务中
  的 system-level outcome、intended use 与能力边界。
- 影响：当前路线矩阵能够消解冲突，因此不是方法冲突；但正文单独阅读时可能模糊章级评价责任。
- 建议修复：writer pass 用上述两个窄责任替换笼统的“科学适用性”，不增加新评价维度。

## 3. 未发现的阻断问题

- `2,228 / 150 / 60`、`107 / 63`、Route B `2–3` 个冻结案例和 manual 301 角色均保持；
- Route B 仍是“推荐但待研究者确认”，RSS 与 quick corridor baseline 的边界未被抹平；
- Ch1 工程支持、Ch2 reviewer-ready、Ch3 static-audit 与正式效果 `OPEN` 的主要状态未被晋级；
- 第三章没有把用户效用、生态功能、跨城市泛化、自演进或强化学习写成已支持结果；
- 三章的局部机制验证与系统级评测在路线矩阵中保持分层。

## 4. Judgment audit

| 维度 | 得分（0--2） | 证据 |
| --- | ---: | --- |
| 术语 | 1 | 主体术语稳定，但附录出现一个章级主术语漂移。 |
| 数字／状态保持 | 1 | 保护数字均保持；第一章预期创新的待验证状态未局部附着。 |
| Claim--evidence fit | 1 | 三章主要状态有证据路由；第一章创新点 1 的效果措辞超过当前 OPEN 证据。 |
| 引用完整性 | 0 | 6 处内容性 `[REF-MISSING]` 仍没有已核验引用键或 entailment。 |
| 段落功能 | 2 | 不足、问题、目标、内容、路线和基础各有主导功能。 |
| 连贯性 | 2 | 三项不足到三个验证对象及章际接口的推导清楚。 |
| 中文可读性 | 1 | 整体可读；“错误成功报告”和局部超长责任句存在摩擦。 |
| 范围／限定 | 1 | 主要边界存在；第一章创新限定与三章科学适用性责任仍不够局部。 |

本评分只用于审阅分流，不是科学有效性证书。由于存在两个 P1 和 6 处未核验引用，本稿不能称为
`thesis-ready`。

## 5. Reviewer 结论与下一停止点

本轮只交付 findings，不修改主稿、路线矩阵、合同或证据矩阵。下一唯一动作是在独立 writer pass
中只修复 P1-01 与 P1-02，并同步判断两个 P2 是否可在同一受限 scope 内机械收窄；随后重新运行
O1 writing-contract V0 审计，再做一次只读差异复核。若 P1 关闭且没有新增 P1，才进入导师讨论包
首轮。

研究者当前无需决定新问题：四项 findings 均可在既有源定义和合同内处理，不涉及 claim、
scientific gold、方法版本或正式题目晋级。

