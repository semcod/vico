from vico.models import Capsule, CapsuleSelection, FrozenSnapshot


def test_capsule_roundtrip():
    capsule = Capsule(name="demo", selection=CapsuleSelection(domain="menu", include=["src/**"]))
    restored = Capsule.from_dict(capsule.to_dict())
    assert restored.name == "demo"
    assert restored.selection.domain == "menu"


def test_snapshot_roundtrip():
    snapshot = FrozenSnapshot(id="baseline", project_root="/tmp/x")
    restored = FrozenSnapshot.from_dict(snapshot.to_dict())
    assert restored.id == "baseline"
