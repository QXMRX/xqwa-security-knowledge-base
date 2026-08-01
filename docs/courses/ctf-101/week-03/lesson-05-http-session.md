---
title: 第 5 节：HTTP、Cookie 与 Session
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 5 节：HTTP、Cookie 与 Session

> Web · 95 分钟 · 浏览器开发者工具

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 阅读 HTTP 请求行、头部和消息体。
- 区分 Cookie、Session 与 Token 的角色。
- 在本地应用中重放并比较一次请求。

## 先抓住主线

HTTP 本身不记得上一次请求。应用为了保持登录状态，会让客户端携带一个可关联状态的凭据。可以把 Cookie 理解为浏览器代为携带的小纸条，但真正的权限判断仍必须发生在服务端。

## 核心概念

| 概念 | 作用与边界 |
|---|---|
| Header | 描述请求环境、内容类型和客户端状态 |
| Cookie | 浏览器按规则保存并随请求携带的数据 |
| Session | 服务端保存的会话状态，通常由标识符关联 |
| Token | 可携带身份或授权信息，仍需验证完整性和有效期 |

## 课堂主线

1. 在本地应用登录，打开浏览器网络面板。
2. 找到登录请求和后续页面请求。
3. 比较登录前后的 Cookie 或授权字段。
4. 退出登录后重放旧请求，观察服务端如何处理。

## 离线替代：读取请求与 Cookie

先使用仓库提供的本地应用完成可复现实验：

```bash
uv run python labs/ctf-101/web/training_app.py
```

另开终端保存教学 Cookie 并访问个人资料：

```bash
curl -i -c /tmp/ctf101-cookie.txt 'http://127.0.0.1:8081/login?user=alice'
curl -i -b /tmp/ctf101-cookie.txt http://127.0.0.1:8081/profile
```

下面的精简版本用于课堂解释请求头。保存为 `local_http.py`；它只在本机回显请求，不实现真实登录：

```python
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        cookie = self.headers.get("Cookie", "(none)")
        body = f"path={self.path}\ncookie={cookie}\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Set-Cookie", "training_session=demo; HttpOnly; SameSite=Lax")
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("127.0.0.1", 8081), Handler).serve_forever()
```

启动后，在另一个终端比较：

```bash
python3 local_http.py
curl -i http://127.0.0.1:8081/profile
curl -i -H 'Cookie: training_session=demo' http://127.0.0.1:8081/profile
```

标出 `Cookie` 请求头和 `Set-Cookie` 响应头。示例 Cookie 只是教学文本，不能证明用户已登录；真实应用仍须在服务端检查会话和权限。按 `Ctrl+C` 停止服务，并删除 `/tmp/ctf101-cookie.txt`。

## 检查点

你应能指出“浏览器保存了什么”和“服务端依据什么做权限判断”不是同一个问题。

## 可选探索

观察 `HttpOnly`、`Secure`、`SameSite` 属性，并记录它们各自降低哪类风险。

## 安全加餐：隐身模式不是匿名模式

隐身窗口主要减少本机留下的历史与站点数据；网站、网络服务提供方和组织网络仍可能看到相应访问。它解决的是本机痕迹管理，不是完整匿名。

## 课后轻任务

预计 20—30 分钟：截取一份不含真实凭据的本地 HTTP 请求，标注方法、路径、状态字段和会话字段。

## 常见卡点

- 找不到请求：关闭过滤条件并刷新页面。
- 把 Cookie 等同于密码：Cookie 只是容器，内容和安全属性取决于应用设计。
- 重放结果不同：检查会话是否过期、请求中是否有一次性字段。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 5 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=05)
