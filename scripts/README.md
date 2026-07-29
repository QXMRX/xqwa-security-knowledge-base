# Scripts

本目录用于存放本地和 GitHub Actions 共用的自动化脚本。

当前脚本：

- `check_all.py`：统一运行所有本地质量检查，供贡献者和 GitHub Actions 使用。
- `check_markdown.py`：检查 Markdown 文件是否为空、是否有一级标题、是否存在行尾空格。
- `check_metadata.py`：检查 `docs/` 页面是否包含必需维护元数据。
- `check_security_content.py`：检查疑似真实密钥、高风险命令和指向公网目标的攻击工具示例。
- `common.py`：共享文件遍历、UTF-8 读取和检查结果输出逻辑。

运行方式：

```bash
python scripts/check_all.py
```

后续扩展时应保持模块化，不要把 metadata 检查、危险内容检查、AI Review 和 RAG 索引全部塞进一个脚本。
