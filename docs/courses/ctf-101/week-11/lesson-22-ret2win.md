---
title: 第 22 节：ret2win 与基础利用脚本
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 22 节：ret2win 与基础利用脚本

> Pwn · 95 分钟 · 本地 CTF 教学程序

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 理解覆盖返回地址如何改变控制流。
- 找到本地 `win` 函数并计算教学程序中的偏移。
- 使用 pwntools 编写可复现的本地交互脚本。

## 先抓住主线

ret2win 是教学模型：程序故意保留一个正常流程不会调用的目标函数，并关闭部分现代防护，让学生观察“输入—内存覆盖—返回地址—目标函数”的完整证据链。它不代表真实系统通常如此简单。

## 核心概念

| 概念 | 本节作用 |
|---|---|
| 返回地址 | 函数结束后继续执行的位置 |
| 偏移 | 缓冲区起点到目标控制数据的距离 |
| 字节序 | 多字节地址在内存中的排列方式 |
| pwntools | 组织本地进程交互和字节数据 |

## 课堂主线

1. 检查课程程序架构与防护配置。
2. 使用模式输入确定偏移，并用调试器验证。
3. 定位 `win` 函数地址，构造本地输入。
4. 将过程写成脚本，重复运行确认稳定性。

## 离线替代脚本：记录偏移与符号来源

优先分析课前核验的 BUUCTF `jarvisoj_level0` 候选题。以下离线脚本只对运行 `make -C labs/ctf-101/binary ret2win_demo` 生成的故意脆弱本地程序使用，并在该二进制目录中执行：

```python
from pwn import ELF, context, cyclic, cyclic_find, process

context.binary = binary = ELF("./ret2win_demo", checksec=False)
print(binary.checksec())
print("win symbol:", hex(binary.symbols["win"]))

# 第一阶段只生成可识别模式，崩溃位置必须由本地调试器读取。
pattern = cyclic(128)
target = process(binary.path)
target.sendline(pattern)
target.wait()
print("process status:", target.poll())

# 将调试器观察到的 4 字节模式填入，而不是猜偏移。
# offset = cyclic_find(b"...")
```

调试时使用 `gdb -q ./ret2win_demo`、`run`、`info registers` 和 `x/24gx $sp` 记录证据。完成偏移确认后，课堂脚本只能通过 `process(binary.path)` 启动本地文件，不添加主机名、IP 或远程连接。每段字节都要注释来源。

## 检查点

脚本中的每段字节都应能解释来源：填充长度、目标地址和交互步骤。

## 可选探索

为脚本增加清晰日志和失败提示，不增加远程目标功能。

## 安全加餐：漏洞利用脚本也是软件

可复现、可读、能处理失败的脚本更有学习价值。课程脚本固定为本地进程，不加入公网地址或未授权目标。

## 课后轻任务

预计 25—40 分钟：补全脚本注释，或画出控制流变化图，二选一。

## 常见卡点

- 偏移靠猜：用模式和调试证据确认。
- 地址打包错误：检查架构位数与字节序。
- 一次成功就结束：至少重复验证，并记录环境。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 22 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=22)
