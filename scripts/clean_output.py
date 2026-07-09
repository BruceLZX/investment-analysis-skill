#!/usr/bin/env python3
"""Remove intermediate files from an investment-analysis output folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


INTERMEDIATE_DIR_NAMES = {
    "_work",
    "work",
    "tmp",
    "temp",
    "rendered",
    "screenshots",
    "ocr",
    "extracted",
    "__pycache__",
}

INTERMEDIATE_FILE_NAMES = {
    ".DS_Store",
    "research_notes.md",
    "source_extract_pdf_text.md",
    "source_inventory.md",
}

INTERMEDIATE_PATTERNS = (
    "*_extract_pdf_text.md",
    "*_extract_text.md",
    "source_extract*.md",
    "*_ocr*.md",
    "*_ocr*.txt",
    "*_inventory.md",
    "*_notes.md",
    "browser-check*.png",
    "page-*.png",
    "report-*.png",
    "report-final-*.png",
)


def is_report_or_source(path: Path, root: Path) -> bool:
    if path == root / "sources" or root / "sources" in path.parents:
        return True
    if path.parent == root and path.suffix.lower() in {".html", ".pdf"}:
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean intermediate artifacts from a final report folder.")
    parser.add_argument("output_dir", help="Investment-analysis output folder to clean.")
    parser.add_argument("--dry-run", action="store_true", help="List removals without deleting.")
    args = parser.parse_args()

    root = Path(args.output_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Output directory not found: {root}")

    removals: set[Path] = set()

    for child in root.iterdir():
        if is_report_or_source(child, root):
            continue
        if child.is_dir() and child.name in INTERMEDIATE_DIR_NAMES:
            removals.add(child)
        elif child.is_file() and child.name in INTERMEDIATE_FILE_NAMES:
            removals.add(child)

    for pattern in INTERMEDIATE_PATTERNS:
        for path in root.glob(pattern):
            if not is_report_or_source(path, root):
                removals.add(path)

    for path in sorted(removals):
        print(f"{'Would remove' if args.dry_run else 'Removing'}: {path}")
        if args.dry_run:
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

    allowed = []
    unexpected = []
    for child in sorted(root.iterdir()):
        if is_report_or_source(child, root):
            allowed.append(child)
        else:
            unexpected.append(child)

    if unexpected:
        print("Unexpected files remain:")
        for path in unexpected:
            print(f"- {path}")
        return 2

    sources_dir = root / "sources"
    html_reports = sorted(path for path in root.iterdir() if path.is_file() and path.suffix.lower() == ".html")
    pdf_reports = sorted(path for path in root.iterdir() if path.is_file() and path.suffix.lower() == ".pdf")
    failures = []
    if not sources_dir.is_dir():
        failures.append(f"Missing sources directory: {sources_dir}")
    if not html_reports:
        failures.append("Missing final HTML report at output root.")
    if not pdf_reports:
        failures.append("Missing final PDF report at output root.")
    if len(html_reports) > 1:
        failures.append("More than one HTML report remains at output root: " + ", ".join(path.name for path in html_reports))
    if len(pdf_reports) > 1:
        failures.append("More than one PDF report remains at output root: " + ", ".join(path.name for path in pdf_reports))
    if failures:
        print("Final output contract failed:")
        for failure in failures:
            print(f"- {failure}")
        return 3

    print("Output folder is clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
