#!/usr/bin/env python3
import json, re, os

BASE = "/Users/nicoleemrich/Documents/Claude/Projects/WPP Media"
html_path = os.path.join(BASE, "tuic-9127-yoy-tool.html")
data_path = os.path.join(BASE, "tuic_9127_abs_data.json")

with open(data_path) as f:
    data = json.load(f)
compact = json.dumps(data, ensure_ascii=False, separators=(", ", ": "))

with open(html_path) as f:
    html = f.read()

# Replace the const DATA = {...}; block only (non-greedy up to ;\nconst MONTHS)
pattern = re.compile(r"const DATA\s*=\s*\{.*?\};(?=\s*\nconst MONTHS)", re.DOTALL)
new_block = "const DATA = " + compact + ";"
html2, n = pattern.subn(new_block, html)
if n != 1:
    raise SystemExit(f"ERROR: expected 1 DATA replacement, got {n}")

with open(html_path, "w") as f:
    f.write(html2)

print(f"OK replaced {n} block, today={data['meta']['today']}")
