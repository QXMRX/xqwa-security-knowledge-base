"""Check that CTF 101 handouts and slide decks stay associated."""

from __future__ import annotations

import re
import sys

from common import Finding, print_findings, read_utf8, repo_root


PATH_PATTERN = re.compile(r'"(week-\d{2}/lesson-(\d{2})-[^"]+\.md)"')
DECK_PATTERN = re.compile(r'^\s*"(\d{2})":\s*\{', re.MULTILINE)


def main() -> int:
    root = repo_root()
    course_root = root / "docs" / "courses" / "ctf-101"
    slides_root = root / "docs" / "slides" / "ctf-101"
    links_file = slides_root / "assets" / "js" / "course-links.js"
    decks_file = slides_root / "assets" / "js" / "course-decks.js"
    findings: list[Finding] = []

    links_text, links_error = read_utf8(links_file)
    decks_text, decks_error = read_utf8(decks_file)
    if links_error:
        findings.append(links_error)
    if decks_error:
        findings.append(decks_error)
    if findings:
        print_findings("CTF 101 course sync", findings, root)
        return 1

    assert links_text is not None
    assert decks_text is not None
    paths = PATH_PATTERN.findall(links_text)
    expected_ids = [f"{number:02d}" for number in range(1, 33)]
    listed_ids = [lesson_id for _, lesson_id in paths]
    if listed_ids != expected_ids:
        findings.append(
            Finding(links_file, "lesson manifest must list lesson IDs 01 through 32 in order")
        )

    actual_docs = {
        path.relative_to(course_root).as_posix()
        for path in course_root.glob("week-*/lesson-*.md")
    }
    listed_docs = {path for path, _ in paths}
    for path in sorted(listed_docs - actual_docs):
        findings.append(Finding(links_file, f"listed handout does not exist: {path}"))
    for path in sorted(actual_docs - listed_docs):
        findings.append(Finding(course_root / path, "handout is missing from course-links.js"))

    deck_ids = set(DECK_PATTERN.findall(decks_text))
    for lesson_id in expected_ids[2:]:
        if lesson_id not in deck_ids:
            findings.append(Finding(decks_file, f"missing slide data for lesson {lesson_id}"))

    standalone = {
        "01": slides_root / "lesson-01-ctf.html",
        "02": slides_root / "lesson-02-linux.html",
    }
    for lesson_id, slide in standalone.items():
        if not slide.is_file():
            findings.append(Finding(slide, f"missing standalone slides for lesson {lesson_id}"))

    if findings:
        print_findings("CTF 101 course sync", findings, root)
        return 1

    print("CTF 101 sync checks passed for 32 handouts and slide decks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
