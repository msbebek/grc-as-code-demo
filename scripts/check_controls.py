#!/usr/bin/env python3
"""Validate control files and report framework coverage.

Usage: python3 scripts/check_controls.py
Fails (exit 1) if a control is missing a required field or maps to a requirement
that does not exist in frameworks/. Writes reports/coverage.md, including the gaps:
in-scope requirements that no control covers yet.
"""
import glob, sys
import yaml

REQUIRED = ["id", "title", "owner", "frequency", "type", "description", "test_procedure", "evidence", "mappings"]
FRAMEWORKS = {"soc2": "frameworks/soc2.yaml", "iso27001": "frameworks/iso27001.yaml"}

frameworks = {k: yaml.safe_load(open(p)) for k, p in FRAMEWORKS.items()}
controls = [yaml.safe_load(open(p)) | {"_file": p} for p in sorted(glob.glob("controls/*.yaml"))]

errors = []
covered = {k: {} for k in FRAMEWORKS}
for c in controls:
    for field in REQUIRED:
        if not c.get(field):
            errors.append(f"{c['_file']}: missing '{field}'")
    for fw, reqs in (c.get("mappings") or {}).items():
        if fw not in frameworks:
            errors.append(f"{c['_file']}: unknown framework '{fw}'")
            continue
        for r in reqs:
            r = str(r)
            if r not in frameworks[fw]["requirements"]:
                errors.append(f"{c['_file']}: {fw} requirement '{r}' is not in {FRAMEWORKS[fw]}")
            covered[fw].setdefault(r, []).append(c["id"])

lines = ["# Control coverage report", "", f"Controls: {len(controls)}", ""]
for fw, data in frameworks.items():
    reqs = data["requirements"]
    hit = [r for r in reqs if r in covered[fw]]
    lines += [f"## {data['framework']}: {len(hit)}/{len(reqs)} requirements covered", "",
              "| Requirement | Description | Controls |", "|---|---|---|"]
    for r, desc in reqs.items():
        ids = ", ".join(covered[fw].get(r, [])) or "**GAP**"
        lines.append(f"| {r} | {desc} | {ids} |")
    lines.append("")
open("reports/coverage.md", "w").write("\n".join(lines))
print("\n".join(lines))

if errors:
    print("\nERRORS:\n" + "\n".join(errors))
    sys.exit(1)
