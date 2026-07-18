# Idea 维护说明

## Canonical files

- `../THESIS_STATE.md`：当前总体状态、总科学问题和维护边界；
- `chapter_ideas.md`：三项研究内容的完整 idea；
- `../decisions/`：已经接受的方向性决策及原因；
- `../claims/key_claims.md`：待验证的工作性论断。

## Update rule

1. 新讨论先修改 `chapter_ideas.md` 草案；
2. 人工确认后更新 `THESIS_STATE.md`；
3. 涉及主线或边界变化时新增/修订 decision；
4. 同步调整 working claims；
5. Idea 版本稳定后，再单独更新中文提纲和下游执行计划。

## Scope boundary

Idea 文件不维护：

- 中文论文的节级目录；
- 具体算法实现；
- 实验组、任务数量和统计方案；
- 子仓库进度和运行结果；
- 项目排期。

中文大论文正式提纲计划维护在 `../thesis/outline_zh.md`，并通过独立提交与相应 idea 版本关联。
