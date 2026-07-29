"""Assemble the Docsify site deployed to GitHub Pages."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from common import repo_root


def copy_contents(source: Path, destination: Path) -> None:
    """Copy all direct children from source into destination."""
    if not source.is_dir():
        raise RuntimeError(f"required source directory does not exist: {source}")

    for item in source.iterdir():
        target = destination / item.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("_site"),
        help="Directory to write the assembled Pages site into.",
    )
    return parser.parse_args()


def main() -> int:
    """Build the static Docsify Pages directory."""
    root = repo_root()
    output = parse_args().output
    output = output if output.is_absolute() else root / output

    forbidden_outputs = {root.resolve(), (root / "docs").resolve(), (root / "docsify").resolve()}
    if output.resolve() in forbidden_outputs:
        raise RuntimeError("refusing to overwrite the repository root or source directories")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    copy_contents(root / "docs", output)
    copy_contents(root / "docsify", output)

    print(f"Docsify Pages site written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
