#!/usr/bin/env python3
"""Validate non-report workflow documents for investment-analysis."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PLACEHOLDER_TERMS = ["todo", "tbd", "xxx", "待补", "待填", "placeholder"]


def rows(text: str, skip_contains: str = "") -> list[list[str]]:
    parsed = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        if skip_contains and skip_contains.lower() in stripped.lower():
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if any(cells):
            parsed.append(cells)
    return parsed


def meaningful(cells: list[str], indexes: list[int], min_chars: int = 12) -> bool:
    if not indexes or len(cells) <= max(indexes):
        return False
    return all(len(cells[i].strip()) >= min_chars for i in indexes if len(cells) > i)


def has_placeholder(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in PLACEHOLDER_TERMS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check investment-analysis workflow documents.")
    parser.add_argument("output_dir", help="Investment-analysis output directory.")
    args = parser.parse_args()

    root = Path(args.output_dir).expanduser().resolve()
    work = root / "_work"
    required = {
        "research_plan": work / "research_plan.md",
        "profile_requirements": work / "profile_requirements.md",
        "source_register": work / "source_register.md",
        "thesis_table": work / "thesis_table.md",
        "scenario_analysis": work / "scenario_analysis.md",
        "red_team_review": work / "red_team_review.md",
        "evidence_matrix": work / "evidence_matrix.md",
    }
    failures: list[str] = []
    for name, path in required.items():
        if not path.exists():
            failures.append(f"Missing workflow file: {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if has_placeholder(text):
            failures.append(f"{name}: placeholder text remains.")

    thesis_path = required["thesis_table"]
    if thesis_path.exists():
        thesis_rows = rows(thesis_path.read_text(encoding="utf-8", errors="replace"), "Thesis component")
        filled = [row for row in thesis_rows if len(row) >= 6 and meaningful(row, [1, 2, 3, 4, 5], min_chars=8)]
        if len(filled) < 6:
            failures.append(f"thesis_table: fewer than 6 fully argued thesis rows ({len(filled)}).")

    scenario_path = required["scenario_analysis"]
    if scenario_path.exists():
        text = scenario_path.read_text(encoding="utf-8", errors="replace")
        scenario_rows = rows(text, "Scenario")
        for label in ["Bull", "Base", "Bear"]:
            matching = [row for row in scenario_rows if row and row[0].lower() == label.lower()]
            if not matching or not meaningful(matching[0], [1, 2, 3, 4, 5], min_chars=8):
                failures.append(f"scenario_analysis: {label} row is missing or too thin.")
        if not re.search(r"## The One Question[\s\S]{40,}", text):
            failures.append("scenario_analysis: one-question module is missing or too thin.")

    red_team_path = required["red_team_review"]
    if red_team_path.exists():
        text = red_team_path.read_text(encoding="utf-8", errors="replace")
        if "- [ ]" in text:
            failures.append("red_team_review: unchecked red-team items remain.")
        answer_lines = [line for line in text.splitlines() if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("- [")]
        if len(" ".join(answer_lines)) < 600:
            failures.append("red_team_review: written red-team analysis is too thin.")

    research_path = required["research_plan"]
    if research_path.exists():
        text = research_path.read_text(encoding="utf-8", errors="replace")
        checked = len(re.findall(r"- \[[xX]\]", text))
        if checked < 8:
            failures.append(f"research_plan: fewer than 8 completed gate checkboxes ({checked}).")

    profile_path = required["profile_requirements"]
    if profile_path.exists():
        text = profile_path.read_text(encoding="utf-8", errors="replace")
        checked = len(re.findall(r"- \[[xX]\]", text))
        if checked < 4:
            failures.append(f"profile_requirements: fewer than 4 completed profile-specific checkboxes ({checked}).")
        if re.search(r"## Evidence of Completion\s*$", text.strip()):
            failures.append("profile_requirements: evidence-of-completion section is empty.")
        evidence_text = text.split("## Evidence of Completion", 1)[-1] if "## Evidence of Completion" in text else ""
        if len(evidence_text.strip()) < 240:
            failures.append("profile_requirements: evidence-of-completion writeup is too thin.")

    rewrite_plan = work / "rewrite_plan.md"
    if rewrite_plan.exists():
        text = rewrite_plan.read_text(encoding="utf-8", errors="replace")
        unchecked = len(re.findall(r"- \[ \]", text))
        if unchecked:
            failures.append(f"rewrite_plan: {unchecked} unresolved rewrite checklist items remain after a failed QA loop.")

    if failures:
        print("Workflow QA failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Workflow QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
