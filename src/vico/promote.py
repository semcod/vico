from __future__ import annotations

from pathlib import Path

from .capsule import load_capsule
from .files import collect_files, rel
from .models import utc_now, write_yaml
from .paths import capsule_dir


def build_promotion_plan(root: Path, name: str) -> dict:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    files = collect_files(base / "src")
    source_files = [rel(path, base / "src") for path in files]
    plan = {
        "capsule": name,
        "created_at": utc_now(),
        "source_project_root": capsule.source_project_root,
        "source_snapshot_id": capsule.source_snapshot_id,
        "source_git_sha": capsule.source_git_sha,
        "mode": "dry_run",
        "files_to_review": source_files,
        "instructions": [
            "Review every file before applying it to the source project.",
            "Run Intract/Vico verification after promotion.",
            "Prefer small patches mapped from capsule src/ to real project paths.",
        ],
    }
    write_yaml(base / "promotion-plan.yaml", plan)
    return plan
