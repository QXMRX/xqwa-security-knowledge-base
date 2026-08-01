---
title: 第 12 节：古典密码与 XOR
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 12 节：古典密码与 XOR

> Crypto · 95 分钟 · 模式与脚本

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 识别 Caesar、Vigenère 和重复密钥 XOR 的基本模式。
- 利用已知格式、频率或密钥长度缩小搜索空间。
- 编写可解释的 XOR 辅助脚本。

## 先抓住主线

古典密码和弱 XOR 题的突破口常来自“重复模式”和“已知结构”。CTF 的 Flag 格式、自然语言分布和密钥复用都会提供约束；分析是在利用约束，不是凭感觉猜答案。

## 核心概念

| 方法 | 可观察线索 |
|---|---|
| Caesar | 字母整体平移，搜索空间很小 |
| Vigenère | 多组平移按周期重复 |
| XOR | 相同位异或两次恢复原值 |
| 已知明文 | 已知格式可帮助恢复局部密钥流 |

## 课堂主线

1. 手工完成一个短 Caesar 示例，理解平移模型。
2. 用脚本枚举有限候选并保留可读输出。
3. 对重复密钥 XOR 观察周期和已知前缀。
4. 为脚本增加结果评分或人工筛选说明。

## 实操代码：枚举 Caesar 与验证 XOR

```python
import string


def caesar(text: str, shift: int) -> str:
    alphabet = string.ascii_lowercase
    result = []
    for char in text.lower():
        result.append(alphabet[(alphabet.index(char) - shift) % 26] if char in alphabet else char)
    return "".join(result)


for shift in range(26):
    candidate = caesar("iodj{fdhvdu}", shift)
    if "flag{" in candidate or "ctf" in candidate:
        print(shift, candidate)


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(value ^ key[index % len(key)] for index, value in enumerate(data))


plain = b"flag{xor_is_reversible}"
key = b"KEY"
cipher = xor_bytes(plain, key)
print(cipher.hex())
assert xor_bytes(cipher, key) == plain
```

枚举只是生成候选，仍要解释为何候选符合语言、格式和上下文。XOR 示例使用明确给出的教学密钥；不要把短重复密钥当作真实加密方案。

本节脚本只在内存中处理教学文本，无需额外清理。

## 检查点

脚本输出一百个候选不算分析完成；还需要说明为什么某个候选更符合题目约束。

## 可选探索

尝试基于可打印字符比例给候选结果排序。

## 安全加餐：恩尼格玛与“机制公开”

现代密码学不依赖算法保密，而依赖密钥和经过公开检验的机制。历史故事用于理解设计思想，不把战争传奇替代数学原理。

## 课后轻任务

预计 20—30 分钟：从 Caesar 或 XOR 中任选一题，提交约束、候选和选择依据。

## 常见卡点

- 只看最终明文：保留密钥、输入格式和筛选过程。
- 混淆字符串与整数 XOR：先明确数据如何转为字节。
- 暴力枚举无边界：先使用题目结构缩小空间。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 12 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=12)
