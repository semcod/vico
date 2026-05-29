from __future__ import annotations

from pathlib import Path

from .capsule import load_capsule
from .diff import diff_capsule
from .models import read_yaml
from .paths import capsule_dir


def capsule_status(root: Path, name: str) -> dict:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    diff = diff_capsule(root, name)
    verification_path = base / "evidence" / "verification.yaml"
    verification = read_yaml(verification_path) if verification_path.exists() else None
    return {
        "name": capsule.name,
        "type": capsule.type,
        "domain": capsule.selection.domain,
        "routes": capsule.selection.routes,
        "endpoints": capsule.selection.endpoints,
        "source_snapshot_id": capsule.source_snapshot_id,
        "source_git_sha": capsule.source_git_sha,
        "iterations": capsule.iterations,
        "latest_iteration": capsule.iterations[-1] if capsule.iterations else "S0",
        "files": {
            "baseline": len(capsule.baseline_files),
            "added": len(diff.added),
            "modified": len(diff.modified),
            "deleted": len(diff.deleted),
            "unchanged": len(diff.unchanged),
        },
        "verification": verification,
    }
