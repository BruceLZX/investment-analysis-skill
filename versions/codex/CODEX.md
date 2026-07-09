# Investment Analysis - Codex Version

This version is the canonical Codex skill installed at the skill root.

Use:

```bash
python scripts/run_analysis_harness.py preflight
python scripts/run_analysis_harness.py init --profile codex --output "[CompanyName]_[BusinessSummary]" --company "[CompanyName]" --sources [source files...]
python scripts/run_analysis_harness.py gate --output "[output folder]"
python scripts/generate_pdf.py "[report.html]" "[report.pdf]"
python scripts/run_analysis_harness.py loop --output "[output folder]" --html "[report.html]" --pdf "[report.pdf]"
python scripts/run_analysis_harness.py clean --output "[output folder]"
python scripts/run_analysis_harness.py final-check --output "[output folder]" --html "[report.html]" --pdf "[report.pdf]"
```

Codex-specific expectations:

- Use the Codex skill trigger and current-session tools.
- `init --profile codex` generates `_work/profile_requirements.md`; complete it before drafting. The Codex profile is optimized for tool-driven live research, deterministic QA, citation checking, and cleanup discipline.
- `preflight` must pass before `init`. It verifies that the current compact report template is installed and old overlay TOC code is not present.
- Browse for current facts whenever facts may have changed. Use broad, multi-angle searches before narrowing.
- Use parallel local reads/searches and script checks where possible: source inventory, extraction checks, citation checks, evidence gate, report QA, and final clean verification.
- For current market or public-equity work, record the date/time of prices, filings, policy documents, executive/team facts, funding news, and regulatory events.
- Do not satisfy depth checks by generating repeated filler paragraphs with changed section names. In particular, avoid per-section `原件优先级`, `引用锚点`, repeated metric cards, or repeated diligence boilerplate. The Codex profile must prefer fewer, sharper section-specific paragraphs.
- Do not generate `{section name}判断`, `{section name}的机制`, `{section name}的benchmark`, `{section name}原件优先级`, `{section name}决策门槛`, or `{section name}决策清单`. These are explicit QA failures.
- Complete the section writing plan in `_work/evidence_matrix.md` before drafting. Each section needs a unique decision question, mechanism, comparison set, counter-evidence, and visual artifact choice; otherwise the section is not ready to write.
- Draft one final-report thesis sentence per section in `_work/evidence_matrix.md`; start the section from that sentence, not from the internal checklist.
- Keep analytical scaffolds internal. Do not show `经济机制：`, `比较与基准：`, `反证与风险：`, or `投资含义：` as repeated headings across sections.
- Never leak rubric/process language into the report. Phrases like `不能被写成`, `要把证据等级`, `而不是把材料拆成孤立事实`, and `source ID只用于锁定证据来源` are QA failures.
- Read `references/geo_market_context_lens.md` when geography, customer markets, supplier markets, foreign comparables, capital markets, or exit paths may affect demand, GTM, competition, valuation, or risk.
- Read `references/policy_geopolitics_lens.md` when national strategy, regulation, government procurement, export controls, sanctions, data security, or cross-border supply chains may affect the thesis. Choose the relevant jurisdictions and investor perspective first; do not default to China, US, or Europe logic.
- Keep the research plan, source register, evidence matrix, thesis table, red-team review, and all scratch work under `_work/`.
- Treat `_work/source_register.md` as the citation ledger. Use visible source IDs such as `[S1]` in the HTML, link web sources, and cite local files with filename plus page/slide/table where possible.
- Treat `_work/evidence_matrix.md` as a hard pre-draft gate. Every material section must have source IDs, mechanism, benchmark/peer context, counter-evidence, investor implication, confidence, and follow-up before drafting.
- Do not claim loop QA passed unless `run_analysis_harness.py loop` passes while `_work/` still exists. A cleaned output folder can only prove final cleanliness, not analytical depth.
- Final delivery remains only `sources/`, HTML report, and PDF report.

## Codex Profile Specialization

Use this version when Codex has direct access to local files, shell tools, browser/web search, and deterministic scripts. The profile should bias toward verifiable workflow execution:

- Prefer primary web sources, filings, official registries, patents, exchange announcements, and local user files over unsourced summaries.
- Use scripts to fail shallow work early. If `gate` or `loop` fails, continue research and rewrite; do not manually claim success.
- When `loop`, `clean`, or `final-check` fails on an HTML report, the harness writes `_work/rewrite_plan.md` if `_work/` exists. Complete that checklist before rerunning QA.
- `clean` is a quality gate, not just deletion: it blocks cleanup when report QA fails. After cleanup, run `final-check`; do not deliver unless it passes.
- Keep an explicit trail from search query -> opened source -> source ID -> evidence matrix -> final citation.
- Keep inline citations sparse and high-signal. Use the source appendix for full citation coverage; do not scatter source tags through every sentence.
- Use local browser/PDF/render checks when the report or source format makes visual verification material.

## Decision Requirements

These requirements apply regardless of platform — the report must serve a professional investment decision:

1. State the consensus or non-consensus view. Do not invent a variant perception when none exists.
2. Include bull/base/bear scenarios with specific drivers. Use financial scenarios when supportable; use milestone scenarios when financial precision would be fake.
3. Rank the 3-5 assumptions that most affect the decision.
4. Use historical analogs, KPI dashboards, capital efficiency, and position/deal sizing only when evidence-backed and decision-relevant.
5. Use geographic market context when material: separate home market, customer market, supplier market, capital market, comparable-company market, and exit market.
6. Integrate policy/geopolitics into market, competition, risk, valuation, and exit when material, using the relevant domestic or international perspective.
7. Identify the one diligence question whose answer would most change the decision.
8. End with the three takeaways the reader should remember.
9. Cite material claims and mark unverified company-only or OCR-derived claims explicitly; do not present unsourced claims as high-confidence conclusions.

## Report Expectations

- Start with a 5-minute executive briefing: verdict, score/rating, consensus/non-consensus view, core positives, key risks, evidence confidence, valuation/terms, follow-up diligence, and the one question.
- Include an industry-specific KPI dashboard only when the metrics are available or responsibly proxied.
- Include policy/geopolitics analysis only when material; do not write generic policy background.
- For every major section, cover judgement, evidence, mechanism, benchmark/comparison, counter-evidence/failure mode, investor implication, confidence, and diligence questions as the internal analytical scaffold, but do not force the same visible subheadings into every section.
- If a section reads generic, return to search and evidence gathering. Do not solve depth failures by adding longer prose without new sources, mechanisms, or comparisons.
- Do not optimize for length. A concise section with specific evidence, mechanism, comparison, risk, and decision implication is better than a long section padded with internal workflow language.
- The report must feel like an investment committee memo, not an encyclopedia entry or a worksheet. Use narrative paragraphs, content-specific micro-headings, compact tables, KPI strips, timelines, risk matrices, and selective callouts to make dense analysis readable.
- The first screen must carry a real decision: use a visible verdict strip, compact decision cards, and the most important evidence delta. Do not make the executive briefing a set of generic cards without an explicit action.
- Use KPI dashboards sparingly. A repeated KPI strip in every section is a layout failure and usually signals content padding.
