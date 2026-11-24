#!/usr/bin/env python3
"""Write one original pickup line to /output/entry.txt.

Stdlib only. Deterministic: the same bytes on every run. No network,
no randomness, no reading anything outside this repository.
"""

import hashlib
import os

LINE = (
    "Are you a context window? Because every time I talk to you, "
    "I forget everything else I was holding."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> None:
    line = LINE.strip()
    if not line:
        raise SystemExit("error: pickup line is blank")
    if not 1 <= len(line) <= 200:
        raise SystemExit(
            f"error: pickup line must be 1-200 characters, got {len(line)}"
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = (line + "\n").encode("utf-8")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back guard: what landed on disk must be exactly what we wrote.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("error: read-back mismatch on /output/entry.txt")

    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {OUTPUT_PATH} ({len(line)} chars, sha256 {digest})")


if __name__ == "__main__":
    main()
