<p align="center">
  <img src="https://img.shields.io/badge/version-v2.0-0f766e?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Cursor-202124?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-15803d?style=for-the-badge" alt="License">
</p>

<h1 align="center">Investment Analysis Skill</h1>
<p align="center">
  <b>AI-Powered Investment Research Engine</b><br>
  Generate decision-grade investment reports for primary & secondary markets<br>
  <sub>14-Dimension Framework · Harness-Driven QA · Dual-Format Output (HTML+PDF)</sub>
</p>

---

## What is this?

A professional-grade AI skill that turns a company name, ticker, or pitch deck into a **comprehensive, evidence-backed investment research report**. Designed for venture capital, private equity, and public market investors who demand depth, rigor, and auditability.

Think of it as having a top-tier investment analyst who works at machine speed — reading your source files, searching the web across 5 dimensions in both Chinese and English, cross-verifying claims against primary sources, and producing a beautifully formatted HTML+PDF report that can go straight to your investment committee.


## Quick Start

### Claude Code

```bash
# Install the skill
cp -r investment-analysis ~/.claude/skills/

# Use it
/投资分析 大疆无人机
# or
分析一下这家公司的路演材料 [drag & drop PDF/PPT]
```

### Codex / Cursor

Copy `versions/codex/CODEX.md` into `.cursor/rules/`, then:

```
@investment-analysis Analyze [Company Name]
```

### Any AI Tool

Copy `prompt_universal.md` as the system prompt, then send your company name or files.

## What You Get

```
[CompanyName]_[BusinessSummary]/
├── sources/                         # Original source files
├── [CompanyName]_投资分析报告.html   # Interactive HTML (~50-130KB)
└── [CompanyName]_投资分析报告.pdf    # Print-ready PDF (~400-800KB)
```

### Report Coverage (14 Dimensions)


### Investor-Grade Depth

Every section must satisfy a **Mandatory Evidence Gate**: 3-6 targeted searches, ≥2 independent sources, ≥1 primary/source-of-truth check, ≥2 quantified facts/proxies, ≥1 benchmark comparison, ≥1 counter-evidence, investor implication, and 2-5 diligence questions.

## Architecture

```
investment-analysis/
├── SKILL.md                          # Skill entry point & workflow
├── agents/openai.yaml                # Codex agent interface
├── references/                       # Analyst playbooks
│   ├── report_strategy_playbook.md   # 15+ report spines (public equity, deep tech, biotech...)
│   ├── analysis_core.md              # Evidence gate, writing contract, red-team standard
│   ├── decision_framework.md         # Scenario analysis, non-consensus insight, position sizing
│   ├── section_deepening.md          # Section-specific research prompts
│   ├── geo_market_context_lens.md    # Geographic market system analysis
│   ├── policy_geopolitics_lens.md    # Policy/regulatory/geopolitical analysis
│   └── public_equity_financials_lens.md  # Financial statement & valuation framework
├── scripts/                          # Python harness & QA tools
│   ├── run_analysis_harness.py       # Central orchestrator (init/gate/loop/clean)
│   ├── check_evidence.py             # Evidence matrix validator
│   ├── check_depth.py                # Section depth QA (anti-shallow)
│   ├── check_report.py               # Report completeness QA
│   ├── check_citations.py            # Citation & source reliability check
│   ├── check_source_register.py      # Source ledger validator
│   ├── check_workflow_docs.py        # Workflow documentation gate
│   ├── clean_output.py               # Final output contract enforcer
│   ├── generate_pdf.py               # HTML→PDF (WeasyPrint)
│   ├── inventory_sources.py          # Source file inventory & SHA-256
│   └── diagnose_report.py            # Report diagnostic tool
├── templates/
│   └── report_template.html          # Professional report template with sidebar, search, print
└── versions/                         # Platform-specific profiles
    ├── claude-code-claude/CLAUDE.md
    ├── claude-code-deepseek-ocr/CLAUDE.md
    └── codex/CODEX.md
```

## Analysis Spines

The skill adapts its analytical lens to the company type:


## The Harness Loop

The skill is not a one-shot prompt — it's a **disciplined workflow with automated quality gates**:

```bash
# 1. Initialize workspace
python scripts/run_analysis_harness.py init \
  --output "CompanyName_BusinessSummary" \
  --company "CompanyName" \
  --sources pitch_deck.pdf cap_table.xlsx

# 2. Pre-draft gate (must pass before writing)
python scripts/run_analysis_harness.py gate --output "output folder"

# 3. Write the HTML report using templates/report_template.html

# 4. QA loop (evidence + depth + report integrity)
python scripts/run_analysis_harness.py loop \
  --output "output folder" --html "report.html" --pdf "report.pdf"

# 5. Clean & deliver
python scripts/run_analysis_harness.py clean --output "output folder"
```

## Key Design Principles

### 1. Evidence Over Opinion
Every claim must trace to a source. The source register maps `[S1]...[SN]` to URLs, file pages, source types, and confidence levels. No fact floats without attribution.

### 2. Counter-Evidence is Mandatory
Every section must include at least one weakening or contradicting source. The red-team pass asks: *"What fact, if wrong, would most damage the thesis?"*

### 3. No False Precision
If revenue data is unavailable, state "未公开" (not publicly disclosed). If a metric would create false precision, explain why it's omitted and what data would be needed. Do not invent numbers.

### 4. Decision-Grade, Not Encyclopedia
The report should answer: *"What should an investor do now?"* — not just describe what the company does. Every paragraph should earn its place by advancing the investment decision.

### 5. Multi-Platform, One Standard
Whether running on Claude Code, Codex, or Cursor, the same 14-dimension framework and evidence gate applies. Platform-specific profiles handle tool availability and model characteristics.


## Requirements

- **Python 3.10+** for harness scripts
- **WeasyPrint** (`pip install weasyprint`) for PDF generation
- **Claude Code / Codex / Cursor** as the AI runtime

```bash
# macOS
pip install weasyprint
brew install pango

# Ubuntu/Debian
pip install weasyprint
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0
```

## Contributing

The skill is designed to be extended:

- **Add a new analysis spine**: Edit `references/report_strategy_playbook.md`
- **Add a new QA check**: Add a script in `scripts/` and wire it into `run_analysis_harness.py`
- **Add a new lens**: Create a new reference file and reference it from `SKILL.md`
- **Support a new platform**: Add a version profile in `versions/`

## Disclaimer

This skill generates investment analysis reports based on publicly available information. Reports are for research reference only and do not constitute investment advice. Investment decisions should combine professional judgment and consultation with licensed advisors.

---

<p align="center">
  <sub>Built for investors who demand depth · <a href="https://github.com/BruceLZX/investment-analysis-skill">GitHub</a></sub>
</p>
