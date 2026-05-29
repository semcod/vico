from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class FrozenFile:
    path: str
    sha256: str
    size: int


@dataclass
class FrozenSnapshot:
    id: str
    project_root: str
    created_at: str = field(default_factory=utc_now)
    git_sha: str | None = None
    files: list[FrozenFile] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FrozenSnapshot":
        files = [FrozenFile(**item) for item in data.get("files", [])]
        return cls(
            id=data["id"],
            project_root=data["project_root"],
            created_at=data.get("created_at", utc_now()),
            git_sha=data.get("git_sha"),
            files=files,
        )


@dataclass
class CapsuleSelection:
    domain: str = "general"
    routes: list[str] = field(default_factory=list)
    endpoints: list[str] = field(default_factory=list)
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=lambda: [".git/**", ".venv/**", "node_modules/**", "dist/**", "build/**"])


@dataclass
class CapsuleRuntime:
    frontend: str | None = None
    backend: str | None = None
    data: list[str] = field(default_factory=list)


@dataclass
class Capsule:
    name: str
    type: str = "vertical_slice"
    source_project_root: str = "."
    source_snapshot_id: str | None = None
    source_git_sha: str | None = None
    selection: CapsuleSelection = field(default_factory=CapsuleSelection)
    runtime: CapsuleRuntime = field(default_factory=CapsuleRuntime)
    contracts_manifest: str = "intract.yaml"
    created_at: str = field(default_factory=utc_now)
    iterations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Capsule":
        selection = CapsuleSelection(**data.get("selection", {}))
        runtime = CapsuleRuntime(**data.get("runtime", {}))
        return cls(
            name=data["name"],
            type=data.get("type", "vertical_slice"),
            source_project_root=data.get("source_project_root", "."),
            source_snapshot_id=data.get("source_snapshot_id"),
            source_git_sha=data.get("source_git_sha"),
            selection=selection,
            runtime=runtime,
            contracts_manifest=data.get("contracts_manifest", "intract.yaml"),
            created_at=data.get("created_at", utc_now()),
            iterations=list(data.get("iterations", [])),
        )


@dataclass
class VerificationFinding:
    code: str
    status: str
    message: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class VerificationReport:
    capsule: str
    status: str
    score: float
    findings: list[VerificationFinding] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data
