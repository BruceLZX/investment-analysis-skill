# Section Standards

Every sub-skill must satisfy these minimum evidence and depth standards before writing its section HTML.

## Mandatory Evidence Gate

| Required item | Minimum standard |
| --- | --- |
| Targeted searches | 3-6 queries specific to this section's topic |
| Independent sources | At least 2; 3+ for market, competition, team, funding, financials, risk |
| Primary source check | At least 1 primary/near-primary source where available |
| Quantification | At least 2 numbers, ranges, or proxies; if unavailable, state what's missing |
| Comparison | At least 1 competitor, benchmark, base rate, industry norm, or historical comparable |
| Counter-evidence | At least 1 contradicting source, weakness, adverse case, or reason thesis may fail |
| Investor implication | A decision-relevant conclusion |
| Source IDs | At least 2 distinct source IDs in the final HTML |

## Depth Standard (enforced by check_depth.py)

- 2,500+ plain-text characters per section
- 8+ numeric facts/proxies
- 6+ source/evidence mentions
- 4+ distinct source IDs
- 6+ analytical paragraphs
- Coverage: evidence, mechanism, comparison, counter-evidence, investor implication, diligence

## Output Rules

- Write only the HTML fragment (no `<html>`, `<head>`, `<body>`)
- Use `<a href="#src-SX" class="source-tag">[SX]</a>` for inline citations
- Use `.source-confidence.conf-high` / `.conf-medium` / `.conf-low` for confidence badges
- Never include scaffolding language (e.g., "本节应该...", "source ID用于...")
- Never use repeated checklist subheadings across sections
