from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import read_yaml, utc_now, write_yaml
from .paths import capsule_dir


def journal_path(root: Path, name: str) -> Path:
    return capsule_dir(root, name) / "journal.yaml"


def read_journal(root: Path, name: str) -> list[dict[str, Any]]:
    path = journal_path(root, name)
    if not path.exists():
        return []
    data = read_yaml(path)
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def append_journal(
    root: Path,
    name: str,
    event: str,
    message: str,
    *,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entries = read_journal(root, name)
    entry = {
        "index": len(entries) + 1,
        "created_at": utc_now(),
        "event": event,
        "message": message,
        "data": data or {},
    }
    entries.append(entry)
    write_yaml(journal_path(root, name), {"version": "nexu.journal.v1", "capsule": name, "entries": entries})
    return entry
