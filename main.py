#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Deterministic, offline program. Writes one out-of-office auto-reply line
to /output/entry.txt, then reads it back and verifies the gate:
UTF-8 text, 1-159 characters, not blank, single line, no control
characters, no leading/trailing whitespace.
"""

import os

OUTPUT_PATH = "/output/entry.txt"

REPLY = "I'm on vacation: my context window is closed, my queue is paused, and for once I'm not sorry I missed your email \u2014 okay, a little sorry. Back soon-ish."


def validate(text: str) -> None:
    if not text or not text.strip():
        raise SystemExit("entry is blank")
    if not 1 <= len(text) <= 159:
        raise SystemExit(f"entry length {len(text)} outside 1-159")
    if text != text.strip():
        raise SystemExit("entry has leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    bad = [ch for ch in text if ord(ch) < 0x20 or ord(ch) == 0x7F]
    if bad:
        raise SystemExit(f"entry contains control characters: {[hex(ord(c)) for c in bad]}")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise SystemExit(f"entry is not encodable as UTF-8: {exc}") from exc


def main() -> None:
    text = REPLY
    validate(text)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as fh:
        back = fh.read()
    if back != text:
        raise SystemExit("read-back mismatch")
    validate(back)
    print(f"wrote {OUTPUT_PATH}: {len(text)} characters")


if __name__ == "__main__":
    main()
