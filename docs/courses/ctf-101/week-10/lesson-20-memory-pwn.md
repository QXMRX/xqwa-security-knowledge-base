---
title: 第 20 节：C 内存模型与 Pwn 基础
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 20 节：C 内存模型与 Pwn 基础

> Pwn · 95 分钟 · 从 C 指针回到运行时内存

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 区分代码、全局数据、堆与栈的常见职责。
- 解释数组边界和指针错误为何可能改变相邻状态。
- 使用调试器观察本地程序的内存布局。

## 先抓住主线

C 允许程序直接表达地址和内存操作，这带来性能与控制力，也把边界责任交给开发者。内存区域不是绝对固定的“格子图”，但分区模型能帮助我们理解对象生命周期和常见错误。

## 核心概念

| 区域 | 常见内容与生命周期 |
|---|---|
| 代码/只读数据 | 指令、常量，通常限制写入 |
| 全局数据 | 与程序生命周期相近的对象 |
| 堆 | 运行时动态申请与释放的数据 |
| 栈 | 函数调用相关的临时状态 |

## 课堂主线

1. 阅读一个含数组、指针和局部变量的短程序。
2. 预测各对象可能位于哪里、活多久。
3. 在本地调试器中查看地址和相邻数据。
4. 修改为带边界检查的版本并比较行为。

## 离线替代：观察对象地址与生命周期

```c
#include <stdio.h>
#include <stdlib.h>

int global_value = 7;

int main(void) {
    int local_value = 11;
    int *heap_value = malloc(sizeof(*heap_value));
    if (heap_value == NULL) return 1;
    *heap_value = 13;

    printf("global=%p local=%p heap=%p\n",
           (void *)&global_value, (void *)&local_value, (void *)heap_value);
    free(heap_value);
    heap_value = NULL;
    return 0;
}
```

```bash
cc -Wall -Wextra -g -O0 memory_map.c -o memory_map
./memory_map
./memory_map
```

比较两次地址，讨论 ASLR 可能造成的变化。`free()` 后将指针置空只减少误用机会，不会让其他悬空引用自动安全。用 `valgrind ./memory_map`（若已安装）或编译器地址检测器检查明显内存错误。

实验后运行 `make -C labs/ctf-101/binary clean` 清理构建产物。

## 检查点

“越界会崩溃”只是可能结果；更准确的说法是越界造成未定义行为，影响取决于布局、输入和防护。

## 可选探索

使用地址检测工具观察同一错误的诊断信息。

## 安全加餐：内存安全语言解决了什么

更强的类型和运行时检查能消除大量内存错误，但不会自动修复业务逻辑、权限或密码学设计问题。

## 课后轻任务

预计 20—30 分钟：为一个 C 函数画对象生命周期图，或补全安全改写，二选一。

## 常见卡点

- 把示意图当成所有系统的精确地址布局。
- 只观察崩溃，不追踪写入影响了什么。
- 在重要文件或真实服务上实验：本模块只使用课程程序。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 20 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=20)
