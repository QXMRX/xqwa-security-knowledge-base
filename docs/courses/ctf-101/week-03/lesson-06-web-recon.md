---
title: 第 6 节：Web 信息收集与源码阅读
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 6 节：Web 信息收集与源码阅读

> Web · 95 分钟 · 仅限课程站点

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 从页面源码、脚本和错误信息中整理线索。
- 区分“公开可见”与“获得测试授权”。
- 为本地 Web 题建立一张入口与数据流清单。

## 先抓住主线

信息收集不是无目标地扫描。好的起点是回答三个问题：应用暴露了哪些入口、数据从哪里进入、服务端返回了哪些异常信息。

## 核心概念

| 线索来源 | 可能回答的问题 |
|---|---|
| HTML 注释 | 开发者留下了什么上下文 |
| JavaScript | 前端调用了哪些接口、使用哪些参数 |
| `robots.txt` | 站点希望爬虫避开的路径，不代表访问授权 |
| 错误响应 | 技术栈、字段名称或处理阶段 |

## 课堂主线

1. 浏览课程站点并记录正常功能入口。
2. 阅读 HTML 和 JavaScript，整理接口与参数。
3. 对一个本地错误页面区分事实、推测和待验证项。
4. 画出“用户输入—请求—服务端—响应”的简图。

## 离线替代：从源码建立入口清单

创建一个只含虚构接口的静态页面：

```bash
mkdir -p /tmp/ctf101-recon
printf '<!-- training build -->\n<script src="app.js"></script>\n' > /tmp/ctf101-recon/index.html
printf 'fetch("/api/profile?id=demo").then(r => r.json())\n' > /tmp/ctf101-recon/app.js
printf 'User-agent: *\nDisallow: /training-notes/\n' > /tmp/ctf101-recon/robots.txt
python3 -m http.server 8082 --bind 127.0.0.1 --directory /tmp/ctf101-recon
```

在另一终端收集证据：

```bash
curl -s http://127.0.0.1:8082/
curl -s http://127.0.0.1:8082/app.js
curl -s http://127.0.0.1:8082/robots.txt
```

整理成“来源、原文、可以确认的事实、仍待验证的推测”四列。`robots.txt` 中出现路径不代表你获得访问任何真实站点的授权。结束时按 `Ctrl+C` 停止服务。

预期证据至少包括 HTML 注释、JavaScript 中的虚构接口和 `robots.txt` 路径三项；不能仅写“发现隐藏页面”。

## 检查点

每条发现都应附带来源，例如“脚本第 X 行调用了 `/api/profile`”，而不是只写“这里可能有接口”。

## 可选探索

尝试为线索标注置信度：已验证、合理推测、尚无证据。

## 安全加餐：公开信息不等于可以利用

网页能访问、域名能搜索到，都不等于获得了安全测试授权。课程只在本地应用和明确授权平台演示信息收集。

## 课后轻任务

预计 20 分钟：整理课堂站点的入口清单，最多五项；每项写明证据来源。

## 常见卡点

- 一上来就跑大量工具：先人工理解正常功能。
- 把错误文本全部当事实：错误可能经过包装，也可能故意误导。
- 线索太多：围绕题目目标筛选能被验证的信息。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 6 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=06)
