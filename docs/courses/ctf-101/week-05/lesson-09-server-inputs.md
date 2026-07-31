---
title: 第 9 节：文件、模板与服务端请求
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 9 节：文件、模板与服务端请求

> Web · 95 分钟 · 风险地图课

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 识别上传文件、模板变量和服务端取址三类输入边界。
- 用数据流描述输入如何到达危险操作。
- 给出至少一种设计层面的防护方法。

## 先抓住主线

文件上传、模板注入和 SSRF 看起来是三类题，背后都在问同一件事：不可信输入最终被哪个高能力组件解释了？输入只是“数据”，还是被当作路径、模板或网络地址执行？

## 核心概念

| 场景 | 需要守住的边界 |
|---|---|
| 文件上传 | 类型、内容、存储位置和执行权限 |
| 路径处理 | 用户输入不能任意决定服务端文件位置 |
| 模板渲染 | 数据不应被重新解释为模板表达式 |
| 服务端请求 | 目标地址、协议和响应处理需要限制 |

## 课堂主线

1. 阅读三个经过简化的本地代码片段。
2. 标出输入源、转换步骤和最终敏感操作。
3. 对每个场景提出一个可验证的风险假设。
4. 补充白名单、隔离存储或目标限制等防护。

## 实操代码：收紧文件与地址边界

先从防御角度实现两个小函数：

```python
import ipaddress
from pathlib import Path
from urllib.parse import urlparse

UPLOAD_ROOT = Path("/tmp/ctf101-uploads").resolve()
ALLOWED_SUFFIXES = {".txt", ".png"}


def safe_upload_path(original_name: str) -> Path:
    clean_name = Path(original_name).name
    destination = (UPLOAD_ROOT / clean_name).resolve()
    if destination.parent != UPLOAD_ROOT:
        raise ValueError("文件必须保存在上传目录")
    if destination.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError("不允许的文件类型")
    return destination


def validate_training_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("只允许明确配置的 HTTPS 目标")
    address = ipaddress.ip_address(parsed.hostname)
    if address.is_private or address.is_loopback or address.is_link_local:
        raise ValueError("不允许访问内部或本机地址")
    return value
```

用虚构文件名测试 `safe_upload_path()`，记录哪些输入被拒绝以及原因。URL 校验只是教学片段：生产实现还要处理 DNS 解析变化、重定向、域名白名单、响应大小和超时，不能只检查字符串前缀。

预期结果是普通 `.txt` 名称被映射到 `/tmp/ctf101-uploads`，不允许的后缀和内部地址被明确拒绝。示例函数本身不写文件、不发网络请求，因此退出解释器即完成清理。

## 检查点

能够画出数据流，比记住零散漏洞名更重要：输入从哪里来、经过什么、最后影响了什么。

## 可选探索

将三类风险整理为一张“输入—解释器—影响—防护”对照表。

## 安全加餐：文件扩展名不是身份证

扩展名只是命名的一部分，不能独立证明文件真实类型或安全性。文件处理还需要内容检测、隔离存储和最小权限。

## 课后轻任务

预计 20—30 分钟：从三种场景中任选一种，提交数据流图和一条防护建议。

## 常见卡点

- 同时研究太多漏洞：先追踪一条输入路径。
- 只写“过滤输入”：说明允许什么、在哪里验证、失败如何处理。
- 测试真实服务：本节只使用静态代码和本地靶场。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 9 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=09)
