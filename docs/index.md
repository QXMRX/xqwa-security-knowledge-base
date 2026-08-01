---
title: XQWA Security Knowledge Base
audience: 全体成员
status: stable
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-31
---

# XQWA Security Knowledge Base

欢迎来到 XQWA 网络安全社团教学资料库。

本资料库用于沉淀社团课程、实验、练习题和协作规范。当前已经建立最小可运行结构：文档能被 MkDocs 构建，Markdown 能被基础脚本检查，所有协作都通过 Pull Request。

## 适用对象

- 网络安全社团新成员。
- 社团教学负责人。
- 资料维护者。
- Pull Request 审核者。

## 当前内容范围

- 项目目录设计。
- 新成员入门说明。
- 安全边界说明。
- Pull Request 审核流程。
- 分支保护建议。
- 自动检查说明。
- AI Review 说明。
- 许可证建议。

当前已加入 [CTF 网络安全实战基础](courses/ctf-101/index.md) 的完整 16 周、32 节课程讲义、
Reveal.js 课件、BUUCTF 优先题单和可公开访问的离线实验源码。教师应在课前确认平台题目可用；
平台不可用时切换到同主题离线实验。Pages 阅读界面由 Docsify 组装并通过 GitHub Actions 部署。

## 协作要求

所有内容修改必须通过 Pull Request。提交前请运行：

```bash
uv run python scripts/check_all.py
uv run mkdocs build --strict
```

AI 可以辅助检查和建议，但最终审核、批准和合并必须由人工维护者完成。
