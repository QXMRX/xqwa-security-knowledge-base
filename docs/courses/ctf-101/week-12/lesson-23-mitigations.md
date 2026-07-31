---
title: 第 23 节：二进制保护机制
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 23 节：二进制保护机制

> Pwn · 95 分钟 · 比较实验

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 解释 NX、Canary、PIE、ASLR、RELRO 的基本作用。
- 使用 `checksec` 读取本地程序保护状态。
- 将保护机制与它试图提高成本的攻击步骤对应起来。

## 先抓住主线

防护机制不是“有就绝对安全”的开关，而是让某类内存错误更难转化为稳定控制。它们相互配合：有的限制执行，有的检测破坏，有的随机化位置，有的保护链接数据。

## 核心概念

| 机制 | 主要作用 |
|---|---|
| NX | 限制数据页直接执行 |
| Canary | 检测函数返回前的栈破坏 |
| PIE/ASLR | 随机化代码与内存位置 |
| RELRO | 加强动态链接相关区域保护 |

## 课堂主线

1. 对多组教师编译的本地程序运行 `checksec`。
2. 比较同一漏洞在不同保护组合下的表现。
3. 将上一节 ret2win 的前提逐项写出来。
4. 讨论源代码修复为什么仍然是第一目标。

## 离线替代：比较构建保护

BUUCTF 主线用于观察题目附件的保护配置；离线对照使用 `labs/ctf-101/binary/guard_demo.c`。从仓库根目录执行 `cd labs/ctf-101/binary`，再构建两组程序：

```bash
cc -Wall -Wextra -O0 -g guard_demo.c -o guard-default
cc -Wall -Wextra -O2 -D_FORTIFY_SOURCE=2 -fstack-protector-strong \
  -fPIE -pie -Wl,-z,relro,-z,now guard_demo.c -o guard-hardened
checksec --file=guard-default
checksec --file=guard-hardened
readelf -W -l guard-hardened | grep GNU_STACK
readelf -h guard-hardened | grep Type
```

若系统没有 `checksec`，仍可用 `readelf` 和 `hardening-check`（若已安装）收集部分证据。填写对照表：

| 保护 | 观察命令 | 阻碍的步骤 | 不能解决的问题 |
|---|---|---|---|
| NX | `readelf -W -l` | 数据页直接执行 | 越界写本身 |
| PIE/ASLR | `readelf -h` | 固定地址假设 | 信息泄露与逻辑漏洞 |
| Canary | `checksec` | 未检测的栈破坏 | 所有内存错误 |
| RELRO | `checksec` | 部分链接数据改写 | 源代码缺陷 |

预期加固版本显示 PIE、NX、Canary/栈保护与完整 RELRO 中更多保护项。结束后删除本节生成的 `guard-default` 与 `guard-hardened`，不要删除源码。

## 检查点

看到“Canary 开启”只能说明存在一层检测，不能证明程序没有内存漏洞。

## 可选探索

查阅编译器文档，记录一个保护选项在构建链中的配置位置。

## 安全加餐：纵深防御

安全依靠多层机制共同降低风险：安全代码、编译保护、操作系统隔离、监控和更新都各自承担一部分责任。

## 课后轻任务

预计 20—30 分钟：制作“机制—阻碍步骤—不能解决的问题”对照表。

## 常见卡点

- 把 ASLR 与 PIE 混为一谈：一个是系统随机化能力，一个让主程序可被重定位。
- 看到保护少就判断一定可利用：仍需具体漏洞和控制证据。
- 只关闭保护做实验：也要保留安全构建对照。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 23 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=23)
