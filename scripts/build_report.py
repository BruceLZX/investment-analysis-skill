#!/usr/bin/env python3
"""Build investment report by reading section files and replacing template placeholders.

Usage:
    python scripts/build_report.py <template.html> <output.html> <sections_dir/>

Supports both .html and .txt section files (prefers .html if both exist).
Reads meta.txt from sections_dir for company metadata.
"""
import sys, os, re

def main():
    template_path = sys.argv[1]
    output_path = sys.argv[2]
    sections_dir = sys.argv[3]

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Read metadata from meta.txt
    meta = {}
    meta_path = os.path.join(sections_dir, 'meta.txt')
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    meta[key.strip()] = val.strip()

    for key, val in meta.items():
        content = content.replace('{{' + key + '}}', val)

    # Read section files (prefer .html, fall back to .txt)
    for i in range(1, 15):
        section_html = None
        for ext in ('.html', '.txt'):
            section_file = os.path.join(sections_dir, f'SECTION_{i}{ext}')
            if os.path.exists(section_file):
                with open(section_file, 'r', encoding='utf-8') as f:
                    section_html = f.read()
                break
        if section_html is not None:
            content = content.replace('{{SECTION_' + str(i) + '}}', section_html)
        else:
            print(f"WARNING: SECTION_{i} not found in {sections_dir}")

    # Executive summary
    for ext in ('.html', '.txt'):
        exec_file = os.path.join(sections_dir, f'EXECUTIVE_SUMMARY{ext}')
        if os.path.exists(exec_file):
            with open(exec_file, 'r', encoding='utf-8') as f:
                content = content.replace('{{EXECUTIVE_SUMMARY}}', f.read())
            break

    # Source appendix
    for ext in ('.html', '.txt'):
        src_file = os.path.join(sections_dir, f'SOURCE_APPENDIX{ext}')
        if os.path.exists(src_file):
            with open(src_file, 'r', encoding='utf-8') as f:
                content = content.replace('{{SOURCE_APPENDIX}}', f.read())
            break

    # Check for any remaining placeholders
    remaining = re.findall(r'\{\{(\w+)\}\}', content)
    if remaining:
        print(f"WARNING: Unreplaced placeholders: {remaining}")
        return 1

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Report built: {output_path}")
    print(f"Size: {len(content)} bytes")
    return 0

if __name__ == '__main__':
    sys.exit(main())
