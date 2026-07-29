# Pull Request 审核流程

本阶段建立 Pull Request 审核流程。目标是让每一次资料修改都能被人工审核、被自动检查、被清晰追踪。

## 用途

Pull Request 是本项目唯一的正式变更入口。它承担三件事：

- 记录变更原因。
- 触发基础自动检查。
- 提供人工审核和讨论空间。

任何人都不应直接向 `main` 推送内容。

## 目录

本阶段新增和维护的文件包括：

- `.github/pull_request_template.md`：贡献者提交 Pull Request 时填写的模板。
- `.github/CODEOWNERS`：默认审核责任人配置。
- `docs/governance/pr-review-process.md`：审核流程说明。
- `docs/governance/branch-protection.md`：分支保护建议。
- `templates/review-checklist.md`：人工审核清单模板。

## 调用关系

贡献者创建 Pull Request 后，GitHub 会自动加载 `.github/pull_request_template.md`。Pull Request 指向 `main` 时，`Basic Checks` workflow 会运行 Markdown 检查和 MkDocs 构建。

如果仓库启用了 CODEOWNERS 和分支保护，GitHub 会根据 `.github/CODEOWNERS` 请求默认维护者审核。维护者审核时可以参考 `templates/review-checklist.md`，并在 GitHub Review 中选择 `Approve`、`Comment` 或 `Request changes`。

## 审核角色

贡献者负责：

- 按模板说明变更目的。
- 标明是否涉及实验、命令或安全测试步骤。
- 本地运行基础检查。
- 根据审核意见修改。

审核者负责：

- 判断内容是否符合教学目标。
- 判断安全边界是否明确。
- 检查是否存在敏感信息。
- 检查实验是否可复现。
- 确认 CI 是否通过。
- 给出明确审核结论。

AI 只负责辅助发现问题和提出建议，不负责批准或合并。

## 审核结论

`Approve` 表示没有阻塞问题，可以合并。

`Comment` 表示有建议或小问题，但不阻塞合并。

`Request changes` 表示存在必须修改的问题。以下情况必须选择 `Request changes`：

- 出现真实 Token、Cookie、密码、API Key、SSH Key 或数据库账号。
- 包含未授权公网目标的扫描、爆破、利用或攻击步骤。
- 实验步骤无法复现，且会误导新成员。
- 高风险命令没有说明影响范围和清理方式。
- Pull Request 改动范围过大，无法有效审核。

## 如何测试

贡献者和审核者都可以运行：

```bash
python scripts/check_markdown.py
mkdocs build --strict
```

审核者还应在 GitHub 页面确认 `Basic Checks` 通过。

## 如何维护

当社团审核标准变化时，优先更新：

1. `.github/pull_request_template.md`
2. `templates/review-checklist.md`
3. 本页面

如果某类问题反复出现，应先把规则写进模板或检查清单。只有当规则稳定、误报可控时，才进入第三阶段，把它升级为 GitHub Actions 自动检查。

## 后续扩展

第三阶段可以增加更细的自动检查，例如：

- metadata 必填字段检查。
- Markdown 链接检查。
- 敏感信息扫描增强。
- 危险命令规则拆分。
- Pull Request 标题规范检查。

第四阶段再接入 Codex AI Review，但 AI Review 仍然只能提出建议，不自动批准 Pull Request。
