from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = [
    ROOT / "examples" / "frontend_view",
    ROOT / "examples" / "backend_service",
]


def run(cmd: list[str], cwd: Path) -> None:
    print("$", " ".join(cmd))
    env = os.environ.copy()
    src_path = str(ROOT / "src")
    env["PYTHONPATH"] = src_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, env=env)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(result.returncode)


def main() -> None:
    env_python = sys.executable
    for example in EXAMPLES:
        work = example / ".tmp_vico_run"
        if work.exists():
            shutil.rmtree(work)
        shutil.copytree(example, work, ignore=shutil.ignore_patterns(".tmp_vico_run", ".vico"))
        run([env_python, "-m", "vico", "init", "."], work)
        run([env_python, "-m", "vico", "freeze", ".", "--name", "baseline"], work)
        run([env_python, "-m", "vico", "capsule", "create", ".", "--name", "demo", "--include", "**/*.py"], work)
        run([env_python, "-m", "vico", "capsule", "iterate", "demo", "--steps", "2", "--goal", "demo"], work)
        run([env_python, "-m", "vico", "capsule", "verify", "demo"], work)
        print(f"{example.name}: ok")


if __name__ == "__main__":
    main()
