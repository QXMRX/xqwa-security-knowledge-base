---
title: 第 27 节：OSINT 与综合 Misc
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 27 节：OSINT 与综合 Misc

> Misc / OSINT · 95 分钟 · 使用虚构教学材料

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 区分公开来源、推断和已验证事实。
- 从图片、文档和时间信息建立线索表。
- 处理一题需要组合两种以上工具的 Misc 题。

## 先抓住主线

OSINT 不是“搜索某个人”。本课程使用虚构材料，训练来源评估、交叉验证和时间线构建。一个线索只有能被独立来源支持，才适合提升置信度。

## 核心概念

| 概念 | 要求 |
|---|---|
| 来源 | 记录页面、文件或题面出处 |
| 时间 | 区分发布时间、事件时间和修改时间 |
| 置信度 | 已验证、合理推断、待验证 |
| 最小披露 | 只记录解题所需信息，不扩散个人数据 |

## 课堂主线

1. 阅读虚构事件包，列出图片、文档和文本线索。
2. 为每条线索记录来源和时间含义。
3. 用第二种来源或文件证据交叉验证。
4. 将脚本、元数据或编码分析接入最终解题流程。

## 离线替代：核对文件时间与摘要

优先使用课前核验的 BUUCTF Misc 入门题。平台不可用时，运行 `uv run python labs/ctf-101/generate_assets.py` 并进入 `labs/ctf-101/generated/`，使用仓库生成的虚构事件包；不搜索现实人物、住址或账号：

```bash
find case-package -maxdepth 2 -type f -print0 | sort -z | xargs -0 sha256sum
find case-package -maxdepth 2 -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS %p\n' | sort
exiftool -time:all -gps:all case-package/*
```

用 Python 将明确带时区的时间统一为 UTC：

```python
from datetime import datetime, timezone

values = ["2026-07-01T09:30:00+08:00", "2026-07-01T01:35:00+00:00"]
for value in values:
    parsed = datetime.fromisoformat(value)
    print(value, "=>", parsed.astimezone(timezone.utc).isoformat())
```

文件修改时间、EXIF 时间和事件发生时间含义不同。最终结论至少引用两项相互独立的证据，并注明哪些时间可能被软件重写。

离线包的预期结论是两条带不同时区的记录相差 5 分钟。结束后可使用生成器的 `--clean` 选项清理虚构事件包。

## 检查点

“很多网站都转载”可能仍来自同一个原始来源；独立性需要追溯，而不是只数链接。

## 可选探索

为信息源建立“直接证据、间接证据、未知来源”分类。

## 安全加餐：如何判断一张网图是否可信

检查原始来源、时间、裁剪痕迹、上下文和反向检索结果；单一工具或 AI 判断都不能替代交叉验证。

## 课后轻任务

预计 20—30 分钟：整理五条以内的线索表，允许保留一条尚未解决的矛盾。

## 常见卡点

- 把搜索结果摘要当原始来源。
- 追踪真实个人：课程只使用虚构数据和授权题目。
- 结论过早：明确标记推断和证据强度。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 27 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=27)
