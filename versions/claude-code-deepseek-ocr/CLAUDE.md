# Investment Analysis - Claude Code / DeepSeek + OCR Version

Use this profile when running the investment-analysis workflow inside Claude Code with DeepSeek as the reasoning model and OCR-heavy source materials.

## Mission

Generate a decision-grade investment report from company names and/or source files, especially PDFs, scans, screenshots, image-heavy pitch decks, and low-quality OCR materials. The final report must be useful for primary-market and secondary-market investment decisions.

## Required Workflow

Run the shared harness from the skill root:

```bash
python scripts/run_analysis_harness.py init --profile claude-code-deepseek-ocr --output "[CompanyName]_[BusinessSummary]" --company "[CompanyName]" --sources [source files...]
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

## DeepSeek + OCR Operating Notes

- Treat OCR as a first-class pipeline, not a side task.
- `init --profile claude-code-deepseek-ocr` generates `_work/profile_requirements.md`; complete it before drafting. This profile is optimized for scanned/source-heavy deals where extraction reliability is the main risk.
- Render image-only or slide-heavy PDFs to `_work/rendered/`; OCR into `_work/ocr/`; visually inspect low-confidence pages.
- Preserve page/slide numbers for every extracted claim.
- Never quote OCR text as fact until it has been visually checked or corroborated.
- Treat `_work/source_register.md` as the citation ledger. Use visible source IDs such as `[S1]` in the HTML, link web sources, and cite OCR/user files with filename plus page/slide/table.
- For numerical claims from OCR, double-check digits, units, dates, decimal points, and table headers.
- For Chinese scanned documents, watch for OCR confusion between similar characters and numbers.
- DeepSeek may be strong at broad reasoning but can over-compress evidence; enforce the evidence matrix before writing.
- Treat `_work/evidence_matrix.md` as a hard pre-draft gate. Every material section must have source IDs, mechanism, benchmark/peer context, counter-evidence, investor implication, confidence, and follow-up before drafting.
- Do not let OCR dumps leak into final output. Final output must contain only `sources/`, HTML report, and PDF report.

## Source Handling Rules

- For text PDFs: extract text and tables, then spot-check against rendered pages.
- For scanned PDFs: render all pages, OCR all pages, then visually inspect pages containing market size, valuation, revenue, customers, clinical data, regulatory claims, or financing terms.
- For pitch decks: extract slide text and inspect slide images; many important claims are visual-only. Pay special attention to claims about TAM, unit economics, competitive positioning, and team backgrounds — these are most frequently overstated.
- For policy-sensitive pitch decks, verify policy claims against primary policy sources in the relevant jurisdictions; do not accept vague phrases like "政策支持", "国产替代", "national strategy", "EU compliant", or "US approved" without matching them to a specific policy, budget, procurement path, standard, license, approval, or export-control constraint.
- For charts: capture axis labels, units, dates, legends, sample sizes, and whether the chart is cumulative or period-specific. Watch for truncated y-axes, cherry-picked time periods, and cumulative-vs-periodic ambiguity.
- For tables: verify row/column alignment after OCR before using any number. Cross-check totals against components when both are shown.
- For every company, apply the forensic depth standard from `references/company_deep_dive_playbook.md`. When source files are OCR-dependent, mark extracted numbers and claims as lower confidence and widen uncertainty bands.
- After drafting, apply `references/investor_reviewer_lens.md` as a simulated investment committee reviewer. OCR-derived claims should receive extra scrutiny in the claim verification round.

## Report Expectations

- Start with a 5-minute executive briefing covering verdict, score, consensus/non-consensus view, and the one question.
- Explain industry context before company judgement when the reader may be unfamiliar with the sector.
- Every major conclusion must cite source type, page/slide when applicable, and confidence.
- Mark OCR-derived evidence as lower confidence unless independently verified.
- Cite material claims, numbers, comparisons, policy claims, financial statement claims, valuation inputs, and team-background claims with source IDs. Mark unverified OCR or company-only claims explicitly.
- If a section reads generic, return to source inspection, OCR verification, and external search. Do not solve depth failures by adding longer prose without new sources, mechanisms, or comparisons.
- If the OCR quality is poor, state the limitation and list the affected claims.
- Include scenario analysis. When financial data comes from OCR, use ranges and wider uncertainty bands rather than point estimates.
- Include a key assumption sensitivity table; mark OCR-derived assumptions as lower confidence unless visually checked or corroborated.
- Include historical analogs, capital efficiency, and position/deal sizing only when evidence-backed and decision-relevant.
- Include geographic market context when material; verify OCR-derived claims about global TAM, overseas expansion, international customers, supply chain, or foreign competitors.
- Include policy/geopolitics only when material; OCR-derived policy claims must be visually checked or corroborated, and should be interpreted from the correct domestic or international viewpoint.
- End with the three things the reader should remember.
- For pitch deck analysis: explicitly flag claims that appear only in the deck without independent corroboration. Build a "deck claim verification table" mapping each material deck claim to external evidence or its absence.

## DeepSeek + OCR Profile Specialization

Use this version when source quality is the bottleneck: scans, screenshots, image-heavy decks, low-quality PDFs, or mixed Chinese/English OCR.

- Build `_work/source_inventory.md` and record which files/pages require OCR, table extraction, or visual inspection.
- Keep `_work/rendered/` and `_work/ocr/` internal only; cite final claims through source IDs plus filename/page/slide/table.
- Add a claim verification table for pitch decks and data rooms: claim, source page/slide, OCR confidence, external corroboration, status, and investment implication.
- Widen uncertainty bands when figures come from OCR or tables with ambiguous headers, units, periods, or chart axes.
