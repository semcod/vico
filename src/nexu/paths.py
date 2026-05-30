from __future__ import annotations

from pathlib import Path


def project_root(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def nexu_dir(root: Path) -> Path:
    return root / ".nexu"


def snapshots_dir(root: Path) -> Path:
    return nexu_dir(root) / "snapshots"


def capsules_dir(root: Path) -> Path:
    return nexu_dir(root) / "capsules"


def capsule_dir(root: Path, name: str) -> Path:
    return capsules_dir(root) / name


def ensure_project_dirs(root: Path) -> None:
    for sub in [
        nexu_dir(root),
        snapshots_dir(root),
        capsules_dir(root),
        nexu_dir(root) / "runs",
        nexu_dir(root) / "evidence",
        nexu_dir(root) / "prompts",
    ]:
        sub.mkdir(parents=True, exist_ok=True)
