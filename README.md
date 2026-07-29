# XQWA Security Knowledge Base

面向网络安全社团的教学资料库，用于沉淀课程讲义、实验说明、练习题、社团协作规范和后续 AI 辅助审核能力。

当前仓库处于第一阶段：项目初始化。目标是先建立一个能被 GitHub Actions 检查、能被 MkDocs 构建、能让成员按 Pull Request 协作的最小可运行资料库。

## 当前阶段目标

- 建立统一目录结构。
- 建立 Markdown 教学资料入口。
- 建立贡献和审核规则。
- 建立基础自动检查，不包含 AI 审核。
- 为后续 MkDocs Pages 部署、Codex Review、RAG 问答系统预留清晰扩展点。

## 为什么这样设计

项目优先采用简单、稳定、低维护成本的结构。Markdown 负责资料内容，MkDocs Material 负责网站构建，Python 脚本负责本地和 CI 中复用的检查逻辑，GitHub Actions 只负责自动执行基础检查。

AI 在本项目中只作为辅助审核者，不自动批准 Pull Request，不自动合并主分支，不替代教学负责人。

## 仓库结构

```text
.
├── docs/                 # 面向网站发布的正式教学文档
├── labs/                 # 可复现实验，必须限定 Docker、CTF、本地或授权环境
├── exercises/            # 练习题、复盘题、阶段测验
├── templates/            # 内容模板、实验模板、审核模板
├── scripts/              # 本地和 CI 共用的检查脚本
├── .github/workflows/    # GitHub Actions 工作流
├── AGENTS.md             # AI 协作规则
├── CONTRIBUTING.md       # 人类贡献者协作规范
├── LICENSE               # 代码许可证
├── mkdocs.yml            # MkDocs 站点配置
└── requirements.txt      # 文档构建依赖
```

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_markdown.py
mkdocs build --strict
mkdocs serve
```

本地预览启动后，访问 `http://127.0.0.1:8000`。

## 协作流程

所有修改必须通过 Pull Request：

1. 从 `main` 创建功能分支。
2. 在分支中修改 Markdown、脚本或配置。
3. 本地运行 `python scripts/check_markdown.py` 和 `mkdocs build --strict`。
4. 提交 Pull Request。
5. 等待人工审核和 CI 通过。
6. 由维护者合并。

禁止直接向 `main` 推送内容。仓库维护者需要在 GitHub 中开启分支保护规则。

## 安全边界

本项目只允许面向合法教学场景的内容：

- Docker 本地实验。
- CTF 靶场。
- 本地虚拟机环境。
- 明确授权的测试环境。

不得引导攻击公网、真实服务器或第三方网站。不得提交真实 Token、Cookie、密码、API Key、SSH Key 或数据库账号。

## 许可证建议

当前仓库已有 MIT License，适合代码、脚本和配置文件。由于本项目主体是教学资料，建议后续由社团确认是否增加内容许可证，例如 CC BY 4.0 或 CC BY-NC-SA 4.0，并在 `docs/`、`labs/`、`exercises/` 中明确适用范围。

## 后续里程碑

1. Pull Request 审核流程。
2. GitHub Actions 自动检查增强。
3. Codex AI Review。
4. MkDocs 自动部署到 GitHub Pages。
5. AI 检索系统。
6. RAG 问答平台。
7. 后台管理系统。
