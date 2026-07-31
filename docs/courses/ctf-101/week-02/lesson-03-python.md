---
title: 第 3 节：Python CTF 编程基础
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 3 节：Python CTF 编程基础

> 通用基础 · 95 分钟 · 课堂主线可独立完成

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 区分文本 `str` 与字节 `bytes`。
- 用循环、函数和文件读写减少重复操作。
- 完成一个小型编码转换脚本。

## 先抓住主线

Python 在 CTF 中更像一把随手可改的实验工具：先把一次转换跑通，再把重复步骤装进循环和函数。重点不是背语法，而是让每一步输入、输出都可见。

## 核心概念

| 概念 | 需要理解的事情 |
|---|---|
| `str` | 人阅读的 Unicode 文本 |
| `bytes` | 文件、网络和加密算法直接处理的字节序列 |
| 编解码 | `encode()` 将文本变为字节，`decode()` 反向转换 |
| 异常 | 输入不符合预期时，脚本应给出可理解的错误 |

## 课堂主线

1. 读取仓库中的 `labs/ctf-101/samples/encoding-samples.txt`。
2. 判断输入是十六进制、Base64 还是普通文本。
3. 分别转换并显示中间结果。
4. 把重复逻辑整理成函数，为无法识别的输入保留错误提示。

## 实操代码：可观察的转换器

从仓库根目录执行 `sed -n '1,20p' labs/ctf-101/samples/encoding-samples.txt` 查看输入。然后将下面内容保存为 `decode_sample.py`：

```python
import base64
import binascii


def decode_value(value: str, encoding: str) -> bytes:
    cleaned = value.strip()
    if encoding == "hex":
        return bytes.fromhex(cleaned)
    if encoding == "base64":
        return base64.b64decode(cleaned, validate=True)
    raise ValueError(f"不支持的编码：{encoding}")


samples = [
    ("666c61677b6865787d", "hex"),
    ("ZmxhZ3tiYXNlNjR9", "base64"),
]
for raw, encoding in samples:
    try:
        result = decode_value(raw, encoding)
        print(encoding, type(result), result, result.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, binascii.Error) as error:
        print(f"{encoding} 转换失败：{error}")
```

运行 `python3 decode_sample.py`，确认函数返回的是 `bytes`。随后删掉 Base64 输入最后一个字符，观察错误是否被清晰报告。可选的文件输入方式是 `Path("samples.txt").read_text(encoding="utf-8").splitlines()`。

实验结束后保留去敏后的脚本作为作业，删除包含临时输入的文件即可；本节不会启动后台服务。

## 检查点

你应能解释为什么网络响应常以字节出现，以及为什么“能运行”还不等于“结果可信”。

## 可选探索

加入文件批量读取或正则表达式 Flag 检测。它是扩展项，不要求本周完成。

## 安全加餐：自动化的边界

脚本可以节省重复劳动，也会放大错误。先在一条样本上验证，再批量运行；不要把课堂脚本指向未授权服务或真实账号。

## 课后轻任务

预计 20—30 分钟：给课堂脚本补一段帮助信息，或提交一份“输入—转换—输出”记录。两项任选其一。

## 常见卡点

- 出现乱码：确认字节使用了什么字符编码。
- 类型报错：打印 `type()`，先看参与运算的是文本还是字节。
- 脚本越来越长：先抽出一个只完成一件事的函数。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 3 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=03)
