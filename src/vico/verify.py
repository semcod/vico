from __future__ import annotations

from pathlib import Path

from .capsule import load_capsule
from .files import collect_files, rel
from .intract import IntentContract, read_manifest_contracts, scan_contracts_in_file
from .models import VerificationFinding, VerificationReport, write_yaml
from .paths import capsule_dir

WRITE_PATTERNS = [
    "session.commit(",
    ".commit(",
    "INSERT ",
    "UPDATE ",
    "DELETE ",
    "open(",
    ".write(",
    "fs.writeFile",
    "fetch(",
    "requests.post",
    "httpx.post",
]


def _scan_capsule_contracts(base: Path) -> list[IntentContract]:
    contracts = read_manifest_contracts(base / "intract.yaml")
    for path in collect_files(base / "src"):
        contracts.extend(scan_contracts_in_file(path, base))
    return contracts


def _contains_forbidden_write(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    evidence = []
    for pattern in WRITE_PATTERNS:
        if pattern in text:
            evidence.append(f"{path.name}: contains `{pattern}`")
    return evidence


def verify_capsule(root: Path, name: str) -> VerificationReport:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    findings: list[VerificationFinding] = []

    contracts = _scan_capsule_contracts(base)
    if contracts:
        findings.append(
            VerificationFinding(
                code="contracts_found",
                status="pass",
                message=f"Found {len(contracts)} intent contract(s).",
                evidence=[c.intent for c in contracts if c.intent],
            )
        )
    else:
        findings.append(
            VerificationFinding(
                code="contracts_missing",
                status="fail",
                message="No Intract-style contracts found in capsule.",
            )
        )

    source_files = collect_files(base / "src")
    if source_files:
        findings.append(
            VerificationFinding(
                code="source_files_found",
                status="pass",
                message=f"Capsule contains {len(source_files)} text source file(s).",
                evidence=[rel(path, base) for path in source_files[:20]],
            )
        )
    else:
        findings.append(
            VerificationFinding(
                code="source_files_missing",
                status="fail",
                message="Capsule has no copied source files.",
            )
        )

    forbids_write = any("write" in contract.forbid or "destructive_write" in contract.forbid for contract in contracts)
    write_evidence: list[str] = []
    if forbids_write:
        for path in source_files:
            write_evidence.extend(_contains_forbidden_write(path))
        if write_evidence:
            findings.append(
                VerificationFinding(
                    code="forbidden_write_detected",
                    status="fail",
                    message="A contract forbids write effects, but write-like patterns were detected.",
                    evidence=write_evidence[:20],
                )
            )
        else:
            findings.append(
                VerificationFinding(
                    code="no_forbidden_write",
                    status="pass",
                    message="No obvious forbidden write effect detected.",
                )
            )

    iteration_count = len(capsule.iterations)
    findings.append(
        VerificationFinding(
            code="iteration_count",
            status="pass" if iteration_count else "warn",
            message=f"Capsule has {iteration_count} planned iteration(s).",
            evidence=capsule.iterations,
        )
    )

    statuses = [finding.status for finding in findings]
    if "fail" in statuses:
        status = "fail"
        score = 0.45
    elif "warn" in statuses:
        status = "partial"
        score = 0.75
    else:
        status = "pass"
        score = 1.0

    report = VerificationReport(capsule=name, status=status, score=score, findings=findings)
    write_yaml(base / "evidence" / "verification.yaml", report.to_dict())
    return report
