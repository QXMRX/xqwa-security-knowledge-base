---
title: 第 26 节：网络流量与日志分析
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-31
---

# 第 26 节：网络流量与日志分析

> Misc / Forensics · 95 分钟 · 教学 PCAP

## 实验选择

本节优先使用 [BUUCTF 题单](/courses/ctf-101/buuctf-labs.md) 中对应课次的已核验题目。教师须在课前确认题名、附件和动态实例可用；BUUCTF 归档题不可用时，切换到 DASCTF 同知识点题或本讲义的离线替代。课堂只发布题名与授权范围，不发布 Flag、账号或临时实例地址。

## 本节目标

- 使用过滤条件缩小 PCAP 分析范围。
- 重组一条 TCP/HTTP 会话并恢复关键字段。
- 将流量时间线与应用日志相互印证。

## 先抓住主线

抓包文件像一段拥挤的监控录像：先用时间、地址、协议和会话筛选，再跟踪一条交互。单个数据包往往不能解释完整行为，重组和上下文同样重要。

## 核心概念

| 概念 | 作用 |
|---|---|
| Capture/Display Filter | 控制采集与显示，不能混为一谈 |
| 五元组 | 标识一条网络通信关系 |
| TCP Stream | 将分段数据恢复为会话视图 |
| 时间线 | 把流量、日志和题目事件对齐 |

## 课堂主线

1. 查看教学 PCAP 的协议和端点概览。
2. 根据题目时间范围和协议缩小数据。
3. 跟踪一条 TCP/HTTP 会话，恢复请求与响应。
4. 与给定应用日志对照，指出相互支持或冲突之处。

## 离线替代：用 tshark 缩小 PCAP

优先下载课前核验的 BUUCTF Misc 题附件。平台不可用时，先运行 `uv run python labs/ctf-101/generate_assets.py`，再进入 `labs/ctf-101/generated/traffic/`。所有命令只读分析该目录中的 `training.pcapng`：

```bash
capinfos training.pcapng
tshark -r training.pcapng -q -z io,phs
tshark -r training.pcapng -T fields \
  -e frame.time_relative -e ip.src -e ip.dst -e _ws.col.Protocol | head
tshark -r training.pcapng -Y 'http.request' \
  -T fields -e frame.number -e ip.src -e http.request.method -e http.request.uri
tshark -r training.pcapng -q -z conv,tcp
```

选定教师给出的流编号后，再使用 `tshark -r training.pcapng -q -z follow,tcp,ascii,流编号` 重组会话。过滤器减少显示范围，不会修改原 PCAP。把流量时间转换到日志时区前，先记录两者的时区和时间精度。

分析结束后关闭 Wireshark；使用离线生成包时可运行 `uv run python labs/ctf-101/generate_assets.py --clean` 清理。

## 检查点

过滤结果为空也提供信息：检查字段名称、协议解析和时间范围，而不是立刻扩大到全部流量。

## 可选探索

使用 `tshark` 导出同一筛选结果，比较图形界面与命令行工作流。

## 安全加餐：公共 Wi-Fi 的真实风险

现代 HTTPS 能保护传输内容，但假热点、钓鱼登录页、设备共享设置和证书警告仍值得关注。不要随意忽略浏览器证书错误。

## 课后轻任务

预计 25—35 分钟：提交一张三到五步的流量时间线，每步附上过滤条件或数据来源。

## 常见卡点

- 只看单包：尝试跟踪会话。
- 过滤语法无结果：先用协议概览确认字段存在。
- 把抓到的数据用于真实身份：课程样本全部是虚构数据。

## 延伸资料

- [分方向课程学习资源](/courses/ctf-101/resources.md)

## 课件

[打开第 26 节 Reveal.js 课件](../../../slides/ctf-101/deck.html?lesson=26)
