---
title: 新成员入门
audience: 新成员
status: stable
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-30
---

# 新成员入门

本页面帮助新成员了解如何使用和参与资料库。

## 学习路径

建议先熟悉以下内容：

1. 阅读项目首页，理解资料库目标。
2. 阅读安全边界，明确哪些实验场景被允许。
3. 阅读贡献规范，了解如何通过 Pull Request 提交内容。
4. 阅读 [CTF 网络安全实战基础](courses/ctf-101/index.md)，从第 1 周资料开始。
5. 本地运行基础检查，确认环境可以工作。

## 本地预览

MkDocs 严格构建预览：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

启动后访问 `http://127.0.0.1:8000` 查看文档网站。

Docsify Pages 界面预览：

```bash
python scripts/build_pages_site.py --output /tmp/xqwa-pages-preview
python3 -m http.server 3000 --directory /tmp/xqwa-pages-preview
```

启动后访问 `http://127.0.0.1:3000`。

## 提交内容前

提交 Pull Request 前请确认：

- 文档有清晰标题。
- 实验限定在本地、Docker、CTF 或授权环境。
- 没有真实密钥、账号、Cookie 或 Token。
- 已运行基础检查命令。

## 下一步学习内容

目前已提供课程首页、学习指南和第 1 周教学资料。后续将逐步补充 Web、Crypto、Reverse、Pwn、Misc、AI Security、Docker 实验环境、CTF 题目复盘和安全工具合法使用规范。
