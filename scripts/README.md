# Scripts

本目录用于存放本地和 GitHub Actions 共用的自动化脚本。

当前脚本：

- `check_markdown.py`：检查 Markdown 文件是否为空、是否有一级标题、是否包含疑似敏感信息或高风险命令。

运行方式：

```bash
python scripts/check_markdown.py
```

后续扩展时应保持模块化，不要把 metadata 检查、危险内容检查、AI Review 和 RAG 索引全部塞进一个脚本。
