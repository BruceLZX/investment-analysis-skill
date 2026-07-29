#!/usr/bin/env python3
"""Replace placeholders in template with actual content."""
import sys
import re

def main():
    template_path = sys.argv[1]
    output_path = sys.argv[2]
    replacements = {}

    # Read all key=value pairs from stdin or argv
    for i in range(3, len(sys.argv), 2):
        key = sys.argv[i]
        val = sys.argv[i+1]
        replacements[key] = val

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for key, val in replacements.items():
        content = content.replace('{{' + key + '}}', val)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Report written to {output_path}")

if __name__ == '__main__':
    main()
