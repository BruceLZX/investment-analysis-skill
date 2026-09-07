# Investment Analysis - DSH Version

Use this profile when running the investment-analysis workflow inside **DeepSeek Harness (DSH)** — DSH Desktop, the `dsh` CLI, or any DSH-compatible runtime. DSH is a Cordis-based agent harness with background subagents, a PowerShell shell on Windows, and a filesystem skill provider.

## Mission

Generate a decision-grade investment report for primary-market or secondary-market use. The report must teach a non-specialist reader enough about the company, industry, risks, and valuation to make a professional investment decision.

## Required Workflow

Run the shared harness from the skill root. On Windows, invoke Python through the `pwsh` tool:

```powershell
python scripts/run_analysis_harness.py init --profile dsh --output "[CompanyName]_[BusinessSummary]" --company "[CompanyName]" --sources [source files...]
python scripts/run_analysis_harness.py gate --output "[output folder]"
python scripts/generate_pdf.py "[report.html]" "[report.pdf]"
python scripts/run_analysis_harness.py loop --output "[output folder]" --html "[report.html]" --pdf "[report.pdf]"
python scripts/run_analysis_harness.py clean --output "[output folder]"
python scripts/run_analysis_harness.py final-check --output "[output folder]" --html "[report.html]" --pdf "[report.pdf]"
```

Read before drafting:

- `references/report_strategy_playbook.md`
- `references/analysis_core.md`
- `references/decision_framework.md`
- `references/company_deep_dive_playbook.md`

Read `references/section_deepening.md` only for sections that need planning or rewriting. Read `references/geo_market_context_lens.md` when geography, customer markets, suppliers, channels, foreign comparables, capital markets, or exit paths may affect the thesis. Read `references/policy_geopolitics_lens.md` when national strategy, regulation, government procurement, export controls, sanctions, data security, or cross-border supply chains may affect the thesis.

## DSH Tool Mapping

The shared `SKILL.md` orchestrator is written in Claude Code terms. Translate to DSH tools:

| Claude Code term | DSH tool | Notes |
| --- | --- | --- |
| Agent tool / Task | `subagent` | Runs a self-contained task in a **fresh context**. Background by default — launch all independent agents in ONE message for concurrency. |
| `subagent_type: "general-purpose"` | (none) | Use `subagent` with `description` + `prompt`; there is no type parameter. |
| Skill tool | `skill` | Loads skill instructions by exact name. |
| Bash | `pwsh` | Windows PowerShell. Prefix the Python harness with `python`. |
| WebSearch / WebFetch | `web_search` / `web_fetch` | |
| Read / Write / Edit | `read` / `write` / `edit` (plus `glob`, `grep`) | File discovery and editing. |
| (task tracking) | `todo_write` | Track the staged workflow. |
| (job control) | `job_output` / `job_kill` / `job_list` | Collect, cancel, or list background subagents. |

## DSH-Specific Operating Notes

- `init --profile dsh` generates `_work/profile_requirements.md`; complete it before drafting. This profile is optimized for DSH's background subagent fan-out.
- **DSH subagents do not inherit the orchestrator's conversation.** Every section agent's prompt must be fully self-contained: role, section mandate (from `references/section_deepening.md`), evidence gate (from `_shared/section_standards.md`), company context, source file paths, and the exact output contract.
- Launch the 12 independent section agents (S1-S10, S12, S13) as `subagent` calls in a **single message** with `run_in_background: true` so they execute concurrently with independent context windows. Wait for all of them to settle (completion notices or `job_output`); do not busy-poll.
- For the dependent sections (S11 investment thesis, S14 scoring), either feed the collected section summaries inline into a self-contained `subagent` prompt, or use `subagent_fork` to inherit the orchestrator's context. Prefer the self-contained prompt for reproducibility.
- Use the `pwsh` tool (not a Bash tool) for every Python harness invocation on Windows. The harness is pure stdlib; no third-party packages are required for `init`/`gate`/`loop`/`clean`/`final-check`.
- Use `web_search` + `web_fetch` for live research, and `read`/`glob`/`grep` for local files and `references/`.
- Use `todo_write` to track stages and `job_output` to collect background results. Use `job_kill` only to cancel a genuinely stuck or superseded agent.
- Treat `_work/evidence_matrix.md` as a hard pre-draft gate and the harness loop as a hard stop — a failed `gate`, `check_citations`, `check_depth`, `check_report`, or final clean check means return to research and rewrite. Do not claim loop QA passed unless `loop` ran while `_work/` still existed.
- Keep the research plan, source register, evidence matrix, thesis table, scenario analysis, red-team review, investor review, and all scratch work under `_work/`. Final output must contain only `sources/`, HTML report, and PDF report.

## DSH Profile Specialization

Use this version when DSH is the execution surface. The profile should bias toward deterministic, verifiable execution:

- Fan out independent section research across background `subagent` calls; each agent has a clean context window, so the depth of a section never competes with the other sections for context.
- Make each section agent's prompt self-contained and non-negotiable: it must produce `_work/sections/SECTION_N.html` with the required CSS classes and inline `[SX]` source tags, and update `_work/sections/context.json` with status, confidence, and a 2-3 sentence summary.
- Run the Python QA scripts through `pwsh` and let them fail shallow work early. If `gate`, `loop`, `clean`, or `final-check` fails, continue research and rewrite; do not manually claim success.
- When `loop`, `clean`, or `final-check` fails on an HTML report, the harness writes `_work/rewrite_plan.md` when `_work/` exists. Complete that checklist before rerunning QA.
- Keep an explicit trail from search query → opened source → source ID → evidence matrix → final citation.
- Treat `_work/source_register.md` as the citation ledger: visible `[S1]`-style IDs in the HTML, linked web sources, and local files cited by filename plus page/slide/table.

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
- Use KPI dashboards sparingly. A repeated KPI strip in every section is a layout failure and usually signals content padding.
