---
title: 第 15 节：程序、编译与二进制
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 15 节：程序、编译与二进制

> Reverse · 95 分钟 · 从熟悉的 C 代码出发

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 说出源码、目标文件和可执行文件之间的关系。
- 使用基础工具查看 ELF 类型、字符串、符号和节。
- 从程序输入输出定位可能的校验逻辑。

## 先抓住主线

可执行文件不是一团随机字节。它保存机器指令、数据、装载信息和调试线索。逆向的第一步不是立刻读汇编，而是用成本最低的观察建立程序地图。

## 核心概念

| 概念 | 本节关注点 |
|---|---|
| 编译 | 将源码逐步转换为机器可执行形式 |
| ELF | Linux 常见可执行文件格式 |
| 节与段 | 文件组织与运行时装载的不同视角 |
| 符号与字符串 | 函数名、常量和提示文本等线索 |

## 课堂主线

1. 编译仓库中的 `labs/ctf-101/binary/hello_binary.c` 并运行。
2. 使用 `file`、`strings`、`readelf` 观察文件。
3. 将提示字符串与源码位置对应起来。
4. 对去除部分符号后的版本重复观察，比较线索变化。

## 离线替代：从源码到 ELF 画像

仓库已保存同一源码；下列代码用于课堂逐行讲解：

```c
#include <stdio.h>
#include <string.h>

int check(const char *input) {
    return strcmp(input, "training") == 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        puts("usage: ./hello_binary WORD");
        return 1;
    }
    puts(check(argv[1]) ? "accepted" : "rejected");
    return 0;
}
```

编译并观察：

```bash
cd labs/ctf-101/binary
cc -Wall -Wextra -g -O0 hello_binary.c -o hello_binary
./hello_binary training
file hello_binary
strings -n 5 hello_binary | grep -E 'accepted|rejected|training'
readelf -h hello_binary
readelf -s hello_binary | grep -E ' main$| check$'
```

先写出格式、架构、入口行为、关键字符串和符号五项画像，再进入反汇编。只分析 BUUCTF 题目附件、自己编译或仓库提供的文件。

预期 `file` 报告 ELF 可执行文件，`strings` 找到三条教学字符串，`readelf -s` 找到 `main` 与 `check`。实验后运行 `make -C labs/ctf-101/binary clean` 清理构建产物。

## 检查点

能在不读汇编的情况下说出程序格式、架构、可能输入和关键字符串，就是有效的第一轮分析。

## 可选探索

比较调试构建与发布构建在符号和文件大小上的差异。

## 安全加餐：软件为何能跨机器分发

二进制格式、操作系统接口和处理器架构共同规定了程序如何被装载。一个文件“是可执行程序”不代表它适合当前系统运行。

## 课后轻任务

预计 20—30 分钟：为一个本地程序写五行“初步画像”，包括格式、架构、入口线索、字符串和下一步。

## 常见卡点

- 一看到二进制就打开反编译器：先做低成本观察。
- 把节和段完全等同：本节先理解各自服务文件与装载视角。
- 运行来源未知程序：只分析 BUUCTF 题目附件、自己编译或仓库提供的文件。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 15 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=15)
