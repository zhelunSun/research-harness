# Proposal: 冻结第一章底盘与第二、三章的最小对接顺序

## Trigger

URSA 统一 runtime 已接近第一章 5 任务 × 3 条件 live pilot 门槛。Chapter 2 已存在
task-conditioned epistemic contract、证据准入和 candidate update 设计；Chapter 3 已存在
`EvalTask → TrialTrace → Outcome → Evaluation`、北京制图资产和分层评测规划。目前缺口不是新的
论文故事，而是三章之间的版本化运输合同、所有权和合入时序。

若现在直接把知识库、评估器和 runtime 混合实现，会污染第一章 matched comparison，并重新产生
双调度、gold 泄漏和“valid=True”混装科学/工程/评估判断的问题。若完全等待第一章实验结束再开始，
又会无谓阻塞下游 schema 和资产整理。

## Proposed Target

- 论文总控 `process/current_execution_plan_20260802.md` 的跨章接口/下一动作说明；
- Chapter 2 当前 P0 sprint 的 runtime export/import sidecar；
- Chapter 3 E0–E5 evaluation preparation 顺序；
- URSA `docs/thesis/ch1_evidence_system/PLAN.md` 第 10 节作为实现级 active brief。

不改变总题目、三章角色、Chapter 2 P0 / Chapter 1 P1 / Chapter 3 P2 优先级和各章核心 claim。

## Proposed Change

采用三种事实源分离：

1. Chapter 1 runtime 拥有 plan/action/observation/artifact/checkpoint/terminal facts；
2. Chapter 2 拥有 evidence/applicability/obligation/admission facts；
3. Chapter 3 拥有 hidden outcome assertions/gold/fault/rubric/evaluation facts。

冻结以下跨仓库合同：

- Chapter 2 生产版本化 `ScientificContractBundle`；URSA 通过
  `ScientificConstraintPort` 消费并确定性映射
  `pass/revise/add_validation/ask/reject/downgrade/escalate`；
- URSA 生产 portable `TrialExport`；Chapter 3 通过 `EvalTaskAdapter` 和外部 grader 消费；
- task episode 只能生成 Chapter 2 `CandidateUpdatePacket` 并进入 quarantine/review，不能在线修改
  active ledger/contract；
- `RunResult.validation` 只表示 runtime/contract/artifact 完整性，不代表科学正确或 Chapter 3 评分。

采用并行但隔离的时序：

1. 现在完成 X0 schema/ownership review；
2. Chapter 2 和 Chapter 3 现在可分别导出一个 schema + example + validator；
3. URSA WP1 合入后，在独立分支实现 NoOp/Fake ports 与 `TrialExport`；
4. 第一章 live 5×3 始终在无跨章端口污染的冻结 commit 上完成；
5. 15-run 完成并形成 claim-safe memo 后，再合入端口并做 Chapter 2 diagnostic loop 和 Chapter 3
   deterministic evaluation MVP；
6. Chapter 2 正式效果实验、Chapter 3 grader/user study 各自通过人工 Gate 后单独启动。

建议工程版本：`v0.5.1` 第一章 pilot freeze；`v0.6.0` extension-ready；`v0.6.1` Ch2 diagnostic
contract loop；`v0.7.0` Ch3 deterministic evaluation MVP/cross-chapter demo。这些是工程里程碑，不是
论文证据等级。

## Evidence

- `URSA/docs/thesis/ch1_evidence_system/PLAN.md`, section 10.
- `chapter2-urban-forest-knowledge/thinking-space/task-conditioned-epistemic-contract-spec.md`.
- `chapter2-urban-forest-knowledge/config/ch2_constraint_pipeline.json`.
- `chapter2-urban-forest-knowledge/config/ch2_update_packet.schema.json`.
- `urbfo-agent-demo/docs/plans/ch3_reliability_validation_alignment_20260730.md`.
- `urbfo-agent-demo/docs/plans/ch3_asset_to_eval_and_hitl_plan_20260731.md`.
- Evidence status: existing designs are `frozen-design` or candidate/diagnostic; cross-chapter implementation and
  effect evidence remain open.

## Risk

若采用，主要风险是接口过早标准化。缓解方式是 v1 只支持一个 Ch2 bundle 和一个 Ch3 task/export
例子，所有 schema 带版本并 fail closed，不引入通用 hook/plugin 平台。

若不采用，三个仓库很可能各自复制 task、trace、validation、report 和 runner 语义，重新形成系统
拼盘；也可能让 Chapter 3 evaluator 或 Chapter 2 gold 进入 Agent 上下文，破坏实验有效性。

## Human Decision Needed

Yes.

请研究者确认：

1. 是否接受三种事实源和 schema ownership 分离；
2. 是否允许 X0/X1 schema 准备与第一章 5×3 并行，但端口实现隔离到独立分支；
3. 是否接受先做 Ch2 diagnostic behavior change、Ch3 deterministic MVP，再分别进入正式效果与
   用户研究；
4. 是否接受 `v0.7.0` 只表示跨章研究系统演示完成，不表示第二、三章科学结论完成。

