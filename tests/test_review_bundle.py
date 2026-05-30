from pathlib import Path

from nexu.bundle import build_capsule_bundle
from nexu.capsule import create_capsule
from nexu.config import load_config
from nexu.freeze import freeze_project
from nexu.init_project import init_project
from nexu.iterate import iterate_capsule
from nexu.promote import build_promotion_plan
from nexu.review import build_review_packet


def test_review_bundle_and_promotion_prechecks(tmp_path: Path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        '# @intract.v1 scope:function intent:preview:item priority:1 domain:demo input:item output:evolved_capsule,promotion_plan,evidence_map effect:read forbid:write,secret_leak validate:output_presence,no_forbidden_effect meaning:"demo"\n'
        'def preview_item(item):\n'
        '    evidence_map = {"item": item}\n'
        '    return {"evolved_capsule": item, "promotion_plan": [], "evidence_map": evidence_map}\n',
        encoding="utf-8",
    )
    init_project(tmp_path)
    config = load_config(tmp_path)
    assert config.llm.provider == "offline"
    assert config.review.require_human_approval is True

    snapshot = freeze_project(tmp_path, "baseline")
    create_capsule(tmp_path, "demo", include=["src/**"], snapshot_id=snapshot.id)
    iterate_capsule(tmp_path, "demo", steps=1, goal="review handoff")

    review = build_review_packet(tmp_path, "demo")
    assert Path(review["yaml"]).exists()
    assert Path(review["prompt"]).exists()
    assert review["decision"] in {"approve", "needs_revision", "reject"}
    assert review["llm_called"] is False

    bundle = build_capsule_bundle(tmp_path, "demo", include_src=False)
    assert Path(bundle["path"]).exists()
    assert bundle["file_count"] > 0
    assert all(not item.startswith("src/") for item in bundle["included"])

    plan = build_promotion_plan(tmp_path, "demo")
    assert "prechecks" in plan
    assert "promotion_map" in plan
    assert plan["mode"] == "dry_run"
