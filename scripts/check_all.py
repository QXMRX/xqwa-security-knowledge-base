"""Run all local repository quality checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


CHECKS = (
    ("Markdown structure", "check_markdown.py"),
    ("Documentation metadata", "check_metadata.py"),
    ("Security content", "check_security_content.py"),
)


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent

    for label, script_name in CHECKS:
        print(f"==> {label}", flush=True)
        result = subprocess.run(
            [sys.executable, str(scripts_dir / script_name)],
            check=False,
        )
        if result.returncode != 0:
            print(f"{label} failed.")
            return result.returncode

    print("All repository quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
