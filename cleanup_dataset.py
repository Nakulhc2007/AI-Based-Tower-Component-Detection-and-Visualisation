"""
Cleanup script: removes exact duplicate images from the sample/ directory.
Identified duplicates (same MD5 hash) from the inspection report.
"""

import os
from pathlib import Path

SAMPLE_DIR = Path(r"a:\projects\ksit hackathon\sample")

# Duplicates identified by MD5 hash (keep first, remove second)
DUPLICATES_TO_REMOVE = [
    "img_2bc4c71be05a4ddf.JPG",   # dup of img_03a380add45d48ab.JPG
    "img_29c096afeb0f4b7f.JPG",   # dup of img_071c8e9f3df7415a.JPG
    "img_69e6287b52a74e3d.JPG",   # dup of img_09401dd6590e4a35.JPG
    "img_b4c54c0927624533.JPG",   # dup of img_7f301fb5fe5e48ff.JPG
]


def cleanup():
    removed = 0
    for fname in DUPLICATES_TO_REMOVE:
        fpath = SAMPLE_DIR / fname
        if fpath.exists():
            fpath.unlink()
            print(f"  Removed: {fname}")
            removed += 1
        else:
            print(f"  Already gone: {fname}")

    remaining = len(list(SAMPLE_DIR.iterdir()))
    print(f"\nRemoved {removed} duplicates. {remaining} images remain.")


if __name__ == "__main__":
    cleanup()
