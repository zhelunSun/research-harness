# Proposal: 将第一章状态更新为“统一方法基线 v1，真实模型对照待完成”

## Trigger

URSA 在 `codex/ch1-unified-runtime` 分支完成了一轮架构收敛。此前并列的 AG2 历史会话、独立
workflow runtime 和 D3-light runner 现在有了清楚的主次关系：新工作只通过统一
`ExpertsRSSystem.run()/resume()` 执行；历史 notebook 继续独立复现；D3 evaluator 改为从外部
调用统一系统并读取结果。

当前论文总控仍记录“D2 最小实现待完成”“43 项相关测试”等旧快照，无法准确反映已完成的
工程/诊断证据，也容易让后续 Agent 重复建设第一章或误把真实模型证据视为已经完成。

## Proposed Target

- `process/current_execution_plan_20260802.md` 的 `0.2`、`0.3` 和 M1 checkpoint；
- `evidence/opening_evidence_matrix.md` 的研究内容一证据表和开题门槛；
- 如人类接受证据状态更新，再判断 `THESIS_STATE.md` 是否只需更新证据指针而不发布新 Idea 版本。

不建议改变总题目、三项研究角色、C1 工作性论断、Chapter 2 P0 / Chapter 1 P1 优先级或
`idea-v2026.08.02`。

## Proposed Change

1. 把 M1 当前状态更新为：**统一方法基线 v1 completed-offline；D3-light live evidence open**。
2. 新增或更新以下跨仓库证据指针：
   - branch `codex/ch1-unified-runtime`；
   - baseline `64bfbdc`；统一 runtime checkpoint `31c5c09`；统一 D3 evaluator `8b372b9`；
   - `URSA/docs/thesis/ch1_evidence_system/system_convergence_audit_20260813.md`；
   - `URSA/docs/thesis/ch1_evidence_system/UNIFIED_RUNTIME_REVIEW_PACKET.md`；
   - `URSA/docs/thesis/ch1_evidence_system/PLAN.md`。
3. 将旧“43 项测试”更新为“2026-08-13 标准发现 75 项通过”，但保持为
   `VERIFIED-ASSET / engineering support`，不晋级为效果证据。
4. 在 opening evidence matrix 中区分两行：
   - 统一 `run/resume`、真实本地工具、权限、轨迹、逻辑检查点和离线场景：
     `VERIFIED-ASSET / DIAGNOSTIC`；
   - 真实模型 matched comparison：`OPEN`。
5. 将第一章五项开题门槛记为：1、2、3、5 已有可检查实现证据；4 只有 5 任务 × 3 条件的
   离线协议预飞行，真实模型小试仍未完成。
6. 当前唯一论文级下一动作仍保持 Chapter 2 P0。第一章后续作为有界 P1：先完成 live 所需最小
   加固，经 API/披露门禁后跑三次 smoke 和 5×3 小对照；完成 claim-safe 结果备忘即停止扩建。
7. 记录命名冲突供人类裁决：第一章条件曾使用 `P0–P3`、`B0–B3`，第二章已使用 `B0–B5`。
   建议保留冻结 JSON 中的历史 ID，并在新材料加章节前缀写作
   `C1-B1/C1-B2/C1-B3`；若正式改 ID，须新建协议版本，不回写历史结果。

建议总控允许的阶段表述：

> 第一章新增方法已经形成统一、可运行、可审计的离线方法基线，真实模型匹配效果证据仍待完成。

禁止晋级为：

- “第一章已经实验完成”；
- “系统整体在真实模型下通过”；
- “多智能体或检查点恢复已证明提升可靠性”；
- “18 个工具均已由 Agent 自主可靠调用”；
- “具备通用进程崩溃恢复能力”。

## Evidence

- `D:/projects/phd-thesis/URSA`, branch `codex/ch1-unified-runtime`, commits
  `31c5c09` and `8b372b9` on baseline `64bfbdc`.
- 2026-08-13 rerun: `python -m unittest discover -s ExpertsRS -q` → 75 tests, OK.
- `URSA/docs/thesis/ch1_evidence_system/system_convergence_audit_20260813.md`.
- `URSA/docs/thesis/ch1_evidence_system/UNIFIED_RUNTIME_REVIEW_PACKET.md`.
- Evidence status: local code/test facts are `verified-asset`; scripted runs and offline D3 slots are
  `diagnostic`; live treatment effects remain `open`.

## Risk

采用本提案的风险是，“统一底盘”可能在汇报中被误听为完整科学系统或正式结果，因此必须同时
保留 non-claims 和 live gate。若不采用，旧总控快照会诱导后续 Agent 重复 D2、继续引用错误测试
数量，并把第一章扩大成长期平台工程。

另一个风险是第一章条件命名与第二章 B0–B5 冲突。命名调整只能影响未来正式协议，不能回写或
重命名历史工件。

## Human Decision Needed

Yes.

请研究者确认：

1. 是否接受“方法基线 v1 completed-offline / live matched comparison open”的证据状态；
2. 是否保持 Chapter 2 P0、Chapter 1 P1 的总体优先级；
3. 是否接受第一章正式条件改用不与第二章冲突的新前缀；
4. 是否认可第一章在最小 5×3 live 对照后停止平台扩建。
