from pathlib import Path

from nexu.capsule import create_capsule
from nexu.init_project import init_project
from nexu.iterate import iterate_capsule
from nexu.journal import read_journal
from nexu.plan import build_iteration_plan
from nexu.report import build_capsule_report
from nexu.runtime import build_capsule_runtime


def test_plan_runtime_report_and_journal(tmp_path: Path):
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
    create_capsule(
        tmp_path,
        "demo",
        include=["src/**"],
        routes=["/demo"],
        endpoints=["GET:/api/demo"],
    )

    plan = build_iteration_plan(tmp_path, "demo", steps=4, goal="ship a better preview")
    assert len(plan["steps"]) == 4
    assert (tmp_path / ".nexu" / "capsules" / "demo" / "plan" / "iteration-plan.yaml").exists()

    iterate_capsule(tmp_path, "demo", steps=2, goal="demo")
    runtime = build_capsule_runtime(tmp_path, "demo")
    runtime_html = Path(runtime["index"])
    assert runtime_html.exists()
    assert "nexu Capsule Runtime" in runtime_html.read_text(encoding="utf-8")

    report = build_capsule_report(tmp_path, "demo")
    assert Path(report["markdown"]).exists()
    assert Path(report["html"]).exists()
    assert report["status"] in {"pass", "partial"}

    events = [entry["event"] for entry in read_journal(tmp_path, "demo")]
    assert "capsule.created" in events
    assert "plan.created" in events
    assert "runtime.built" in events
    assert "report.built" in events
