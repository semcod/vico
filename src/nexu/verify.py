from __future__ import annotations

import re
from pathlib import Path

from .capsule import load_capsule
from .diff import diff_capsule
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

SECRET_PATTERNS = [
    "OPENAI_API_KEY=",
    "OPENROUTER_API_KEY=",
    "SECRET_KEY=",
    "password=",
    "api_key=",
]


def _scan_capsule_contracts(base: Path, manifest_name: str = "intract.yaml") -> list[IntentContract]:
    contracts = read_manifest_contracts(base / manifest_name)
    for path in collect_files(base / "src"):
        contracts.extend(scan_contracts_in_file(path, base))
    return contracts


def _text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def _contains_patterns(path: Path, patterns: list[str]) -> list[str]:
    text = _text(path)
    evidence = []
    for pattern in patterns:
        if pattern in text:
            evidence.append(f"{path.name}: contains `{pattern}`")
    return evidence


def _find_term_evidence(source_files: list[Path], base: Path, terms: list[str]) -> dict[str, list[str]]:
    evidence: dict[str, list[str]] = {}
    for term in terms:
        term_evidence: list[str] = []
        normalized = re.sub(r"[^a-zA-Z0-9]+", "_", term).strip("_")
        variants = {term, normalized, normalized.lower(), normalized.upper()}
        for path in source_files:
            text = _text(path)
            if any(variant and variant in text for variant in variants):
                term_evidence.append(rel(path, base))
        evidence[term] = term_evidence
    return evidence


def verify_capsule(root: Path, name: str) -> VerificationReport:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    findings: list[VerificationFinding] = []

    contracts = _scan_capsule_contracts(base, capsule.contracts_manifest)
    if contracts:
        findings.append(
            VerificationFinding(
                code="contracts_found",
                status="pass",
                message=f"Found {len(contracts)} intent contract(s).",
                evidence=[contract.key for contract in contracts if contract.key],
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

    if capsule.baseline_files:
        diff = diff_capsule(root, name)
        findings.append(
            VerificationFinding(
                code="baseline_lock",
                status="pass",
                message=f"Baseline lock tracks {len(capsule.baseline_files)} file(s).",
                evidence=[f"modified={len(diff.modified)}", f"added={len(diff.added)}", f"deleted={len(diff.deleted)}"],
            )
        )
    else:
        findings.append(
            VerificationFinding(
                code="baseline_lock_missing",
                status="warn",
                message="Capsule has no baseline file hash lock. Recreate capsule for stronger drift checks.",
            )
        )

    forbids_write = any(
        "write" in contract.forbid or "destructive_write" in contract.forbid for contract in contracts
    )
    write_evidence: list[str] = []
    if forbids_write:
        for path in source_files:
            write_evidence.extend(_contains_patterns(path, WRITE_PATTERNS))
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

    forbids_secret = any(
        "secret_leak" in contract.forbid or "secrets" in contract.forbid for contract in contracts
    )
    if forbids_secret:
        secret_evidence: list[str] = []
        for path in source_files:
            secret_evidence.extend(_contains_patterns(path, SECRET_PATTERNS))
        findings.append(
            VerificationFinding(
                code="secret_leak_check",
                status="fail" if secret_evidence else "pass",
                message="Secret-like values detected." if secret_evidence else "No obvious secret-like values detected.",
                evidence=secret_evidence[:20],
            )
        )

    required_outputs = sorted({output for contract in contracts for output in contract.output})
    if required_outputs and source_files:
        output_evidence = _find_term_evidence(source_files, base, required_outputs)
        missing_outputs = [term for term, evidence in output_evidence.items() if not evidence]
        findings.append(
            VerificationFinding(
                code="output_presence",
                status="warn" if missing_outputs else "pass",
                message=(
                    "Some declared outputs have no text evidence."
                    if missing_outputs
                    else "Declared outputs have text evidence in capsule sources."
                ),
                evidence=[f"missing:{term}" for term in missing_outputs]
                or [f"{term}: {', '.join(paths[:3])}" for term, paths in output_evidence.items()],
            )
        )

    required = sorted({item for contract in contracts for item in contract.require})
    provided_keys = {contract.intent for contract in contracts} | {contract.contract_id for contract in contracts}
    if required:
        missing_required = [item for item in required if item not in provided_keys]
        findings.append(
            VerificationFinding(
                code="required_intents",
                status="warn" if missing_required else "pass",
                message=(
                    "Some required sub-intents are not explicitly present."
                    if missing_required
                    else "Required sub-intents are explicitly present."
                ),
                evidence=[f"missing:{item}" for item in missing_required] or sorted(required),
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
    fail_count = statuses.count("fail")
    warn_count = statuses.count("warn")
    if fail_count:
        status = "fail"
    elif warn_count:
        status = "partial"
    else:
        status = "pass"

    total = len(findings) or 1
    score = max(0.0, min(1.0, (total - fail_count - 0.4 * warn_count) / total))

    report = VerificationReport(capsule=name, status=status, score=round(score, 3), findings=findings)
    write_yaml(base / "evidence" / "verification.yaml", report.to_dict())
    return report
