---
title: CTF 网络安全实战基础
audience: 计算机系大一新生
status: review
owner: QXMRX
review_cycle: yearly
updated_at: 2026-07-30
---

# CTF 网络安全实战基础

欢迎来到社团的 CTF 入门课程。这里不要求你立刻成为高手；课程先带你学会看见线索、提出猜想、验证结果，并在授权环境中把问题讲清楚。

## 这门课适合谁

- 学过或正在学习 C 语言基础，希望知道它在真实程序中如何运行。
- 对网页、密码学、逆向、二进制、AI 安全或 CTF 感兴趣，但还没有系统路径。
- 愿意尝试命令行和脚本，也允许自己在题目面前卡一会儿。

不要求有竞赛经历，也不要求提前装好一整套安全工具。

## 学完后你能做到什么

你将能够在本地靶场或明确授权的平台中完成入门级题目，使用 Linux 和 Python 辅助分析，并写出包含过程、证据和结论的简短 Writeup。课程覆盖 Web、Crypto、Reverse、Pwn、Misc 与 AI Security；第一学期更看重广泛建立直觉，再选择一个方向继续深入。

## 学习方式

每节课由主线实验和可选探索组成。主线尽量在课堂内完成；课后任务通常不超过 40 分钟，可补交，也可以提交卡点记录。比赛是展示成长的机会，不是一场高压考试。

开始前，请阅读：

- [课程学习指南](/courses/ctf-101/learning-guide.md)
- [视觉与内容标准](/courses/ctf-101/art-direction.md)
- [题目与平台规划](/courses/ctf-101/platform-plan.md)
- [BUUCTF 优先实验题单](/courses/ctf-101/buuctf-labs.md)
- [远程授课指南](/courses/ctf-101/remote-teaching.md)
- [教师授课手册](/courses/ctf-101/instructor-guide.md)
- [分方向学习资源](/courses/ctf-101/resources.md)
- [第 1 节：什么是 CTF](/courses/ctf-101/week-01/lesson-01-ctf.md)
- [第 2 节：Linux 与终端基础](/courses/ctf-101/week-01/lesson-02-linux.md)

全部 32 节讲义和对应 Reveal.js 课件已经按周组织，可从网站侧边栏或[可搜索的幻灯片索引](/courses/ctf-101/slides.md)进入。课程允许按方向跳读，但第一次参加时建议先完成第 1—4 节通用基础。

在 Docsify 中打开任意一节讲义，页面顶部可直接切换到该节幻灯片；幻灯片右上角也能返回详细讲义。两者分工明确：讲义保存完整解释、步骤和资源，幻灯片只保留课堂主线、提问与演示提示。

## 学习地图

```text
基础工具 → Web / Crypto → Reverse / Pwn → Misc / AI Security → 模拟 CTF 与复盘
```

每一段都围绕同一条路径：观察线索、提出假设、收集证据、编写辅助脚本、解释结果与安全边界。

## 安全边界

本课程的实验仅限本地 Docker、虚拟机、社团靶场和明确授权的 CTF 平台。请不要将课堂工具、脚本或思路用于公网目标、真实账号或第三方服务。
