from pathlib import Path

from vico.blueprint import build_blueprint
from vico.capsule import create_capsule
from vico.diff import diff_capsule
from vico.drift import check_source_drift
from vico.export_prompt import export_iteration_prompt
from vico.init_project import init_project
from vico.iterate import iterate_capsule
from vico.status import capsule_status
from vico.verify import verify_capsule


def test_capsule_blueprint_prompt_diff_status_and_drift(tmp_path: Path):
    (tmp_path / "src").mkdir()
    app = tmp_path / "src" / "app.py"
    app.write_text(
        '# @intract.v1 scope:function intent:preview:item priority:1 domain:demo input:item output:evolved_capsule,promotion_plan,evidence_map effect:read forbid:write,secret_leak validate:output_presence,no_forbidden_effect meaning:"demo"\n'
        'def preview_item(item):\n'
        '    evidence_map = {"item": item}\n'
        '    return {"evolved_capsule": item, "promotion_plan": [], "evidence_map": evidence_map}\n',
        encoding="utf-8",
    )
    init_project(tmp_path)
    capsule = create_capsule(
        tmp_path,
        "demo",
        include=["src/**"],
        routes=["/demo"],
        endpoints=["GET:/api/demo"],
    )
    assert capsule.baseline_files

    blueprint = build_blueprint(tmp_path, "demo")
    assert blueprint["ui"]["screens"][0]["route"] == "/demo"
    assert blueprint["api"]["endpoints"][0]["path"] == "/api/demo"

    iterate_capsule(tmp_path, "demo", steps=1, goal="polish demo")
    export = export_iteration_prompt(tmp_path, "demo")
    assert Path(export.path).exists()
    assert "Intract contracts" in Path(export.path).read_text(encoding="utf-8")

    copied = tmp_path / ".vico" / "capsules" / "demo" / "src" / "src" / "app.py"
    copied.write_text(copied.read_text(encoding="utf-8") + "\n# local capsule change\n", encoding="utf-8")
    diff = diff_capsule(tmp_path, "demo")
    assert "src/app.py" in diff.modified

    report = verify_capsule(tmp_path, "demo")
    assert report.status in {"pass", "partial"}

    status = capsule_status(tmp_path, "demo")
    assert status["files"]["modified"] == 1

    drift = check_source_drift(tmp_path, "demo")
    assert drift["status"] == "pass"
    app.write_text(app.read_text(encoding="utf-8") + "\n# source drift\n", encoding="utf-8")
    drift = check_source_drift(tmp_path, "demo")
    assert drift["status"] == "drift"
