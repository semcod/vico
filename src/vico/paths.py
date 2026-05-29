from __future__ import annotations

from pathlib import Path


def project_root(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def vico_dir(root: Path) -> Path:
    return root / ".vico"


def snapshots_dir(root: Path) -> Path:
    return vico_dir(root) / "snapshots"


def capsules_dir(root: Path) -> Path:
    return vico_dir(root) / "capsules"


def capsule_dir(root: Path, name: str) -> Path:
    return capsules_dir(root) / name


def ensure_project_dirs(root: Path) -> None:
    for sub in [
        vico_dir(root),
        snapshots_dir(root),
        capsules_dir(root),
        vico_dir(root) / "runs",
        vico_dir(root) / "evidence",
        vico_dir(root) / "prompts",
    ]:
        sub.mkdir(parents=True, exist_ok=True)
