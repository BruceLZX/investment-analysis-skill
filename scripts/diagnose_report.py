#!/usr/bin/env python3
"""Create a targeted rewrite plan for a failed investment-analysis report."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")
STYLE_SCRIPT_PATTERN = re.compile(r"<(style|script)[^>]*>[\s\S]*?</\1>", re.IGNORECASE)
SECTION_PATTERN = re.compile(
    r'<section[^>]+class="[^"]*section-card[^"]*"[^>]+id="s(?P<num>\d+)"[\s\S]*?>(?P<body>[\s\S]*?)</section>',
    re.IGNORECASE,
)

SECTION_TITLES = {
    "1": "公司概览",
    "2": "创始人与核心团队",
    "3": "技术与产品",
    "4": "市场与行业分析",
    "5": "竞争格局",
    "6": "商业模式",
    "7": "财务分析",
    "8": "融资历程与估值",
    "9": "发展方向与战略",
    "10": "风险评估",
    "11": "投资潜力与投资逻辑",
    "12": "退出策略分析",
    "13": "ESG评估",
    "14": "综合评分与投资建议",
}

META_PATTERNS = [
    "不能被写成",
    "要把证据等级",
    "而不是把材料拆成孤立事实",
    "同时处理证据、反证、机制和投资含义",
    "source ID只用于锁定证据来源",
    "本节应支持",
]

SCAFFOLD_PATTERNS = [
    "的机制：",
    "的benchmark：",
    "原件优先级：",
    "决策门槛：",
    "决策清单：",
    "投资含义：",
]


def strip_html(fragment: str) -> str:
    text = TAG_PATTERN.sub(" ", fragment)
    return SPACE_PATTERN.sub(" ", html.unescape(text)).strip()


def class_count(report_html: str, class_name: str) -> int:
    return len(re.findall(r'class="[^"]*\b' + re.escape(class_name) + r'\b[^"]*"', report_html))


def diagnose_sections(report_html: str) -> list[str]:
    findings: list[str] = []
    for match in SECTION_PATTERN.finditer(report_html):
        section_num = match.group("num")
        title = SECTION_TITLES.get(section_num, f"Section {section_num}")
        body_html = match.group("body")
        text = strip_html(body_html)
        reasons = []
        title_count = text.count(title)
        if title_count > 4:
            reasons.append(f"章节标题在正文中重复 {title_count} 次")
        meta_hits = [term for term in META_PATTERNS if term in text]
        if meta_hits:
            reasons.append("出现内部写作规范语言：" + "、".join(meta_hits[:4]))
        scaffold_hits = [term for term in SCAFFOLD_PATTERNS if term in text]
        if scaffold_hits:
            reasons.append("出现可见模板脚手架：" + "、".join(scaffold_hits[:5]))
        source_tags = len(re.findall(r'class="[^"]*\bsource-tag\b[^"]*"', body_html))
        if source_tags > 6:
            reasons.append(f"inline source-tag 过多：{source_tags} 个")
        if reasons:
            findings.append(f"- [ ] Section {section_num} {title}: 删除模板化正文并重写。问题：{'；'.join(reasons)}。")
    return findings


def build_plan(output_dir: Path, html_path: Path) -> str:
    report_html = html_path.read_text(encoding="utf-8", errors="replace")
    visible_text = strip_html(STYLE_SCRIPT_PATTERN.sub(" ", report_html))
    actions: list[str] = [
        "# Rewrite Plan",
        "",
        "This file is generated after report QA failure. Complete every checkbox before rerunning `loop` or `clean`.",
        "",
        "## Root Cause",
        "",
    ]

    root_causes = []
    if 'data-template-version="codex-compact-toc-v3"' not in report_html:
        root_causes.append("HTML was not generated from the current compact Codex template.")
    if re.search(r'id="openToc"|id="tocBackdrop"|id="closeToc"|setTocOpen\(', report_html):
        root_causes.append("Old overlay TOC code is present.")
    if any(term in visible_text for term in META_PATTERNS):
        root_causes.append("Internal writing instructions leaked into final prose.")
    if sum(visible_text.count(term) for term in SCAFFOLD_PATTERNS) > 8:
        root_causes.append("Sections were filled by repeating a visible scaffold instead of writing analysis.")
    if class_count(report_html, "kpi-dashboard") > 6:
        root_causes.append("KPI dashboard/cards were repeated as filler.")
    inline_source_tags = class_count(report_html, "source-tag")
    if inline_source_tags > 60:
        root_causes.append(f"Inline source tags are excessive ({inline_source_tags}); citations are being used as noise.")

    if not root_causes:
        root_causes.append("Report failed QA; inspect check_depth/check_report output and rewrite weak sections.")
    for cause in root_causes:
        actions.append(f"- {cause}")

    actions.extend(
        [
            "",
            "## Required Fixes",
            "",
            "- [ ] Regenerate the HTML from `templates/report_template.html`; do not patch an old overlay-TOC file in place.",
            "- [ ] Remove all final-report prose that explains how the section should be written. The report must analyze the company, not describe the rubric.",
            "- [ ] Rewrite affected sections from `_work/evidence_matrix.md` using the `Final-report thesis sentence` as the opening judgement.",
            "- [ ] Replace repeated `机制/benchmark/原件优先级/决策门槛/决策清单/投资含义` blocks with section-specific narrative paragraphs.",
            "- [ ] Keep inline source tags to material claims only; move full source detail to the source appendix.",
            "- [ ] Use tables or matrices only where they clarify evidence, scenarios, comparables, risks, or citations.",
            "- [ ] Rerun `python scripts/run_analysis_harness.py loop --output ... --html ... --pdf ...` after rewriting.",
            "",
            "## Section Rewrite Checklist",
            "",
        ]
    )
    section_findings = diagnose_sections(report_html)
    actions.extend(section_findings or ["- [ ] No section-specific diagnosis found; inspect QA output manually."])
    actions.append("")
    return "\n".join(actions)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a rewrite plan for a failed investment-analysis report.")
    parser.add_argument("--output", required=True, help="Report output folder.")
    parser.add_argument("--html", required=True, help="Failed HTML report path.")
    args = parser.parse_args()

    output_dir = Path(args.output).expanduser().resolve()
    html_path = Path(args.html).expanduser().resolve()
    if not html_path.exists():
        raise SystemExit(f"HTML report not found: {html_path}")

    plan = build_plan(output_dir, html_path)
    work_dir = output_dir / "_work"
    if work_dir.is_dir():
        target = work_dir / "rewrite_plan.md"
        target.write_text(plan, encoding="utf-8")
        print(f"Rewrite plan written: {target}")
    else:
        print(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
