---
title: Pages 部署
audience: 维护者和仓库管理员
status: review
owner: QXMRX
review_cycle: quarterly
updated_at: 2026-07-29
---

# Pages 部署

本仓库使用 Docsify 作为 GitHub Pages 的线上阅读界面。Docsify 直接在浏览器中渲染 Markdown，适合当前以文档为主、构建步骤较轻的资料库。

MkDocs 仍保留为本地和 CI 中的严格构建检查，用来发现导航、Markdown 扩展和结构问题。Pages 部署则由 Docsify 提供更轻量的静态界面。

## 目录

相关文件：

- `docs/`：正式 Markdown 内容源。
- `docsify/index.html`：Docsify 页面入口。
- `docsify/_sidebar.md`：Docsify 侧边栏。
- `docsify/.nojekyll`：避免 GitHub Pages 忽略下划线开头文件。
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
4. 上传 `_site/` 为 Pages artifact。
5. 部署到 `github-pages` 环境。

## 本地预览

本地预览 Docsify Pages 界面：

```bash
python scripts/build_pages_site.py --output /tmp/xqwa-pages-preview
python3 -m http.server 3000 --directory /tmp/xqwa-pages-preview
```

启动后访问 `http://127.0.0.1:3000`。

## 安全设计

Pages 部署采用保守设计：

- 只在 `main` push 或维护者手动触发时部署。
- 不使用 `pull_request_target`。
- 不读取 AI API Key 或其他 repository secret；只使用 GitHub 自动注入的 token 完成 Pages 发布。
- 只部署 `docs/` 和 `docsify/` 组装后的静态文件。
- 不部署本地 `.venv/`、`site/`、Git 历史或工作区临时文件。

## 维护要求

维护时遵守：

- 修改 `docsify/index.html` 后运行本地预览。
- 修改部署脚本后运行 `python -m compileall scripts`。
- 修改文档后运行 `python scripts/check_all.py` 和 `mkdocs build --strict`。
- 不把真实密钥、Cookie、Token 或个人账号写入 Pages 内容。
