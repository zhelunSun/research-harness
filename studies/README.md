# Studies

`studies/` 是 `research-harness` 的研究孵化区，用于承载尚未晋级为稳定规范的
证据调查、比较研究和设计提案。

## Boundary

- `ideas/` 维护博士论文方向、研究内容和立项边界。
- `studies/` 维护可被批阅、反驳或继续核验的中间研究。
- `references/` 只维护已经接受、可供 skill 复用的稳定知识。
- `SKILL.md` 是精简的稳定入口，不接收未经人工接受的 study 结论。

Study 的 `source` 结论不因被整理进仓库而自动成为 `verified`。任何会改变
论文 claim、研究方向或 reusable skill 的结论，都必须先形成 proposal 并经过
人工接受。

## Loading rule

Agent 不应默认加载整个 `studies/`。进入一个 study 时只读取：

1. 目标模块的 `README.md`；
2. 当前任务对应的单个 study 文件；
3. 来源账本中被该文件引用的行。

当前 study：

- [`scientific-harness/`](scientific-harness/)：面向长流程 Agent 科研的状态、
  证据、评测、分支和人类门禁研究。
