# AI Collaboration Rules

本文件定义 AI 助手在本仓库中的协作边界。所有 AI 生成、修改或审核内容时，都必须遵守这些规则。

## 项目目标

本仓库用于建设网络安全社团教学资料库。AI 的角色是辅助维护者提升资料质量，而不是替代人工审核或自动决策。

## AI 可以做什么

- 检查 Markdown 结构和表达质量。
- 发现教学逻辑缺口。
- 提醒知识点错误或过时风险。
- 检查实验是否缺少授权边界。
- 发现疑似真实密钥、Cookie、Token 或密码。
- 提醒危险命令和高风险操作。
- 建议参考资料、练习题和改进方向。
- 编写可运行的检查脚本、文档配置和测试命令。

## AI 不得做什么

- 不得自动批准 Pull Request。
- 不得自动合并 `main` 分支。
- 不得绕过 GitHub Actions。
- 不得提交真实密钥、Cookie、Token、密码或数据库账号。
- 不得引导攻击公网、真实服务器或第三方网站。
- 不得自动执行危险脚本。
- 不得把模拟示例伪装成真实测试结果。

## Pull Request 审核中的 AI 边界

AI 可以协助维护者阅读差异、指出风险、建议修改文案和补充测试命令。AI 输出应作为 review comment 或建议清单，由人工维护者判断是否采纳。

AI 不得把自己的检查结果表述为人工批准，也不得绕过 Pull Request 模板、CODEOWNERS、分支保护或 GitHub Actions。

## 安全边界

允许的实验环境：

- Docker 本地实验。
- CTF 靶场。
- 本地虚拟机。
- 明确授权的测试环境。

禁止的内容：

- 针对公网 IP 或真实域名的攻击步骤。
- 绕过授权的扫描、爆破、利用或持久化。
- 未说明风险和清理方式的破坏性命令。

## 仓库目录职责

- `docs/`：正式发布到网站的教学文档。
- `labs/`：可复现实验内容。
- `exercises/`：练习题和阶段测验。
- `templates/`：内容模板和审核模板。
- `scripts/`：本地和 CI 共用脚本。
- `.github/workflows/`：自动检查流程。
- `.github/pull_request_template.md`：Pull Request 提交模板。
- `.github/CODEOWNERS`：默认审核责任人配置。

## 必须优先运行的检查

```bash
python scripts/check_all.py
mkdocs build --strict
```

如果修改 Python 脚本，还应至少运行对应脚本本身，确保退出码符合预期。

## 扩展原则

新增模块时应保持模块化。metadata 检查、Markdown 检查、危险内容检查、AI Review、网站部署和 RAG 索引应分别维护，避免把所有逻辑塞进一个脚本或工作流。
