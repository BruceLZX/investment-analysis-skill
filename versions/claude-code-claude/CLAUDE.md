# Investment Analysis - Claude Code / Claude Version

Use this profile when running the investment-analysis workflow inside Claude Code with Claude as the reasoning model.

## Mission

Generate a decision-grade investment report for primary-market or secondary-market use. The report must teach a non-specialist reader enough about the company, industry, risks, and valuation to make a professional investment decision.

## Required Workflow

Run the shared harness from the skill root:

```bash
python scripts/run_analysis_harness.py init --profile claude-code-claude --output "[CompanyName]_[BusinessSummary]" --company "[CompanyName]" --sources [source files...]
python scripts/run_analysis_harness.py gate --output "[output folder]"
python scripts/generate_pdf.py "[report.html]" "[report.pdf]"
python scripts/run_analysis_harness.py loop --output "[output folder]" --html "[report.html]" --pdf "[report.pdf]"
python scripts/run_analysis_harness.py clean --output "[output folder]"
```

Read before drafting:

- `references/report_strategy_playbook.md`
- `references/analysis_core.md`
- `references/decision_framework.md`

Read `references/section_deepening.md` only for sections that need planning or rewriting. Read `references/geo_market_context_lens.md` when geography, customer markets, suppliers, channels, foreign comparables, capital markets, or exit paths may affect the thesis. Read `references/policy_geopolitics_lens.md` when national strategy, regulation, government procurement, export controls, sanctions, data security, or cross-border supply chains may affect the thesis.

## Claude-Specific Operating Notes

- Use Claude's strength in synthesis, long-form reasoning, and red-team critique. Use it to test consensus/non-consensus views and scenario logic, but do not invent precision that the evidence cannot support.
- `init --profile claude-code-claude` generates `_work/profile_requirements.md`; complete it before drafting. This profile is optimized for thesis synthesis, red-team critique, and investment committee readability after the evidence gate is complete.
- Do not skip the evidence matrix. Claude may write fluent but shallow prose if the evidence gate is incomplete.
- Use the harness loop as a hard stop: failed `gate`, `check_workflow_docs`, `check_citations`, `check_depth`, `check_report`, or final clean check means return to research and rewrite.
- Treat `_work/evidence_matrix.md` as a hard pre-draft gate. Every material section must have source IDs, mechanism, benchmark/peer context, counter-evidence, investor implication, confidence, and follow-up before drafting.
- Use web search, local source extraction, filings, company materials, investor announcements, regulatory databases, patents, and industry reports as evidence.
- Treat `_work/source_register.md` as the citation ledger. Use visible source IDs such as `[S1]` in the HTML, link web sources, and cite local files with filename plus page/slide/table where possible.
- For policy-sensitive sectors, use primary policy sources where possible: laws, official plans, procurement notices, standards bodies, export-control lists, sanctions lists, regulatory approvals, official budgets, and filings. Separate home-market, revenue-market, supplier-market, listing-market, and acquirer-market rules.
- Before drafting, read `references/company_deep_dive_playbook.md` for the mandatory forensic depth standard across all seven deep-dive areas.
- After drafting, use `references/investor_reviewer_lens.md` as a simulated investment committee reviewer. Challenge every claim, flag every gap. All Critical items must be resolved before the report can proceed.
- Keep the research plan, source register, evidence matrix, thesis table, scenario analysis, red-team review, investor review, interim notes, rendered pages, OCR text, and search logs in `_work/`.
- Final output must contain only `sources/`, HTML report, and PDF report.

## Claude Profile Specialization

Use this version when Claude Code is the execution surface and Claude is the reasoning model. The profile should bias toward synthesis quality after evidence collection:

- Write a short synthesis memo in `_work/profile_requirements.md` connecting evidence, counter-evidence, valuation/terms, scenarios, and the one diligence question.
- Use red-team critique as a real pass, not a decorative section. Identify the weakest section, the most dangerous single wrong fact, and the claim most dependent on company-provided material.
- Preserve narrative quality, but every strong paragraph must trace back to the source register and evidence matrix.
- When evidence is weak, the correct output is a calibrated low-confidence conclusion, not a more fluent positive thesis.

## Report Expectations

- Start with a 5-minute executive briefing that includes verdict, score, consensus/non-consensus view, and the one question.
- Explain industry context before company judgement when the reader may be unfamiliar with the sector.
- For every major section, cover judgement, evidence, mechanism, benchmark/comparison, counter-evidence, investor implication, confidence, and diligence questions as the internal analytical scaffold, but do not force the same visible subheadings into every section.
- If a section reads generic, return to search and evidence gathering. Do not solve depth failures by adding longer prose without new sources, mechanisms, or comparisons.
- Use narrative paragraphs, content-specific micro-headings, compact tables, KPI strips, timelines, risk matrices, and selective callouts so the report is readable without becoming a wall of text.
- Include scenario analysis (bull/base/bear) with explicit drivers. Use financial scenarios only when data supports them; otherwise use milestone scenarios.
- Include a key assumption sensitivity table identifying the 3-5 assumptions that most affect the investment outcome.
- Include historical analogs, capital efficiency, and position/deal sizing only when evidence-backed and decision-relevant.
- Include geographic market context when material, and connect it to demand, GTM, pricing, supply chain, competition, valuation, risk, and exit.
- Include policy/geopolitics only when material, and connect it to market size, competition, risk, valuation, or exit from the relevant domestic or international investor viewpoint.
- Cite material claims, numbers, comparisons, policy claims, financial statement claims, valuation inputs, and team-background claims with source IDs. Mark company-only or unverified claims explicitly.
- For primary-market analysis, emphasize team, product proof, customer validation, terms, next-round milestones, dilution, and founder reference checks.
- For secondary-market analysis, emphasize revenue quality, margin, cash flow, valuation, catalysts, downside case, consensus mismatch, and short interest.
- End with the three things the reader should remember.
