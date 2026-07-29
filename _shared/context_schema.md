# Context JSON Schema

Every sub-skill reads and writes `_work/sections/context.json` to pass findings between sections.

## Schema

```json
{
  "report_metadata": {
    "company_name": "string",
    "report_date": "string (YYYY-MM-DD)",
    "data_as_of": "string (YYYY-MM-DD)",
    "industry": "string",
    "headquarters": "string",
    "stage": "string"
  },
  "sections": {
    "s1": {
      "status": "completed | in_progress | pending",
      "confidence": "high | medium | low",
      "summary": "2-3 sentence summary of key findings",
      "key_findings": ["finding 1", "finding 2", "..."],
      "critical_gaps": ["gap 1", "..."],
      "html_path": "_work/sections/SECTION_1.html"
    }
  }
}
```

## Usage

- **Orchestrator**: creates skeleton with `report_metadata` populated
- **Independent sub-skills (S1-S10, S12, S13)**: read full context, update only their `sections.sN` key
- **Dependent sub-skills (S11, S14)**: read all section summaries before drafting
- **Executive summary**: reads all 14 section summaries
- **Source appendix**: reads `_work/source_register.md` directly
