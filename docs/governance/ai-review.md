---
title: AI Review
audience: 维护者和审核者
status: review
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-29
---

# AI Review

AI Review 是本仓库的辅助审核流程，用于在人工维护者合并 Pull Request 前生成一份安全和质量建议报告。

它不替代人工审核，不批准 Pull Request，不合并分支，也不自动绕过 GitHub Actions。

## 用途

AI Review 适合检查人工审核中容易遗漏的线索：

- 是否疑似包含真实密钥、Token、Cookie、密码或私钥。
- 是否出现未授权公网攻击、真实目标扫描、爆破、利用或破坏步骤。
- 实验是否限定在 Docker、CTF、本地虚拟机或授权环境。
- 文档 metadata、MkDocs 导航、贡献规范和脚本说明是否同步。
- Pull Request 范围是否清晰，是否缺少必要测试。

AI Review 的输出是建议清单。最终结论仍由维护者给出。

## 目录

相关文件：

- `scripts/ai_review.py`：AI Review 报告生成脚本。
- `templates/ai-review-prompt.md`：可审核、可版本管理的提示词模板。
- `.github/workflows/ai-review.yml`：手动触发的 GitHub Actions 工作流。
- `AGENTS.md`：AI 协作边界。
- `CONTRIBUTING.md`：人工贡献和审核规范。

## 配置

仓库维护者在 GitHub 中配置：

- Secret：`OPENAI_API_KEY`，用于调用 OpenAI API。
- Variable：`OPENAI_REVIEW_MODEL`，可选；默认使用 `gpt-5.6`。

不要把 API Key 写入仓库、文档、Issue、Pull Request 或日志。

## 运行方式

在 GitHub 页面运行：

1. 打开 `Actions`。
2. 选择 `AI Review`。
3. 点击 `Run workflow`。
4. 输入 Pull Request 编号。
5. 如只想验证提示词构造，将 `dry_run` 设为 `true`。

工作流会生成：

- Workflow summary 中的审核报告。
- `ai-review-report` artifact。

工作流不会自动评论 Pull Request，也不会批准或合并 Pull Request。

## 本地 dry-run

贡献者可以在本地验证提示词构造：

```bash
python scripts/ai_review.py --dry-run --base origin/main --output /tmp/ai-review-dry-run.md
```

这个命令不会调用 OpenAI API，也不需要密钥。

## 本地审核 Pull Request

维护者如果需要在本地生成真实 AI Review 报告，可以设置环境变量后运行：

```bash
GITHUB_TOKEN=your-github-token \
OPENAI_API_KEY=your-openai-api-key \
python scripts/ai_review.py \
  --repo QXMRX/xqwa-security-knowledge-base \
  --pr 1 \
  --output ai-review-report.md
```

如果账号没有默认模型权限，可以设置：

```bash
OPENAI_REVIEW_MODEL=gpt-5.6
```

## 安全设计

AI Review 工作流采用保守设计：

- 只支持 `workflow_dispatch` 手动触发。
- 不使用 `pull_request_target`。
- GitHub 权限只读：`contents: read` 和 `pull-requests: read`。
- 报告只写入 workflow summary 和 artifact。
- 不自动发布评论，不自动 approve，不自动 merge。
- 脚本默认只使用 Python 标准库。

这样可以减少密钥暴露和未审核代码自动接触密钥的风险。

## 审核结论

维护者阅读报告时应重点区分：

- `P0`：真实密钥、未授权攻击或危险破坏性操作，必须阻止。
- `P1`：安全边界、可运行性、CI 或治理流程问题，合并前必须修复。
- `P2`：影响维护质量、教学清晰度或长期演进的问题。
- `P3`：不阻塞合并的格式、表述或补充建议。

AI Review 没有发现问题，不等于 Pull Request 自动通过。维护者仍需检查 PR 模板、CI、CODEOWNERS、分支保护和人工审核意见。

## 如何维护

维护时遵守：

- 修改提示词时同步运行 dry-run。
- 修改脚本时运行 `python -m compileall scripts`。
- 不把 AI Review 变成阻塞式自动批准机制。
- 不在脚本中硬编码密钥、组织 ID 或个人账号。
- 不把报告直接作为最终审核结论。
