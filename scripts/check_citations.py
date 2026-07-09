#!/usr/bin/env python3
"""Validate visible citations against the source register."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


SOURCE_ID_RE = re.compile(r"\bS\d+\b")
URL_RE = re.compile(r"https?://[^\s|)>\"]+")


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden_depth = 0
        self.text: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self.hidden_depth += 1
        if tag == "a":
            for key, value in attrs:
                if key == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.text.append(data)


def split_markdown_row(line: str) -> list[str]:
    raw = line.strip()
    if not raw.startswith("|") or not raw.endswith("|"):
        return []
    cells = next(csv.reader([raw.strip("|")], delimiter="|"))
    return [cell.strip() for cell in cells]


def read_source_register(path: Path) -> tuple[set[str], dict[str, str]]:
    ids: set[str] = set()
    urls: dict[str, str] = {}
    if not path.exists():
        raise SystemExit(f"Missing source register: {path}")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        cells = split_markdown_row(line)
        if len(cells) < 4:
            continue
        source_id = cells[0].strip()
        if not SOURCE_ID_RE.fullmatch(source_id):
            continue
        ids.add(source_id)
        match = URL_RE.search(cells[3])
        if match:
            urls[source_id] = match.group(0).rstrip(".,;")
    return ids, urls


def read_visible_html(path: Path) -> tuple[str, set[str]]:
    if not path.exists():
        raise SystemExit(f"Missing HTML report: {path}")
    parser = VisibleTextParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return " ".join(parser.text), set(parser.links)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check report citations against _work/source_register.md")
    parser.add_argument("--output", required=True, help="Output folder containing _work/source_register.md")
    parser.add_argument("--html", required=True, help="Final HTML report path")
    parser.add_argument("--min-cited-sources", type=int, default=5)
    args = parser.parse_args()

    output_dir = Path(args.output).expanduser().resolve()
    source_register = output_dir / "_work" / "source_register.md"
    registered_ids, registered_urls = read_source_register(source_register)
    visible_text, html_links = read_visible_html(Path(args.html).expanduser().resolve())
    visible_ids = set(SOURCE_ID_RE.findall(visible_text))

    failures: list[str] = []
    if not registered_ids:
        failures.append("source register has no source IDs like S1, S2")

    cited_registered_ids = visible_ids & registered_ids
    required_citation_count = min(len(registered_ids), args.min_cited_sources)
    if len(cited_registered_ids) < required_citation_count:
        failures.append(
            f"only {len(cited_registered_ids)} registered source IDs are visible in HTML; "
            f"expected at least {required_citation_count}"
        )

    orphan_ids = visible_ids - registered_ids
    if orphan_ids:
        failures.append("HTML cites source IDs not in source register: " + ", ".join(sorted(orphan_ids)))

    if registered_urls:
        linked_registered_urls = {url for url in registered_urls.values() if url in html_links}
        required_link_count = min(len(registered_urls), 3)
        if len(linked_registered_urls) < required_link_count:
            failures.append(
                f"only {len(linked_registered_urls)} registered URLs are linked in HTML; "
                f"expected at least {required_link_count}"
            )

    if not re.search(r"来源|source|citation|evidence", visible_text, re.IGNORECASE):
        failures.append("HTML has visible source IDs but no visible source/evidence labeling")

    if failures:
        print("Citation QA failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Citation QA passed: "
        f"{len(cited_registered_ids)} registered source IDs visible, "
        f"{len(registered_urls)} registered URLs tracked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
