# Pull Request Review Checklist

本模板供维护者审核 Pull Request 时参考。可以复制到 GitHub Review 评论中，也可以作为审核前的个人清单。

## 基本信息

- Pull Request 是否只解决一个明确问题。
- 标题是否能准确描述变更。
- 描述是否说明了为什么需要修改。
- 变更文件是否和描述一致。

## 教学质量

- 内容是否服务于明确学习目标。
- 是否说明适用对象和前置知识。
- 是否避免只堆命令而不解释原因。
- 是否需要补充练习题、参考资料或复盘问题。

## 安全边界

- 是否限定在 Docker、CTF、本地虚拟机或明确授权环境。
- 是否避免引导攻击公网、真实服务器或第三方网站。
- 是否没有真实 Token、Cookie、密码、API Key、SSH Key 或数据库账号。
- 高风险命令是否说明影响范围、执行条件和清理方式。

## 可运行性

- `python scripts/check_markdown.py` 是否通过。
- `mkdocs build --strict` 是否通过。
- GitHub Actions 中 `Basic Checks` 是否通过。
- 如果包含实验，步骤是否足够复现。

## 审核结论

建议选择：

- `Approve`：没有阻塞问题。
- `Comment`：只有非阻塞建议。
- `Request changes`：存在安全、可运行性、结构或敏感信息问题。

## 维护说明

如果同类问题反复出现，应更新 Pull Request 模板或自动检查脚本，而不是只在单个 Pull Request 中重复提醒。
