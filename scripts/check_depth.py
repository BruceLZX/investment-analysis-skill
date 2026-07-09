#!/usr/bin/env python3
"""Heuristic depth checks for generated investment-analysis HTML reports."""

from __future__ import annotations

import argparse
import html
import re
from difflib import SequenceMatcher
from pathlib import Path


SECTION_PATTERN = re.compile(
    r'<section[^>]+class="[^"]*section-card[^"]*"[^>]+id="s(?P<num>\d+)"[\s\S]*?>(?P<body>[\s\S]*?)</section>',
    re.IGNORECASE,
)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")
PARAGRAPH_PATTERN = re.compile(r"<p(?:\s+[^>]*)?>[\s\S]*?</p>", re.IGNORECASE)
SENTENCE_PATTERN = re.compile(r"[^。！？.!?]{24,}[。！？.!?]")
SOURCE_ID_PATTERN = re.compile(r"\[?S\d+\]?")

ANALYTICAL_COVERAGE_TERMS = {
    "evidence/source grounding": ["证据", "来源", "source", "验证", "公开", "披露", "公告", "年报", "招股书", "监管", "据"],
    "economic/strategic interpretation": ["原因", "驱动", "为什么", "意味着", "反映", "导致", "because", "driven by", "economics", "unit economics", "经济"],
    "comparison/context": ["对标", "竞品", "竞争", "同行", "同业", "替代", "benchmark", "peer", "comparable", "相比", "高于", "低于"],
    "counter-evidence/risk": ["风险", "失败", "局限", "不确定", "挑战", "压力", "下行", "反过来", "counter", "bear case", "downside"],
    "investor implication": ["投资", "决策", "估值", "条款", "建议", "买入", "卖出", "持有", "等待", "watchlist", "implication"],
    "open diligence": ["待验证", "尽调", "待核实", "下一步", "仍需确认", "需要核实", "diligence", "follow-up", "open question"],
    "confidence/calibration": ["置信", "confidence", "High", "Medium", "Low", "高", "中", "低", "把握", "确定性", "可信度"],
}

SHALLOW_PHRASES = [
    "市场空间广阔",
    "团队背景强",
    "技术壁垒高",
    "商业模式清晰",
    "竞争激烈",
    "风险可控",
    "发展前景良好",
    "具有较大潜力",
]

BOILERPLATE_LIMITS = [
    ("repeated investor-read callout", r"投资人读法", 2),
    ("repeated source-note paragraph", r'class="source-note"', 2),
    ("repeated citation-anchor paragraph", r"引用锚点", 1),
    ("repeated original-document-priority paragraph", r"原件优先级应按3层推进", 1),
    ("repeated ownership/cash boilerplate", r"第一层是能否证明目标公司真实拥有资产、人员和合同", 1),
    ("repeated citation disclaimer", r"这些ID只说明证据来源，不替代原件尽调", 1),
    ("repeated generic milestone diligence", r"还需要单独检查2026年预算、2027年里程碑", 1),
    ("repeated evidence-strength card copy", r"公开来源与公司材料交叉校验", 4),
    ("repeated milestone-pricing card copy", r"不为未验证里程碑一次性定价", 3),
    ("repeated generic market-heat sentence", r"相比只看赛道热度", 2),
    ("repeated generic transaction-structure paragraph", r"交易结构含义也很直接", 2),
    ("repeated generic section implication sentence", r"因此本节的投资含义", 3),
    ("repeated visible mechanism scaffold", r"经济机制：", 4),
    ("repeated visible benchmark scaffold", r"比较与基准：", 4),
    ("repeated visible counter-evidence scaffold", r"反证与风险：", 4),
    ("repeated visible investor-implication scaffold", r"投资含义：", 4),
    ("repeated section-name judgement scaffold", r"判断：[^。]{0,80}要把证据等级、经济机制、替代方案、反证和投资动作放在同一条逻辑链", 1),
    ("repeated generic device-commercialization mechanism", r"里的经济机制要通过注册证、医生采用、患者依从、支付路径、渠道复购和真实回款共同解释", 1),
    ("repeated section-name benchmark scaffold", r"的benchmark：", 1),
    ("repeated section-name original-document priority scaffold", r"原件优先级：", 1),
    ("repeated section-name decision-threshold scaffold", r"决策门槛：", 1),
    ("repeated section-name decision-checklist scaffold", r"决策清单：", 1),
]

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

FINAL_REPORT_FORBIDDEN_PATTERNS = [
    ("meta-writing phrase `不能被写成`", r"不能被写成"),
    ("meta-writing phrase `要把证据等级`", r"要把证据等级"),
    ("meta-writing phrase `而不是把材料拆成孤立事实`", r"而不是把材料拆成孤立事实"),
    ("meta-writing phrase `同时处理证据、反证、机制和投资含义`", r"同时处理证据、反证、机制和投资含义"),
    ("meta-citation phrase `source ID只用于锁定证据来源`", r"source\s*ID只用于锁定证据来源"),
    ("meta-valuation phrase `必须放回.*自身语境判断`", r"必须放回[^。]{0,40}自身语境判断"),
    ("generic 18-24 month evidence fallback", r"关键原件在18-24个月内无法提供"),
    ("generic original-control-before-market phrase", r"先核实目标公司真实控制什么，再讨论行业空间"),
    ("meta-section phrase `本节应支持`", r"本节应支持"),
]


def strip_html(fragment: str) -> str:
    text = TAG_PATTERN.sub(" ", fragment)
    return SPACE_PATTERN.sub(" ", html.unescape(text)).strip()


def count_numbers(text: str) -> int:
    return len(re.findall(r"(?<![A-Za-z])(?:\d+(?:\.\d+)?%?|\d{4}年|\d+(?:\.\d+)?\s*(?:万|亿|百万|千万|billion|million|m|bn|元|美元|个月|年))", text, re.IGNORECASE))


def count_sources(fragment: str, text: str) -> int:
    source_like = 0
    source_like += len(re.findall(r"https?://", fragment))
    source_like += len(re.findall(r"class=\"source-tag\"", fragment))
    source_like += len(re.findall(r"(来源|Source|source|据|披露|公告|年报|招股书|专利|监管|新闻|报告)", text))
    return source_like


def count_source_ids(text: str) -> int:
    return len(set(re.findall(r"\bS\d+\b", text)))


def count_source_tags(fragment: str) -> int:
    return len(re.findall(r'class="[^"]*\bsource-tag\b[^"]*"', fragment))


def count_paragraphs(fragment: str) -> int:
    return len([match.group(0) for match in PARAGRAPH_PATTERN.finditer(fragment) if "source-note" not in match.group(0)])


def missing_analytical_coverage(text: str) -> list[str]:
    lowered = text.lower()
    missing = []
    for group, terms in ANALYTICAL_COVERAGE_TERMS.items():
        if not any(term.lower() in lowered for term in terms):
            missing.append(group)
    return missing


def repeated_sentences(report: str) -> list[tuple[str, int]]:
    normalized_counts: dict[str, int] = {}
    display: dict[str, str] = {}
    for sentence in SENTENCE_PATTERN.findall(strip_html(report)):
        compact = SPACE_PATTERN.sub("", sentence)
        if len(compact) < 28:
            continue
        normalized_counts[compact] = normalized_counts.get(compact, 0) + 1
        display.setdefault(compact, sentence.strip())
    return [(display[key], count) for key, count in normalized_counts.items() if count > 2]


def paragraph_texts(report: str) -> list[str]:
    texts = []
    for match in PARAGRAPH_PATTERN.finditer(report):
        paragraph = match.group(0)
        if "source-note" in paragraph:
            continue
        text = strip_html(paragraph)
        if len(text) >= 80:
            texts.append(text)
    return texts


def normalize_for_similarity(text: str) -> str:
    normalized = SOURCE_ID_PATTERN.sub("S", text)
    for term in SECTION_NAME_TERMS:
        normalized = normalized.replace(term, "本节")
    normalized = re.sub(r"\d+(?:\.\d+)?%?", "N", normalized)
    normalized = re.sub(r"[A-Za-z]+", "E", normalized)
    normalized = re.sub(r"[，。；：、,.!?！？;:（）()《》“”\"'\\s]+", "", normalized)
    return normalized


def near_duplicate_paragraphs(report: str) -> list[tuple[str, int]]:
    paragraphs = paragraph_texts(report)
    normalized = [normalize_for_similarity(text) for text in paragraphs]
    findings: list[tuple[str, int]] = []
    used: set[int] = set()
    for idx, base in enumerate(normalized):
        if idx in used or len(base) < 80:
            continue
        similar = [idx]
        for other_idx in range(idx + 1, len(normalized)):
            other = normalized[other_idx]
            if len(other) < 80:
                continue
            ratio = SequenceMatcher(None, base, other).ratio()
            if ratio >= 0.82:
                similar.append(other_idx)
        if len(similar) >= 3:
            used.update(similar)
            findings.append((paragraphs[idx], len(similar)))
    return findings


def print_failures(failures: list[str], limit: int = 80) -> None:
    print("Depth QA failed:")
    for failure in failures[:limit]:
        print(f"- {failure}")
    remaining = len(failures) - limit
    if remaining > 0:
        print(f"- ... {remaining} additional failures omitted; fix the repeated root cause and rerun QA.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether an investment-analysis report has enough section-level depth.")
    parser.add_argument("html_path", help="Generated HTML report path.")
    parser.add_argument("--min-chars", type=int, default=850, help="Minimum plain-text characters per section.")
    parser.add_argument("--min-numbers", type=int, default=2, help="Minimum numeric facts/proxies per section.")
    parser.add_argument("--min-source-mentions", type=int, default=3, help="Minimum source-like mentions per section.")
    parser.add_argument("--min-source-ids", type=int, default=2, help="Minimum distinct source IDs per section.")
    parser.add_argument("--min-paragraphs", type=int, default=3, help="Minimum analytical paragraphs per section.")
    args = parser.parse_args()

    html_path = Path(args.html_path).expanduser().resolve()
    if not html_path.exists():
        raise SystemExit(f"HTML report not found: {html_path}")

    report = html_path.read_text(encoding="utf-8", errors="replace")
    matches = list(SECTION_PATTERN.finditer(report))
    failures: list[str] = []

    if len(matches) != 14:
        failures.append(f"Expected 14 analysis sections, found {len(matches)}.")

    for label, pattern, max_count in BOILERPLATE_LIMITS:
        count = len(re.findall(pattern, report, flags=re.IGNORECASE))
        if count > max_count:
            failures.append(f"Report has {count} instances of {label}; maximum allowed is {max_count}.")

    for sentence, count in repeated_sentences(report):
        failures.append(f"Repeated long sentence appears {count} times: {sentence[:120]}")

    for paragraph, count in near_duplicate_paragraphs(report):
        failures.append(
            f"Near-duplicate paragraph pattern appears {count} times; rewrite instead of filling sections with a template: "
            f"{paragraph[:140]}"
        )

    for match in matches:
        section_num = match.group("num")
        body = match.group("body")
        text = strip_html(body)
        text_len = len(text)
        numbers = count_numbers(text)
        sources = count_sources(body, text)
        source_ids = count_source_ids(text)
        source_tags = count_source_tags(body)
        paragraphs = count_paragraphs(body)
        missing_groups = missing_analytical_coverage(text)
        shallow_hits = [phrase for phrase in SHALLOW_PHRASES if phrase in text]
        section_boilerplate = [
            phrase
            for phrase in [
                "原件优先级应按3层推进",
                "这些ID只说明证据来源，不替代原件尽调",
                "公开来源与公司材料交叉校验",
                "不为未验证里程碑一次性定价",
            ]
            if phrase in text
        ]
        section_title = SECTION_TITLES.get(section_num, "")

        if section_title and text.count(section_title) > 4:
            failures.append(
                f"Section {section_num}: section title `{section_title}` appears {text.count(section_title)} times in its own body; "
                "this reads like a template/rubric rather than analysis."
            )

        for label, pattern in FINAL_REPORT_FORBIDDEN_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                failures.append(
                    f"Section {section_num}: final report contains {label}; remove internal writing instructions from the delivered analysis."
                )

        if text_len < args.min_chars:
            failures.append(f"Section {section_num}: too short ({text_len} chars, minimum {args.min_chars}).")
        if paragraphs < args.min_paragraphs:
            failures.append(f"Section {section_num}: too few analytical paragraphs ({paragraphs}, minimum {args.min_paragraphs}).")
        if numbers < args.min_numbers:
            failures.append(f"Section {section_num}: too few numeric facts/proxies ({numbers}, minimum {args.min_numbers}).")
        if sources < args.min_source_mentions:
            failures.append(f"Section {section_num}: too few source/evidence mentions ({sources}, minimum {args.min_source_mentions}).")
        if source_ids < args.min_source_ids:
            failures.append(f"Section {section_num}: too few distinct source IDs ({source_ids}, minimum {args.min_source_ids}).")
        if source_tags > 6:
            failures.append(
                f"Section {section_num}: too many inline source tags ({source_tags}, maximum 6). "
                "Use fewer high-signal citations and put full details in the source appendix."
            )
        if missing_groups:
            failures.append(f"Section {section_num}: missing analytical coverage: {', '.join(missing_groups)}.")
        if shallow_hits:
            failures.append(f"Section {section_num}: shallow phrases need evidence-backed rewriting: {', '.join(shallow_hits)}.")
        if section_boilerplate:
            failures.append(
                f"Section {section_num}: template filler detected; rewrite as section-specific analysis: "
                + ", ".join(section_boilerplate)
            )

    if failures:
        print_failures(failures)
        return 1

    print("Depth QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
