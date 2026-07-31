---
title: 第 13 节：RSA 基础与错误配置
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 13 节：RSA 基础与错误配置

> Crypto · 95 分钟 · 数学直觉与脚本

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 理解 RSA 中模运算、公钥和私钥的关系。
- 读懂 `n`、`e`、`c` 等常见题目变量。
- 在给定弱参数的教学题中完成恢复过程。

## 先抓住主线

RSA 的安全不来自公式难懂，而来自正确参数下某些计算问题足够困难。CTF 入门题通常故意破坏一个前提，例如素数太小、参数复用或明文范围过窄。

## 核心概念

| 符号 | 含义 |
|---|---|
| `p, q` | 构造模数的素数 |
| `n` | 公共模数，通常为 `p × q` |
| `e` | 公钥指数 |
| `d` | 私钥指数 |
| `m, c` | 明文整数与密文整数 |

## 课堂主线

1. 用小整数演示模运算和幂运算。
2. 将短字节串转换为整数再还原。
3. 分析一个参数明显偏弱的教学 RSA 题。
4. 用 Python 验证恢复结果，并说明弱点位于哪里。

## 实操代码：小整数 RSA 模型

以下参数刻意很小，只用于理解公式，完全不具备安全性：

```python
p, q = 61, 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17
d = pow(e, -1, phi)

message = 65
ciphertext = pow(message, e, n)
recovered = pow(ciphertext, d, n)

print({"n": n, "phi": phi, "e": e, "d": d})
print("明文、密文、恢复：", message, ciphertext, recovered)
assert recovered == message

raw = b"OK"
number = int.from_bytes(raw, "big")
assert number.to_bytes(len(raw), "big") == raw
```

逐项说明 `p、q、n、e、d` 是公开还是应保密，以及 `message < n` 为什么是这个简化模型的前提。真实 RSA 必须使用成熟库、足够密钥长度和 OAEP 等安全填充，不能照搬此教学代码。

示例没有生成或保存真实密钥，退出解释器即完成清理。

## 检查点

你不需要手算大整数，但应知道脚本中的每个变量来自题目哪条信息。

## 可选探索

比较“破解 RSA”与“利用错误参数”的区别。

## 安全加餐：HTTPS 不只做加密

HTTPS 同时涉及服务器身份验证、协商和数据完整性。浏览器显示安全连接，不代表网站内容本身可信，也不代表业务逻辑没有漏洞。

## 课后轻任务

预计 25—35 分钟：为课堂脚本添加变量注释和一次结果校验；数学推导可选做。

## 常见卡点

- 把所有 RSA 题都理解为分解大整数：先找被破坏的前提。
- 字节与整数转换方向错误：用短样本先往返验证。
- 只调用工具：保留参数、假设和校验依据。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 13 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=13)
