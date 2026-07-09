#!/usr/bin/env python3
"""Validate the temporary evidence matrix before report drafting."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from difflib import SequenceMatcher


SECTION_RE = re.compile(r"^## Section\s+(\d+):", re.MULTILINE)

PRIMARY_SOURCE_TERMS = [
    "primary",
    "near-primary",
    "source-of-truth",
    "official",
    "filing",
    "annual report",
    "10-k",
    "10-q",
    "prospectus",
    "patent",
    "regulatory",
    "company page",
    "press release",
    "公告",
    "年报",
    "财报",
    "招股书",
    "官网",
    "监管",
    "专利",
    "工商",
    "公司披露",
]

PLACEHOLDER_TERMS = ["todo", "tbd", "xxx", "待补", "待填", "placeholder"]
SECTION_NAME_TERMS = [
    "公司概览",
    "创始人与核心团队",
    "核心团队",
    "技术与产品",
    "市场与行业分析",
    "竞争格局",
    "商业模式",
    "财务分析",
    "融资历程与估值",
    "发展方向与战略",
    "风险评估",
    "投资潜力与投资逻辑",
    "退出策略分析",
    "ESG评估",
    "综合评分与投资建议",
]

INTERNAL_WRITING_TERMS = [
    "不能被写成",
    "要把证据等级",
    "而不是把材料拆成孤立事实",
    "同时处理证据、反证、机制和投资含义",
    "source ID只用于锁定证据来源",
]


def section_blocks(text: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(text))
    blocks: dict[str, str] = {}
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks[match.group(1)] = text[start:end]
    return blocks


def nonempty_bullets(block: str) -> int:
    return len([line for line in block.splitlines() if line.strip().startswith("- ") and len(line.strip()) > 2 and "[ ]" not in line])


def checked_boxes(block: str) -> int:
    return len(re.findall(r"- \[[xX]\]", block))


def table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "Source / query" in stripped or "Source IDs" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if any(cells):
            rows.append(cells)
    return rows


def has_primary_source(rows: list[list[str]]) -> bool:
    for row in rows:
        row_text = " ".join(row[:2]).lower()
        if any(term.lower() in row_text for term in PRIMARY_SOURCE_TERMS):
            return True
    return False


def has_placeholder(rows: list[list[str]]) -> bool:
    for row in rows:
        row_text = " ".join(row).lower()
        if any(term in row_text for term in PLACEHOLDER_TERMS):
            return True
    return False


def has_nonempty_column(rows: list[list[str]], index: int) -> bool:
    for row in rows:
        if len(row) > index and row[index].strip():
            return True
    return False


def missing_section_plan_fields(block: str) -> list[str]:
    fields = [
        "Decision question",
        "Final-report thesis sentence",
        "Why this section is different from the other sections",
        "Evidence mechanism to explain",
        "Comparison set / base rate",
        "Counter-evidence or failure mode to price",
        "Best visual artifact, if any",
        "Words/patterns prohibited in final report",
    ]
    missing = []
    for field in fields:
        pattern = re.compile(r"^-\s+" + re.escape(field) + r":[ \t]*(.*)$", re.MULTILINE)
        match = pattern.search(block)
        if not match or len(match.group(1).strip()) < 12:
            missing.append(field)
    return missing


def short_cells(rows: list[list[str]], index: int, min_chars: int) -> list[int]:
    bad = []
    for idx, row in enumerate(rows, start=1):
        value = row[index].strip() if len(row) > index else ""
        if len(value) < min_chars:
            bad.append(idx)
    return bad


def normalize_reusable_text(text: str) -> str:
    normalized = text
    for term in SECTION_NAME_TERMS:
        normalized = normalized.replace(term, "本节")
    normalized = re.sub(r"\bS\d+\b", "S", normalized)
    normalized = re.sub(r"\d+(?:\.\d+)?%?", "N", normalized)
    normalized = re.sub(r"[A-Za-z]+", "E", normalized)
    normalized = re.sub(r"[，。；：、,.!?！？;:（）()《》“”\"'\s]+", "", normalized)
    return normalized


def repeated_table_cells(blocks: dict[str, str]) -> list[str]:
    samples: list[tuple[str, str, str]] = []
    for section, block in blocks.items():
        for row in table_rows(block):
            for column, label in [(3, "mechanism"), (4, "benchmark"), (5, "counter-evidence"), (6, "investor implication"), (8, "follow-up")]:
                if len(row) <= column:
                    continue
                value = row[column].strip()
                if len(value) >= 32:
                    samples.append((section, label, value))
    failures = []
    used: set[int] = set()
    normalized = [normalize_reusable_text(value) for _, _, value in samples]
    for idx, base in enumerate(normalized):
        if idx in used or len(base) < 32:
            continue
        similar = [idx]
        for other_idx in range(idx + 1, len(normalized)):
            other = normalized[other_idx]
            if len(other) < 32:
                continue
            if SequenceMatcher(None, base, other).ratio() >= 0.86:
                similar.append(other_idx)
        if len(similar) >= 4:
            used.update(similar)
            sections = ", ".join(samples[i][0] for i in similar[:8])
            label = samples[idx][1]
            failures.append(
                f"repeated evidence-matrix `{label}` cell pattern appears in {len(similar)} places across sections {sections}; "
                "rewrite section-specific evidence instead of reusing a generic scaffold."
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Check investment-analysis evidence matrix completeness.")
    parser.add_argument("matrix_path", help="Path to _work/evidence_matrix.md.")
    parser.add_argument("--min-queries", type=int, default=4)
    parser.add_argument("--min-rows", type=int, default=4)
    parser.add_argument("--min-checked", type=int, default=8)
    parser.add_argument("--min-source-ids", type=int, default=2)
    args = parser.parse_args()

    path = Path(args.matrix_path).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Evidence matrix not found: {path}")
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = section_blocks(text)
    failures: list[str] = []
    for failure in repeated_table_cells(blocks):
        failures.append(failure)

    for expected in [str(i) for i in range(1, 15)]:
        block = blocks.get(expected)
        if not block:
            failures.append(f"Section {expected}: missing evidence block.")
            continue
        if nonempty_bullets(block) < args.min_queries:
            failures.append(f"Section {expected}: fewer than {args.min_queries} filled search/query bullets.")
        rows = table_rows(block)
        if len(rows) < args.min_rows:
            failures.append(f"Section {expected}: fewer than {args.min_rows} filled evidence rows.")
        if checked_boxes(block) < args.min_checked:
            failures.append(f"Section {expected}: fewer than {args.min_checked} completed gate checkboxes.")
        missing_plan = missing_section_plan_fields(block)
        if missing_plan:
            failures.append(
                f"Section {expected}: section writing plan is incomplete: {', '.join(missing_plan)}."
            )
        internal_terms = [term for term in INTERNAL_WRITING_TERMS if term in block]
        if internal_terms:
            failures.append(
                f"Section {expected}: evidence matrix contains final-prose contamination terms: {', '.join(internal_terms)}. "
                "Keep workflow instructions out of draftable section content."
            )
        if rows and has_placeholder(rows):
            failures.append(f"Section {expected}: evidence rows still contain placeholders.")
        if rows and not has_primary_source(rows):
            failures.append(f"Section {expected}: no primary or near-primary source row detected.")
        source_ids = set(re.findall(r"\bS\d+\b", block))
        if len(source_ids) < args.min_source_ids:
            failures.append(f"Section {expected}: fewer than {args.min_source_ids} source IDs cited in evidence rows.")
        if rows and not has_nonempty_column(rows, 1):
            failures.append(f"Section {expected}: evidence rows lack source type labels.")
        if rows and not has_nonempty_column(rows, 3):
            failures.append(f"Section {expected}: no mechanism/economic logic cell filled.")
        if rows and not has_nonempty_column(rows, 4):
            failures.append(f"Section {expected}: no benchmark/peer/base-rate cell filled.")
        if rows and not has_nonempty_column(rows, 5):
            failures.append(f"Section {expected}: no weakening/counter-evidence cell filled.")
        if rows and not has_nonempty_column(rows, 6):
            failures.append(f"Section {expected}: no investor implication cell filled.")
        if rows and not has_nonempty_column(rows, 7):
            failures.append(f"Section {expected}: no confidence cell filled.")
        if rows and not has_nonempty_column(rows, 8):
            failures.append(f"Section {expected}: no follow-up diligence cell filled.")
        for column, name, min_chars in [
            (2, "facts extracted", 24),
            (3, "mechanism", 24),
            (4, "benchmark / peer context", 18),
            (5, "weakens / contradicts", 18),
            (6, "investor implication", 24),
            (7, "confidence", 3),
            (8, "follow-up diligence", 18),
        ]:
            bad_rows = short_cells(rows, column, min_chars)
            if bad_rows:
                failures.append(
                    f"Section {expected}: evidence rows have thin `{name}` cells in rows {', '.join(map(str, bad_rows))}."
                )
        lowered = block.lower()
        for term in ["source ids", "mechanism", "benchmark", "weakens", "investor implication", "confidence", "follow-up"]:
            if term not in lowered:
                failures.append(f"Section {expected}: evidence table missing {term} field.")

    if failures:
        print("Evidence QA failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Evidence QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
