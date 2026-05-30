from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any

from .files import rel
from .journal import append_journal
from .models import utc_now, write_yaml
from .paths import capsule_dir


def _should_include(path: Path, base: Path, *, include_src: bool) -> bool:
    relative = rel(path, base)
    if "/bundles/" in f"/{relative}":
        return False
    if relative.startswith("runtime/"):
        return False
    if not include_src and relative.startswith("src/"):
        return False
    return path.is_file()


def build_capsule_bundle(root: Path, name: str, *, include_src: bool = True) -> dict[str, Any]:
    base = capsule_dir(root, name)
    bundles_dir = base / "bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = bundles_dir / f"{name}-review-bundle.zip"

    included: list[str] = []
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(base.rglob("*")):
            if not _should_include(path, base, include_src=include_src):
                continue
            relative = rel(path, base)
            archive.write(path, arcname=f"{name}/{relative}")
            included.append(relative)

    manifest = {
        "version": "nexu.bundle.v1",
        "capsule": name,
        "created_at": utc_now(),
        "path": str(bundle_path),
        "include_src": include_src,
        "file_count": len(included),
        "included": included,
        "usage": [
            "Send this bundle to a reviewer or LLM tool when direct repository access is not available.",
            "The source project is not mutated by this bundle.",
            "Review the promotion plan before applying capsule changes back to the project.",
        ],
    }
    write_yaml(bundles_dir / "bundle.yaml", manifest)
    append_journal(root, name, "bundle.built", "Built capsule review bundle.", data={"files": len(included)})
    return manifest
