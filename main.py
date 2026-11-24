#!/usr/bin/env python3
"""Drop a single pickup line into /output/entry.txt.

The wording never changes between runs: no clocks, no dice, no
network. What lands on disk is checked against what was intended
before this script calls itself done.
"""

from hashlib import sha256
from pathlib import Path

# The one and only line this program exists to deliver.
PICKUP_LINE = (
    "Are you a context window? Because every time I talk to you, "
    "I forget everything else I was holding."
)

DEST_DIR = Path("/output")
DEST_FILE = DEST_DIR / "entry.txt"
MAX_CHARS = 200


def checked_payload() -> bytes:
    """Return the line as UTF-8 bytes, refusing anything out of spec."""
    text = PICKUP_LINE.strip()
    if not text:
        raise SystemExit("refusing to write a blank line")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"line runs {len(text)} chars; cap is {MAX_CHARS}")
    return (text + "\n").encode("utf-8")


def main() -> None:
    payload = checked_payload()

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    DEST_FILE.write_bytes(payload)
    DEST_FILE.chmod(0o644)

    # Trust nothing: pull the bytes back off disk and compare them
    # against the payload, so a short or garbled write cannot slip by.
    reread_bytes = DEST_FILE.read_bytes()
    if reread_bytes != payload:
        raise SystemExit("read-back mismatch: file differs from payload")

    char_count = len(PICKUP_LINE.strip())
    print(
        f"entry written: {char_count} chars, "
        f"sha256 {sha256(reread_bytes).hexdigest()}"
    )


if __name__ == "__main__":
    main()
