---
title: 第 25 节：文件格式与隐藏信息
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 25 节：文件格式与隐藏信息

> Misc / Forensics · 95 分钟 · 离线文件

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 从文件头、元数据和结构判断真实类型。
- 区分附加数据、嵌入文件、元数据与隐写线索。
- 建立先无损观察、后提取副本的取证习惯。

## 先抓住主线

文件名是标签，文件结构才是证据。分析时保留原文件和校验值，在副本上操作；先确认格式和结构，再选择针对性工具，避免“把所有工具都跑一遍”。

## 核心概念

| 概念 | 关注点 |
|---|---|
| Magic bytes | 文件格式常见的开头标识 |
| 元数据 | 创建工具、时间、设备等上下文 |
| 容器格式 | 一个文件中可能组织多种数据 |
| 隐写 | 让信息不易被注意，不等同于加密 |

## 课堂主线

1. 记录样本文件大小与摘要，复制分析副本。
2. 使用 `file`、`exiftool` 等查看类型和元数据。
3. 观察文件尾、容器结构和嵌入对象线索。
4. 提取目标并再次识别，记录完整证据链。

## 离线替代：保留原件并分析副本

优先下载课前核验的 BUUCTF Misc 题附件。平台不可用时，运行 `uv run python labs/ctf-101/generate_assets.py`，然后进入 `labs/ctf-101/generated/`。下列命令从该目录执行，先建立工作副本：

```bash
mkdir -p work
sha256sum evidence/sample.bin | tee work/original.sha256
cp --preserve=timestamps evidence/sample.bin work/sample-copy.bin
file work/sample-copy.bin
stat work/sample-copy.bin
exiftool work/sample-copy.bin
xxd -l 64 work/sample-copy.bin
tail -c 64 work/sample-copy.bin | xxd
```

如果 `file` 判断为 ZIP、PNG 或其他容器，再选对应工具：

```bash
unzip -l work/sample-copy.bin
binwalk work/sample-copy.bin
```

不要一开始就批量提取或改写原件。每次操作记录“命令、输入文件摘要、输出路径、观察”。若工具缺失，保存错误信息并使用 `file`、`xxd` 等基础工具完成最低分析。

预期 `file` 将离线 `sample.bin` 识别为 ZIP 容器，`unzip -l` 列出两个教学文件。结束后运行生成器的 `--clean` 选项清理仓库内生成资产，个人分析记录另行保留。

## 检查点

每次提取都应说明依据：哪个结构、偏移或元数据让你决定继续。

## 可选探索

比较删除图片元数据前后的文件差异，不使用真实私人照片。

## 安全加餐：照片可能暴露什么

时间、设备、位置和拍摄参数可能存在于元数据中。上传前可检查并按场景移除，但不要假设所有平台都会自动清理。

## 课后轻任务

预计 20—30 分钟：提交一份文件分析时间线，最多六步，包含工具、观察和下一步理由。

## 常见卡点

- 直接修改原文件：始终保留原始样本。
- 扩展名与结构冲突：优先相信结构证据。
- 工具输出很多：围绕题目目标筛选相关项。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 25 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=25)
