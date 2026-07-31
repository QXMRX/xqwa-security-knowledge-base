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


def copy_public_labs(root: Path, destination: Path) -> None:
    """Publish reproducible lab sources without generated or compiled outputs."""
    source = root / "labs" / "ctf-101"
    target = destination / "labs" / "ctf-101"
    if not source.is_dir():
        raise RuntimeError(f"required lab source directory does not exist: {source}")

    compiled_programs = {
        "hello_binary",
        "classify",
        "memory_map",
        "stack_demo",
        "ret2win_demo",
        "guard_demo",
        "rop_demo",
    }

    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored = {"__pycache__"} & set(names)
        current = Path(directory)
        if current == source and "generated" in names:
            ignored.add("generated")
        if current == source / "binary":
            ignored.update(compiled_programs & set(names))
        return ignored

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=ignore)

    required = {
        target / "README.md",
        target / "generate_assets.py",
        target / "web" / "training_app.py",
        target / "binary" / "ret2win_demo.c",
    }
    missing = sorted(str(path.relative_to(destination)) for path in required if not path.is_file())
    if missing:
        raise RuntimeError(f"public lab source is incomplete: {', '.join(missing)}")

    forbidden = [target / "generated", target / "__pycache__"]
    forbidden.extend(target / "binary" / name for name in compiled_programs)
    leaked = sorted(str(path.relative_to(destination)) for path in forbidden if path.exists())
    if leaked:
        raise RuntimeError(f"refusing to publish generated or compiled lab files: {', '.join(leaked)}")


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
    copy_public_labs(root, output)

    print(f"Docsify Pages site written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
