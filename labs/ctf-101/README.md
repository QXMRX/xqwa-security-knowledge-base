# CTF 101 本地实验包

本目录为 32 节课程提供不依赖公网平台的最低可行实验材料。讲义中的命令默认从仓库根目录执行。

## 环境与边界

- 基础课程：Python 3.11+、`curl`、常见 GNU/Linux 命令。
- 二进制课程：C 编译器、Binutils；GDB、Ghidra、pwntools、checksec 按对应课次选装。
- 取证课程：`file`、`xxd`；Wireshark/tshark、ExifTool、Binwalk 按对应课次选装。
- 所有网络服务只绑定 `127.0.0.1`，不得改为公网地址。
- `binary/ret2win_demo.c` 与 `binary/rop_demo.c` 是故意脆弱的教学程序，只能在本地编译和分析。

## 一次性准备

生成离线 PCAP、文件取证样本和虚构 OSINT 事件包：

```bash
uv run python labs/ctf-101/generate_assets.py
```

生成结果位于 `labs/ctf-101/generated/`。脚本可重复运行，会覆盖它自己管理的教学文件，不读取个人目录。

编译二进制实验：

```bash
make -C labs/ctf-101/binary
```

只运行安全冒烟测试，不自动触发故意脆弱输入：

```bash
uv run python labs/ctf-101/verify_labs.py
```

## 课程映射

| 课次 | 材料 |
|---|---|
| 1—3 | `samples/encoding-samples.txt` |
| 4—10 | `samples/http-exchange.txt`、`web/training_app.py` |
| 15—19 | `binary/hello_binary.c`、`binary/classify.c` |
| 20—24 | `binary/memory_map.c`、`stack_demo.c`、`ret2win_demo.c`、`guard_demo.c`、`rop_demo.c` |
| 25 | `generated/evidence/sample.bin` |
| 26 | `generated/traffic/training.pcapng`、`generated/traffic/app.log` |
| 27 | `generated/case-package/` |
| 28—29 | `samples/llm-documents.json` |
| 30—32 | 讲义中的记录与复盘模板 |

## 清理

```bash
make -C labs/ctf-101/binary clean
uv run python labs/ctf-101/generate_assets.py --clean
```

清理命令仅删除实验包内明确列出的构建产物和 `generated/` 目录。
