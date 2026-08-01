---
title: Pages 部署
audience: 维护者和仓库管理员
status: review
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-31
---

# Pages 部署

本仓库使用 Docsify 作为 GitHub Pages 的公开阅读界面。站点不设置登录、访问名单或应用层鉴权，
任何人都可以通过 `https://qxmrx.github.io/xqwa-security-knowledge-base/` 访问讲义、
幻灯片和公开实验源码。BUUCTF、DASCTF 等外部平台是否需要登录，由对应平台决定。

MkDocs 仍保留为本地和 CI 中的严格构建检查，用来发现导航、Markdown 扩展和结构问题。Pages 部署则由 Docsify 提供更轻量的静态界面。

## 目录

相关文件：

- `docs/`：正式 Markdown 内容源。
- `docsify/index.html`：Docsify 页面入口。
- `docsify/_sidebar.md`：Docsify 侧边栏。
- `docsify/.nojekyll`：避免 GitHub Pages 忽略下划线开头文件。
- `labs/ctf-101/`：可公开分发的本地实验源码、样例和生成脚本。
- `scripts/build_pages_site.py`：组装 Pages 静态目录。
- `.github/workflows/deploy-pages.yml`：部署 GitHub Pages 的 Actions 工作流。

## 运行方式

仓库管理员需要在 GitHub 页面配置：

```text
Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

合并到 `main` 后，`Deploy Pages` workflow 会自动执行：

1. 检出仓库。
2. 将 `docs/` 内容复制到 `_site/`。
3. 将 `docsify/` 中的入口文件覆盖到 `_site/`。
4. 复制筛选后的 `labs/ctf-101/` 源码，排除生成物、缓存和编译后的漏洞程序。
5. 上传 `_site/` 为 Pages artifact。
6. 部署到 `github-pages` 环境。

## 本地预览

本地预览 Docsify Pages 界面：

```bash
uv run python scripts/build_pages_site.py --output /tmp/xqwa-pages-preview
python3 -m http.server 3000 --directory /tmp/xqwa-pages-preview
```

启动后访问 `http://127.0.0.1:3000`。

## 安全设计

Pages 部署采用保守设计：

- 只在 `main` push 或维护者手动触发时部署。
- 不使用 `pull_request_target`。
- 不读取 AI API Key 或其他 repository secret；只使用 GitHub 自动注入的 token 完成 Pages 发布。
- 只部署 `docs/`、`docsify/` 与筛选后的 `labs/ctf-101/` 源码。
- 不发布 `labs/ctf-101/generated/`、`__pycache__/` 或编译后的漏洞演示程序。
- 不部署本地 `.venv/`、`site/`、Git 历史或工作区临时文件。

## 维护要求

维护时遵守：

- 修改 `docsify/index.html` 后运行本地预览。
- 修改部署脚本后运行 `uv run python -m compileall scripts`。
- 修改文档后运行 `uv run python scripts/check_all.py` 和 `uv run mkdocs build --strict`。
- 不把真实密钥、Cookie、Token 或个人账号写入 Pages 内容。
