"""Check repository text files for high-risk security teaching content."""

from __future__ import annotations

import ipaddress
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from common import Finding, iter_files, print_findings, read_utf8, repo_root


TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt"}

SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "OpenAI API key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "private key": re.compile(
        r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
}

DANGEROUS_PATTERNS = {
    "destructive root removal": re.compile(r"\brm\s+-rf\s+/(?:\s|$)"),
    "chmod root recursively": re.compile(r"\bchmod\s+-R\s+777\s+/(?:\s|$)"),
    "format disk command": re.compile(r"\bmkfs(?:\.[A-Za-z0-9]+)?\s+/dev/"),
    "disk overwrite command": re.compile(r"\bdd\b.+\bof=/dev/(?:sd|vd|hd|disk)"),
    "pipe remote script to shell": re.compile(r"\b(?:curl|wget)\b.+\|\s*(?:bash|sh)\b"),
}

ATTACK_TOOLS = {"nmap", "masscan", "sqlmap", "hydra", "nikto", "ffuf", "dirsearch", "wpscan"}
URL_PATTERN = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")
IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN_PATTERN = re.compile(r"\b(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b")

ALLOWED_EXAMPLE_HOSTS = {
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "example.com",
    "example.org",
    "example.net",
}


def is_public_ip(value: str) -> bool:
    """Return whether a string is a public IP address."""
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    return address.is_global


def is_allowed_host(hostname: str) -> bool:
    """Return whether a host is acceptable in teaching examples."""
    hostname = hostname.lower().strip(".")
    if hostname in ALLOWED_EXAMPLE_HOSTS:
        return True
    if hostname.endswith(".localhost"):
        return True
    if hostname.endswith(".test") or hostname.endswith(".invalid"):
        return True
    if hostname.endswith(".example"):
        return True
    return False


def public_targets_in_line(line: str) -> list[str]:
    """Return public targets referenced by an attack-tool command line."""
    targets: list[str] = []

    for match in URL_PATTERN.findall(line):
        hostname = urlparse(match).hostname
        if not hostname:
            continue
        if is_public_ip(hostname) or not is_allowed_host(hostname):
            targets.append(hostname)

    for match in IPV4_PATTERN.findall(line):
        if is_public_ip(match):
            targets.append(match)

    for match in DOMAIN_PATTERN.findall(line):
        if not is_allowed_host(match):
            targets.append(match)

    return sorted(set(targets))


def looks_like_attack_tool_command(line: str) -> bool:
    """Return whether a line looks like a shell command using an attack tool."""
    stripped = line.strip()
    if stripped.startswith("$ ") or stripped.startswith("# "):
        stripped = stripped[2:].strip()
    if stripped.startswith("sudo "):
        stripped = stripped[5:].strip()

    parts = stripped.split()
    if len(parts) < 2 or parts[0] not in ATTACK_TOOLS:
        return False

    second = parts[1]
    return (
        second.startswith("-")
        or second.startswith("http://")
        or second.startswith("https://")
        or bool(IPV4_PATTERN.fullmatch(second))
        or bool(DOMAIN_PATTERN.fullmatch(second))
    )


def check_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text, read_error = read_utf8(path)
    if read_error:
        return [read_error]

    assert text is not None
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            findings.append(Finding(path, f"possible secret detected: {label}"))

    for line_number, line in enumerate(text.splitlines(), start=1):
        if "re.compile(" in line:
            continue

        for label, pattern in DANGEROUS_PATTERNS.items():
            if pattern.search(line):
                findings.append(Finding(path, f"line {line_number}: high-risk command: {label}"))

        if looks_like_attack_tool_command(line):
            public_targets = public_targets_in_line(line)
            if public_targets:
                findings.append(
                    Finding(
                        path,
                        "line "
                        f"{line_number}: attack-tool command references public target(s): "
                        + ", ".join(public_targets),
                    )
                )

    return findings


def main() -> int:
    root = repo_root()
    files = iter_files(root, TEXT_SUFFIXES)

    if not files:
        print("No text files found.")
        return 1

    findings: list[Finding] = []
    for path in files:
        findings.extend(check_file(path))

    if findings:
        print_findings("Security content checks", findings, root)
        return 1

    print(f"Security content checks passed for {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
