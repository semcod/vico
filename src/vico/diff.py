from __future__ import annotations

from pathlib import Path

from .capsule import load_capsule
from .files import collect_files, rel
from .hashing import sha256_file
from .models import CapsuleDiff, write_yaml
from .paths import capsule_dir


def diff_capsule(root: Path, name: str) -> CapsuleDiff:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    src = base / "src"
    current: dict[str, str] = {
        rel(path, src): sha256_file(path)
        for path in collect_files(src)
    }
    baseline = capsule.baseline_files

    added = sorted(path for path in current if path not in baseline)
    deleted = sorted(path for path in baseline if path not in current)
    modified = sorted(path for path, digest in current.items() if path in baseline and baseline[path] != digest)
    unchanged = sorted(path for path, digest in current.items() if path in baseline and baseline[path] == digest)

    report = CapsuleDiff(
        capsule=name,
        added=added,
        modified=modified,
        deleted=deleted,
        unchanged=unchanged,
    )
    write_yaml(base / "evidence" / "diff.yaml", report.to_dict())
    return report
