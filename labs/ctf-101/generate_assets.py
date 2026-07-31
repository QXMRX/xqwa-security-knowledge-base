"""Generate deterministic offline assets for CTF 101 lessons 25-27."""

from __future__ import annotations

import argparse
import os
import shutil
import socket
import struct
import zipfile
from pathlib import Path


LAB_ROOT = Path(__file__).resolve().parent
GENERATED = LAB_ROOT / "generated"


def checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    words = struct.unpack(f"!{len(data) // 2}H", data)
    total = sum(words)
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def tcp_packet(
    source_ip: str,
    destination_ip: str,
    source_port: int,
    destination_port: int,
    sequence: int,
    acknowledgement: int,
    payload: bytes,
) -> bytes:
    ethernet = (
        bytes.fromhex("020000000002")
        + bytes.fromhex("020000000001")
        + struct.pack("!H", 0x0800)
    )
    source = socket.inet_aton(source_ip)
    destination = socket.inet_aton(destination_ip)
    tcp = struct.pack(
        "!HHLLBBHHH",
        source_port,
        destination_port,
        sequence,
        acknowledgement,
        5 << 4,
        0x18,
        65535,
        0,
        0,
    )
    pseudo = source + destination + struct.pack("!BBH", 0, 6, len(tcp) + len(payload))
    tcp_checksum = checksum(pseudo + tcp + payload)
    tcp = tcp[:16] + struct.pack("!H", tcp_checksum) + tcp[18:]
    total_length = 20 + len(tcp) + len(payload)
    ipv4 = struct.pack(
        "!BBHHHBBH4s4s",
        0x45,
        0,
        total_length,
        1,
        0x4000,
        64,
        6,
        0,
        source,
        destination,
    )
    ipv4 = ipv4[:10] + struct.pack("!H", checksum(ipv4)) + ipv4[12:]
    return ethernet + ipv4 + tcp + payload


def write_pcap(path: Path) -> None:
    request = (
        b"GET /profile?id=alice HTTP/1.1\r\n"
        b"Host: 127.0.0.1:8081\r\n"
        b"Cookie: training_session=alice\r\n\r\n"
    )
    response = (
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
        b"Content-Length: 30\r\n\r\n"
        b'{"id":"alice","role":"member"}'
    )
    packets = [
        tcp_packet("127.0.0.1", "127.0.0.1", 49152, 8081, 1, 1, request),
        tcp_packet("127.0.0.1", "127.0.0.1", 8081, 49152, 1, 1 + len(request), response),
    ]
    with path.open("wb") as output:
        output.write(struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
        for offset, packet in enumerate(packets):
            output.write(struct.pack("<IIII", 1_783_000_000 + offset, 0, len(packet), len(packet)))
            output.write(packet)


def generate() -> None:
    evidence = GENERATED / "evidence"
    traffic = GENERATED / "traffic"
    case_package = GENERATED / "case-package"
    for directory in (evidence, traffic, case_package):
        directory.mkdir(parents=True, exist_ok=True)

    sample = evidence / "sample.bin"
    with zipfile.ZipFile(sample, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("notes/readme.txt", "观察容器结构，再提取 flag{offline_file_evidence}\n")
        archive.writestr("metadata/source.txt", "XQWA CTF 101 synthetic evidence\n")

    write_pcap(traffic / "training.pcapng")
    (traffic / "app.log").write_text(
        "2026-07-01T01:35:00+00:00 INFO user=alice path=/profile status=200\n",
        encoding="utf-8",
    )

    files = {
        "brief.txt": "虚构事件：核对两个带时区的时间记录，不搜索现实人物。\n",
        "message-a.txt": "2026-07-01T09:30:00+08:00 created training package\n",
        "message-b.txt": "2026-07-01T01:35:00+00:00 reviewed training package\n",
    }
    fixed_time = 1_783_000_000
    for name, content in files.items():
        path = case_package / name
        path.write_text(content, encoding="utf-8")
        os.utime(path, (fixed_time, fixed_time))

    print(f"Generated offline lab assets in {GENERATED}")


def clean() -> None:
    if GENERATED.parent != LAB_ROOT or GENERATED.name != "generated":
        raise RuntimeError("refusing to clean an unexpected path")
    if GENERATED.exists():
        shutil.rmtree(GENERATED)
    print(f"Removed generated lab assets from {GENERATED}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="remove generated assets")
    args = parser.parse_args()
    clean() if args.clean else generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
