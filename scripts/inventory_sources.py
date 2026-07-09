#!/usr/bin/env python3
"""Create a lightweight inventory for investment-analysis source files."""

from __future__ import annotations

import argparse
import hashlib
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SUPPORTED_HINTS = {
    ".pdf": "PDF: extract text; if image-only, render pages and OCR.",
    ".ppt": "PowerPoint: inspect with office tooling or convert to PDF/images.",
    ".pptx": "PowerPoint: extract slide text and visually inspect screenshots.",
    ".doc": "Word: extract text/tables; preserve page or section references.",
    ".docx": "Word: extract text/tables; inspect comments and tracked changes if available.",
    ".xls": "Spreadsheet: inspect sheets, formulas, units, and hidden assumptions.",
    ".xlsx": "Spreadsheet: inspect sheets, formulas, units, and hidden assumptions.",
    ".csv": "CSV: identify delimiter, columns, units, and date range.",
    ".png": "Image: OCR and visually inspect labels, legends, and dates.",
    ".jpg": "Image: OCR and visually inspect labels, legends, and dates.",
    ".jpeg": "Image: OCR and visually inspect labels, legends, and dates.",
    ".tif": "Image: OCR and visually inspect labels, legends, and dates.",
    ".tiff": "Image: OCR and visually inspect labels, legends, and dates.",
}


def sha256_prefix(path: Path, block_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(block_size), b""):
            digest.update(block)
    return digest.hexdigest()[:16]


def iter_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    yield child


def format_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{num_bytes} B"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory source files for investment analysis.")
    parser.add_argument("paths", nargs="+", help="Files or directories to inventory.")
    args = parser.parse_args()

    input_paths = [Path(item).expanduser().resolve() for item in args.paths]
    files = list(iter_files(input_paths))
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print("# Temporary Working Notes")
    print()
    print(f"Generated source inventory: {generated_at}")
    print()
    print("- Company: `TODO`")
    print("- Report date: `TODO`")
    print("- Data as of: `TODO`")
    print("- Scope: `TODO`")
    print()
    print("## Source Inventory")
    print()
    print("| ID | File | Type | Size | Modified | SHA-256 prefix | Handling note |")
    print("| --- | --- | --- | ---: | --- | --- | --- |")

    if not files:
        print("| S0 | No files found | | | | | |")
        return 0

    for index, path in enumerate(files, start=1):
        stat = path.stat()
        suffix = path.suffix.lower()
        mime_type = mimetypes.guess_type(path.name)[0] or "unknown"
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        note = SUPPORTED_HINTS.get(suffix, "Inspect manually; determine whether OCR, parsing, or conversion is needed.")
        print(
            "| S{idx} | {file} | {mime} | {size} | {modified} | {digest} | {note} |".format(
                idx=index,
                file=str(path),
                mime=mime_type,
                size=format_size(stat.st_size),
                modified=modified,
                digest=sha256_prefix(path),
                note=note,
            )
        )

    print()
    print("## Claim Verification")
    print()
    print("| Claim | Source file/page | External corroboration | Verdict | Notes |")
    print("| --- | --- | --- | --- | --- |")
    print()
    print("## Source Register")
    print()
    print("| ID | Source | URL/file page | Date | Source type | Key facts | Confidence |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
