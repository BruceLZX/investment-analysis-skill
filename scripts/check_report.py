#!/usr/bin/env python3
"""Basic QA checks for generated investment-analysis reports."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z0-9_]+\}\}")
EXEC_PATTERN = re.compile(
    r'<section[^>]+class="[^"]*exec-summary[^"]*"[\s\S]*?>(?P<body>[\s\S]*?)</section>',
    re.IGNORECASE,
)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")
STYLE_SCRIPT_PATTERN = re.compile(r"<(style|script)[^>]*>[\s\S]*?</\1>", re.IGNORECASE)

EXEC_REQUIRED_GROUPS = {
    "verdict/action": ["结论", "建议", "行动", "verdict", "action"],
    "score/rating": ["评分", "评级", "score", "rating"],
    "core positives": ["核心理由", "正面", "优势", "bull", "positive"],
    "key risks": ["风险", "下行", "bear", "risk"],
    "evidence confidence": ["置信", "confidence", "证据质量", "source confidence"],
    "valuation/terms": ["估值", "价格", "条款", "valuation", "price", "terms"],
    "follow-up diligence": ["尽调", "待验证", "待核实", "follow-up", "diligence"],
    "one question": ["最重要的问题", "一个问题", "one question", "关键问题"],
    "three takeaways": ["三件事", "三个要点", "three takeaways", "three things"],
}

PUBLIC_EQUITY_DETECT_TERMS = [
    "股票",
    "股价",
    "证券代码",
    "ticker",
    "share price",
    "market cap",
    "市值",
    "上市公司",
    "二级市场",
    "public equity",
]

PUBLIC_EQUITY_REQUIRED_GROUPS = {
    "stock price context": ["股价", "share price", "价格截至", "交易日", "市值", "market cap", "ticker", "证券代码"],
    "income statement quality": ["利润表", "收入", "毛利率", "营业利润", "净利润", "eps", "margin", "earnings quality", "盈利质量"],
    "cash flow": ["现金流", "经营现金流", "自由现金流", "capex", "资本开支", "fcf", "cash conversion", "现金转化"],
    "balance sheet": ["资产负债表", "资产", "负债", "现金", "债务", "流动性", "杠杆", "balance sheet"],
    "notes/accounting quality": ["附注", "会计", "审计", "减值", "关联方", "表外", "accounting", "auditor", "impairment", "related-party"],
    "valuation": ["估值", "pe", "p/e", "ev/ebitda", "ev/sales", "pb", "p/b", "fcf yield", "市盈率", "市净率"],
    "position sizing": ["仓位", "position sizing", "配置", "买入", "持有", "卖出", "watchlist", "reduce", "sell", "buy"],
}

FINAL_REPORT_FORBIDDEN_PATTERNS = {
    "meta-writing phrase `不能被写成`": r"不能被写成",
    "meta-writing phrase `要把证据等级`": r"要把证据等级",
    "meta-writing phrase `而不是把材料拆成孤立事实`": r"而不是把材料拆成孤立事实",
    "meta-writing phrase `同时处理证据、反证、机制和投资含义`": r"同时处理证据、反证、机制和投资含义",
    "meta-citation phrase `source ID只用于锁定证据来源`": r"source\s*ID只用于锁定证据来源",
    "meta-valuation phrase `必须放回自身语境判断`": r"必须放回[^。]{0,40}自身语境判断",
    "generic 18-24 month evidence fallback": r"关键原件在18-24个月内无法提供",
    "generic original-control-before-market phrase": r"先核实目标公司真实控制什么，再讨论行业空间",
    "meta-section phrase `本节应支持`": r"本节应支持",
}


def strip_html(fragment: str) -> str:
    text = TAG_PATTERN.sub(" ", fragment)
    return SPACE_PATTERN.sub(" ", html.unescape(text)).strip()


def missing_exec_groups(text: str) -> list[str]:
    lowered = text.lower()
    missing = []
    for group, terms in EXEC_REQUIRED_GROUPS.items():
        if not any(term.lower() in lowered for term in terms):
            missing.append(group)
    return missing


def looks_like_public_equity(text: str) -> bool:
    lowered = text.lower()
    strong_markers = ["股价", "证券代码", "ticker", "share price", "market cap", "市值"]
    marker_count = sum(1 for term in PUBLIC_EQUITY_DETECT_TERMS if term.lower() in lowered)
    has_strong_marker = any(term.lower() in lowered for term in strong_markers)
    return has_strong_marker and marker_count >= 2


def missing_public_equity_groups(text: str) -> list[str]:
    lowered = text.lower()
    missing = []
    for group, terms in PUBLIC_EQUITY_REQUIRED_GROUPS.items():
        if not any(term.lower() in lowered for term in terms):
            missing.append(group)
    return missing


def class_count(report_html: str, class_name: str) -> int:
    return len(re.findall(r'class="[^"]*\b' + re.escape(class_name) + r'\b[^"]*"', report_html))


def print_failures(failures: list[str], limit: int = 80) -> None:
    print("Report QA failed:")
    for failure in failures[:limit]:
        print(f"- {failure}")
    remaining = len(failures) - limit
    if remaining > 0:
        print(f"- ... {remaining} additional failures omitted; fix the repeated root cause and rerun QA.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated HTML/PDF investment report files.")
    parser.add_argument("html_path", help="Generated HTML report path.")
    parser.add_argument("pdf_path", nargs="?", help="Generated PDF report path.")
    args = parser.parse_args()

    html_path = Path(args.html_path).expanduser().resolve()
    pdf_path = Path(args.pdf_path).expanduser().resolve() if args.pdf_path else html_path.with_suffix(".pdf")

    failures: list[str] = []

    if not html_path.exists():
        failures.append(f"HTML report missing: {html_path}")
    elif html_path.stat().st_size == 0:
        failures.append(f"HTML report is empty: {html_path}")
    else:
        report_html = html_path.read_text(encoding="utf-8", errors="replace")
        visible_text = strip_html(STYLE_SCRIPT_PATTERN.sub(" ", report_html))
        visible_lower = visible_text.lower()
        if 'data-template-version="codex-compact-toc-v3"' not in report_html:
            failures.append("Layout quality: current Codex compact template marker missing; regenerate from templates/report_template.html.")
        if re.search(r'id="openToc"|id="tocBackdrop"|id="closeToc"|setTocOpen\(', report_html):
            failures.append("Layout quality: old overlay table-of-contents UI detected; use the compact non-overlapping TOC template.")
        placeholders = sorted(set(PLACEHOLDER_PATTERN.findall(report_html)))
        if placeholders:
            failures.append("Unreplaced placeholders: " + ", ".join(placeholders))
        for required_text in ["5分钟速读", "重要声明", "数据截至", "风险", "投资"]:
            if required_text not in report_html:
                failures.append(f"Expected report text not found in HTML: {required_text}")
        exec_match = EXEC_PATTERN.search(report_html)
        if not exec_match:
            failures.append("Executive briefing section not found.")
        else:
            exec_html = exec_match.group("body")
            exec_text = strip_html(exec_match.group("body"))
            if len(exec_text) < 900:
                failures.append(f"Executive briefing is too thin ({len(exec_text)} chars, minimum 900).")
            missing = missing_exec_groups(exec_text)
            if missing:
                failures.append("Executive briefing missing decision fields: " + ", ".join(missing))
            if class_count(exec_html, "verdict-strip") < 1:
                failures.append("Executive briefing missing a visible verdict strip; start with the decision, not generic cards.")
            if class_count(exec_html, "brief-card") < 5:
                failures.append("Executive briefing needs at least 5 compact decision cards after the verdict strip.")
        source_mentions = len(
            re.findall(
                r'class="[^"]*source-(?:tag|confidence)[^"]*"',
                report_html,
            )
        ) + len(re.findall(r"来源|Source|source|公告|年报|招股书|专利|监管", visible_text))
        if source_mentions < 30:
            failures.append(f"Report has too few visible source/confidence mentions ({source_mentions}, minimum 30).")

        inline_source_tags = len(re.findall(r'class="[^"]*source-tag[^"]*"', report_html))
        if inline_source_tags > 60:
            failures.append(
                f"Citation quality: too many inline source tags ({inline_source_tags}, maximum 60). "
                "Use a consolidated source appendix and cite only material claims inline."
            )
        citation_anchor_count = len(re.findall(r'class="[^"]*citation-line[^"]*"|引用锚点', report_html))
        if citation_anchor_count > 1:
            failures.append(
                f"Reading quality: repeated per-section citation-anchor blocks detected ({citation_anchor_count}). "
                "Use one source appendix instead of repeated citation filler."
            )

        if not re.search(r"(数据来源与引用|引用附录|Source Appendix|source appendix)", visible_text, re.IGNORECASE):
            failures.append("Citation quality: consolidated source appendix not found.")
        citation_links = len(re.findall(r"<a\s+[^>]*href=", report_html, re.IGNORECASE))
        if citation_links < 5:
            failures.append(f"Citation quality: too few clickable citation/source links ({citation_links}, minimum 5).")
        boilerplate_checks = {
            "投资人读法": 2,
            "来源/Source": 2,
            "相比只看赛道热度": 2,
            "交易结构含义也很直接": 2,
            "原件优先级应按3层推进": 1,
            "这些ID只说明证据来源，不替代原件尽调": 1,
            "公开来源与公司材料交叉校验": 4,
            "不为未验证里程碑一次性定价": 3,
        }
        for phrase, max_count in boilerplate_checks.items():
            count = visible_text.count(phrase)
            if count > max_count:
                failures.append(f"Reading quality: repeated boilerplate phrase `{phrase}` appears {count} times.")

        repeated_subheads = ["经济机制：", "比较与基准：", "反证与风险：", "投资含义："]
        for subhead in repeated_subheads:
            count = visible_text.count(subhead)
            if count > 4:
                failures.append(
                    f"Reading quality: repeated visible scaffold `{subhead}` appears {count} times. "
                    "Use section-specific micro-headings and narrative analysis instead."
                )

        template_patterns = {
            "section-name judgement scaffold": r"判断：[^。]{0,80}要把证据等级、经济机制、替代方案、反证和投资动作放在同一条逻辑链",
            "generic device-commercialization mechanism": r"里的经济机制要通过注册证、医生采用、患者依从、支付路径、渠道复购和真实回款共同解释",
            "section-name benchmark scaffold": r"的benchmark：",
            "section-name original-document priority scaffold": r"原件优先级：",
            "section-name decision-threshold scaffold": r"决策门槛：",
            "section-name decision-checklist scaffold": r"决策清单：",
        }
        for label, pattern in template_patterns.items():
            count = len(re.findall(pattern, visible_text, flags=re.IGNORECASE))
            if count > 1:
                failures.append(
                    f"Reading quality: repeated `{label}` appears {count} times. "
                    "This indicates section-name substitution rather than section-specific analysis."
                )

        for label, pattern in FINAL_REPORT_FORBIDDEN_PATTERNS.items():
            count = len(re.findall(pattern, visible_text, flags=re.IGNORECASE))
            if count:
                failures.append(
                    f"Reading quality: final report contains {label} ({count}). "
                    "Do not leak internal writing instructions into the delivered analysis."
                )

        table_count = len(re.findall(r"<table\b", report_html, re.IGNORECASE))
        if table_count < 4:
            failures.append(
                f"Visual/analytical structure: too few data/scenario/source tables ({table_count}, minimum 4). "
                "Use tables where they clarify evidence, scenarios, comparables, risks, or citations."
            )
        kpi_dashboard_count = class_count(report_html, "kpi-dashboard")
        if kpi_dashboard_count > 6:
            failures.append(
                f"Visual quality: KPI dashboard repeated {kpi_dashboard_count} times. "
                "Use one or two high-signal KPI strips, not the same visual module in every section."
            )

        # Decision-quality checks. Keep these broad to avoid forcing false precision.
        lowered_html = report_html.lower()

        scenario_count = len(re.findall(r'(bull|bear|base)\s*(case|情景|场景)', lowered_html))
        if scenario_count < 3:
            failures.append(f"Decision quality: too few scenario references ({scenario_count}, need bull/base/bear or equivalent).")

        if not re.search(r'(关键假设|敏感性分析|sensitivity|assumption.*impact|如果.*会)', visible_lower):
            failures.append("Decision quality: no key assumption or sensitivity analysis found.")

        if not re.search(r'(非共识|non.consensus|variant perception|市场共识|共识)', visible_lower):
            failures.append("Decision quality: no non-consensus/consensus view found.")

        if not re.search(
            r'(地理|市场体系|国内|国际|海外|本土|全球|区域|跨境|客户市场|供应链|资本市场|退出市场|home market|customer market|supplier market|capital market|exit market|geographic)',
            visible_lower,
        ):
            failures.append("Decision quality: no geographic/market-system perspective found.")

        if looks_like_public_equity(visible_text):
            missing = missing_public_equity_groups(visible_text)
            if missing:
                failures.append("Public-equity financial analysis missing fields: " + ", ".join(missing))

    if not pdf_path.exists():
        failures.append(f"PDF report missing: {pdf_path}")
    elif pdf_path.stat().st_size == 0:
        failures.append(f"PDF report is empty: {pdf_path}")

    if failures:
        print_failures(failures)
        return 1

    print("Report QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
