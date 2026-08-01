---
title: 第 14 节：哈希、随机数与脚本化分析
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 14 节：哈希、随机数与脚本化分析

> Crypto · 95 分钟 · 从安全性质出发

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 理解抗碰撞、原像困难和完整性校验的基本含义。
- 区分普通伪随机与密码学安全随机数。
- 分析一个可预测随机或弱口令哈希教学题。

## 先抓住主线

哈希不是“不可逆加密”，随机也不是“看起来没有规律”。安全分析要问具体性质：攻击者能否预测下一个值、能否低成本枚举输入、摘要是否带有随机盐和上下文。

## 核心概念

| 概念 | 本节关注点 |
|---|---|
| 原像困难 | 已知摘要时难以找到对应输入 |
| 碰撞 | 两个不同输入产生相同摘要 |
| 盐 | 让相同密码不再产生相同存储结果 |
| CSPRNG | 面向安全用途、难以预测的随机生成器 |

## 课堂主线

1. 比较相同输入、微小变化输入的摘要。
2. 观察无盐弱口令列表为何容易被批量匹配。
3. 分析一个固定种子或时间种子的教学随机序列。
4. 写脚本验证预测，并给出更安全的设计方向。

## 实操代码：摘要、盐与随机源

```python
import hashlib
import random
import secrets

for value in (b"lesson", b"Lesson"):
    print(value, hashlib.sha256(value).hexdigest())

password = b"training-password"
salt_a = b"user-a"
salt_b = b"user-b"
print(hashlib.pbkdf2_hmac("sha256", password, salt_a, 100_000).hex())
print(hashlib.pbkdf2_hmac("sha256", password, salt_b, 100_000).hex())

predictable_a = random.Random(2026)
predictable_b = random.Random(2026)
assert predictable_a.randrange(1_000_000) == predictable_b.randrange(1_000_000)
print("安全用途示例：", secrets.token_hex(16))
```

相同种子产生相同伪随机序列，适合可复现实验，不适合生成会话密钥。`secrets` 面向安全用途，但令牌仍需足够长度、服务端保护、过期和撤销机制。密码存储应优先采用 Argon2、scrypt 等专用方案；PBKDF2 此处只用于展示盐的作用。

输出中的随机教学令牌没有连接任何账号，关闭终端即可，不要将其误作真实凭据。

## 检查点

“随机种子未知”不自动等于安全；还要考虑种子空间、可观察输出和生成器用途。

## 可选探索

用本地文件校验演示完整性检测，并记录它不能证明来源可信。

## 安全加餐：下载文件为什么要校验

摘要可以检测文件是否变化；若摘要也来自被篡改的位置，它不能单独证明发布者身份。更完整的方案还需要可信渠道或数字签名。

## 课后轻任务

预计 20—30 分钟：写一段“哈希适合做什么、不适合做什么”的说明，或补全随机数实验记录。

## 常见卡点

- 把碰撞与还原原文混为一谈。
- 使用普通随机模块生成密码或 Token。
- 只比较最终值：记录种子、输入格式和生成步骤。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 14 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=14)
