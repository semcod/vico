from __future__ import annotations

import html
from pathlib import Path
from typing import Any

import yaml

from .diff import diff_capsule
from .drift import check_source_drift
from .journal import append_journal, read_journal
from .models import utc_now, write_yaml
from .paths import capsule_dir
from .status import capsule_status
from .verify import verify_capsule


def _finding_table(findings: list[dict[str, Any]]) -> str:
    rows = ["| Gate | Status | Message |", "|---|---:|---|"]
    for finding in findings:
        rows.append(
            f"| `{finding.get('code', '')}` | **{finding.get('status', '')}** | {str(finding.get('message', '')).replace('|', '/')} |"
        )
    return "\n".join(rows)


def _html_from_markdownish(title: str, markdown: str) -> str:
    escaped = html.escape(markdown)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:980px;margin:40px auto;padding:0 20px;line-height:1.5}}pre{{white-space:pre-wrap;background:#f5f5f5;padding:16px;border-radius:10px}}</style>
</head><body><pre>{escaped}</pre></body></html>"""


def build_capsule_report(root: Path, name: str) -> dict[str, Any]:
    base = capsule_dir(root, name)
    verification = verify_capsule(root, name)
    diff = diff_capsule(root, name)
    drift = check_source_drift(root, name)
    status = capsule_status(root, name)
    journal = read_journal(root, name)

    report = {
        "version": "vico.report.v1",
        "capsule": name,
        "created_at": utc_now(),
        "status": status,
        "verification": verification.to_dict(),
        "diff": diff.to_dict(),
        "drift": drift,
        "journal_tail": journal[-10:],
    }
    reports_dir = base / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(reports_dir / "report.yaml", report)

    findings = verification.to_dict().get("findings", [])
    markdown = f"""# Vico capsule report — {name}

Created at: {report['created_at']}

## Decision

- Status: **{verification.status}**
- Score: **{verification.score:.3f}**
- Latest iteration: **{status.get('latest_iteration')}**

## Diff from capsule baseline

- Added: {len(diff.added)}
- Modified: {len(diff.modified)}
- Deleted: {len(diff.deleted)}
- Unchanged: {len(diff.unchanged)}

## Source drift

- Status: **{drift.get('status')}**
- Changed source files: {len(drift.get('changed', []))}
- Missing source files: {len(drift.get('missing', []))}

## Verification gates

{_finding_table(findings)}

## Journal tail

```yaml
{yaml.safe_dump(journal[-10:], sort_keys=False, allow_unicode=True)}
```
"""
    (reports_dir / "report.md").write_text(markdown, encoding="utf-8")
    (reports_dir / "report.html").write_text(_html_from_markdownish(f"Vico report {name}", markdown), encoding="utf-8")
    append_journal(root, name, "report.built", "Built capsule verification report.", data={"status": verification.status})
    return {"yaml": str(reports_dir / "report.yaml"), "markdown": str(reports_dir / "report.md"), "html": str(reports_dir / "report.html"), "status": verification.status, "score": verification.score}
