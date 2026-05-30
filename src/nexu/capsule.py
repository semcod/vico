from __future__ import annotations

import shutil
from pathlib import Path

from .files import collect_files, rel
from .git import current_git_sha
from .hashing import sha256_file
from .journal import append_journal
from .models import Capsule, CapsuleSelection, read_yaml, utc_now, write_yaml
from .paths import capsule_dir, capsules_dir, ensure_project_dirs


def default_contract_manifest(capsule: Capsule) -> dict:
    intent = f"evolve:{capsule.name.replace('-', '_')}"
    return {
        "version": "intract.v1",
        "project": {"name": capsule.name, "intent": intent},
        "contracts": [
            {
                "id": f"capsule.{capsule.name}.main",
                "scope": "module",
                "intent": intent,
                "priority": 2,
                "domain": capsule.selection.domain,
                "input": ["frozen_slice", "fixtures", "user_goal"],
                "output": ["evolved_capsule", "promotion_plan", "evidence_map"],
                "effect": ["read"],
                "forbid": ["destructive_write", "secret_leak"],
                "require": ["validate.contracts", "verify.capsule"],
                "validate": ["input_presence", "output_presence", "no_forbidden_effect"],
                "meaning": "evolve this isolated project slice without mutating the source project",
            }
        ],
    }


def create_capsule(
    root: Path,
    name: str,
    *,
    domain: str = "general",
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    routes: list[str] | None = None,
    endpoints: list[str] | None = None,
    snapshot_id: str | None = None,
) -> Capsule:
    ensure_project_dirs(root)
    include = include or ["src/**", "contracts/**", "frontend/**", "backend/**", "shared/**", "*.py", "*.md"]
    selection = CapsuleSelection(
        domain=domain,
        routes=routes or [],
        endpoints=endpoints or [],
        include=include,
        exclude=exclude or [],
    )
    target = capsule_dir(root, name)
    if target.exists():
        raise FileExistsError(f"Capsule already exists: {target}")

    copied: list[str] = []
    baseline_files: dict[str, str] = {}
    capsule = Capsule(
        name=name,
        source_project_root=str(root),
        source_snapshot_id=snapshot_id,
        source_git_sha=current_git_sha(root),
        selection=selection,
        baseline_files=baseline_files,
    )

    for subdir in [
        target / "src",
        target / "fixtures",
        target / "iterations" / "S0",
        target / "evidence",
        target / "prompts",
        target / "blueprints",
    ]:
        subdir.mkdir(parents=True, exist_ok=True)

    for source in collect_files(root, include=include, exclude=selection.exclude):
        relative = rel(source, root)
        destination = target / "src" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(relative)
        baseline_files[relative] = sha256_file(source)

    write_yaml(target / "capsule.yaml", capsule.to_dict())
    write_yaml(target / "intract.yaml", default_contract_manifest(capsule))
    write_yaml(
        target / "iterations" / "S0" / "state.yaml",
        {
            "state": "S0",
            "created_at": utc_now(),
            "description": "Frozen capsule baseline copied from source project.",
            "copied_files": copied,
            "baseline_lock": {
                "source_git_sha": capsule.source_git_sha,
                "source_snapshot_id": capsule.source_snapshot_id,
                "file_count": len(baseline_files),
            },
        },
    )
    append_journal(root, name, "capsule.created", "Created capsule from selected project slice.", data={"files": len(baseline_files), "domain": domain})
    return capsule


def list_capsules(root: Path) -> list[str]:
    base = capsules_dir(root)
    if not base.exists():
        return []
    return sorted(path.name for path in base.iterdir() if path.is_dir())


def load_capsule(root: Path, name: str) -> Capsule:
    data = read_yaml(capsule_dir(root, name) / "capsule.yaml")
    return Capsule.from_dict(data)


def save_capsule(root: Path, capsule: Capsule) -> None:
    write_yaml(capsule_dir(root, capsule.name) / "capsule.yaml", capsule.to_dict())
