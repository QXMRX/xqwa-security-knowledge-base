"""Basic Markdown checks for the knowledge base."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "site",
}

SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "OpenAI API key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(
        r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
}

DANGEROUS_PATTERNS = {
    "destructive root removal": re.compile(r"\brm\s+-rf\s+/(?:\s|$)"),
    "pipe remote script to shell": re.compile(r"\b(?:curl|wget)\b.+\|\s*(?:bash|sh)\b"),
}


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


def iter_markdown_files(root: Path) -> list[Path]:
    """Return Markdown files outside ignored generated or local directories."""
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


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


def check_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [Finding(path, "file is not valid UTF-8")]

    if not text.strip():
        findings.append(Finding(path, "file is empty"))
        return findings

    if not has_top_level_heading(text):
        findings.append(Finding(path, "first meaningful line must be a level-one heading"))

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() != line:
            findings.append(Finding(path, f"line {line_number} has trailing whitespace"))

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            findings.append(Finding(path, f"possible secret detected: {label}"))

    for label, pattern in DANGEROUS_PATTERNS.items():
        if pattern.search(text):
            findings.append(Finding(path, f"high-risk command detected: {label}"))

    return findings


def main() -> int:
    root = Path.cwd()
    markdown_files = iter_markdown_files(root)

    if not markdown_files:
        print("No Markdown files found.")
        return 1

    findings: list[Finding] = []
    for path in markdown_files:
        findings.extend(check_file(path))

    if findings:
        print("Markdown checks failed:")
        for finding in findings:
            print(f"- {finding.path}: {finding.message}")
        return 1

    print(f"Markdown checks passed for {len(markdown_files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
