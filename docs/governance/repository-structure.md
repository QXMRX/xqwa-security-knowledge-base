---
title: 目录设计
audience: 维护者
status: stable
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-29
---

# 目录设计

本仓库采用按职责拆分的目录结构，避免教学内容、实验、练习和自动化脚本混在一起。

## 目录说明

`docs/` 存放正式发布到网站的教学文档。它是 MkDocs 的内容源，适合放课程说明、学习路径、治理规则和知识文章。

`labs/` 存放可复现实验。实验必须说明运行环境、授权边界、启动方式、验证方式和清理方式。

`exercises/` 存放练习题、复盘题和阶段测验。练习应服务于教学目标，而不是只堆命令或答案。

`templates/` 存放模板。后续可以加入课程模板、实验模板、Pull Request 审核模板和 AI Review 提示词模板。

`scripts/` 存放本地和 CI 共用的自动检查脚本。脚本应保持模块化，方便后续逐步增加 metadata 检查、Markdown 检查、危险内容检查和 AI Review 调用。

`.github/` 存放 GitHub 协作配置，包括 Pull Request 模板、CODEOWNERS 和 GitHub Actions。当前 workflow 只执行基础检查，不接入 AI，不需要写权限。

## 为什么不拆得更细

当前目标是保持项目可运行，而不是设计一个庞大平台。过早拆分会增加维护成本，也会让新成员难以理解项目入口。

当某个目录内容变多时，再按主题拆分。例如 `docs/web/`、`docs/linux/`、`labs/web/`、`labs/forensics/`。

## 后续扩展方式

后续可以逐步增加：

- `scripts/check_metadata.py`：检查文档元数据。
- `scripts/check_security_risks.py`：检查危险命令和敏感信息。
- `scripts/build_rag_index.py`：为问答系统生成索引。
- `.github/workflows/deploy-docs.yml`：部署 MkDocs 到 GitHub Pages。
- `.github/workflows/ai-review.yml`：在人工审核前生成 AI 建议。
