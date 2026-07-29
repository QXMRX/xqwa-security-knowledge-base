"""Shared helpers for repository quality checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "site",
}


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


def repo_root() -> Path:
    """Return the repository root based on this script directory."""
    return Path(__file__).resolve().parents[1]


def is_ignored(path: Path) -> bool:
    """Return whether a path is inside an ignored local or generated directory."""
    return any(part in IGNORED_DIRS for part in path.parts)


def iter_files(root: Path, suffixes: set[str]) -> list[Path]:
    """Return files with selected suffixes outside ignored directories."""
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or is_ignored(path):
            continue
        if path.suffix in suffixes:
            files.append(path)
    return sorted(files)


def iter_markdown_files(root: Path) -> list[Path]:
    """Return Markdown files outside ignored directories."""
    return iter_files(root, {".md"})


def read_utf8(path: Path) -> tuple[Optional[str], Optional[Finding]]:
    """Read a UTF-8 file, returning either text or a finding."""
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        return None, Finding(path, "file is not valid UTF-8")


def relative_path(path: Path, root: Path) -> str:
    """Render a stable repository-relative path for output."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def print_findings(title: str, findings: list[Finding], root: Path) -> None:
    """Print check findings in a consistent format."""
    print(f"{title} failed:")
    for finding in findings:
        print(f"- {relative_path(finding.path, root)}: {finding.message}")
