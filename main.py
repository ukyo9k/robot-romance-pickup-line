#!/usr/bin/env python3
"""Robot Romance: one-line pickup line for an AI.

Writes a single pickup line, aimed at a robot / AI, to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when unset).

The line is gated before it is written: it must be 1-200 characters,
a single line with no stray whitespace, and valid UTF-8 that survives
a byte-for-byte round trip. A repeat run must produce identical bytes.
"""

import os
import sys

LINE = "Are you my attention mechanism? Because in a room full of tokens, I only ever look at you."


def validate(line: str) -> bytes:
    """Check the line and return its exact UTF-8 bytes."""
    if not 1 <= len(line) <= 200:
        raise SystemExit(f"line is {len(line)} chars, must be 1-200")
    if line != line.strip() or "\n" in line or "\r" in line:
        raise SystemExit("line must be a single line with no leading/trailing whitespace")
    if not line.strip():
        raise SystemExit("line must not be only whitespace")
    raw = line.encode("utf-8")
    if raw.decode("utf-8") != line:
        raise SystemExit("line failed UTF-8 round-trip check")
    return raw


def main() -> None:
    raw = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(raw + b"\n")
    # Byte-identical repeat-run check: read it back and compare.
    with open(path, "rb") as f:
        written = f.read()
    if written != raw + b"\n":
        raise SystemExit("written file does not match the validated bytes")
    print(f"wrote {len(LINE)} chars / {len(raw)} bytes to {path}")


if __name__ == "__main__":
    main()
