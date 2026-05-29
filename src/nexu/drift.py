from __future__ import annotations

from pathlib import Path

from .capsule import load_capsule
from .hashing import sha256_file
from .models import utc_now, write_yaml
from .paths import capsule_dir


def check_source_drift(root: Path, name: str) -> dict:
    capsule = load_capsule(root, name)
    source_root = Path(capsule.source_project_root)
    changed: list[dict[str, str]] = []
    missing: list[str] = []

    for relative, expected_hash in capsule.baseline_files.items():
        source_path = source_root / relative
        if not source_path.exists():
            missing.append(relative)
            continue
        current_hash = sha256_file(source_path)
        if current_hash != expected_hash:
            changed.append({"path": relative, "baseline": expected_hash, "current": current_hash})

    status = "pass" if not changed and not missing else "drift"
    report = {
        "capsule": name,
        "created_at": utc_now(),
        "status": status,
        "changed": changed,
        "missing": missing,
        "recommendation": "rebase capsule or promote manually with extra review" if status == "drift" else "source baseline still matches",
    }
    write_yaml(capsule_dir(root, name) / "evidence" / "source-drift.yaml", report)
    return report
