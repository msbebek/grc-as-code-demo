# GRC as code: demo

A small, working example of managing a compliance program as code: controls are versioned files,
changes go through pull requests with review, and a GitHub Action validates every change and
reports framework coverage. Built as a learning exercise with Claude Code. All data is synthetic.

## Structure
| Path | What it holds |
|---|---|
| `controls/` | One YAML file per control: owner, frequency, test procedure, evidence, mappings |
| `frameworks/` | In-scope requirements of SOC 2 and ISO 27001:2022 (a subset) |
| `policies/` | Policies in Markdown, linked to the controls that enforce them |
| `scripts/check_controls.py` | Validates every control and writes `reports/coverage.md` with the gaps |
| `scripts/uar_check.py` | Automates the quarterly user access review (control AC-01, AC-02) |
| `evidence/` | Synthetic HR list and application accounts for the access review |
| `.github/workflows/` | Runs both scripts on every pull request |

## Why this way
- **Audit trail for free:** every change to a control or policy has an author, a reviewer, a date and a reason (the pull request).
- **Test once, satisfy many:** one control maps to several frameworks, so one test produces evidence for SOC 2 and ISO 27001.
- **Gaps are visible:** the coverage report lists in-scope requirements without a control.
- **Evidence is reproducible:** the access review runs the same rules every quarter and keeps the exception list.

## Run locally
```
pip install pyyaml
python3 scripts/check_controls.py
python3 scripts/uar_check.py evidence/uar-2026-q3/hr_active.csv evidence/uar-2026-q3/app_accounts.csv
```

## Current gaps (see reports/coverage.md)
SOC 2 CC6.6, CC6.7, CC7.3 and ISO 27001 8.15, 8.24 have no control yet.
