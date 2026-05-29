from __future__ import annotations

from pathlib import Path

from .files import collect_files, rel
from .git import current_git_sha
from .hashing import sha256_file
from .models import FrozenFile, FrozenSnapshot, write_yaml
from .paths import ensure_project_dirs, snapshots_dir


def freeze_project(root: Path, name: str, include: list[str] | None = None) -> FrozenSnapshot:
    ensure_project_dirs(root)
    files = [
        FrozenFile(path=rel(path, root), sha256=sha256_file(path), size=path.stat().st_size)
        for path in collect_files(root, include=include)
    ]
    snapshot = FrozenSnapshot(
        id=name,
        project_root=str(root),
        git_sha=current_git_sha(root),
        files=files,
    )
    snapshot_path = snapshots_dir(root) / name / "snapshot.yaml"
    write_yaml(snapshot_path, snapshot.to_dict())
    return snapshot
