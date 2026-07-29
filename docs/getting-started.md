# 新成员入门

本页面帮助新成员了解如何使用和参与资料库。

## 学习路径

第一阶段尚未建立完整课程体系。当前建议先熟悉以下内容：

1. 阅读项目首页，理解资料库目标。
2. 阅读安全边界，明确哪些实验场景被允许。
3. 阅读贡献规范，了解如何通过 Pull Request 提交内容。
4. 本地运行基础检查，确认环境可以工作。

## 本地预览

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

启动后访问 `http://127.0.0.1:8000` 查看文档网站。

## 提交内容前

提交 Pull Request 前请确认：

- 文档有清晰标题。
- 实验限定在本地、Docker、CTF 或授权环境。
- 没有真实密钥、账号、Cookie 或 Token。
- 已运行基础检查命令。

## 下一步学习内容

后续阶段会逐步补充：

- Web 安全基础。
- Linux 与网络基础。
- Docker 实验环境。
- CTF 题目复盘。
- 安全工具合法使用规范。
