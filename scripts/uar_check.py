#!/usr/bin/env python3
"""User access review (control AC-01 / AC-02): compare an application's accounts with the HR list.

Usage: python3 scripts/uar_check.py evidence/uar-2026-q3/hr_active.csv evidence/uar-2026-q3/app_accounts.csv
Flags: accounts of people not active in HR (leavers or unknown), privileged accounts without an
approval reference, and accounts whose role does not match the department's allowed roles.
Writes the exception list next to the input as exceptions.csv.
"""
import csv, os, sys

ALLOWED_ROLES = {  # role-to-department rule set agreed with the application owner
    "Finance": {"viewer", "accountant", "approver"},
    "Engineering": {"viewer", "developer", "admin"},
    "Sales": {"viewer"},
    "People": {"viewer"},
}
PRIVILEGED = {"admin", "approver"}

hr_path, acc_path = sys.argv[1:3]
hr = {r["email"].lower(): r for r in csv.DictReader(open(hr_path))}
out = []
for a in csv.DictReader(open(acc_path)):
    email, role = a["email"].lower(), a["role"]
    person = hr.get(email)
    if not person:
        out.append([email, role, "No active employee in HR (leaver or unknown account)"])
        continue
    if role not in ALLOWED_ROLES.get(person["department"], set()):
        out.append([email, role, f"Role not allowed for department {person['department']}"])
    if role in PRIVILEGED and not a.get("approval_ref"):
        out.append([email, role, "Privileged access without approval reference"])

dst = os.path.join(os.path.dirname(acc_path), "exceptions.csv")
with open(dst, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["email", "role", "exception"])
    w.writerows(out)
print(f"{len(out)} exceptions written to {dst}")
for row in out:
    print(" - " + " | ".join(row))
