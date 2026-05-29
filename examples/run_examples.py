from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexu.blueprint import build_blueprint  # noqa: E402
from nexu.capsule import create_capsule  # noqa: E402
from nexu.diff import diff_capsule  # noqa: E402
from nexu.drift import check_source_drift  # noqa: E402
from nexu.export_prompt import export_iteration_prompt  # noqa: E402
from nexu.freeze import freeze_project  # noqa: E402
from nexu.init_project import init_project  # noqa: E402
from nexu.iterate import iterate_capsule  # noqa: E402
from nexu.verify import verify_capsule  # noqa: E402

EXAMPLES = [
    ROOT / "examples" / "frontend_view",
    ROOT / "examples" / "backend_service",
    ROOT / "examples" / "vertical_slice",
]


def run_example(example: Path) -> None:
    work = example / ".tmp_vico_run"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(example, work, ignore=shutil.ignore_patterns(".tmp_vico_run", ".vico"))

    init_project(work)
    snapshot = freeze_project(work, "baseline")
    capsule = create_capsule(
        work,
        "demo",
        include=["**/*.py"],
        routes=["/demo"],
        endpoints=["GET:/api/demo"],
        snapshot_id=snapshot.id,
    )
    blueprint = build_blueprint(work, capsule.name)
    iterations = iterate_capsule(work, capsule.name, steps=2, goal="demo")
    prompt = export_iteration_prompt(work, capsule.name)
    diff = diff_capsule(work, capsule.name)
    drift = check_source_drift(work, capsule.name)
    report = verify_capsule(work, capsule.name)

    print(
        f"{example.name}: ok | files={len(capsule.baseline_files)} "
        f"iterations={','.join(iterations)} blueprint={blueprint['version']} "
        f"prompt={Path(prompt.path).name} diff_modified={len(diff.modified)} "
        f"drift={drift['status']} verify={report.status}"
    )


def main() -> None:
    for example in EXAMPLES:
        run_example(example)


if __name__ == "__main__":
    main()
