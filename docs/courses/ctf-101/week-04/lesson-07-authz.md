---
title: 第 7 节：身份认证与访问控制
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 7 节：身份认证与访问控制

> Web · 95 分钟 · 本地多用户靶场

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 区分认证、授权和会话管理。
- 识别对象级权限检查缺失的现象。
- 为一个接口写出最小权限判断规则。

## 先抓住主线

认证回答“你是谁”，授权回答“你能做什么”。前端隐藏按钮只改变界面，不构成权限控制；服务端必须对每个受保护对象重新判断访问者是否有权操作。

## 核心概念

| 概念 | 关键问题 |
|---|---|
| 认证 | 当前请求属于哪个身份 |
| 授权 | 该身份能否执行当前动作 |
| 水平越权 | 访问了同级其他用户的数据 |
| 垂直越权 | 普通身份获得更高权限功能 |

## 课堂主线

1. 启动 `labs/ctf-101/web/training_app.py`，使用 Alice 与 Bob 两个虚构身份。
2. 比较各自可访问的资源标识符。
3. 在授权范围内验证服务端是否检查资源所有者。
4. 用伪代码补上服务端权限检查，并讨论错误响应。

## 实操代码：把授权写成明确规则

终端 A 运行 `uv run python labs/ctf-101/web/training_app.py`。终端 B 验证 Alice 只能读取自己的文档：

```bash
curl -sS -c /tmp/alice-cookie.txt 'http://127.0.0.1:8081/login?user=alice'
curl -sS -b /tmp/alice-cookie.txt 'http://127.0.0.1:8081/document?id=doc-a'
curl -i -b /tmp/alice-cookie.txt 'http://127.0.0.1:8081/document?id=doc-b'
```

第三条应返回 `403 Forbidden`。停止本地服务后删除教学 Cookie 文件。

下面的纯 Python 示例不启动网络服务，只验证对象级授权：

```python
DOCUMENTS = {
    "doc-a": {"owner": "alice", "content": "Alice 的教学记录"},
    "doc-b": {"owner": "bob", "content": "Bob 的教学记录"},
}


def read_document(user: dict, document_id: str) -> str:
    document = DOCUMENTS.get(document_id)
    if document is None:
        raise LookupError("资源不存在")
    if user["role"] != "admin" and document["owner"] != user["name"]:
        raise PermissionError("无权访问该资源")
    return document["content"]


alice = {"name": "alice", "role": "member"}
for document_id in ("doc-a", "doc-b"):
    try:
        print(document_id, read_document(alice, document_id))
    except (LookupError, PermissionError) as error:
        print(document_id, type(error).__name__, error)
```

运行后，Alice 应只能读取 `doc-a`。分别修改用户角色、对象所有者和不存在的 ID，验证每个分支。关键检查必须位于服务端敏感操作之前，不能只依赖前端是否显示按钮。

## 检查点

你应能解释为什么“页面上看不到入口”不能证明接口安全。

## 可选探索

为管理员、普通用户和访客画一张最小权限矩阵。

## 安全加餐：双因素认证解决什么

双因素认证能降低密码泄露后的风险，但不能修复服务端越权，也不能替代钓鱼识别和会话保护。

## 课后轻任务

预计 20 分钟：为“查看个人资料”和“修改他人资料”各写一条服务端授权规则。

## 常见卡点

- 把登录成功当作拥有全部权限。
- 只检查用户角色，不检查资源归属。
- 使用真实账号实验：课堂统一使用虚构测试账户。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 7 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=07)
