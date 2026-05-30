from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path

DEFAULT_EXCLUDE = [
    ".git/**",
    ".nexu/**",
    ".venv/**",
    "venv/**",
    "node_modules/**",
    "dist/**",
    "build/**",
    "__pycache__/**",
    "*.pyc",
]

TEXT_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".yaml", ".yml", ".toml", ".md",
    ".txt", ".css", ".html", ".less", ".scss", ".sql", ".sh",
}


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def matches_any(value: str, patterns: list[str]) -> bool:
    return any(fnmatch(value, pattern) or fnmatch(value, pattern.rstrip("/**")) for pattern in patterns)


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"Dockerfile", "Makefile"}


def collect_files(root: Path, include: list[str] | None = None, exclude: list[str] | None = None) -> list[Path]:
    include = include or ["**/*"]
    exclude = (exclude or []) + DEFAULT_EXCLUDE
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = rel(path, root)
        if matches_any(relative, exclude):
            continue
        if not matches_any(relative, include):
            continue
        if not is_text_file(path):
            continue
        files.append(path)
    return sorted(files)
