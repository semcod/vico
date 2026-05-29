from __future__ import annotations

from pathlib import Path

from .models import write_yaml
from .paths import ensure_project_dirs


def init_project(root: Path) -> list[Path]:
    ensure_project_dirs(root)
    created: list[Path] = []

    vico_yaml = root / "vico.yaml"
    if not vico_yaml.exists():
        write_yaml(
            vico_yaml,
            {
                "version": "vico.v1",
                "project": {
                    "name": root.name,
                    "source_of_truth": {
                        "intent": "intract.yaml",
                        "capsules": ".vico/capsules",
                        "snapshots": ".vico/snapshots",
                    },
                },
                "verification": {
                    "fail_on": ["forbidden_effect", "invalid_contract"],
                    "warn_on": ["missing_tests", "partial_output_match"],
                },
                "preview": {"default_horizon": 10, "render": ["text_wireframe", "ui_blueprint"]},
            },
        )
        created.append(vico_yaml)

    intract_yaml = root / "intract.yaml"
    if not intract_yaml.exists():
        write_yaml(
            intract_yaml,
            {
                "version": "intract.v1",
                "project": {"name": root.name, "intent": "orchestrate:project_capsules"},
                "contracts": [
                    {
                        "id": "project.capsules",
                        "scope": "project",
                        "intent": "orchestrate:project_capsules",
                        "priority": 2,
                        "domain": "architecture",
                        "input": ["project_state", "user_goal"],
                        "output": ["capsule", "evidence_map", "promotion_plan"],
                        "effect": ["read"],
                        "forbid": ["destructive_write", "secret_leak"],
                        "require": ["freeze.baseline", "verify.capsule", "promote.after_review"],
                        "validate": ["input_presence", "output_presence", "no_forbidden_effect"],
                    }
                ],
            },
        )
        created.append(intract_yaml)

    return created
