"""Run all local repository quality checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


CHECKS = (
    ("Markdown structure", ["check_markdown.py"]),
    ("Documentation metadata", ["check_metadata.py"]),
    ("Security content", ["check_security_content.py"]),
    ("CTF 101 handout/slide sync", ["check_course_sync.py"]),
    ("CTF 101 independent-teaching content", ["check_course_content.py"]),
    ("Docsify Pages assembly", ["build_pages_site.py", "--output", "/tmp/xqwa-pages-check"]),
)


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent

    for label, command in CHECKS:
        print(f"==> {label}", flush=True)
        script_name, *args = command
        result = subprocess.run(
            [sys.executable, str(scripts_dir / script_name), *args],
            check=False,
        )
        if result.returncode != 0:
            print(f"{label} failed.")
            return result.returncode

    print("All repository quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
