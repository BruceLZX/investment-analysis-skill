#!/usr/bin/env python3
"""Validate the temporary source register before report drafting."""

from __future__ import annotations

import argparse
from pathlib import Path


PRIMARY_TERMS = [
    "primary",
    "near-primary",
    "official",
    "filing",
    "annual report",
    "10-k",
    "10-q",
    "8-k",
    "prospectus",
    "company ir",
    "exchange",
    "sec",
    "edgar",
    "hkex",
    "cninfo",
    "sse",
    "szse",
    "patent",
    "regulatory",
    "公告",
    "年报",
    "季报",
    "半年报",
    "财报",
    "交易所",
    "巨潮",
    "披露易",
    "上交所",
    "深交所",
    "北交所",
    "招股书",
    "官网",
    "监管",
    "专利",
    "工商",
]

INDEPENDENT_TERMS = [
    "independent",
    "third-party",
    "filing",
    "regulatory",
    "media",
    "industry report",
    "market data",
    "broker",
    "database",
    "patent",
    "customer",
    "procurement",
    "独立",
    "第三方",
    "监管",
    "媒体",
    "行业报告",
    "行情",
    "券商",
    "数据库",
    "专利",
    "客户",
    "采购",
]

CONFIDENCE_TERMS = ["high", "medium", "low", "高", "中", "低"]
PLACEHOLDER_TERMS = ["todo", "tbd", "xxx", "待补", "待填", "placeholder"]


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "Source title" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if any(cells):
            rows.append(cells)
    return rows


def is_filled(row: list[str]) -> bool:
    if len(row) < 8:
        return False
    row_text = " ".join(row).lower()
    if any(term in row_text for term in PLACEHOLDER_TERMS):
        return False
    title = row[1].strip()
    source_type = row[2].strip()
    locator = row[3].strip()
    date = row[4].strip()
    claims_supported = row[5].strip()
    confidence = row[7].strip().lower()
    return bool(title and source_type and locator and date and claims_supported) and any(term in confidence for term in CONFIDENCE_TERMS)


def contains_any(row: list[str], terms: list[str]) -> bool:
    row_text = " ".join(row).lower()
    return any(term.lower() in row_text for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check investment-analysis source register completeness.")
    parser.add_argument("register_path", help="Path to _work/source_register.md.")
    parser.add_argument("--min-sources", type=int, default=8)
    parser.add_argument("--min-independent", type=int, default=4)
    parser.add_argument("--min-primary", type=int, default=1)
    args = parser.parse_args()

    path = Path(args.register_path).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Source register not found: {path}")

    rows = table_rows(path.read_text(encoding="utf-8", errors="replace"))
    filled = [row for row in rows if is_filled(row)]
    independent = [row for row in filled if contains_any(row, INDEPENDENT_TERMS)]
    primary = [row for row in filled if contains_any(row, PRIMARY_TERMS)]

    failures: list[str] = []
    if len(filled) < args.min_sources:
        failures.append(f"Fewer than {args.min_sources} usable source rows ({len(filled)}).")
    if len(independent) < args.min_independent:
        failures.append(f"Fewer than {args.min_independent} independent source rows ({len(independent)}).")
    if len(primary) < args.min_primary:
        failures.append(f"Fewer than {args.min_primary} primary or near-primary source rows ({len(primary)}).")

    if failures:
        print("Source register QA failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Source register QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
