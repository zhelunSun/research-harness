# Section brief

- Document / section: `thesis/opening_report_draft_zh.md`, Sections 2.5–5.4
- Writing mode: argument edit
- Reader question answered: 现有研究的三个不足如何导出总体科学问题、三项递进研究、技术路线和已有基础？
- One-sentence section job: 在不改变第 0 节章级源定义的前提下，把“研究不足—科学问题—目标—研究内容—技术路线—前期基础”编辑为可连续阅读的 O1 论证链。
- Authoritative sources: 相邻 writing contract 所列决策、claim ledger、opening evidence matrix、章级源定义、三章路线矩阵和 Ch3 静态审计。
- Approved claims: Ch1 工程与小规模集成闭环已完成但正式机制效果 open；Ch2 知识与任务资产已可操作但方法与效果待验证；Ch3 真实资产可转换为评测任务，但首轮路线和系统效果均未确认。
- Evidence route for each claim: Ch1 claim registry/evidence index；Ch2 C0/G3/G4 artifacts；Ch3 asset–task–grader–claim audit 与实际 manifest 核数。
- Method/data/evaluation state: Ch1 `engineering_support + diagnostic_evidence`；Ch2 `reviewer-ready; pending human shallow review`；Ch3 `static audit completed; Evaluation MVP pending human route confirmation`.
- Required limitations: 不晋级规划优越性、scientific gold、系统可靠性、用户效用、生态功能、跨任务或跨城市泛化。
- Canonical terms and English anchors: 三项工作标题；可调整的分层规划；随执行更新的过程图；任务条件化科学知识表示；Route B 只读离线治理链；`TrialTrace`、`Outcome`、`Evaluation`.
- Protected numbers and literals: `2,228 / 150 / 60`；`107 / 63`；Route B 首轮 `2–3` 个冻结案例；见相邻 writing contract。
- Required citations: 不新增外部引文；全文保留原有 `[REF-MISSING]` 和直接证据路由。
- Unresolved markers: 外部文献引用；Ch2 最小表示与运行界面；Ch3 Route B 首轮路线；最终送审题目。
- Explicit non-goals: 不修改第 0 节源定义；不创建新 Idea/claim；不冻结 Ch2/Ch3 方法；不运行实验；不制作正式引用。
- Paragraph function map: 三个研究缺口及其共同对象链 → 总问题的三个可验证对象 → 三项目标的交付接口 → 每章问题/方法/验证/边界 → 局部机制与系统评测分工 → 前期资产与待闭合实证环。

## Change ledger

| ID | Type: argument/language | Before | After | Evidence or authorization |
| --- | --- | --- | --- | --- |
| L1 | argument | 2.5 的三项不足与 3.1 总问题直接相邻 | 增加“工作流形成—知识作用—系统评测”共同链条和三个可验证对象 | 章级源定义 0.1–0.4；三章路线矩阵 |
| L2 | argument | 三项目标只按编号并列 | 显式写出上游交付与下游消费接口，并限定第三章不替代前两章消融 | `B12/B23`；opening route matrix |
| L3 | argument | Ch3 泛写两至三条任务链并先恢复环境 | 改为“少量任务链 + Route B 首组 2–3 个冻结案例”，RSS 作备选，路线仍待研究者确认 | Ch3 静态审计 7.1–7.2 |
| L4 | argument | 前期基础四节结束后直接进入预期创新 | 增加“资产支持可执行性、不替代三个实证环”的收束段 | opening evidence matrix Section 6 |
| L5 | evidence correction | opening evidence matrix 把 manifest 的 64 个物理行写成 64 条记录，并保留易过时的日志行数 | 按 `Import-Csv` 核验改为 63 条数据记录；将日志改为“持续更新”而不用物理行数作稳定指标 | `urbfo-agent-demo/experiments/results/manifest.csv` 现场核数 |
| L6 | language | 章节之间主要依赖标题和编号过渡 | 只增加局部因果与边界过渡，不改变原有 claim 强度 | O1 连续正文里程碑 |

## Validation debt

- V0 deterministic: 本轮完成后运行全文 writing-contract 审计、JSON 解析、Markdown 链接和 `git diff --check`。
- V1 fresh-context review: 待一名未参与本轮生成的 reviewer 检查 claim–evidence、章节衔接和限定语是否局部附着；未闭合前不称 thesis-ready。
- V2 researcher gate: Ch3 Route B 首轮路线、Ch2 最小表示与运行界面、最终题目和正式 claim 保持未决。

## Writer judgment audit

| Dimension | Score | Evidence |
| --- | --- | --- |
| Terminology | 2 | 三项标题、任务条件化知识表示、Route B 与 RSS 的名称和角色一致。 |
| Number/state preservation | 2 | Ch2 `2,228 / 150 / 60`、Ch3 `107 / 63`与 `2–3` 冻结案例已绑定；候选、诊断、open 和 pending 状态未晋级。 |
| Claim–evidence fit | 2 | 工程闭环、任务队列和评测资产各自紧邻“能支持／不能支持”限定。 |
| Citation integrity | 1 | 本轮没有发明引用并保留全部 `[REF-MISSING]`；文献 entailment 尚未完成。 |
| Paragraph function | 2 | 新增段落分别承担缺口汇合、问题分解、目标交付、章际责任和基础收束。 |
| Coherence | 2 | 研究不足到科学问题、研究目标、技术路线和前期基础已有显式推导关系。 |
| Chinese readability | 2 | 主语、操作和限定语就近，未增加宣传性结论或空泛创新口号。 |
| Scope/limitations | 2 | Route B 明确不代表端到端制图能力；三章已有资产均不替代匹配实验或跨方法试跑。 |

本表是 writer 自审，不满足 V1 角色分离。当前唯一确定性修正为：将 manifest 从含表头的 64 个物理行改为 63 条数据记录，并移除易过时的日志物理行数。
