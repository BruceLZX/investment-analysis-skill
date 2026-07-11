---
name: investment-analysis
description: "Harness-driven company and industry investment research for primary-market and secondary-market decisions. Use when the user asks for company analysis, investment due diligence, pitch deck review, industry research, valuation work, competitor analysis, policy/regulatory/geopolitical analysis, public-equity research, stock/financial-statement analysis, balance-sheet health, VC/PE diligence, or a professional HTML/PDF investment report from a company name, ticker, or source files such as PDF, PPT, DOC, spreadsheets, screenshots, or scanned materials."
---

# Investment Analysis

Produce a decision-grade investment report that can teach a reader enough about the company and industry to make a professional investment decision. Use the harness and QA loop; do not rely on a one-shot report draft.

Default output language: match the user's language. For Chinese requests, write the report in Chinese while preserving official English names.

## Required Workflow

1. Read `references/report_strategy_playbook.md` to choose the report spine. Use the closest investment context rather than forcing every company into the same outline.
2. Read `references/analysis_core.md` for the evidence gate, section writing contract, thesis workflow, and red-team standard.
3. Read `references/decision_framework.md` before drafting the executive briefing, investment thesis, recommendation, scoring, or final decision. Use `references/section_deepening.md` only when planning section-level research or rewriting weak sections; load only the relevant headings when possible.
4. Read `references/geo_market_context_lens.md` when geography, jurisdiction, customer markets, suppliers, channels, localization, foreign comparables, capital markets, or exit paths can affect TAM, GTM, competition, pricing, risk, valuation, or strategy.
5. Read `references/policy_geopolitics_lens.md` when policy, national strategy, international exposure, regulation, government procurement, export controls, sanctions, data security, or cross-border supply chain can affect the thesis. Choose the relevant jurisdictions and investor perspective first; do not apply one country's policy lens to all companies.
6. Read `references/public_equity_financials_lens.md` when the company is listed, has a ticker/security code, is a liquid secondary-market target, or the user asks whether a stock is worth buying. This lens is mandatory for public equities and must be integrated into valuation, recommendation, risk, and position sizing.
7. Read `references/regulatory_database_lens.md` for every company. This lens maps each industry to its authoritative government registries (NMPA/CDE for biotech, SASAC for SOEs, MIIT/CNIPA for semiconductors, CAC for AI, CAAC for aerospace, PBOC/NFRA for fintech, and gsxt.gov.cn + wenshu.court.gov.cn as universal baselines). Search public regulatory databases for licenses, approvals, clinical trial status, patent legal status, procurement awards, and compliance records. When a database requires login or is restricted, do NOT silently skip it — emit a User Data Request telling the user exactly what to fetch, from which database, why it matters to the investment decision, and how to obtain it.
8. Read `references/company_deep_dive_playbook.md` for **every** company. This is the mandatory forensic depth standard. Every report must include: (a) legal entity map with exact ownership percentages, (b) complete timeline with specific dates (not "recently"), (c) equity cap table with share classes and voting rights, (d) per-person founder/executive CVs with education, career chronology, patents, and prior exits, (e) patent portfolio table with numbers/dates/jurisdictions, (f) per-product forensic detail (for medical: indication, current standard of care, competitor products, clinical data; for SaaS: workflow, competitor tools, unit economics), (g) domestic vs. international market bifurcation by region (US/EU/China/Japan/SEA), (h) complete competitor landscape with all material players and product comparison. When data is unavailable, state what is missing, how material it is, and what source would be needed.
9. Run template preflight, then initialize the harness:

   ```bash
   python scripts/run_analysis_harness.py preflight
   python scripts/run_analysis_harness.py init --output "[CompanyName]_[BusinessSummary]" --company "[CompanyName]" --sources [source files...]
   ```

9. Put all extraction notes, OCR text, rendered pages, screenshots, search notes, and scratch work under `_work/`. Never place intermediate files in the final output root.
10. Use _work/research_plan.md`, `_work/source_register.md`, `_work/thesis_table.md`, `_work/scenario_analysis.md`, and `_work/red_team_review.md` as internal workflow files. Keep them current; they are deleted before delivery.
11. Use _work/profile_requirements.md` to enforce the selected profile. The shared skill has three managed profiles: `codex`, `claude-code-claude`, and `claude-code-deepseek-ocr`. Do not collapse them into one generic workflow; complete the profile-specific checklist before drafting.
12. Extract and inspect user-provided materials. Copy originals into `sources/`.
13. For public equities, capture the ticker/security code, exchange, currency, latest available share price, market cap, enterprise value if available, trading date/time, latest annual report, latest interim/quarterly report, and any post-period guidance or profit warning before drafting. Perform professional financial statement analysis across income statement, balance sheet, cash flow statement, and notes. If any item cannot be sourced, state that explicitly and do not substitute unsourced estimates.
14. Build `_work/source_register.md` and `_work/evidence_matrix.md` before drafting. The source register must map sources to source IDs, links or file/page references, claims, confidence, and source type. The evidence matrix must cover every material section with searches, source IDs, independent sources, a primary/source-of-truth check where available, finding/fact, mechanism, quantification/proxies, benchmark or peer context, counter-evidence, investor implication, confidence, and follow-up diligence questions. For public equities, include dedicated evidence rows for market data, income statement, cash flow, balance sheet/debt, valuation, consensus/guidance, and capital allocation.
15. Preserve source auditability in the final report. Add a visible `数据来源与引用 / Source Appendix` module with clickable links or local source paths, source type, confidence, and the claims each source supports. Inline source tags are allowed for important claims, but source tags alone are insufficient.
16. Run the pre-draft gate before writing:

   ```bash
   python scripts/run_analysis_harness.py gate --output "[output folder]"
   ```

17. Draft the HTML report using the current `templates/report_template.html` only. The generated HTML must retain `data-template-version="codex-compact-toc-v3"` and must not contain old overlay TOC ids such as `openToc`, `tocBackdrop`, or `closeToc`. The report may reorder or merge the 14 coverage areas when the company requires a different narrative, but it must still cover all material areas.

**Minimum content depth (enforced by check_depth.py):** 2,500+ plain-text characters per section (≈5-7 substantial analytical paragraphs), 8+ numeric facts/proxies, 6+ source mentions, 4+ distinct source IDs, 6+ analytical paragraphs. A section with 3 short paragraphs and 2 numbers FAILS the depth gate. Depth is not about length — it's about evidence density.

**Per-section deep research mandate:** Before drafting a section, the analyst must do at least 3 targeted searches SPECIFIC to that section's topic (not generic company name search). Examples:
- S3 Technology: "[technology name] mechanism", "[technology name] clinical paper", "[competitor technology] vs [our technology] comparison", site:pubmed.ncbi.nlm.nih.gov "[technology name]"
- S4 Market: "[industry] market size 2025 2026 report", "[industry] CAGR forecast", site:grandviewresearch.com OR site:marketsandmarkets.com "[industry]"
- S5 Competition: "[competitor name] product specifications", "[competitor name] funding valuation", "[competitor name] vs [company name] comparison"
- S2 Team: "[founder name] LinkedIn", "[founder name] publication", "[founder name] interview", site:patents.google.com "[founder name]"
- All sections: search company official website, government databases (NMPA/FDA/SAMR), academic databases (PubMed/arXiv/Google Scholar) where relevant.

18. Run the **Investor Reviewer** using `references/investor_reviewer_lens.md`. This is a simulated investment committee partner who reads the report with fresh eyes and challenges it on completeness, detail sharpness, and claim verification. The reviewer produces `_work/investor_review.md` with Critical/Important/Minor items across 5 rounds: (1) Completeness Sweep — is every section at the forensic depth standard? Does each section have sufficient depth or is it a few short paragraphs? (2) Claim Verification — is every claim sourced and current? (3) Missing Competitors — who did the analyst forget? (4) Product/Market Fit — the uncomfortable commercial questions. (5) Number Stress-Test — key assumptions at -30%. **All Critical items must be resolved before proceeding.** The analyst must either add the missing information (by doing ADDITIONAL targeted searches, not by rewording existing content) or explicitly state why it cannot be obtained and how that impacts confidence.
19. Generate PDF:

   ```bash
   python scripts/generate_pdf.py "[report.html]" "[report.pdf]"
   ```

19. Run the QA loop after drafting and PDF generation. The loop is valid only when `_work/` still contains completed profile requirements, research, source register, thesis table, scenario analysis, red-team review, and evidence matrix. If `_work/` is absent or the loop fails, the report has not passed harness QA.

   ```bash
   python scripts/run_analysis_harness.py loop --output "[output folder]" --html "[report.html]" --pdf "[report.pdf]"
   ```

   If the loop fails, return to search/evidence gathering and rewrite the weak sections. Do not solve failures by adding generic wording without new evidence.
   When the loop fails, the harness generates `_work/rewrite_plan.md` when an HTML report exists. Treat every unchecked item in that file as mandatory; `gate` will fail until the rewrite checklist is resolved.

20. Re-run the QA loop after every material rewrite or PDF regeneration, visually check HTML/PDF when possible, then clean. `clean` now runs report QA first when an HTML report exists; if QA fails, cleanup is blocked so `_work/` remains available for repair. Do not run or claim harness-loop QA after cleanup.

   ```bash
   python scripts/run_analysis_harness.py clean --output "[output folder]"
   ```

21. Run the post-clean final check. This is mandatory for Codex because `clean_output.py` alone only verifies folder cleanliness, not report quality.

   ```bash
   python scripts/run_analysis_harness.py final-check --output "[output folder]" --html "[report.html]" --pdf "[report.pdf]"
   ```

22. Final output folder must contain only:

   ```text
   [CompanyName]_[BusinessSummary]/
   ├── sources/
   ├── [CompanyName]_投资分析报告.html
   └── [CompanyName]_投资分析报告.pdf
   ```

## Report Requirements

The report must make a reader competent enough to understand the company, its industry, and the investment decision. It should not merely list broad due-diligence dimensions.

Mandatory top module:

- `{{EXECUTIVE_SUMMARY}}` is a "5-minute read" briefing with verdict/action, score/rating, strongest positives, most important risks, key facts, evidence confidence, valuation/terms, follow-up diligence, the one question, and three takeaways.
- Include a non-consensus insight when one exists. If the thesis is consensus or there is no clear analytical edge, say that directly rather than inventing one.

Mandatory depth standard:

- Each section must satisfy the Mandatory Evidence Gate in `references/analysis_core.md`.
- Each section must be drafted from the completed `Deep Evidence Table`, not from the outline alone. If a section does not have source IDs, mechanism, benchmark context, counter-evidence, and investor implication in `_work/evidence_matrix.md`, keep researching before drafting.
- Each section must also have a completed internal section plan in `_work/evidence_matrix.md`: decision question, final-report thesis sentence, why the section is different from the other sections, evidence mechanism, comparison set/base rate, counter-evidence, visual artifact choice, and words/patterns prohibited in the final report.
- Each section must cover judgement, evidence, mechanism, benchmark/comparison, counter-evidence or failure mode, investor implication, confidence, and diligence questions, but the final writing should be narrative and content-specific rather than a repeated checklist of identical subheadings.
- Do not turn the report into pure black text on a white background. Use visual hierarchy, compact tables, KPI strips, timelines, scenario tables, risk matrices, and selective callouts to break up dense analysis and improve reading flow.
- Do not append the same `投资人读法`, `来源/Source`, `数字锚点`, `引用锚点`, `原件优先级`, `仍需确认`, metric-card copy, or transaction-structure paragraph to every section. Replacing the section name inside the same paragraph is still filler and must fail QA. Put full source details in the source appendix and reserve callouts for section-specific insight or decision-changing risks.
- Keep section scaffolds internal. Do not display `经济机制：`, `比较与基准：`, `反证与风险：`, or `投资含义：` as repeated headings across many sections; use content-specific micro-headings or direct narrative instead.
- Never write sections as `{section name}判断`, `{section name}的机制`, `{section name}的benchmark`, `{section name}原件优先级`, `{section name}决策门槛`, or `{section name}决策清单`. This is section-name substitution, not analysis, and must fail QA.
- The final report must never explain how the section should be written. Phrases such as `不能被写成`, `要把证据等级`, `而不是把材料拆成孤立事实`, `source ID只用于锁定证据来源`, or `同时处理证据、反证、机制和投资含义` belong only in internal workflow files and must fail final QA.
- Prefer a shorter section with one real judgement, one evidence mechanism, one comparison, and one priced risk over a long section padded with workflow language. Length is not depth.
- If a section lacks independent investigation, mark it low-confidence and keep searching before writing a strong conclusion.

Decision modules:

- Always include scenario analysis and key assumptions, but choose the right precision. Use financial bull/base/bear cases when data supports it; use milestone or probability scenarios for early-stage, biotech, hard-tech, or data-poor cases.
- Always identify the one diligence question that would most change the decision.
- Use industry KPIs, historical analogs, capital efficiency, and position sizing only when they are decision-relevant and evidence-backed. If a module would create false precision, state why it is not used and what data would be needed.
- Use the geographic market context lens when material. Separate home market, customer market, supplier market, comparable-company market, capital market, and exit market before making market, competition, valuation, or strategy claims.
- Use the policy/geopolitics lens when material. Integrate it into market, competition, risk, valuation, and exit rather than writing generic policy background.
- For public equities or liquid secondaries, include latest stock price context, market cap/enterprise value where available, valuation multiples, income statement quality, margin drivers, recurring vs. non-recurring profit, cash flow conversion, working-capital drivers, capex, balance-sheet health, liquidity, debt maturity, asset quality, accounting policies/notes, related-party/off-balance-sheet risks where material, consensus/guidance delta, catalysts, downside case, and position sizing. Use primary filings for financial statements whenever available.
- For public equities or liquid secondaries, include position sizing context. For primary-market deals, translate this into deal size, valuation discipline, downside loss, and follow-on reserve logic.
- End with three takeaways that a reader should remember after closing the report.

Mandatory cleanliness:

- Do not deliver `_work/`, `rendered/`, screenshots, OCR dumps, `research_notes.md`, `source_extract*.md`, or temporary inventories.
- Run `scripts/clean_output.py` or `run_analysis_harness.py clean` before final delivery.

Citation and source reliability:

- No source is treated as guaranteed. Material claims must be anchored to the best available source hierarchy: primary/source-of-truth first, near-primary second, independent secondary third, company-provided material only with caution, and OCR-derived evidence only after visual check or corroboration.
- Cite every material number, comparison, valuation input, team-background claim, policy/regulatory claim, market-size claim, financial-statement claim, and major risk statement with a visible source ID such as `[S1]`.
- Web sources should be linked in the HTML. User-provided files should be cited by filename plus page/slide/table where possible. Market data must include exchange, currency, and date/time. OCR-derived claims must keep page/slide references and lower confidence unless visually checked or independently corroborated. Do not over-tag every sentence; use inline tags for material claims and a consolidated source appendix for full source detail.
- If a material claim cannot be independently verified, write `未独立验证` and do not present it as a high-confidence conclusion.

## Report Template

Use `templates/report_template.html` and replace:

- `{{COMPANY_NAME}}`
- `{{COMPANY_TAGLINE}}`
- `{{COMPANY_BUSINESS_SUMMARY}}`
- `{{REPORT_DATE}}`
- `{{DATA_AS_OF}}`
- `{{INDUSTRY}}`
- `{{HEADQUARTERS}}`
- `{{STAGE}}`
- `{{EXECUTIVE_SUMMARY}}`
- `{{SECTION_1}}` through `{{SECTION_14}}`
- `{{YEAR}}`

Use `.verdict-strip`, `.briefing-grid`, `.brief-card`, `.evidence-card`, `.info-card`, `.warning`, `.danger`, `.source-tag`, `.source-confidence`, `.table-wrap`, `.data-table`, `.scenario-table`, `.sensitivity-table`, `.one-question`, `.takeaway-strip`, `.kpi-dashboard`, `.analog-grid`, `.efficiency-strip`, `.risk-matrix`, and `.timeline` when they improve scanability. The executive briefing must start with `.verdict-strip` and then compact decision cards. Do not turn every section into the same set of evidence/mechanism/risk cards or repeated KPI dashboards; prefer narrative paragraphs, content-specific micro-headings, compact tables, KPI strips, and selective callouts where they make the investment logic easier to read. Avoid long unbroken paragraphs and avoid decorative panels that do not carry evidence or a decision. Add one consolidated source appendix with links instead of repeated per-section source blocks.

## Final QA

Before delivery:

- `run_analysis_harness.py check-evidence` passes.
- `run_analysis_harness.py gate` passes before drafting.
- `check_workflow_docs.py` passes on `_work/` before final QA.
- If `_work/rewrite_plan.md` exists, all rewrite checklist items are resolved before rerunning `gate`, `loop`, `clean`, or `final-check`.
- `check_citations.py` passes on HTML.
- `check_depth.py` passes on HTML.
- `check_report.py` passes on HTML/PDF.
- `clean_output.py` passes on the output folder.
- `run_analysis_harness.py final-check` passes after cleanup.
- Final folder contains only `sources/`, HTML report, and PDF report.
