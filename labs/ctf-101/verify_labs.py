"""Verify CTF 101 source assets and safe execution paths."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path


LAB_ROOT = Path(__file__).resolve().parent
BINARY_ROOT = LAB_ROOT / "binary"
GENERATED = LAB_ROOT / "generated"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=BINARY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def main() -> int:
    required = [
        LAB_ROOT / "samples" / "encoding-samples.txt",
        LAB_ROOT / "samples" / "http-exchange.txt",
        LAB_ROOT / "samples" / "llm-documents.json",
        GENERATED / "evidence" / "sample.bin",
        GENERATED / "traffic" / "training.pcapng",
        GENERATED / "traffic" / "app.log",
        GENERATED / "case-package" / "brief.txt",
    ]
    missing = [path for path in required if not path.is_file()]
    if missing:
        for path in missing:
            print(f"missing generated lab asset: {path.relative_to(LAB_ROOT)}")
        print("Run: uv run python labs/ctf-101/generate_assets.py")
        return 1

    with zipfile.ZipFile(GENERATED / "evidence" / "sample.bin") as archive:
        if "notes/readme.txt" not in archive.namelist():
            raise RuntimeError("forensics sample is missing notes/readme.txt")

    documents = json.loads((LAB_ROOT / "samples" / "llm-documents.json").read_text())
    if {item["owner"] for item in documents} != {"alice", "bob"}:
        raise RuntimeError("LLM sample must contain isolated alice and bob documents")

    run(["make", "clean"])
    run(["make", "all"])
    expected = {
        "hello_binary": (["training"], "accepted"),
        "classify": (["11"], "22"),
        "guard_demo": (["short"], "stored: short"),
    }
    for program, (arguments, output) in expected.items():
        result = run([str(BINARY_ROOT / program), *arguments])
        if output not in result.stdout:
            raise RuntimeError(f"{program} smoke output did not contain {output!r}")

    for program in ("memory_map", "stack_demo", "ret2win_demo", "rop_demo"):
        if not (BINARY_ROOT / program).is_file():
            raise RuntimeError(f"binary was not built: {program}")

    print("CTF 101 lab verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
