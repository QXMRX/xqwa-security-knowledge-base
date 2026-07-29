"""Check Markdown structure and formatting."""

from __future__ import annotations

import sys

from common import Finding, iter_markdown_files, print_findings, read_utf8, repo_root


DOCSIFY_CONTROL_FILES = {"_sidebar.md", "_navbar.md", "_coverpage.md"}


def strip_front_matter(text: str) -> str:
    """Remove simple YAML front matter before checking the first heading."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :])
    return text


def has_top_level_heading(text: str) -> bool:
    """Require the first meaningful Markdown line to be a level-one heading."""
    body = strip_front_matter(text)
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        return stripped.startswith("# ")
    return False


def check_file(path) -> list[Finding]:
    findings: list[Finding] = []
    if path.name in DOCSIFY_CONTROL_FILES:
        return findings

    text, read_error = read_utf8(path)
    if read_error:
        return [read_error]

    assert text is not None
    if not text.strip():
        findings.append(Finding(path, "file is empty"))
        return findings

    if not has_top_level_heading(text):
        findings.append(Finding(path, "first meaningful line must be a level-one heading"))

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() != line:
            findings.append(Finding(path, f"line {line_number} has trailing whitespace"))

    return findings


def main() -> int:
    root = repo_root()
    markdown_files = iter_markdown_files(root)

    if not markdown_files:
        print("No Markdown files found.")
        return 1

    findings: list[Finding] = []
    for path in markdown_files:
        findings.extend(check_file(path))

    if findings:
        print_findings("Markdown checks", findings, root)
        return 1

    print(f"Markdown checks passed for {len(markdown_files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
