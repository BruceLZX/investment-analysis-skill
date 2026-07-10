#!/usr/bin/env python3
"""Harness for investment-analysis report workflows.

This script does not replace the analyst/agent. It creates a disciplined working
structure, generates evidence templates, runs QA gates, and cleans final output.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SECTIONS = [
    ("1", "Company overview / 公司概览"),
    ("2", "Founders and team / 创始人与核心团队"),
    ("3", "Technology and product / 技术与产品"),
    ("4", "Market and industry / 市场与行业"),
    ("5", "Competition / 竞争格局"),
    ("6", "Business model / 商业模式"),
    ("7", "Financials / 财务分析"),
    ("8", "Funding and valuation / 融资与估值"),
    ("9", "Strategy / 发展战略"),
    ("10", "Risk / 风险评估"),
    ("11", "Investment thesis / 投资逻辑"),
    ("12", "Exit strategy / 退出路径"),
    ("13", "ESG and governance / ESG与治理"),
    ("14", "Scoring and recommendation / 综合评分与建议"),
]


PROFILE_REQUIREMENTS = {
    "codex": [
        "Use current-session web/file/tools aggressively for fresh facts; browse whenever a company, market, price, policy, filing, funding, or executive/team fact may have changed.",
        "For each major section, record targeted search strings, opened sources, source IDs, and why the selected sources are decision-grade rather than merely convenient.",
        "Use local scripts for deterministic checks, extraction inventories, citation QA, and final cleanup; do not rely on a one-shot narrative draft.",
        "Do not generate repeated filler paragraphs such as per-section original-document priority, citation-anchor blocks, or repeated metric-card copy; each section must contain content-specific analysis.",
        "Before drafting, write a section distinctness plan: the unique decision question, mechanism, comparison set, counter-evidence, and best visual artifact for each section.",
        "For each section, draft one final-report thesis sentence that directly analyzes the company; never copy internal plan labels or rubric language into the report.",
        "During final rewrite, remove repeated visible scaffolds such as `经济机制`, `比较与基准`, `反证与风险`, and `投资含义`; keep the scaffold internal and write section-specific prose.",
        "Use a verdict strip, compact decision cards, selected tables, and at most a few KPI strips; do not repeat the same card/grid/dashboard pattern in every section.",
        "Before writing the executive briefing, summarize the non-consensus or consensus view and the exact evidence that changes the decision.",
    ],
    "claude-code-claude": [
        "Use Claude's synthesis strength for thesis formation, scenario reasoning, and red-team critique, but do not let fluent prose substitute for source-backed evidence.",
        "After completing the evidence matrix, write a short synthesis memo that connects evidence to thesis, counter-thesis, valuation/terms, and the one diligence question.",
        "Run a dedicated red-team pass before report drafting: identify the most damaging wrong fact, weakest source dependency, and section most likely to be generic.",
        "Rewrite weak sections from new evidence or sharper reasoning; never fix QA failures by lengthening prose alone.",
    ],
    "claude-code-deepseek-ocr": [
        "Treat OCR as a pipeline: inventory files, render scan/slide-heavy materials, OCR into _work/ocr, and preserve page/slide/table references for every extracted claim.",
        "Visually inspect low-confidence pages and any page containing numbers, TAM, valuation, customers, clinical/regulatory claims, policy claims, financing terms, or team credentials.",
        "Mark OCR-derived claims as low confidence until visually checked or externally corroborated; use ranges and wider uncertainty bands for OCR-derived financial inputs.",
        "Build a deck/source claim verification table for material company-provided claims, explicitly marking verified, partially verified, unverified, contradicted, or not publicly disclosed.",
    ],
}


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd)


def resolve_report_paths(output_dir: Path, html_arg: str | None = None, pdf_arg: str | None = None) -> tuple[Path | None, Path | None]:
    html_path = Path(html_arg).expanduser().resolve() if html_arg else next(output_dir.glob("*.html"), None)
    pdf_path = Path(pdf_arg).expanduser().resolve() if pdf_arg else (next(output_dir.glob("*.pdf"), None) if output_dir.exists() else None)
    return html_path, pdf_path


def report_only_qa(output_dir: Path, html_path: Path, pdf_path: Path | None) -> int:
    status = 0
    for cmd in [
        [sys.executable, str(skill_root() / "scripts" / "check_depth.py"), str(html_path)],
        [sys.executable, str(skill_root() / "scripts" / "check_report.py"), str(html_path), str(pdf_path or html_path.with_suffix(".pdf"))],
    ]:
        status = run(cmd) or status
    return status


def write_rewrite_plan(output_dir: Path, html_path: Path | None) -> int:
    if html_path is None:
        return 0
    return run(
        [
            sys.executable,
            str(skill_root() / "scripts" / "diagnose_report.py"),
            "--output",
            str(output_dir),
            "--html",
            str(html_path),
        ]
    )


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def check_template_current() -> int:
    template = skill_root() / "templates" / "report_template.html"
    if not template.exists():
        print(f"Template missing: {template}")
        return 1
    text = template.read_text(encoding="utf-8", errors="replace")
    failures = []
    if 'data-template-version="codex-compact-toc-v3"' not in text:
        failures.append("current template marker missing")
    if 'id="openToc"' in text or 'id="tocBackdrop"' in text or 'id="closeToc"' in text or "setTocOpen(" in text:
        failures.append("old overlay TOC code still present")
    if "<nav class=\"sidebar\"" not in text:
        failures.append("compact navigation markup missing")
    if failures:
        print("Template preflight failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Template preflight passed: {template}")
    return 0


def source_register_template(company: str) -> str:
    return "\n".join(
        [
            "# Source Register",
            "",
            f"Company: {company or 'TODO'}",
            "",
            "Use this as the source-of-truth ledger and citation ledger for the report. Every important claim should trace to a source here or to a user-provided file in `sources/`, and the final HTML should cite the relevant source ID such as [S1].",
            "",
            "| ID | Source title / file | Type | URL or file path | Date / accessed | Claims supported | Claims weakened | Confidence | Citation use | Notes |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "| S1 | | primary / near-primary / independent / company-provided / market data / OCR | | | | | high / medium / low | cite as [S1] with link or file/page | |",
            "",
        ]
    )


def research_plan_template(company: str, scope: str, profile: str) -> str:
    return "\n".join(
        [
            "# Research Plan",
            "",
            f"- Company: {company or 'TODO'}",
            f"- Scope: {scope or 'primary + secondary market investment analysis'}",
            f"- Profile: {profile}",
            "",
            "## Gates",
            "",
            "- [ ] Confirm company identity, legal entity, geography, stage, and business model.",
            "- [ ] Choose 1-3 report spines from `references/report_strategy_playbook.md`.",
            "- [ ] Decide whether `references/geo_market_context_lens.md` is material; if yes, map home market, revenue market, target expansion market, supplier market, comparable-company market, capital market, exit market, and investor perspective before drafting market/GTM/competition/valuation/risk/exit sections.",
            "- [ ] Decide whether `references/policy_geopolitics_lens.md` is material; if yes, map jurisdictions and perspective before applying policy evidence to market, competition, risk, valuation, and exit.",
            "- [ ] Inventory user-provided files and copy originals into `sources/`.",
            "- [ ] Complete `_work/profile_requirements.md` for the selected profile before drafting.",
            "- [ ] Build source register with source type, date, confidence, claim mapping, URL or file/page reference, and visible source IDs.",
            "- [ ] Use source IDs such as [S1] as visible citations in the HTML report, with clickable links for web sources and filename/page or slide references for local files.",
            "- [ ] Complete evidence matrix for all material sections before drafting.",
            "- [ ] Run pre-draft evidence QA and fix failures.",
            "- [ ] Draft report from evidence, not from outline memory.",
            "- [ ] Run red-team pass and rewrite weak sections.",
            "- [ ] Run final QA, generate PDF, clean output, and verify final folder contract.",
            "",
            "## Current Decision Hypothesis",
            "",
            "Write the tentative invest / wait / pass view here after initial research, then update it after evidence and red-team passes.",
            "",
        ]
    )


def profile_requirements_template(profile: str) -> str:
    requirements = PROFILE_REQUIREMENTS[profile]
    chunks = [
        "# Profile Requirements",
        "",
        f"Profile: {profile}",
        "",
        "Complete this file before `gate`. These are profile-specific obligations on top of the shared investment-analysis harness.",
        "",
        "## Required Actions",
        "",
    ]
    for item in requirements:
        chunks.append(f"- [ ] {item}")
    chunks.extend(
        [
            "",
            "## Evidence of Completion",
            "",
            "Briefly record what was done for each required action, with source IDs or local `_work/` paths where relevant.",
            "",
        ]
    )
    return "\n".join(chunks)


def thesis_table_template() -> str:
    return "\n".join(
        [
            "# Thesis Table",
            "",
            "| Thesis component | Current belief | Evidence | Counter-evidence | Confidence | What would change it |",
            "| --- | --- | --- | --- | --- | --- |",
            "| Customer pain | | | | | |",
            "| Product advantage | | | | | |",
            "| Market timing | | | | | |",
            "| GTM scalability | | | | | |",
            "| Unit economics | | | | | |",
            "| Team execution | | | | | |",
            "| Valuation fit | | | | | |",
            "| Exit path | | | | | |",
            "",
        ]
    )


def red_team_template() -> str:
    return "\n".join(
        [
            "# Red-Team Review",
            "",
            "Complete this before final QA. Failed answers must send the analyst back to research or rewriting.",
            "",
            "- [ ] What fact, if wrong, would most damage the thesis?",
            "- [ ] Which positive claims rely only on company-provided materials?",
            "- [ ] Which section is generic or lacks source-backed mechanism?",
            "- [ ] Which risk is mentioned but not priced into the recommendation?",
            "- [ ] What would a skeptical investment committee partner challenge first?",
            "- [ ] Does the conclusion survive downside assumptions: market 50% smaller, CAC 2x higher, revenue 30% lower, financing delayed 6 months?",
            "- [ ] Are all OCR-derived claims visually checked or independently corroborated?",
            "",
        ]
    )


def investor_review_template(company: str) -> str:
    return "\n".join(
        [
            "# Investor Committee Review",
            "",
            f"Company: {company or 'TODO'}",
            "",
            "Complete this review AFTER drafting the report. Read the report as a skeptical investment committee member. Challenge every claim, flag every gap. The analyst must resolve all Critical items before proceeding.",
            "",
            "## Round 1: Completeness Gaps",
            "",
            "### Critical (Must Fix Before Final)",
            "- [ ] ",
            "- [ ] ",
            "",
            "### Important (Should Fix)",
            "- [ ] ",
            "- [ ] ",
            "",
            "### Minor (Nice to Have)",
            "- [ ] ",
            "",
            "## Round 2: Claim Verification Issues",
            "",
            "| Claim (Report Text) | Source Quality | Issue | Action Required |",
            "|---------------------|---------------|-------|-----------------|",
            "| | | | |",
            "",
            "## Round 3: Missing Competitors",
            "",
            "| Competitor | Why Missing | Threat Level | Action |",
            "|-----------|-------------|-------------|--------|",
            "| | | High/Med/Low | |",
            "",
            "## Round 4: Product/Market Fit Questions",
            "",
            "1. ",
            "2. ",
            "",
            "## Round 5: Number Stress-Test",
            "",
            "| Number in Report | Source | If 30% Worse | Still Works? |",
            "|-----------------|--------|-------------|-------------|",
            "| | | | |",
            "",
            "## Overall Assessment",
            "",
            "- Report depth grade: [A/B/C/D/F]",
            "- Top 3 things to fix:",
            "  1.",
            "  2.",
            "  3.",
            "- Ready for investment decision? [Yes/No/With fixes above]",
            "",
        ]
    )


def scenario_analysis_template(company: str) -> str:
    return "\n".join(
        [
            "# Decision Scenarios",
            "",
            f"Company: {company or 'TODO'}",
            "",
            "Use financial scenarios when data supports them. Use milestone scenarios when financial precision would be fake.",
            "",
            "| Scenario | Probability | Specific driver | Evidence | Financial / milestone outcome | Investor implication |",
            "| --- | --- | --- | --- | --- | --- |",
            "| Bull | | | | | |",
            "| Base | | | | | |",
            "| Bear | | | | | |",
            "",
            "## Key Assumption Sensitivity",
            "",
            "| Rank | Assumption | Confidence | What would disprove it | Impact if wrong | Early warning |",
            "| --- | --- | --- | --- | --- | --- |",
            "| 1 | | | | | |",
            "| 2 | | | | | |",
            "| 3 | | | | | |",
            "",
            "## Optional Decision Modules",
            "",
            "- Historical analogs: use only when the analogy is close enough to teach a decision rule.",
            "- Capital efficiency: use when funding, revenue, burn, or headcount data exists.",
            "- Position sizing: use for public equities, liquid secondaries, or when the user asks for portfolio allocation. For primary deals, discuss check size, valuation discipline, and follow-on reserve.",
            "- Industry KPI dashboard: use the company-type KPI set only when the metrics can be sourced or responsibly proxied.",
            "",
            "## Consensus / Non-Consensus View",
            "",
            "- Market or investor consensus:",
            "- Our view:",
            "- Evidence for the difference, or why no differentiated edge exists:",
            "- What event would prove or disprove this view:",
            "",
            "## The One Question",
            "",
            "> [The question]",
            "",
            "Why the answer would change the decision:",
            "",
        ]
    )


def copy_sources(output_dir: Path, sources: list[str]) -> None:
    sources_dir = output_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    for item in sources:
        src = Path(item).expanduser().resolve()
        if not src.exists():
            raise SystemExit(f"Source not found: {src}")
        dest = sources_dir / src.name
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)


def evidence_template(company: str, scope: str, profile: str = "codex") -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chunks = [
        "# Evidence Matrix",
        "",
        f"- Company: {company or 'TODO'}",
        f"- Profile: {profile}",
        f"- Scope: {scope or 'primary + secondary market investment analysis'}",
        f"- Created: {now}",
        "",
        "Complete this before drafting the final report. Do not leave a section without search work, source IDs, independent sources, mechanism, comparison, counter-evidence, and investor implication. A shallow or generic evidence row should fail the gate.",
        "",
    ]
    for num, title in SECTIONS:
        chunks.extend(
            [
                f"## Section {num}: {title}",
                "",
                "### Search Queries",
                "",
                "- ",
                "- ",
                "- ",
                "- ",
                "",
                "### Deep Evidence Table",
                "",
                "| Source IDs | Source type | Finding / fact | Mechanism | Benchmark / peer context | Weakens / contradicts | Investor implication | Confidence | Follow-up |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                "| | | | | | | | | |",
                "",
                "### Section Gate",
                "",
                "- [ ] 2+ independent sources opened",
                "- [ ] 1+ primary or near-primary source checked where available",
                "- [ ] 2+ numeric facts/proxies or explicit missing-data note",
                "- [ ] source IDs mapped to source register",
                "- [ ] mechanism/economic logic explained from evidence",
                "- [ ] 1+ competitor/benchmark/base-rate comparison",
                "- [ ] 1+ counter-evidence or failure mode",
                "- [ ] investor implication stated",
                "- [ ] 2-5 diligence questions listed",
                "",
                "### Internal Section Plan (do not copy into final report)",
                "",
                "- Decision question: ",
                "- Final-report thesis sentence: ",
                "- Why this section is different from the other sections: ",
                "- Evidence mechanism to explain: ",
                "- Comparison set / base rate: ",
                "- Counter-evidence or failure mode to price: ",
                "- Best visual artifact, if any: ",
                "- Words/patterns prohibited in final report: ",
                "",
            ]
        )
    return "\n".join(chunks)


def init(args: argparse.Namespace) -> int:
    template_status = check_template_current()
    if template_status != 0:
        return template_status
    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "_work").mkdir(exist_ok=True)
    (output_dir / "sources").mkdir(exist_ok=True)
    if args.sources:
        copy_sources(output_dir, args.sources)
    write_if_missing(output_dir / "_work" / "evidence_matrix.md", evidence_template(args.company, args.scope, args.profile))
    write_if_missing(output_dir / "_work" / "source_register.md", source_register_template(args.company))
    write_if_missing(output_dir / "_work" / "research_plan.md", research_plan_template(args.company, args.scope, args.profile))
    write_if_missing(output_dir / "_work" / "profile_requirements.md", profile_requirements_template(args.profile))
    write_if_missing(output_dir / "_work" / "thesis_table.md", thesis_table_template())
    write_if_missing(output_dir / "_work" / "scenario_analysis.md", scenario_analysis_template(args.company))
    write_if_missing(output_dir / "_work" / "red_team_review.md", red_team_template())
    write_if_missing(output_dir / "_work" / "investor_review.md", investor_review_template(args.company))
    write_if_missing(
        output_dir / "_work" / "iteration_log.md",
        "# Iteration Log\n\nRecord each QA failure, additional search pass, rewrite, and final resolution here. Delete `_work/` before delivery.\n",
    )
    print(f"Harness initialized: {output_dir}")
    print(f"Evidence matrix: {output_dir / '_work' / 'evidence_matrix.md'}")
    return 0


def preflight(args: argparse.Namespace) -> int:
    return check_template_current()


def evidence(args: argparse.Namespace) -> int:
    output_dir = Path(args.output).expanduser().resolve()
    matrix = output_dir / "_work" / "evidence_matrix.md"
    if not matrix.exists():
        write_if_missing(matrix, evidence_template(args.company or "", args.scope or "", args.profile))
    print(matrix)
    return 0


def check_evidence(args: argparse.Namespace) -> int:
    script = skill_root() / "scripts" / "check_evidence.py"
    return run([sys.executable, str(script), str(Path(args.output).expanduser().resolve() / "_work" / "evidence_matrix.md")])


def gate(args: argparse.Namespace) -> int:
    output_dir = Path(args.output).expanduser().resolve()
    required = [
        output_dir / "_work" / "research_plan.md",
        output_dir / "_work" / "profile_requirements.md",
        output_dir / "_work" / "source_register.md",
        output_dir / "_work" / "thesis_table.md",
        output_dir / "_work" / "evidence_matrix.md",
        output_dir / "_work" / "scenario_analysis.md",
        output_dir / "_work" / "investor_review.md",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        for path in missing:
            print(f"Missing workflow file: {path}")
        return 1
    status = 0
    status = run([sys.executable, str(skill_root() / "scripts" / "check_workflow_docs.py"), str(output_dir)]) or status
    status = run([sys.executable, str(skill_root() / "scripts" / "check_source_register.py"), str(output_dir / "_work" / "source_register.md")]) or status
    status = check_evidence(args) or status
    return status


def qa(args: argparse.Namespace) -> int:
    output_dir = Path(args.output).expanduser().resolve()
    html_path, pdf_path = resolve_report_paths(output_dir, args.html, args.pdf)
    if html_path is None:
        raise SystemExit("No HTML report found. Pass --html or place the report in the output directory.")
    gate_status = gate(args)
    if gate_status != 0:
        print("QA stopped: workflow/evidence gate failed. Fix _work files and evidence before report QA.")
        return gate_status
    status = run([sys.executable, str(skill_root() / "scripts" / "check_citations.py"), "--output", str(output_dir), "--html", str(html_path)])
    status = report_only_qa(output_dir, html_path, pdf_path) or status
    return status


def loop(args: argparse.Namespace) -> int:
    output_dir = Path(args.output).expanduser().resolve()
    if not (output_dir / "_work").is_dir():
        print(f"QA loop cannot run after cleanup or without harness init: {output_dir / '_work'}")
        print("Run `run_analysis_harness.py init` and complete workflow files before drafting, or do not claim loop QA passed.")
        return 1
    log = output_dir / "_work" / "iteration_log.md"
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = qa(args)
    with log.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## QA loop {started}\n\n")
        if result == 0:
            handle.write("- Result: PASS. Proceed to PDF/render QA and final cleanup.\n")
        else:
            handle.write("- Result: FAIL. Return to evidence search, section rewrite, or report QA based on failed checks.\n")
            handle.write("- Do not solve failures by adding generic wording without new evidence.\n")
            handle.write("- See `_work/rewrite_plan.md` for required rewrite actions when generated.\n")
    if result != 0:
        html_path = Path(args.html).expanduser().resolve() if args.html else next(output_dir.glob("*.html"), None)
        write_rewrite_plan(output_dir, html_path)
    return result


def clean(args: argparse.Namespace) -> int:
    output_dir = Path(args.output).expanduser().resolve()
    html_path, pdf_path = resolve_report_paths(output_dir)
    if html_path is not None:
        report_status = report_only_qa(output_dir, html_path, pdf_path)
        if report_status != 0:
            write_rewrite_plan(output_dir, html_path)
            print("Clean blocked: report QA failed. Fix the report before deleting `_work/` and finalizing output.")
            return report_status
    return run([sys.executable, str(skill_root() / "scripts" / "clean_output.py"), str(output_dir)])


def final_check(args: argparse.Namespace) -> int:
    output_dir = Path(args.output).expanduser().resolve()
    html_path, pdf_path = resolve_report_paths(output_dir, args.html, args.pdf)
    if html_path is None:
        raise SystemExit("No HTML report found. Pass --html or place the report in the output directory.")
    report_status = report_only_qa(output_dir, html_path, pdf_path)
    if report_status != 0:
        write_rewrite_plan(output_dir, html_path)
        print("Final report QA failed before cleanup. Keep `_work/` if present and fix the report before final cleaning.")
        return report_status

    clean_status = run([sys.executable, str(skill_root() / "scripts" / "clean_output.py"), str(output_dir)])
    if clean_status == 0:
        print("Final report QA passed: report depth, report layout/content QA, and final folder cleanliness all passed.")
    else:
        print("Final report QA failed. Do not deliver this report.")
    return clean_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Investment analysis harness.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_preflight = sub.add_parser("preflight", help="Check skill template/version readiness before starting a report.")
    p_preflight.set_defaults(func=preflight)

    p_init = sub.add_parser("init", help="Create output folder, sources/, _work/, and evidence matrix.")
    p_init.add_argument("--output", required=True)
    p_init.add_argument("--company", default="")
    p_init.add_argument("--scope", default="primary + secondary market investment analysis")
    p_init.add_argument("--profile", choices=["codex", "claude-code-claude", "claude-code-deepseek-ocr"], default="codex")
    p_init.add_argument("--sources", nargs="*", default=[])
    p_init.set_defaults(func=init)

    p_evidence = sub.add_parser("evidence", help="Create or print the evidence matrix path.")
    p_evidence.add_argument("--output", required=True)
    p_evidence.add_argument("--company", default="")
    p_evidence.add_argument("--scope", default="")
    p_evidence.add_argument("--profile", choices=["codex", "claude-code-claude", "claude-code-deepseek-ocr"], default="codex")
    p_evidence.set_defaults(func=evidence)

    p_check = sub.add_parser("check-evidence", help="Validate evidence matrix completeness.")
    p_check.add_argument("--output", required=True)
    p_check.set_defaults(func=check_evidence)

    p_gate = sub.add_parser("gate", help="Run the pre-draft workflow gate.")
    p_gate.add_argument("--output", required=True)
    p_gate.set_defaults(func=gate)

    p_qa = sub.add_parser("qa", help="Run evidence, depth, and report QA.")
    p_qa.add_argument("--output", required=True)
    p_qa.add_argument("--html")
    p_qa.add_argument("--pdf")
    p_qa.set_defaults(func=qa)

    p_loop = sub.add_parser("loop", help="Run QA loop and append iteration log.")
    p_loop.add_argument("--output", required=True)
    p_loop.add_argument("--html")
    p_loop.add_argument("--pdf")
    p_loop.set_defaults(func=loop)

    p_clean = sub.add_parser("clean", help="Clean final output directory.")
    p_clean.add_argument("--output", required=True)
    p_clean.set_defaults(func=clean)

    p_final = sub.add_parser("final-check", help="Run report-only QA and final folder cleanliness after cleanup.")
    p_final.add_argument("--output", required=True)
    p_final.add_argument("--html")
    p_final.add_argument("--pdf")
    p_final.set_defaults(func=final_check)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
