"""Generate standalone reveal.js HTML slide decks from course-decks.json data.

Usage:
  node -e "..." > /tmp/course-decks.json   # export JSON from JS
  python3 scripts/generate_slides.py /tmp/course-decks.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ── HTML escape ────────────────────────────────────────────────────────────

def esc(text: str) -> str:
    """Minimal HTML entity escaping for text content."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ── Slide builders ─────────────────────────────────────────────────────────

def slide(eyebrow: str, title: str, body: str) -> str:
    return f"""      <section>
        <p class="eyebrow">{esc(eyebrow)}</p>
        <h2>{esc(title)}</h2>
{body}
      </section>"""


def title_slide(lesson: dict) -> str:
    return f"""      <section>
        <p class="eyebrow">CTF 网络安全实战基础 · {esc(lesson['week'])}</p>
        <h1>{esc(lesson['title'])}</h1>
        <p class="lead">{esc(lesson['hook'])}</p>
        <p class="meta">{esc(lesson['track'])} · 95 分钟 · Signal / Trace</p>
      </section>"""


def goals_slide(lesson: dict) -> str:
    cards = "".join(
        f'<div class="card"><strong>{esc(g[:20])}</strong></div>'
        for g in lesson["goals"]
    )
    return slide(
        "今天能带走什么", "三个目标",
        f'        <div class="grid-three">{cards}</div>\n'
    )


def focus_slide(lesson: dict) -> str:
    return slide(
        "先抓住主线", lesson["focusTitle"],
        f'        <div class="panel">{esc(lesson["focus"])}</div>\n'
    )


def concepts_slide(lesson: dict) -> str:
    cards = "".join(
        f'<div class="card"><strong>{esc(c[0])}</strong>{esc(c[1])}</div>'
        for c in lesson["concepts"]
    )
    return slide(
        "概念地图", "四个关键点",
        f'        <div class="grid-three">{cards}</div>\n'
    )


def activity_slide(lesson: dict) -> str:
    items = "".join(f"<li>{esc(a)}</li>" for a in lesson["activity"])
    return slide(
        "课堂主线", "把猜想变成证据",
        f'        <ul class="step-list">{items}</ul>\n'
    )


def checkpoint_slide(lesson: dict) -> str:
    return slide(
        "检查点", lesson["checkTitle"],
        f'        <p class="lead">{esc(lesson["check"])}</p>\n'
    )


def optional_slide(lesson: dict) -> str:
    return slide(
        "可选探索", "感兴趣再继续",
        f'        <div class="panel"><span class="warm">Optional</span><p>{esc(lesson["optional"])}</p></div>\n'
    )


def snack_slide(lesson: dict) -> str:
    return slide(
        "安全加餐", lesson["snackTitle"],
        f'        <p class="lead">{esc(lesson["snack"])}</p>\n'
    )


def task_slide(lesson: dict) -> str:
    return slide(
        "课后轻任务", lesson["taskTitle"],
        f'        <p>{esc(lesson["task"])}</p>\n        <p class="meta">不要求连续打卡；可以提交卡点记录。</p>\n'
    )


def closing_slide(lesson: dict) -> str:
    return f"""      <section>
        <p class="eyebrow">本节收束</p>
        <h2>{esc(lesson["takeaway"])}</h2>
        <p class="lead">{esc(lesson["next"])}</p>
      </section>"""


# ── Full deck assembly ─────────────────────────────────────────────────────

def build_deck(lesson_id: str, lesson: dict) -> str:
    """Assemble a complete reveal.js HTML document for one lesson."""
    title = lesson["title"]
    filename = f"lesson-{lesson_id}-{slug(title)}.html"

    slides_html = "\n\n".join([
        title_slide(lesson),
        goals_slide(lesson),
        focus_slide(lesson),
        concepts_slide(lesson),
        activity_slide(lesson),
        checkpoint_slide(lesson),
        optional_slide(lesson),
        snack_slide(lesson),
        task_slide(lesson),
        closing_slide(lesson),
    ])

    return filename, f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{esc(title)}｜CTF 网络安全实战基础</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" />
    <link rel="stylesheet" href="assets/css/signal-trace.css?v=20260730c" />
  </head>
  <body>
    <div class="reveal"><div class="slides">
{slides_html}
    </div></div>
    <div class="footer">CTF 101 · Signal / Trace</div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
    <script>Reveal.initialize({{ hash: true, slideNumber: 'c/t', transition: 'fade', transitionSpeed: 'fast' }});</script>
  </body>
</html>"""


def slug(text: str) -> str:
    """Derive a short English-ish filename slug from a Chinese title."""
    mapping = {
        "第 3 节：Python CTF 编程基础": "python",
        "第 4 节：网络基础与信息检索": "network",
        "第 5 节：HTTP、Cookie 与 Session": "http",
        "第 6 节：Web 信息收集与源码阅读": "web-recon",
        "第 7 节：身份认证与访问控制": "authz",
        "第 8 节：SQL 注入基础与安全查询": "sqli",
        "第 9 节：文件、模板与服务端请求": "server-inputs",
        "第 10 节：Web 综合练习": "web-ctf",
        "第 11 节：编码、加密与哈希": "crypto-basics",
        "第 12 节：古典密码与 XOR": "classical-xor",
        "第 13 节：RSA 基础与错误配置": "rsa",
        "第 14 节：哈希、随机数与脚本化分析": "hash-random",
        "第 15 节：程序、编译与二进制": "binary-basics",
        "第 16 节：汇编与函数调用": "assembly",
        "第 17 节：GDB 动态调试": "gdb",
        "第 18 节：Ghidra 静态分析": "ghidra",
        "第 19 节：混淆、校验与 Reverse 综合": "reverse-ctf",
        "第 20 节：C 内存模型与 Pwn 基础": "memory-pwn",
        "第 21 节：栈溢出原理与安全修复": "stack-overflow",
        "第 22 节：ret2win 与基础利用脚本": "ret2win",
        "第 23 节：二进制保护机制": "mitigations",
        "第 24 节：ROP 基础与 Pwn 复盘": "rop",
        "第 25 节：文件格式与隐藏信息": "file-forensics",
        "第 26 节：网络流量与日志分析": "traffic",
        "第 27 节：OSINT 与综合 Misc": "osint-misc",
        "第 28 节：大语言模型应用安全": "llm-security",
        "第 29 节：AI 作为安全工具与攻击面": "ai-ctf",
        "第 30 节：CTF 比赛方法与模拟赛": "ctf-method",
        "第 31 节：学期综合 CTF": "final-ctf",
        "第 32 节：复盘与个人发展规划": "retro",
    }
    return mapping.get(text, f"lesson-{text[:8].replace(' ', '-')}")


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <course-decks.json>", file=sys.stderr)
        return 1

    with open(sys.argv[1], encoding="utf-8") as fh:
        decks = json.load(fh)

    output_dir = Path("docs/slides/ctf-101")
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for lesson_id in sorted(decks, key=int):
        lesson = decks[lesson_id]
        filename, html = build_deck(lesson_id, lesson)
        out_path = output_dir / filename
        out_path.write_text(html, encoding="utf-8")
        generated.append(filename)
        print(f"  {filename}")

    print(f"\nGenerated {len(generated)} slide decks in {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
