from pathlib import Path

from nexu.capsule import create_capsule
from nexu.freeze import freeze_project
from nexu.init_project import init_project
from nexu.iterate import iterate_capsule
from nexu.verify import verify_capsule


def test_capsule_flow(tmp_path: Path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        '# @intract.v1 scope:function intent:query:item priority:2 domain:test input:x output:y effect:read forbid:write validate:output_presence meaning:"demo"\n\n'
        'def item(x):\n    return {"y": x}\n',
        encoding="utf-8",
    )
    init_project(tmp_path)
    snapshot = freeze_project(tmp_path, "baseline")
    assert snapshot.files
    capsule = create_capsule(tmp_path, "demo", include=["src/**"], snapshot_id="baseline")
    assert capsule.name == "demo"
    created = iterate_capsule(tmp_path, "demo", steps=2, goal="test")
    assert created == ["S1", "S2"]
    report = verify_capsule(tmp_path, "demo")
    assert report.status in {"pass", "partial"}
