"""Check that every CTF 101 lesson is independently teachable."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

from common import Finding, print_findings, read_utf8, repo_root


REQUIRED_HEADINGS = {
    "## 实验选择",
    "## 本节目标",
    "## 检查点",
    "## 课后轻任务",
    "## 常见卡点",
    "## 延伸资料",
}
EXPECTED_LANGUAGE = re.compile(r"预期|应看到|应返回|应能|结果")
CLEANUP_LANGUAGE = re.compile(r"清理|停止|关闭|删除|无需清理|结束")
AMBIGUOUS_ASSETS = re.compile(r"教师提供的|课程提供的")
FENCE_PATTERN = re.compile(r"^```", re.MULTILINE)

REQUIRED_LAB_SOURCES = (
    "labs/ctf-101/README.md",
    "labs/ctf-101/generate_assets.py",
    "labs/ctf-101/verify_labs.py",
    "labs/ctf-101/samples/encoding-samples.txt",
    "labs/ctf-101/samples/http-exchange.txt",
    "labs/ctf-101/samples/llm-documents.json",
    "labs/ctf-101/web/training_app.py",
    "labs/ctf-101/binary/Makefile",
    "labs/ctf-101/binary/hello_binary.c",
    "labs/ctf-101/binary/classify.c",
    "labs/ctf-101/binary/memory_map.c",
    "labs/ctf-101/binary/stack_demo.c",
    "labs/ctf-101/binary/ret2win_demo.c",
    "labs/ctf-101/binary/guard_demo.c",
    "labs/ctf-101/binary/rop_demo.c",
)


def check_lesson(path: Path) -> list[Finding]:
    text, error = read_utf8(path)
    if error:
        return [error]
    assert text is not None
    findings: list[Finding] = []

    headings = {line.strip() for line in text.splitlines() if line.startswith("## ")}
    for heading in sorted(REQUIRED_HEADINGS - headings):
        findings.append(Finding(path, f"missing independent-teaching section: {heading}"))

    if not any(
        heading.startswith("## 课堂主线") or heading == "## 课堂流程"
        for heading in headings
    ):
        findings.append(Finding(path, "lesson needs a classroom mainline or classroom flow"))

    fences = len(FENCE_PATTERN.findall(text))
    if fences < 2 or fences % 2:
        findings.append(Finding(path, "lesson needs at least one closed code/command block"))

    if len(text) < 1400:
        findings.append(Finding(path, "lesson is too short for the independent-teaching baseline"))
    if "BUUCTF 题单" not in text:
        findings.append(Finding(path, "lesson must link the BUUCTF-first selection plan"))
    if "离线" not in text:
        findings.append(Finding(path, "lesson must identify an offline fallback"))
    if not EXPECTED_LANGUAGE.search(text):
        findings.append(Finding(path, "lesson must state an expected observation or result"))
    if not CLEANUP_LANGUAGE.search(text):
        findings.append(Finding(path, "lesson must state cleanup or shutdown behavior"))
    if AMBIGUOUS_ASSETS.search(text):
        findings.append(
            Finding(path, "replace ambiguous teacher/course-provided assets with exact paths")
        )

    return findings


def check_python_syntax(path: Path) -> list[Finding]:
    text, error = read_utf8(path)
    if error:
        return [error]
    assert text is not None
    try:
        ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return [Finding(path, f"Python syntax error: {exc.msg} at line {exc.lineno}")]
    return []


def main() -> int:
    root = repo_root()
    lessons = sorted((root / "docs" / "courses" / "ctf-101").glob("week-*/lesson-*.md"))
    findings: list[Finding] = []

    if len(lessons) != 32:
        findings.append(
            Finding(root / "docs" / "courses" / "ctf-101", f"expected 32 lessons, found {len(lessons)}")
        )
    for lesson in lessons:
        findings.extend(check_lesson(lesson))

    for relative in REQUIRED_LAB_SOURCES:
        path = root / relative
        if not path.is_file():
            findings.append(Finding(path, "required offline lab source is missing"))

    for path in sorted((root / "labs" / "ctf-101").rglob("*.py")):
        findings.extend(check_python_syntax(path))

    if findings:
        print_findings("CTF 101 independent-teaching checks", findings, root)
        return 1

    print("CTF 101 independent-teaching checks passed for 32 lessons and the offline lab kit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
