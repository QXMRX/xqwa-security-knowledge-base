---
title: CTF 课程学习指南
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-30
---

# CTF 课程学习指南

## 开课前一次性准备

### 1. 平台账号

使用个人账号登录 [BUUCTF](https://buuoj.cn/)。平台当前处于归档模式，能否启动具体题目以教师课前核验为准；不共享账号，不把 Cookie 或动态实例地址发到群聊和仓库。

### 2. 获取仓库与 Python 环境

```bash
git clone https://github.com/QXMRX/xqwa-security-knowledge-base.git
cd xqwa-security-knowledge-base
uv sync
uv run python scripts/check_all.py
```

Reverse/Pwn 课程需要 pwntools 时再安装实验可选依赖：

```bash
uv sync --extra labs
```

### 3. 准备离线兜底材料

```bash
uv run python labs/ctf-101/generate_assets.py
make -C labs/ctf-101/binary
uv run python labs/ctf-101/verify_labs.py
```

最后一条输出 `CTF 101 lab verification passed.` 才表示仓库内的样本与安全冒烟路径可用。构建工具缺失时，把完整报错发给助教，不要从未知网盘下载二进制。

### 4. 按模块准备工具

| 课次 | 必需 | 可选增强 |
|---|---|---|
| 1—14 | Python 3.11+、浏览器、`curl` | SQLite 命令行 |
| 15—24 | C 编译器、Binutils、GDB | Ghidra、pwntools、checksec、ROPgadget |
| 25—27 | `file`、`xxd`、解压工具 | ExifTool、Wireshark/tshark、Binwalk |
| 28—32 | Python、Markdown 编辑器 | 经教师批准的 AI 工具 |

教师应优先提供已装好工具的虚拟机或容器镜像。学生不需要在第一周安装整套安全发行版。

## 先说结论：不需要把社团变成另一门主科

CTF 的知识面很广，第一次接触时觉得陌生是正常的。本课程不要求你同时擅长所有方向；稳定参与、完成课堂主线、保留自己的问题记录，比短期大量刷题更重要。

## 三种学习任务

| 类型 | 含义 | 建议做法 |
|---|---|---|
| 课堂主线 | 本节最小闭环 | 跟着完成即可，遇到问题先记录 |
| 课后轻任务 | 巩固本节技能 | 选择一个空闲时段完成，通常 20—40 分钟 |
| 可选探索 | 面向兴趣的加深 | 不要求完成，可与同学讨论或留到假期 |

如果某周课业较重，优先完成课堂主线，再在学习记录中写下准备补做的内容。不要为了赶进度直接复制答案。

## 建议的解题记录

每道题只需记录四件事：

1. 我看到了什么线索？
2. 我尝试了什么，结果如何？
3. 最后如何验证结论？
4. 下次遇到类似题，我会先做什么？

这比只保存 Flag 更有助于复盘。即使没有完成题目，也可以提交前两项。

## 工具与 AI 的使用

允许查阅官方文档、公开 Writeup 和工具手册；允许把 AI 当作解释概念、整理思路或检查脚本的助手。任何工具输出都需要自己验证，且不得上传真实密钥、Cookie、个人信息、未公开代码或课程靶场以外的目标信息。

## 需要帮助时

卡住 15—20 分钟后，建议按顺序尝试：重读题目、确认输入输出、查看工具报错、缩小问题、记录猜想、再向同学或助教描述你已经试过的内容。好的提问不是“这题怎么做”，而是“我观察到 X，尝试 Y 后得到 Z，接下来应该验证什么”。
