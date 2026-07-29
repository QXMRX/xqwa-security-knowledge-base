"""Check required metadata for published documentation pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

from common import Finding, print_findings, read_utf8, repo_root
from check_markdown import strip_front_matter


REQUIRED_DOC_FIELDS = {
    "title",
    "audience",
    "status",
    "owner",
    "review_cycle",
    "updated_at",
}

VALID_STATUS = {"draft", "review", "stable", "deprecated"}
VALID_REVIEW_CYCLES = {"monthly", "quarterly", "yearly", "as-needed"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def iter_published_docs(root: Path) -> list[Path]:
    """Return MkDocs source pages that should carry review metadata."""
    return sorted(path for path in (root / "docs").rglob("*.md") if path.is_file())


def parse_front_matter(text: str, path: Path) -> tuple[dict[str, str], list[Finding]]:
    """Parse simple one-line YAML front matter fields."""
    findings: list[Finding] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [Finding(path, "missing YAML front matter")]

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, [Finding(path, "front matter is not closed")]

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end_index], start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            findings.append(Finding(path, f"front matter line {line_number} must use key: value"))
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if not key or not value:
            findings.append(Finding(path, f"front matter line {line_number} has empty key or value"))
            continue
        metadata[key] = value

    return metadata, findings


def first_heading(text: str) -> Optional[str]:
    """Return the first level-one heading after front matter."""
    for line in strip_front_matter(text).splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


def check_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text, read_error = read_utf8(path)
    if read_error:
        return [read_error]

    assert text is not None
    metadata, parse_findings = parse_front_matter(text, path)
    findings.extend(parse_findings)

    missing_fields = sorted(REQUIRED_DOC_FIELDS - metadata.keys())
    for field in missing_fields:
        findings.append(Finding(path, f"missing required metadata field: {field}"))

    status = metadata.get("status")
    if status and status not in VALID_STATUS:
        findings.append(
            Finding(path, f"status must be one of: {', '.join(sorted(VALID_STATUS))}")
        )

    review_cycle = metadata.get("review_cycle")
    if review_cycle and review_cycle not in VALID_REVIEW_CYCLES:
        findings.append(
            Finding(
                path,
                f"review_cycle must be one of: {', '.join(sorted(VALID_REVIEW_CYCLES))}",
            )
        )

    updated_at = metadata.get("updated_at")
    if updated_at and not DATE_PATTERN.match(updated_at):
        findings.append(Finding(path, "updated_at must use YYYY-MM-DD"))

    title = metadata.get("title")
    heading = first_heading(text)
    if title and heading and title != heading:
        findings.append(Finding(path, "metadata title must match the first level-one heading"))

    return findings


def main() -> int:
    root = repo_root()
    docs = iter_published_docs(root)

    if not docs:
        print("No published docs found.")
        return 1

    findings: list[Finding] = []
    for path in docs:
        findings.extend(check_file(path))

    if findings:
        print_findings("Metadata checks", findings, root)
        return 1

    print(f"Metadata checks passed for {len(docs)} docs pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
