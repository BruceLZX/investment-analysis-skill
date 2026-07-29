---
name: investment-analysis
description: "Harness-driven company and industry investment research for primary-market and secondary-market decisions. Use when the user asks for company analysis, investment due diligence, pitch deck review, industry research, valuation work, competitor analysis, policy/regulatory/geopolitical analysis, public-equity research, stock/financial-statement analysis, balance-sheet health, VC/PE diligence, or a professional HTML/PDF investment report from a company name, ticker, or source files such as PDF, PPT, DOC, spreadsheets, screenshots, or scanned materials."
---

# Investment Analysis

Produce a decision-grade investment report that can teach a reader enough about the company and industry to make a professional investment decision. Use the harness and QA loop; do not rely on a one-shot report draft.

Default output language: match the user's language automatically. For Chinese requests, write in Chinese preserving official English names. For English requests, write the full report in English — section headers, analysis text, labels, and the executive summary. The HTML template uses bilingual headers (e.g., "公司概览 Company Overview") and works for both languages. Source citations, tickers, and proper nouns stay in their original language.

## Required Workflow — Agent-Based Orchestrator

This skill spawns independent agents for each section. Every agent gets a **clean context window** and full tool access (WebSearch, WebFetch, Bash, Read, Write). This is the key to depth — each section gets dedicated research capacity without competing for context with other sections.

### Stage 0: Setup

1. Read `references/report_strategy_playbook.md` to choose the report spine.
2. Read `references/analysis_core.md` for evidence standards.
3. Read `references/decision_framework.md` for decision framework.
4. Read `references/company_deep_dive_playbook.md` for forensic depth standard.
5. Read conditional lenses as needed (`geo_market_context_lens.md`, `policy_geopolitics_lens.md`, `public_equity_financials_lens.md`, `regulatory_database_lens.md`).
6. Extract user-provided materials. Copy originals into `sources/`.
7. Initialize:

   ```bash
   python scripts/run_analysis_harness.py preflight
   python scripts/run_analysis_harness.py init --output "[output]" --company "[name]" --sources [files...]
   ```

8. Create `_work/sections/`. Write `context.json` skeleton and `meta.txt`.

### Stage 1: Parallel Agents — Independent Sections (S1-S10, S12, S13)

**CRITICAL**: Use the **Agent tool** (NOT the Skill tool). Launch ALL 12 agents in a SINGLE message with `run_in_background: true` so they execute concurrently with independent context windows.

Each agent uses `subagent_type: "general-purpose"` and receives a self-contained prompt with:
- Role: produce ONE section of an investment report
- The section's research requirements (from `references/section_deepening.md`)
- Evidence standards (from `_shared/section_standards.md`)
- Company context and source file paths
- Output: Write `_work/sections/SECTION_N.html` + update `_work/sections/context.json`

**Agent prompts are constructed inline** by the orchestrator. Each prompt MUST include:

1. **Role**: "You are producing Section N (Title) of a professional investment analysis report for [COMPANY]."
2. **Research Mandate** (section-specific, from section_deepening.md):
   - S1: Map legal entities, build 8-15 event timeline, identify company type, explain customer/product/buyer
   - S2: Verify each founder's education/career/patents/exits against public records, assess founder-market fit, identify team gaps
   - S3: Describe product architecture, identify technical bottleneck, list patents with dates/jurisdictions, assess defensibility and dependencies, evaluate TRL
   - S4: Use two sizing approaches (top-down + bottom-up), bifurcate TAM/SAM/SOM by region, verify all BP market claims against independent sources, identify "why now" catalyst
   - S5: Map ALL material competitors (direct, substitute, international, future entrant), compare products/funding/team/share, include "do nothing" as competitor, assess moat durability
   - S6: Break down unit economics per product line, assess pricing power vs free alternatives, analyze customer concentration, revenue quality (recurring vs one-time), GTM strategy
   - S7: For public: income statement/balance sheet/cash flow/notes analysis. For early-stage: burn rate + runway from team size/location/funding. Mark estimated vs audited.
   - S8: Map every funding round (date/amount/investors/valuation/terms), build cap table (share classes/voting/liquidation pref), benchmark valuation against comps
   - S9: Map strategic roadmap (short/medium/long term), assess resource-strategy coherence, identify aspirational vs evidenced claims
   - S10: Aggregate ALL risks from S1-S9, score probability×impact, identify concentration risks (single tech/customer/geo), separate fatal vs manageable
   - S12: Identify likely acquirers with strategic rationale, assess IPO feasibility (venue/requirements/timeline), analyze cross-border regulatory constraints
   - S13: Score E/S/G dimensions with evidence, map to SDGs, assess materiality to investment decision
3. **Evidence Gate** (from `_shared/section_standards.md`): 3-6 targeted WebSearch calls, 2+ independent sources, 1+ primary source, 2+ numeric facts, 1+ competitor comparison, 1+ counter-evidence, investor implication
4. **Deep Research Trigger**: Do NOT just summarize the BP. Search for:
   - Academic papers (Google Scholar, arXiv, PubMed where relevant)
   - Government/regulatory databases (gsxt.gov.cn, NMPA, CDE, CAC, MIIT, etc. per regulatory_database_lens.md)
   - Industry reports (Counterpoint, IDC, GSMA, Grand View Research, MarketsandMarkets)
   - Competitor official websites, Crunchbase, Pitchbook
   - Patent databases (Google Patents, CNIPA)
   - News archives and founder interviews
5. **Output Instructions**:
   - Write `_work/sections/SECTION_N.html` — valid HTML fragment with required CSS classes (`.kpi-dashboard`, `.data-table`, `.info-card`, etc.)
   - Use `<a href="#src-SX" class="source-tag">[SX]</a>` for inline citations
   - Update `_work/sections/context.json` — add `sections.sN` with status/completed, confidence, 2-3 sentence summary
   - Minimum depth: 2500+ chars, 8+ numeric facts, 6+ source mentions, 4+ source IDs, 6+ paragraphs

**Parallel dispatch**: Send all 12 Agent() calls in ONE message. Each with `run_in_background: true`. The orchestrator waits for all to complete before Stage 2.

### Stage 2: Sequential Agents — Dependent Sections (S11, S14)

After ALL 12 Stage 1 agents complete:
1. Read `_work/sections/context.json` to collect all section summaries
2. Launch `ia-thesis` agent: synthesizes S2-S10 into investment thesis with scenario analysis, analogs, position sizing. Writes `SECTION_11.html`.
3. After S11 completes: Launch `ia-scoring` agent: weighted 10-dimension scoring based on S1-S13 findings. Writes `SECTION_14.html`.

### Stage 3: Final Agents

After S1-S14 complete:
1. Launch Executive Summary agent: synthesizes all 14 summaries into 5-minute briefing. Writes `EXECUTIVE_SUMMARY.html`.
2. Launch Source Appendix agent: compiles source register into formatted HTML. Writes `SOURCE_APPENDIX.html`.

### Stage 4: Assembly

```bash
python scripts/build_report.py templates/report_template.html "[output]/[name]_投资分析报告.html" _work/sections/
```

### Stage 5: QA + PDF + Deliver

```bash
python scripts/run_analysis_harness.py loop --output "[output]" --html "[html]" --pdf "[pdf]"
python scripts/generate_pdf.py "[html]" "[pdf]"
python scripts/run_analysis_harness.py clean --output "[output]"
python scripts/run_analysis_harness.py final-check --output "[output]" --html "[html]" --pdf "[pdf]"
```

If loop fails: read `_work/rewrite_plan.md`, re-launch the weak section's agent with specific fix instructions, re-run Stage 4-5.

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
- `{{SOURCE_APPENDIX}}`
- `{{COMPOSITE_SCORE}}` — the overall composite score like `8.3` (NOT dimension scores). Must appear in both the meta tag and the report's S14 section.
- Source tags in body text (`[S1]`, `[S2]`, etc.) should link to the appendix via `<a href="#src-S1" class="source-tag">[S1]</a>`
- Source appendix rows must follow: `<tr id="src-S1"><td class="src-id">S1</td><td class="src-desc">Source description</td><td class="src-url"><a href="URL">URL or file path</a></td><td class="src-conf">置信度</td></tr>`

**Mandatory visual components — these classes MUST appear at least once in every report:**

| Component | CSS Class | Required Location | Purpose |
|-----------|----------|-------------------|---------|
| Verdict strip | `.verdict-strip` | Top of `{{EXECUTIVE_SUMMARY}}` | Score, rating, action |
| Briefing grid | `.briefing-grid` + `.brief-card` | Executive summary | 3 key judgment cards |
| KPI dashboard | `.kpi-dashboard` + `.kpi-card` + `.kpi-good`/`.kpi-warn` | S1 Company Overview | 4-8 key metrics at a glance |
| Efficiency strip | `.efficiency-strip` + `.eff-card` | Executive summary | Revenue, profit, valuation, margins |
| One question | `.one-question` | Executive summary | The single most important diligence question |
| Three takeaways | `.takeaway-strip` + `.takeaway-item` | End of S14 & Executive summary | 3 numbered takeaways |
| Scenario table | `.scenario-table` with `.bull`/`.base`/`.bear` | S11 Investment Thesis | Probability-weighted bull/base/bear |
| Sensitivity table | `.sensitivity-table` with `.high-impact` | S14 Scoring | Key assumptions ranked by EV impact |
| Risk matrix | `.risk-matrix` with `.level-critical`/`.level-high` | S10 Risk | Color-coded probability × impact |
| Timeline | `.timeline` + `.timeline-item` | S1 Company Overview | Dated company milestones (8-15 events) |
| Source tags | `.source-tag` + `.source-confidence` (`.conf-high`/`conf-medium`/`conf-low`) | Throughout report | Every major claim gets a source+confidence tag |
| Data tables | `.table-wrap` > `.data-table` | Throughout report | Financials, competitors, products, patents |
| Info cards | `.info-card.highlight` / `.info-card.warning` / `.info-card.danger` | Throughout report | Key insights, risks, diligence gaps |
| Evidence cards | `.evidence-card` | S2-S6 | Key evidence packets for major claims |
| Quad grid | `.quad-grid` + `.quad-strength`/`.quad-weakness`/etc | S5 or S10 | SWOT-style analysis |
| Analog grid | `.analog-grid` + `.analog-card.best`/`.cautionary` | S11 | Historical analogs |

**A report without these components is incomplete.** Plain text paragraphs alone do not constitute a professional investment report. Use the components to make data scannable — a 200KB report should have a KPI strip at the top, a verdict badge, scenario tables with color coding, and risk matrices. After using each component once, additional narrative paragraphs, comparison tables, and content-specific subheadings carry the detailed analysis.

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
