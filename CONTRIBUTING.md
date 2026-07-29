# Contributing Guide

感谢参与 XQWA Security Knowledge Base。这个仓库的目标不是收集零散笔记，而是形成长期可维护、可审核、可部署的网络安全教学资料库。

## 基本原则

- 所有修改通过 Pull Request。
- 不直接修改 `main` 分支。
- 每个 Pull Request 只解决一个明确问题。
- 教学内容必须可复现、可审核、可维护。
- 安全实验必须限定在 Docker、CTF、本地环境或明确授权环境。

## 分支命名

推荐格式：

```text
docs/topic-name
labs/lab-name
exercises/exercise-name
scripts/check-name
```

示例：

```text
docs/web-intro
labs/docker-sqli-basic
scripts/markdown-check
```

## 提交内容要求

Markdown 文档应满足：

- 使用清晰的一级标题。
- 说明适用对象。
- 说明前置知识。
- 说明学习目标。
- 如果包含实验，必须说明实验边界和清理方式。
- 不提交真实密钥、账号、Cookie、Token 或个人敏感信息。

脚本应满足：

- 默认使用 Python 3.12。
- 尽量只使用标准库。
- 保持函数短小、职责单一。
- 能在本地和 GitHub Actions 中使用同一条命令运行。

## 本地检查

提交前请运行：

```bash
python scripts/check_all.py
mkdocs build --strict
```

如果还没有安装 MkDocs：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Pull Request 审核要求

提交 Pull Request 时，请完整填写 `.github/pull_request_template.md` 中的字段。模板不是形式主义，它帮助审核者快速判断这次修改是否安全、是否可运行、是否符合教学目标。

维护者审核时重点关注：

- 内容是否符合教学目标。
- 实验是否在合法授权边界内。
- 是否出现真实密钥或敏感信息。
- 是否有危险命令或误导性操作。
- 是否能被 MkDocs 正常构建。
- 是否需要补充练习题或参考资料。

AI 可以辅助发现问题和提出建议，但不得自动批准或合并 Pull Request。

## 审核结论

审核者应使用以下三类结论：

- `Approve`：内容清晰，CI 通过，没有阻塞问题，可以合并。
- `Comment`：有建议或小问题，但不阻塞合并。
- `Request changes`：存在安全边界、可运行性、结构完整性或敏感信息风险，必须修改后再合并。

任何包含真实密钥、未授权公网攻击步骤、不可控危险命令的 Pull Request，都必须选择 `Request changes`。

## 合并前检查

维护者合并前应确认：

- Pull Request 模板已填写。
- 至少一名维护者已审核。
- `Basic Checks` 已通过。
- 没有未解决的阻塞评论。
- 变更范围和 Pull Request 标题一致。
- 不包含真实密钥或未经授权的测试目标。

## 不接受的内容

- 面向公网目标的攻击教程。
- 未授权测试真实网站或真实服务器的步骤。
- 真实 Token、Cookie、密码、API Key、SSH Key、数据库账号。
- 无法复现的实验步骤。
- 只贴工具命令、不解释原理和边界的内容。

## 维护建议

如果某个主题不断扩展，优先拆成多个小文档，而不是维护一个很长的文件。后续可以逐步引入更细的内容模板、AI Review 和 RAG 索引，但每一步都必须保持基础结构可运行。
