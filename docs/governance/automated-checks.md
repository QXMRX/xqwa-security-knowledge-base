---
title: 自动检查
audience: 贡献者和维护者
status: stable
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-29
---

# 自动检查

本页面说明 GitHub Actions 自动检查。目标是把已经稳定的人工审核规则转化为可重复执行的脚本，减少维护者重复检查的负担。

## 用途

自动检查负责发现明确、可机械判断的问题：

- Markdown 文件结构问题。
- 文档维护元数据缺失。
- 疑似真实密钥或敏感凭据。
- 高风险命令。
- 攻击工具示例中指向公网目标的命令。
- MkDocs 构建错误。

自动检查不负责判断教学内容是否讲得好，也不负责批准 Pull Request。这些仍然由人工审核完成。

## 目录

相关文件：

- `scripts/check_all.py`：统一检查入口。
- `scripts/check_markdown.py`：Markdown 结构检查。
- `scripts/check_metadata.py`：文档 metadata 检查。
- `scripts/check_security_content.py`：安全内容检查。
- `scripts/ai_review.py`：手动 AI Review 报告生成脚本，不属于默认阻塞检查。
- `scripts/common.py`：共享工具函数。
- `.github/workflows/basic-checks.yml`：GitHub Actions 工作流。
- `.github/workflows/ai-review.yml`：手动触发的 AI Review 工作流。

## 调用关系

贡献者本地运行：

```bash
python scripts/check_all.py
mkdocs build --strict
```

GitHub Actions 在 Pull Request 和 `main` push 时运行同一组检查：

```bash
python -m compileall scripts
python scripts/check_all.py
mkdocs build --strict
```

`check_all.py` 会按顺序调用 Markdown、metadata 和安全内容检查。任何一个脚本失败，整个检查失败。

AI Review 不在 `check_all.py` 中自动运行。它需要维护者手动触发，用于生成建议报告，而不是替代基础检查或人工审核。

## Metadata 规则

`docs/` 下的正式页面必须包含 YAML front matter：

```yaml
---
title: 文档标题
audience: 适用对象
status: stable
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-29
---
```

字段含义：

- `title`：必须和页面一级标题一致。
- `audience`：说明主要读者。
- `status`：可选 `draft`、`review`、`stable`、`deprecated`。
- `owner`：维护责任人。
- `review_cycle`：可选 `monthly`、`quarterly`、`yearly`、`as-needed`。
- `updated_at`：使用 `YYYY-MM-DD`。

## 安全内容规则

安全内容检查会阻止：

- 常见真实密钥格式。
- 私钥块。
- 破坏性根目录命令。
- 远程脚本直接管道到 shell。
- 常见攻击工具命令中出现公网 IP 或非示例公网域名。

这些检查无法替代人工判断。它们只负责拦截高确定性风险。

## 如何测试

本地运行：

```bash
python scripts/check_all.py
mkdocs build --strict
```

如果修改了检查脚本，还应运行：

```bash
python -m compileall scripts
```

## 如何维护

新增检查时应遵守：

- 优先写成独立脚本。
- 默认只使用 Python 标准库。
- 避免过度激进的规则，减少误报。
- 先在人工审核中验证规则，再升级为 CI 阻塞。
- 在本页面说明用途、调用方式和扩展边界。

## 后续扩展

后续可以增加：

- Markdown 内部链接检查。
- Pull Request 标题检查。
- 实验文档专用 metadata 检查。
- 参考资料 URL 可访问性检查。
- AI Review 报告结构化输出。
