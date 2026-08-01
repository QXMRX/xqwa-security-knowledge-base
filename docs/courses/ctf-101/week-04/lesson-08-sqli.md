---
title: 第 8 节：SQL 注入基础与安全查询
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 8 节：SQL 注入基础与安全查询

> Web · 95 分钟 · 仅使用本地教学数据库

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 理解字符串拼接如何改变 SQL 语句结构。
- 在本地最小示例中观察输入与查询的边界。
- 使用参数化查询修复问题。

## 先抓住主线

SQL 注入的核心不是某个特殊字符串，而是应用把“不可信数据”当成了“查询结构”的一部分。参数化查询让数据库分别接收语句模板和数据，从根本上保留边界。

## 核心概念

| 概念 | 本节关注点 |
|---|---|
| 拼接查询 | 数据可能改变语句结构 |
| 参数化查询 | 查询结构与参数分别传递 |
| 错误回显 | 可能泄露数据库信息，也影响判断 |
| 最小权限 | 即使查询出错，也限制数据库账号能力 |

## 课堂主线

1. 阅读一个本地登录查询的构造过程。
2. 比较普通输入和边界输入生成的 SQL 结构。
3. 在教师靶场观察错误处理差异。
4. 改写为参数化查询并重新验证原有功能。

## 离线替代：比较拼接与参数化查询

下面的 SQLite 示例仅使用内存数据库。先观察字符串拼接如何把数据混入查询文本，再使用参数占位符：

```python
import sqlite3

database = sqlite3.connect(":memory:")
database.execute("CREATE TABLE users (name TEXT, role TEXT)")
database.executemany(
    "INSERT INTO users VALUES (?, ?)",
    [("alice", "member"), ("teacher", "admin")],
)


def unsafe_lookup(name: str):
    query = f"SELECT name, role FROM users WHERE name = '{name}'"
    print("不安全查询文本：", query)
    return database.execute(query).fetchall()


def safe_lookup(name: str):
    query = "SELECT name, role FROM users WHERE name = ?"
    print("参数化模板：", query, "参数：", (name,))
    return database.execute(query, (name,)).fetchall()


print(unsafe_lookup("alice"))
print(safe_lookup("alice"))
```

本节重点是阅读两种数据流，不提供针对外部系统的测试字符串。继续测试空字符串、中文用户名和不存在的用户，确认安全版本仍保持正常业务行为。参数化查询保护结构边界；输入长度限制、最小权限和稳定错误信息仍需分别实现。

数据库只存在于当前 Python 进程内，程序退出后自动清理，不会创建本地数据库文件。

## 检查点

修复后不仅要“拦住异常输入”，还要确认正常登录、错误提示和日志行为没有被破坏。

## 可选探索

比较输入过滤与参数化查询的可靠性，写下过滤规则容易遗漏的原因。

## 安全加餐：泄露往往从一条错误信息开始

详细报错方便开发，也可能向外部暴露表名、路径和技术栈。生产环境应对用户提供稳定错误，对维护者保留受保护的诊断日志。

## 课后轻任务

预计 25—35 分钟：提交一份“存在问题的查询—修复后的查询—验证结果”对照记录。

## 常见卡点

- 只背输入样例：回到“数据是否改变了语句结构”。
- 修复后功能失效：检查参数数量和类型。
- 使用公网网站验证：本节所有测试仅限课程数据库。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 8 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=08)
